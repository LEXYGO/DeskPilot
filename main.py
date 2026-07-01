VERSION = "1.0.4"
BUILD = "2026.07.02/4"

import sys
import os
import json
from platformdirs import user_data_dir
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtWebSockets import QWebSocket
from PySide6.QtCore import QUrl, QTimer, QByteArray, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap, QPalette
from dashboard import Dashboard
from iconhelper import create_tray_icon
from path_helper import resource_path

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

data_dir = user_data_dir("DeskPilot", "DeskPilot")
os.makedirs(data_dir, exist_ok=True)
config_file = os.path.join(data_dir, "config.json")

socket = QWebSocket()
pingtime = 30000
timeouttime = 10000
reconnecttime = 30000

tray_menu_connected = QMenu()
tray_menu_disconnected = QMenu()
height_tray_action = None
connectButton = None
current_taskbar_icon_color = ""

def update_systray_icon(status):
    global current_taskbar_icon_color
    palette = app.palette()
    window_color = palette.color(QPalette.Window)
    darkmode = window_color.lightness() < 128
    
    if status == "connected":
        if darkmode:
            if current_taskbar_icon_color != "#FFFFFF":
                tray.setIcon(create_tray_icon(resource_path("icons/desk.svg"), "#FFFFFF"))
                current_taskbar_icon_color = "#FFFFFF"
                print("update_systray_icon called with status: " + status)
        else:
            if current_taskbar_icon_color != "#000000":
                tray.setIcon(create_tray_icon(resource_path("icons/desk.svg"), "#000000"))
                current_taskbar_icon_color = "#000000"
                print("update_systray_icon called with status: " + status)
    if status == "disconnected":
        if current_taskbar_icon_color != "#FF0000":
            tray.setIcon(create_tray_icon(resource_path("icons/desk.svg"), "#FF0000"))
            current_taskbar_icon_color = "#FF0000"
            print("update_systray_icon called with status: " + status)

def load_config():
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    return {"max_height": -1, "min_height": -1, "preset_count": -1, "ip": "fffff", "port": "81", "p1": "", "p2": "", "p3": "", "p4": "", "p5": "", "p6": "", "p7": "", "p8": "", "p9": ""}

def save_config():
    with open(config_file, "w") as f:
        json.dump(config, f)
        build_tray_menu()

def on_ws_connected():
    print("Verbunden!")
    timer_connection_timeout.start()
    timer_last_message_recieved.start()
    ws_send("i")
    tray.setContextMenu(tray_menu_connected)
    update_systray_icon("connected")

def on_ws_disconnected():
    print("on_ws_disconnected called")
    tray.setVisible(False)
    tray.setContextMenu(tray_menu_disconnected)
    tray.setVisible(True)
    print("menu set")
    connectButton.setEnabled(True)
    print("button enabled")
    update_systray_icon("disconnected")

def on_ws_message(message):
    update_systray_icon("connected")
    print("Nachricht: " + message)
    global max_height, min_height, preset_count
    timer_connection_timeout.start()
    timer_last_message_recieved.start()

    if message.startswith("H: "):
        height_mm = int(message[3:])
        height_cm = height_mm / 10
        if height_tray_action:
            height_tray_action.setText(f"Height: {height_cm}cm")

    elif message.startswith("Info: "):
        config_updated_by_desk = False
        parts = message[6:].split(" ")
        max_height = int(parts[0])
        min_height = int(parts[1])
        preset_count = int(parts[2])
        height_mm = int(parts[3])
        deskname = "".join(parts[4:])

        height_cm = height_mm / 10
        if height_tray_action:
            height_tray_action.setText(f"Height: {height_cm}cm")
        if max_height != config["max_height"]:
            config["max_height"] = max_height
            config_updated_by_desk = True
        if min_height != config["min_height"]:
            config["min_height"] = min_height
            config_updated_by_desk = True
        if preset_count != config["preset_count"]:
            config["preset_count"] = preset_count
            config_updated_by_desk = True
        if config_updated_by_desk:
            save_config()
            tray.setContextMenu(tray_menu_connected)
            print("Config updated by desk, saved and menu rebuilt")

    elif message.startswith("Notify: "):
        payload = message[8:]
        notification_type = "info"
        notification = ""

        if payload.startswith("error"):
            icon = create_tray_icon(resource_path("icons/desk.svg"), "#FF0000")
            notification_type = "ERROR"
            notification = payload[7:-1]
        if payload.startswith("info"):
            palette = app.palette()
            window_color = palette.color(QPalette.Window)
            darkmode = window_color.lightness() < 128
            if darkmode:
                icon = create_tray_icon(resource_path("icons/desk.svg"), "#FFFFFF")
            else:
                icon = create_tray_icon(resource_path("icons/desk.svg"), "#000000")
            notification_type = "INFO"
            notification = payload[6:-1]

        tray.showMessage(
            f"DeskPilot - Recieved {notification_type} from desk",
            notification,
            icon,
            10000
        )
            
            
def ws_send(message):
    socket.sendTextMessage(message)
    print("WS " + message + " gesendet")

def closesocket():
    print("closesocket called")
    timer_connection_timeout.stop()
    print("timeout timer stopped")
    timer_last_message_recieved.stop()
    print("ping timer stopped")
    socket.close()
    print("socket closed")

def connect_socket():
    if connectButton:
        connectButton.setEnabled(False)
    print("Trying to connect....")
    socket.open(QUrl("ws://" + config["ip"] + ":" + config["port"]))

def connection_timeout():
    print("timeout registered")
    print("reconnect initialized")
    reconnect_socket()

def reconnect_socket():
    closesocket()
    timer_time_until_reconnect.start()
    connect_socket()

def build_tray_menu():
    global height_tray_action, connectButton
    tray_menu_connected.clear()
    tray_menu_disconnected.clear()

    if config["preset_count"] >= 1:
        tray_menu_connected.addAction("Preset 1" + " --- " + config["p1"], lambda: ws_send("1"))
    if config["preset_count"] >= 2:
        tray_menu_connected.addAction("Preset 2" + " --- " + config["p2"], lambda: ws_send("2"))
    if config["preset_count"] >= 3:
        tray_menu_connected.addAction("Preset 3" + " --- " + config["p3"], lambda: ws_send("3"))
    if config["preset_count"] >= 4:
        tray_menu_connected.addAction("Preset 4" + " --- " + config["p4"], lambda: ws_send("4"))
    if config["preset_count"] >= 5:
        tray_menu_connected.addAction("Preset 5" + " --- " + config["p5"], lambda: ws_send("5"))
    if config["preset_count"] >= 6:
        tray_menu_connected.addAction("Preset 6" + " --- " + config["p6"], lambda: ws_send("6"))
    if config["preset_count"] >= 7:
        tray_menu_connected.addAction("Preset 7" + " --- " + config["p7"], lambda: ws_send("7"))
    if config["preset_count"] >= 8:
        tray_menu_connected.addAction("Preset 8" + " --- " + config["p8"], lambda: ws_send("8"))
    if config["preset_count"] >= 9:
        tray_menu_connected.addAction("Preset 9" + " --- " + config["p9"], lambda: ws_send("9"))
    tray_menu_connected.addSeparator()
    tray_menu_connected.addAction("open dashboard", lambda: dashboard.show())
    tray_menu_connected.addAction("disconnect", lambda: closesocket())
    tray_menu_connected.addAction("quit", app.quit)
    tray_menu_connected.addSeparator()
    height_tray_action = tray_menu_connected.addAction("Height: --")
    height_tray_action.setEnabled(False)

    tray_menu_disconnected.addAction("Not connected to desk @ IP:" + config["ip"]).setEnabled(False)
    tray_menu_disconnected.addAction("If this IP-Adress is wrong, please change it, using the dashboard").setEnabled(False)
    connectButton = tray_menu_disconnected.addAction("CONNECT", lambda: connect_socket())
    tray_menu_disconnected.addSeparator()
    tray_menu_disconnected.addAction("open dashboard", lambda: dashboard.show())
    tray_menu_disconnected.addAction("quit", app.quit)    




config = load_config()
print(config)

dashboard = Dashboard(config, save_config, reconnect_socket, VERSION, BUILD)

timer_last_message_recieved = QTimer()
timer_last_message_recieved.setInterval(pingtime)
timer_last_message_recieved.timeout.connect(lambda: ws_send("i"))

timer_connection_timeout = QTimer()
timer_connection_timeout.setInterval(pingtime + timeouttime)
timer_connection_timeout.timeout.connect(connection_timeout)

timer_time_until_reconnect = QTimer()
timer_time_until_reconnect.setInterval(reconnecttime)
timer_time_until_reconnect.setSingleShot(True)
timer_time_until_reconnect.timeout.connect(connect_socket)

tray = QSystemTrayIcon()
tray.setIcon(create_tray_icon(resource_path("icons/desk.svg"), "#0066FF"))
current_taskbar_icon_color = "#0066FF"

build_tray_menu()

tray.setContextMenu(tray_menu_disconnected)

tray.setVisible(True)

socket.connected.connect(on_ws_connected)
socket.disconnected.connect(on_ws_disconnected)
socket.textMessageReceived.connect(on_ws_message)
connect_socket()

sys.exit(app.exec())
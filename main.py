import sys
import os
import json
from platformdirs import user_data_dir
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtWebSockets import QWebSocket
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtGui import QIcon

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

data_dir = user_data_dir("DeskMate", "DeskMate")
os.makedirs(data_dir, exist_ok=True)
config_file = os.path.join(data_dir, "config.json")

socket = QWebSocket()
pingtime = 5000
timeouttime = 3000

def load_config():
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    return {"max_height": -1, "min_height": -1, "preset_count": -1, "ip": "fffff", "port": "fffff", "p1": "", "p2": "", "p3": "", "p4": "", "p5": "", "p6": "", "p7": "", "p8": "", "p9": ""}

def save_config():
    with open(config_file, "w") as f:
        json.dump(config, f)

config = load_config()
print(config)

def on_ws_connected():
    print("Verbunden!")
    timer_connection_timeout.start()
    timer_last_message_recieved.start()
    ws_send("i")
    tray.setContextMenu(tray_menu_connected)

def on_ws_disconnected():
    print("Getrennt!")
    tray.setContextMenu(tray_menu_disconnected)
    connectButton.setEnabled(True)

def on_ws_message(message):
    print("Nachricht: " + message)
    global max_height, min_height, preset_count
    timer_connection_timeout.start()
    timer_last_message_recieved.start()

    if message.startswith("H: "):
        height_mm = int(message[3:])

    elif message.startswith("Info: "):
        parts = message[6:].split(" ")
        max_height = int(parts[0])
        min_height = int(parts[1])
        preset_count = int(parts[2])
        height_mm = int(parts[3])

    height_cm = height_mm / 10
    height_tray_action.setText(f"Height: {height_cm}cm")
        
def ws_send(message):
    socket.sendTextMessage(message)
    print("WS " + message + " gesendet")

def closesocket():
    timer_connection_timeout.stop()
    timer_last_message_recieved.stop()
    socket.close()

def connect_socket():
    connectButton.setEnabled(False)
    print("Trying to connect....")
    socket.open(QUrl("ws://" + config["ip"] + ":" + config["port"]))

# def enable_systray():

# def disable_systray():


timer_last_message_recieved = QTimer()
timer_last_message_recieved.setInterval(pingtime)
timer_last_message_recieved.timeout.connect(lambda: ws_send("i"))

timer_connection_timeout = QTimer()
timer_connection_timeout.setInterval(pingtime + timeouttime)
timer_connection_timeout.timeout.connect(closesocket)


tray = QSystemTrayIcon()
tray.setIcon(QIcon.fromTheme("computer"))

tray_menu_connected = QMenu()
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
tray_menu_connected.addAction("Beenden", app.quit)
tray_menu_connected.addSeparator()
height_tray_action = tray_menu_connected.addAction("Höhe: --")
height_tray_action.setEnabled(False)

tray_menu_disconnected = QMenu()
tray_menu_disconnected.addAction("Not connected to ESP").setEnabled(False )
connectButton = tray_menu_disconnected.addAction("CONNECT", lambda: connect_socket())
tray_menu_disconnected.addSeparator()
tray_menu_disconnected.addAction("Beenden", app.quit)

tray.setContextMenu(tray_menu_disconnected)

tray.setVisible(True)

socket.connected.connect(on_ws_connected)
socket.disconnected.connect(on_ws_disconnected)
socket.textMessageReceived.connect(on_ws_message)
connect_socket()

sys.exit(app.exec())
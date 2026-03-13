import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtWebSockets import QWebSocket
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtGui import QIcon

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

socket = QWebSocket()
pingtime = 1000
timeouttime = 500

max_height = -1
min_height = -1
preset_count = -1


def on_ws_connected():
    print("Verbunden!")
    timer_connection_timeout.start()
    timer_last_message_recieved.start()
    timer_reconnect.stop()
    ws_send("i")

def on_ws_disconnected():
    print("Getrennt!")
    timer_reconnect.start()

def on_ws_message(message):
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
    height_action.setText(f"Höhe: {height_cm}cm")
        
def ws_send(message):
    socket.sendTextMessage(message)
    print("WS " + message + " gesendet")

def closesocket():
    timer_connection_timeout.stop()
    timer_last_message_recieved.stop()
    socket.close()


timer_last_message_recieved = QTimer()
timer_last_message_recieved.setInterval(pingtime)
timer_last_message_recieved.timeout.connect(lambda: ws_send("i"))

timer_connection_timeout = QTimer()
timer_connection_timeout.setInterval(pingtime + timeouttime)
timer_connection_timeout.timeout.connect(closesocket)

timer_reconnect = QTimer()
timer_reconnect.setInterval(20*1000)
timer_reconnect.timeout.connect(lambda: socket.open(QUrl("ws://192.168.1.17:81")))

socket.connected.connect(on_ws_connected)
socket.disconnected.connect(on_ws_disconnected)
socket.textMessageReceived.connect(on_ws_message)
socket.open(QUrl("ws://192.168.1.17:81"))

tray = QSystemTrayIcon()
tray.setIcon(QIcon.fromTheme("computer"))
tray.setVisible(True)

menu = QMenu()
menu.addAction("Preset 1", lambda: ws_send("1"))
menu.addAction("Preset 2", lambda: ws_send("2"))
menu.addAction("Preset 3", lambda: ws_send("3"))
menu.addAction("Preset 4", lambda: ws_send("4"))
menu.addSeparator()
menu.addAction("Beenden", app.quit)
menu.addSeparator()
height_action = menu.addAction("Höhe: --")
height_action.setEnabled(False)


tray.setContextMenu(menu)

sys.exit(app.exec())
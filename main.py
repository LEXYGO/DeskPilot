import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtWebSockets import QWebSocket
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtGui import QIcon

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

socket = QWebSocket()

def on_ws_connected():
    print("Verbunden!")

def on_ws_disconnected():
    print("Getrennt!")

def on_ws_message(message):
    if message.startswith("H: "):
        height_mm = int(message[3:])
        height_cm = height_mm / 10
        print(f"Höhe: " + str(height_cm) + "cm")
        
def send(message):
    socket.sendTextMessage(message)
    print("WS " + message + " gesendet")

socket.connected.connect(on_ws_connected)
socket.disconnected.connect(on_ws_disconnected)
socket.textMessageReceived.connect(on_ws_message)
socket.open(QUrl("ws://192.168.1.17:81"))

tray = QSystemTrayIcon()
tray.setIcon(QIcon.fromTheme("computer"))
tray.setVisible(True)

menu = QMenu()
menu.addAction("Preset 1", lambda: send("1"))
menu.addAction("Preset 2", lambda: send("2"))
menu.addAction("Preset 3", lambda: send("3"))
menu.addAction("Preset 4", lambda: send("4"))
menu.addSeparator()
menu.addAction("Beenden", app.quit)

tray.setContextMenu(menu)

sys.exit(app.exec())
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtGui import QAction, QIcon

class Dashboard(QMainWindow):
    def __init__(self, config, save_config, reconnect_socket, version, build):
        super().__init__()
        self.config = config
        self.save_config = save_config
        self.reconnect_socket = reconnect_socket
        self.version = version
        self.build = build

        self.setWindowTitle("DeskPilot Dashboard")
        self.setWindowIcon(QIcon("icons/desk.svg"))

        # Menubar
        help_menu = self.menuBar().addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Main-Area of the Window
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # IP-Input-Field
        ip_layout = QHBoxLayout()

        ip_layout.addWidget(QLabel("IP-Address:"))

        self.ip_input = QLineEdit(self.config["ip"])
        ip_layout.addWidget(self.ip_input)

        layout.addLayout(ip_layout)

        layout.addStretch()

        # Save-Button
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save)
        layout.addWidget(save_btn)

    def save(self):
        self.config["ip"] = self.ip_input.text()
        self.save_config()
        self.reconnect_socket()

    def show_about(self):
        text = f"""
        <h2>DeskPilot</h2>

        <p><b>Version:</b> {self.version}</p>
        <p><b>Build:</b> {self.build}</p>

        <hr>

        <p>
        DeskPilot is a software that allows you to control your standing desk via a websocket connection. It is written in Python and uses the PySide6 library for the GUI.
        </p>

        <p>
        © 2026 Lennard Hanß<br>
        Licensed under the MIT License
        </p>

        <p>
        <a href="https://github.com/LEXYGO/DeskPilot">GitHub</a>
        </p>
        """

        QMessageBox.about(self, "About DeskPilot", text)
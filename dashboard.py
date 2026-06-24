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

        if self.config["preset_count"] >= 1:
            p1_layout = QHBoxLayout()
            p1_layout.addWidget(QLabel("Preset1-Name:"))
            self.p1_input = QLineEdit(self.config["p1"])
            p1_layout.addWidget(self.p1_input)
            layout.addLayout(p1_layout)
        if self.config["preset_count"] >= 2:
            p2_layout = QHBoxLayout()
            p2_layout.addWidget(QLabel("Preset2-Name:"))
            self.p2_input = QLineEdit(self.config["p2"])
            p2_layout.addWidget(self.p2_input)
            layout.addLayout(p2_layout)
        if self.config["preset_count"] >= 3:
            p3_layout = QHBoxLayout()
            p3_layout.addWidget(QLabel("Preset3-Name:"))
            self.p3_input = QLineEdit(self.config["p3"])
            p3_layout.addWidget(self.p3_input)
            layout.addLayout(p3_layout)
        if self.config["preset_count"] >= 4:
            p4_layout = QHBoxLayout()
            p4_layout.addWidget(QLabel("Preset4-Name:"))
            self.p4_input = QLineEdit(self.config["p4"])
            p4_layout.addWidget(self.p4_input)
            layout.addLayout(p4_layout)
        if self.config["preset_count"] >= 5:
            p5_layout = QHBoxLayout()
            p5_layout.addWidget(QLabel("Preset5-Name:"))
            self.p5_input = QLineEdit(self.config["p5"])
            p5_layout.addWidget(self.p5_input)
            layout.addLayout(p5_layout)
        if self.config["preset_count"] >= 6:
            p6_layout = QHBoxLayout()
            p6_layout.addWidget(QLabel("Preset6-Name:"))
            self.p6_input = QLineEdit(self.config["p6"])
            p6_layout.addWidget(self.p6_input)
            layout.addLayout(p6_layout)
        if self.config["preset_count"] >= 7:
            p7_layout = QHBoxLayout()
            p7_layout.addWidget(QLabel("Preset7-Name:"))
            self.p7_input = QLineEdit(self.config["p7"])
            p7_layout.addWidget(self.p7_input)
            layout.addLayout(p7_layout)
        if self.config["preset_count"] >= 8:
            p8_layout = QHBoxLayout()
            p8_layout.addWidget(QLabel("Preset8-Name:"))
            self.p8_input = QLineEdit(self.config["p8"])
            p8_layout.addWidget(self.p8_input)
            layout.addLayout(p8_layout)
        if self.config["preset_count"] >= 9:
            p9_layout = QHBoxLayout()
            p9_layout.addWidget(QLabel("Preset9-Name:"))
            self.p9_input = QLineEdit(self.config["p9"])
            p9_layout.addWidget(self.p9_input)
            layout.addLayout(p9_layout)
    

        layout.addStretch()

        # Save-Button
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save)
        layout.addWidget(save_btn)

    def save(self):
        self.config["ip"] = self.ip_input.text()

        if self.config["preset_count"] >= 1:
            self.config["p1"] = self.p1_input.text()
        if self.config["preset_count"] >= 2:
            self.config["p2"] = self.p2_input.text()
        if self.config["preset_count"] >= 3:
            self.config["p3"] = self.p3_input.text()
        if self.config["preset_count"] >= 4:
            self.config["p4"] = self.p4_input.text()
        if self.config["preset_count"] >= 5:
            self.config["p5"] = self.p5_input.text()
        if self.config["preset_count"] >= 6:
            self.config["p6"] = self.p6_input.text()
        if self.config["preset_count"] >= 7:
            self.config["p7"] = self.p7_input.text()
        if self.config["preset_count"] >= 8:
            self.config["p8"] = self.p8_input.text()
        if self.config["preset_count"] >= 9:
            self.config["p9"] = self.p9_input.text()
        
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
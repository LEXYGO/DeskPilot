from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

class Dashboard(QMainWindow):
    def __init__(self, config, save_config, reconnect_socket):
        super().__init__()
        self.config = config
        self.save_config = save_config
        self.reconnect_socket = reconnect_socket

        self.setWindowTitle("DeskMate Dashboard")

        # Main-Area of the Window
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # IP-Field
        layout.addWidget(QLabel("IP-Adress:"))
        self.ip_input = QLineEdit(self.config["ip"])
        layout.addWidget(self.ip_input)

        # Save-Button
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save)
        layout.addWidget(save_btn)

    def save(self):
        self.config["ip"] = self.ip_input.text()
        self.save_config()
        self.reconnect_socket()
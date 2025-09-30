import sys
import requests
import re
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtCore import QTimer, Qt
from zeroconf import Zeroconf, ServiceBrowser


class ArduinoDiscovery:
    def __init__(self):
        self.zeroconf = Zeroconf()
        self.ip_address = None
        self.browser = ServiceBrowser(self.zeroconf, "_http._tcp.local.", self)

    def remove_service(self, zeroconf, type, name):
        pass

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info and "arduino" in name.lower():
            ip = ".".join(map(str, info.addresses[0]))
            print(f"🔍 Found Arduino at {ip}")
            self.ip_address = ip

    def get_ip(self):
        return self.ip_address

class ArduinoControl(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arduino Controller")
        self.setGeometry(400, 200, 500, 400)

        self.arduino_ip = None
        self.is_connected = False
        self.failed_ping_count = 0

        layout = QVBoxLayout()

        ip_layout = QHBoxLayout()
        ip_label = QLabel("Arduino IP / Host (leave blank for mDNS):")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("e.g. 192.168.1.150 or arduino.local")
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_arduino)
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.ip_input)
        ip_layout.addWidget(self.connect_button)

        button_layout = QHBoxLayout()
        self.on_button = QPushButton("LED ON (F1)")
        self.on_button.setEnabled(False)
        self.on_button.clicked.connect(lambda: self.send_command("on"))

        self.off_button = QPushButton("LED OFF (F2)")
        self.off_button.setEnabled(False)
        self.off_button.clicked.connect(lambda: self.send_command("off"))

        self.status_button = QPushButton("STATUS")
        self.status_button.setEnabled(False)
        self.status_button.clicked.connect(lambda: self.send_command("status"))

        button_layout.addWidget(self.on_button)
        button_layout.addWidget(self.off_button)
        button_layout.addWidget(self.status_button)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        self.reset_log_button = QPushButton("Clear Log")
        self.reset_log_button.clicked.connect(self.clear_log)

        layout.addLayout(ip_layout)
        layout.addLayout(button_layout)
        layout.addWidget(QLabel("Activity Log:"))
        layout.addWidget(self.log_box)
        layout.addWidget(self.reset_log_button)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_status)

    def clear_log(self):
        self.log_box.clear()

    def validate_ip(self, ip):
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        return bool(pattern.match(ip))

    def connect_to_arduino(self):
        ip = self.ip_input.text().strip()

        if not ip:  
            self.log("Searching Arduino via mDNS...")
            discovery = ArduinoDiscovery()
            import time
            time.sleep(3)  
            ip = discovery.get_ip()
            if not ip:
                QMessageBox.warning(self, "Error", "Arduino not found via mDNS!")
                return
            self.log(f"Found Arduino via mDNS at {ip}")

        self.arduino_ip = ip
        self.is_connected = True
        self.on_button.setEnabled(True)
        self.off_button.setEnabled(True)
        self.status_button.setEnabled(True)
        self.status_label_update(True, ip)
        self.failed_ping_count = 0
        self.timer.start(2000)

    def send_command(self, cmd):
        if not self.is_connected or not self.arduino_ip:
            return
        try:
            url = f"http://{self.arduino_ip}/{cmd}"
            r = requests.get(url, timeout=2)
            feedback = r.text.strip() if r.text else "No response"
            self.log(f"Sent {cmd.upper()} → Arduino replied: {feedback}")
        except Exception as e:
            self.log(f"Error sending {cmd.upper()}: {e}")
            self.disconnect_arduino()

    def check_status(self):
        if not self.is_connected or not self.arduino_ip:
            return
        try:
            url = f"http://{self.arduino_ip}/status"
            r = requests.get(url, timeout=2)
            feedback = r.text.strip() if r.text else "No response"
            self.status_label_update(True, self.arduino_ip)
            self.log(f"Heartbeat OK → {feedback}")
            self.failed_ping_count = 0
        except:
            self.failed_ping_count += 1
            self.log(f"Heartbeat Failed ({self.failed_ping_count}x)")
            if self.failed_ping_count >= 3:
                self.disconnect_arduino()

    def disconnect_arduino(self):
        self.is_connected = False
        self.on_button.setEnabled(False)
        self.off_button.setEnabled(False)
        self.status_button.setEnabled(False)
        self.timer.stop()
        self.status_label_update(False)
        self.log("Arduino Disconnected!")

    def status_label_update(self, online, ip=""):
        if online:
            self.setWindowTitle(f"Arduino LED Controller - Connected ({ip})")
        else:
            self.setWindowTitle("Arduino LED Controller - Disconnected")

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.append(f"[{timestamp}] {message}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.connect_to_arduino()
        elif event.key() == Qt.Key_F1 and self.on_button.isEnabled():
            self.send_command("on")
        elif event.key() == Qt.Key_F2 and self.off_button.isEnabled():
            self.send_command("off")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArduinoControl()
    window.show()
    sys.exit(app.exec_())

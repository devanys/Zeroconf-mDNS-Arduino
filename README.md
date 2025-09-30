# Zeroconf mDNS Local Server Arduino R4 Wifi

zero-configuration communication between a Python GUI and an Arduino device over WiFi. By leveraging mDNS (Multicast DNS), the Arduino automatically advertises its presence on the local network, allowing clients to discover it without knowing its IP address. Transforms the Arduino into a mini HTTP server, capable of receiving commands and sending real-time status updates

---

## Features

- Discover Arduino via **mDNS** or connect via IP address
  <img width="693" height="433" alt="image" src="https://github.com/user-attachments/assets/6779fa8c-34d8-49dd-8fce-1f2632c95849" />
- Turn LED **ON/OFF** remotely
- Check LED **status**
- Activity log with timestamps
- Keyboard shortcuts:
  - **F1** → LED ON
  - **F2** → LED OFF
  - **Enter** → Connect to Arduino
    <img width="2256" height="1337" alt="Screenshot 2025-10-01 030130" src="https://github.com/user-attachments/assets/38a01b83-d952-4f78-88ec-08fddecb02e4" />
    
- Demo
  https://github.com/user-attachments/assets/ada94583-821d-4298-be8b-5e37572105eb

---

## Components

- **Python 3** with `PyQt5` and `requests`
- Arduino board with WiFi capability (e.g., **Arduino R4 WiFi**)
- LED connected to pin 13

---

## Python GUI (Client)

The GUI discovers and controls the Arduino over the local network.

### Installation

```bash
pip install pyqt5 requests zeroconf
```
## Usage

Run the Python GUI to control your Arduino LED:

```bash
Main2.py
```
## Arduino Code (Server)

This Arduino sketch connects the board to WiFi, hosts a web server, and responds to HTTP commands.

## Features

- Connect to WiFi with static IP
- Responds to HTTP requests:
  - `/on` → Turn LED ON
  - `/off` → Turn LED OFF
  - `/status` → Get current LED status
- Supports mDNS (`arduino.local`) for automatic discovery

```bash
TestMdns.ino
```

# Arduino R4 WiFi Controller


Arduino-connected LED over WiFi using a Python GUI. The project supports **mDNS discovery**, static IP, and real-time status monitoring.

---

## Features

- Discover Arduino via **mDNS** or connect via IP address
- Turn LED **ON/OFF** remotely
- Check LED **status**
- Activity log with timestamps
- Keyboard shortcuts:
  - **F1** → LED ON
  - **F2** → LED OFF
  - **Enter** → Connect to Arduino

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
TestMDNS.ino
```

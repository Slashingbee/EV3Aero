# EV3Aero ✈️  
**Modular Flight Yoke and Simulator Interface Powered by LEGO EV3**

EV3Aero is a fully open-source flight control system designed for use with LEGO Mindstorms EV3 hardware. It enables makers, educators, and simulator enthusiasts to build programmable yokes and flight interfaces using LEGO motors and sensors. Whether you're flying in a simulator, building a home cockpit, or just experimenting, EV3Aero gives you flexible control and expandability. 

---

## 📦 Features Overview

| Feature                     | Description                                                                                                            |
|-----------------------------|------------------------------------------------------------------------------------------------------------------------|
| 🔁 Modular Design           | Supports pitch/roll/throttle inputs via motors or sensors, easily extendable                                           |
| 🧱 LEGO EV3 Integration     | Uses ev3dev-compatible software to run directly on EV3 hardware (or anything running the ev3dev firmware)              |
| 🎮 Sim-Compatible           | Can output to X-Plane, MSFS, or custom serial / USB protocols (game's that support game controllers)                   |
| ⚙️ Configurable Mapping     | Emulate's a Xbox 360 Game controller interface via HID                                                                 |
| 📡 Data Output Options      | Send inputs over USB, Bluetooth, or sockets for telemetry or sim input                                                 |
| 💡 Open and Customizable    | Written in Python with readable structure for easy modification, with variables to easy config                         |
--------------------------------------------------------------------------------------------------------------------------------------------------------

## 🔧 Requirements

- LEGO EV3 Brick (running ev3dev or compatible OS with python support)
- At least 1 EV3 motor or sensor for input (e.g., throttle axis)
- USB , Bluetooth or TCP/IP (default), connection to a host PC
- Optional: X-Plane or MSFS for sim integration (any game that utilises a gamepad will work

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/EV3Aero.git
cd EV3Aero

# Transfer to your EV3 device and run (Python 3 required)
python3 ev3aero.py

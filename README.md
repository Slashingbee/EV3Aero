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

- LEGO EV3 Brick *(running ev3dev or compatible OS with python support (tested on 2.7 but will ***[Experimentally]*** work on 2.x and 3.x) and the ev3dev package)*
- At least 1 EV3 motor or sensor for input (e.g., throttle axis)
- USB , Bluetooth or TCP/IP (default), connection to a host PC
- Optional: X-Plane or MSFS for sim integration (any game that utilises a gamepad will work


## 🛠️ Installation

EV3Aero is split into two parts:
- **Client**: Runs on the LEGO EV3 brick (requires `ev3dev` or compatible OS).
- **Server**: Runs on the host PC and handles input/output to simulators or other targets.
- By **Default** the script use's the Ev3 central button (OK or Confirm button) to set all position's as the center of the axis.

---

### 📅 1. Clone the Repository

```bash
git clone https://github.com/slashingbee/EV3Aero.git
cd EV3Aero
cd Ev3Aero

```

---

### 🤖 2. Install on EV3 Brick (Client)

#### Prerequisites:
- EV3 running **ev3dev** or a Debian-based OS with Python 3.x or 2.x (Only tested by me on 2.7). 
- SSH or USB access to the EV3 brick (or other thru vscode).

#### Steps:
```bash
# On your EV3, transfer the Client files
scp -r Client/Ev3Aero/ robot@ev3dev.local:~/EV3Aero

# SSH into the EV3
ssh robot@ev3dev.local

# On the EV3:
cd EV3Aero
python3 main.py

# You can also use Visual Studio Code Ev3Dev extenstion to transfer and run the file easier.
```

---

### 💻 3. Install on Host PC (Server)

#### Prerequisites:
- Python 3.x installed (3.9 or higher was tested as working.)
- Any game/sim that supports game controllers (e.g., MSFS, X-Plane)

#### Steps:

```bash
# Move to the Server directory
cd Server

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install Python dependencies
pip install -r requirements.txt

# Run the server-side controller interface
python main.py
```

---

### 🔄 4. Connect Client and Server

- Ensure both devices are on the same network (Wi-Fi , Wi-Fi over HOTSPOT, or USB/BLUETOOTH with different configuration).
- The Client sends control data over sockets or Bluetooth to the Server.
- The Server processes inputs and sends them to the sim as HID/gamepad signals or custom events.

---

## Important info

- The contribution branch is automatically synced, once every a while to the beta branch (with the addition of mine beta features). It might not be stable and might not operate as intended. The main branch should be tested and stable, bug fix report's are a priority.
- The past-*version* branches are version's that were in use before the main branch.
- The contribute.md file show's how can you contribute, implement, add feature's or fork the repo for your improvement.
- Issue report's help make the program better
- If there is anything that needs to be change'd in the readme, file a issue or push request.
- When contributing, aim to maintain clean, readable code with proper documentation. Follow the coding standards outlined in the repo to ensure consistency.
- Always make sure to test the change's you add. Not working code will not be accepted, or will be removed or resolved later.
- Note the license of the following project is important when u want to make edit's or make your own version public. Private projects aren't taken into account.
---
## Mentions

---

- **[ev3drive](https://github.com/Xgames123/evdrive)**  
  A project that heavily inspired this work.

- **[ev3dev](https://www.ev3dev.org)**  
  The open-source operating system that made this possible.  
  Source code available on [GitHub](https://github.com/ev3dev/ev3dev).

- **[Pybricks](https://pybricks.com/)**  
  A Python environment for LEGO® hubs, great for structured, Python-based robotics programming.

- **[leJOS](https://lejos.sourceforge.io)**  
  A Java-based replacement firmware for LEGO Mindstorms, foundational for early programmable robot systems.

---

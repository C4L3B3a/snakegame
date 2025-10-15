# SnakeGame Developer Kit

More of a developer kit for Python game developers.  
Includes:

- A demo Snake game (`snakegame/game.py`)
- Crash detection and telemetry reporting (`snakegame/crash_detector.py`)
- Auto-updater (`snakegame/updater.py`)
- Flask-based support portal (`support_portal/`)

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/C4L3B3a/snakegame.git
cd snakegame
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# On Windows: venv\Scripts\activate
pip install -r requirements.txt
````

---

## Running the Game

```bash
python snakegame/game.py
```

---

## Building / Compiling

### Linux (.deb)

Dependencies:

* Python 3
* `dpkg-deb` (Debian/Ubuntu)

Steps:

1. Make the main script executable:

```bash
chmod +x snakegame/snakegame.py
```

2. Create folder structure for Debian package:

```
snakegame/
├── DEBIAN/
│   └── control
├── usr/
│   └── local/
│       └── bin/
│           └── snakegame.py
```

3. Build the package:

```bash
dpkg-deb --build snakegame_1.0.0
```

4. Install and test:

```bash
sudo dpkg -i snakegame_1.0.0.deb
snakegame.py
```

---

### Windows (.exe)

Dependencies:

* Python 3.8+ installed
* PyInstaller (`pip install pyinstaller`)

Steps:

1. Activate your Python virtual environment (optional):

```powershell
venv\Scripts\activate
```

2. Build the executable:

```bash
pyinstaller --onefile --icon=snake.ico --noconsole snakegame/game.py
```

3. The `.exe` will appear in the `dist/` folder. You can distribute it directly.

---

## Support Portal

Run the Flask app to enable ticketing and telemetry:

```bash
cd support_portal
source venv/bin/activate  # activate your venv
pip install -r requirements.txt
python app.py
```

Then open your browser at `http://localhost:5000` to use the portal.

---

## Telemetry & Crash Reporting

The game automatically detects crashes and can send **anonymous telemetry** to help improve the software.

No personal information (IP, accounts, passwords) is collected.

---

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

---

By C4L
:D

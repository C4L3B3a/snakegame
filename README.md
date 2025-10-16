# SnakeGame Developer Kit

More of a developer kit for Python game developers.  
Includes:

- A demo Snake game (`snakegame/snakegame.py`)
- Crash detection and telemetry reporting (`Function inside snakegame.py`)
- Auto-updater (`Function inside snakegame.py`)
- Admin panel with telemetry reciever and update pushing (`telemetry.php`)
- Flask-based support portal (`support_portal/app.py`)

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
python3 snakegame/game.py
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

The game automatically detects crashes and offers to send **anonymous telemetry** to help improve the software.

No personal information (IP, accounts, passwords) is collected.

---

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

---

## What do you need to host the software

- Personal server (To host the support portal and admin panel)
- WinSCP to host the server

## Recommended actions
- For logins: Use random usernames/password generators
- Build an encrypted system

I will update this repo more soon!

By C4L
:D

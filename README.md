# SnakeGame Developer Kit

More of a developer kit for Python game developers.

Includes:

* A demo Snake game (`snakegame.py`)
* Crash detection and telemetry reporting
* Auto-updater
* Admin panel (`telemetry.php`)
* Flask-based support portal (`support_portal/app.py`)

---

## Installation

```bash
git clone https://github.com/C4L3B3a/snakegame.git
cd snakegame
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Running the Game

```bash
python3 snakegame.py
```

---

## Compiling / Building

### Windows (.exe)

**Dependencies:** Python 3.8+, PyInstaller

**Build for x64/x86:**

```powershell
# Activate virtual environment
venv\Scripts\activate

# Build executable
pyinstaller --onefile --windowed snakegame.py --name SnakeGame_x64
pyinstaller --onefile --windowed snakegame.py --name SnakeGame_x86  # Optional, requires Python x86
```

The executables will appear in the `dist/` folder.

---

### macOS (.app / Executable)

**Dependencies:** Python 3, PyInstaller

**Build for x64/ARM64:**

```bash
# Activate virtual environment
source venv/bin/activate

# Build for Intel
pyinstaller --onefile --windowed snakegame.py --name SnakeGame_mac_x64

# Build for Apple Silicon
pyinstaller --onefile --windowed snakegame.py --name SnakeGame_mac_arm64
```

---

### Linux (.deb / .rpm / .tar.gz)

**Dependencies:** Python 3, `dpkg-dev`, `rpm`, `tar`

**.deb package (Debian/Ubuntu):**

```bash
chmod +x snakegame.py

mkdir -p snakegame-linux/DEBIAN
mkdir -p snakegame-linux/usr/local/bin
cp snakegame.py snakegame-linux/usr/local/bin/snakegame

# Create DEBIAN/control file (update package info)
dpkg-deb --build snakegame-linux
sudo dpkg -i snakegame-linux.deb
```

**.rpm package (Fedora/openSUSE/CentOS):**

```bash
mkdir -p rpm/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
mkdir -p rpm/SOURCES/snakegame-1.0.0
cp snakegame.py rpm/SOURCES/snakegame-1.0.0/
tar czvf rpm/SOURCES/snakegame-1.0.0.tar.gz -C rpm/SOURCES snakegame-1.0.0

# Create rpm/SPECS/snakegame.spec
rpmbuild --define "_topdir $(pwd)/rpm" -bb rpm/SPECS/snakegame.spec
```

**Generic tarball (.tar.gz):**

```bash
mkdir -p tarball/snakegame
cp snakegame.py tarball/snakegame/
cp -r support_portal tarball/snakegame/  # optional
tar czf snakegame_1.0.0.tar.gz -C tarball snakegame
```

---

### Snap (Optional)

**Requirements:** Snapcraft

```bash
sudo snap install snapcraft --classic
snapcraft pack  # creates snakegame_1.0.0_amd64.snap
sudo snap install snakegame_1.0.0_amd64.snap --dangerous
snapcraft upload snakegame_1.0.0_amd64.snap --release=stable
```

---

### Flatpak (Optional)

```bash
sudo apt install flatpak flatpak-builder
flatpak-builder build-dir snakegame.flatpak.yaml --force-clean
flatpak build-bundle repo snakegame.flatpak com.c4l.SnakeGame 1.0.0
```

---

### Notes

* Windows x86 requires Python x86 installed.
* macOS builds require a macOS runner / machine.
* ARM builds may require ARM runners or cross-compilation.
* Snap/Flatpak builds require their respective packaging files (`snapcraft.yaml` / `.flatpak.yaml`).

---

### Admin Panel

Start a local server:

```bash
python3 -m http.server 8000
```

---

### Support Portal

```bash
cd support_portal
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open: [http://localhost:5000](http://localhost:5000)

---

### Telemetry & Crash Reporting

Anonymous telemetry is collected automatically. No personal information is stored.

---

By C4L
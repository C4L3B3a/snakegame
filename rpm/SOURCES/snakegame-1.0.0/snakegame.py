import tkinter as tk
from tkinter import messagebox
import random
import string
import requests
import platform
import time
import secrets  # for secure random IDs
import traceback
import webbrowser
import os
import zipfile
import subprocess
from packaging import version  # used to compare version numbers

# -------------------------------
# Version & Game Info
# -------------------------------
__version__ = "1.0.0"
__game__ = "SnakeGame"

# URLs for telemetry server and website/support portal
TELEMETRY_URL = "http://localhost:8000/telemetry.php"  # change to your server
WEBSITE_URL = "http://localhost:5000/"  # change to your site (Support Portal)
# Btw, the sites need to be working/up to actually redirect, otherwise, you will see 404 or simply "Site cannot be reached" or some similar stuff

# Why IP difference in URLs?
# - TELEMETRY_URL uses normal localhost
# - WEBSITE_URL uses flask, which usually uses http://localhost:5000/ instead of http://localhost:8000/

# -------------------------------
# UPDATE CHECKER
# -------------------------------
def check_update():
    """
    Checks server for updates.
    Downloads and installs if a newer version is available.
    Skips update if current version >= server version.
    """
    OS = platform.system()
    try:
        resp = requests.get(TELEMETRY_URL, params={"check_update": 1, "os": OS}, timeout=5)
        data = resp.json()
        server_version = data.get("version")

        # Skip update if current version is up-to-date or server doesn't provide version
        if not server_version or version.parse(server_version) <= version.parse(__version__):
            print(f"No update needed. Current version: {__version__}, Server version: {server_version}")
            return

        # If update available
        if data.get("update_available"):
            # Show info popup
            info_box = tk.Tk()
            info_box.withdraw()
            messagebox.showinfo(
                "Update available",
                f"New version available: {server_version}\nDownloading and installing..."
            )
            info_box.update()
            
            url = data['url']
            local_zip = os.path.join(os.getcwd(), "update.zip")

            # Download update
            r = requests.get(url)
            with open(local_zip, "wb") as f:
                f.write(r.content)

            # Extract update
            extract_dir = os.path.join(os.getcwd(), "update_temp")
            if not os.path.exists(extract_dir):
                os.makedirs(extract_dir)
            with zipfile.ZipFile(local_zip, "r") as zip_ref:
                zip_ref.extractall(extract_dir)

            # Install update depending on OS
            if OS == "Linux":
                deb_files = [f for f in os.listdir(extract_dir) if f.endswith(".deb")]
                if deb_files:
                    deb_path = os.path.join(extract_dir, deb_files[0])
                    try:
                        subprocess.run(["sudo", "dpkg", "-i", deb_path], check=True)
                        subprocess.run(["sudo", "apt-get", "install", "-f", "-y"], check=True)
                        messagebox.showinfo("Update", "Update installed successfully!\nThe message will close automatically.")
                        info_box.update()
                        info_box.destroy()
                    except subprocess.CalledProcessError as e:
                        messagebox.showerror("Update failed", f"Installation failed:\n{e}")
                        info_box.update()
                        info_box.destroy()
            elif OS == "Windows":
                exe_files = [f for f in os.listdir(extract_dir) if f.endswith(".exe")]
                if exe_files:
                    try:
                        subprocess.Popen([os.path.join(extract_dir, exe_files[0])])
                        messagebox.showinfo("Update", "Update launched successfully!\nThe message will close automatically.")
                        info_box.update()
                        info_box.destroy()
                    except Exception as e:
                        messagebox.showerror("Update failed", f"Failed to launch installer:\n{e}")
                        info_box.update()
                        info_box.destroy()
    except Exception as e:
        print("Update check failed:", e)

# Call update check before starting the game
check_update()

# -------------------------------
# TELEMETRY HELPERS
# -------------------------------
def gerar_id_aleatoria(tamanho=12):
    """Generate a short secure random ID (URL-safe)."""
    alphabet = string.ascii_letters + string.digits + "-_"
    return ''.join(secrets.choice(alphabet) for _ in range(tamanho))

def send_telemetry(crash_id, version, extra=None):
    """
    Send anonymous telemetry data to the server.
    Does NOT include personal info.
    """
    payload = {
        "telemetry_id": crash_id,
        "game": __game__,
        "version": version,
        "os": platform.system(),
        "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    if extra:
        payload["extra"] = extra

    try:
        resp = requests.post(TELEMETRY_URL, data=payload, timeout=5)
        return resp.text
    except Exception as e:
        return f"Failed to send telemetry: {e}"

# -------------------------------
# SNAKE GAME CLASS
# -------------------------------
class SnakeGame:
    def __init__(self, master):
        """Initialize game variables and UI."""
        self.master = master
        self.master.title("Snake Game")
        self.width = 400
        self.height = 400
        self.cell_size = 20
        self.direction = "Right"
        self.running = True

        # Canvas for drawing snake & food
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # Snake starting position
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.place_food()
        self.score = 0

        # Bind arrow keys
        self.master.bind("<Up>", self.go_up)
        self.master.bind("<Down>", self.go_down)
        self.master.bind("<Left>", self.go_left)
        self.master.bind("<Right>", self.go_right)

        # Start game loop
        self.update()

    # -------------------------------
    # GAME LOGIC
    # -------------------------------
    def place_food(self):
        """Randomly place food on the grid where the snake is not."""
        while True:
            x = random.randrange(0, self.width, self.cell_size)
            y = random.randrange(0, self.height, self.cell_size)
            if (x, y) not in self.snake:
                return (x, y)

    # Direction change methods
    def go_up(self, event):
        if self.direction != "Down": self.direction = "Up"
    def go_down(self, event):
        if self.direction != "Up": self.direction = "Down"
    def go_left(self, event):
        if self.direction != "Right": self.direction = "Left"
    def go_right(self, event):
        if self.direction != "Left": self.direction = "Right"

    # Main game loop
    def update(self):
        if not self.running:
            return
        try:
            head_x, head_y = self.snake[0]
            if self.direction == "Up": head_y -= self.cell_size
            elif self.direction == "Down": head_y += self.cell_size
            elif self.direction == "Left": head_x -= self.cell_size
            elif self.direction == "Right": head_x += self.cell_size

            new_head = (head_x, head_y)

            # Check collisions with walls or self
            if head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height or new_head in self.snake:
                self.running = False
                self.handle_crash(reason="Collision")
                return

            # Move snake
            self.snake.insert(0, new_head)

            # Check if food eaten
            if new_head == self.food:
                self.score += 1
                self.food = self.place_food()
            else:
                self.snake.pop()

            # Draw snake & food
            self.draw()

            # Schedule next update
            self.master.after(100, self.update)
        except Exception:
            self.handle_crash(reason="Exception", exception=traceback.format_exc())

    # -------------------------------
    # CRASH HANDLER
    # -------------------------------
    def handle_crash(self, reason, exception=None):
        """
        Handles game crash:
        - Shows a warning
        - Prompts user to send telemetry
        - Optionally opens website for help
        """
        crash_id = gerar_id_aleatoria()
        os_name = platform.system()

        # Collect anonymous info
        extra = f"score={self.score}"
        if exception:
            extra += f" | exception={exception[:800]}"
        else:
            stack = "".join(traceback.format_stack(limit=5))
            extra += f" | stack={stack[:800]}"

        # Show crash warning
        messagebox.showwarning(f"{__game__} crashed!", f"{__game__} has crashed!\n\nCrash ID: {crash_id}")

        # Ask for telemetry consent
        ask_text = (
            f"Do you want to help the developer by sending telemetry?\n\n"
            f"It does NOT send: IP, accounts, passwords, or any personal information.\n\n"
            f"It only sends:\n"
            f"- Crash ID: {crash_id}\n"
            f"- OS: {os_name}\n"
            f"- Where in the code it failed and a short stack trace."
        )
        consent = messagebox.askyesno("Help the developer by sending telemetry", ask_text)

        if consent:
            send_telemetry(crash_id, __version__, extra=extra)
            messagebox.showinfo("Thanks for helping the development",
                                f"Thanks for helping the development of {__game__}!\n"
                                f"Your crash ID was: {crash_id}")
            self.master.destroy()
        else:
            webbrowser.open(WEBSITE_URL)
            messagebox.showerror("No telemetry sent",
                                 "No telemetry was sent to our servers.\n"
                                 "Restart the game to try again.\n"
                                 "If this error keeps happening, visit our website for help.")
            self.master.destroy()

    # -------------------------------
    # DRAW FUNCTION
    # -------------------------------
    def draw(self):
        """Draw snake and food on canvas."""
        self.canvas.delete("all")
        x, y = self.food
        self.canvas.create_rectangle(x, y, x+self.cell_size, y+self.cell_size, fill="red")
        for i, (x, y) in enumerate(self.snake):
            color = "green" if i == 0 else "lightgreen"
            self.canvas.create_rectangle(x, y, x+self.cell_size, y+self.cell_size, fill=color)
        self.canvas.create_text(50, 10, fill="white", text=f"Score: {self.score}", anchor="nw")

# -------------------------------
# MAIN ENTRY POINT
# -------------------------------
def main():
    root = tk.Tk()
    root.geometry("400x400") # Window dimension
    game = SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# By C4L
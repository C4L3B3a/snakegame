from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

# ------------------- App Setup -------------------
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session handling (flash messages, login)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect unauthorized users to login page

DB_PATH = "tickets.db"  # Database file, automatically created

# ------------------- Database Initialization -------------------
def init_db():
    """
    Creates the database and tables if they don't exist yet.
    Two tables:
    - users: stores registered users (username, password hash, role)
    - tickets: stores submitted support tickets linked to users
    """
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Users table: id, username, hashed password, role (user/admin)
        c.execute('''CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT DEFAULT 'user'
                     )''')
        # Tickets table: id, user_id (FK), title, description, status, admin reply
        c.execute('''CREATE TABLE tickets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        title TEXT,
                        description TEXT,
                        status TEXT DEFAULT 'Open',
                        reply TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                     )''')
        conn.commit()
        conn.close()

# Initialize database on app start
init_db()

# ------------------- User Model -------------------
class User(UserMixin):
    """
    User class required by Flask-Login.
    Stores id, username, and role (user/admin).
    """
    def __init__(self, id_, username, role):
        self.id = id_
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login user loader.
    Fetches user from DB by ID.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, role FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return User(*row)
    return None

# ------------------- Routes -------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    User registration page.
    Stores hashed passwords for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])  # hash password
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
            conn.commit()
            conn.close()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists.", "danger")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login page.
    Checks username and password hash.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, username, password, role FROM users WHERE username=?", (username,))
        row = c.fetchone()
        conn.close()
        # Verify password hash
        if row and check_password_hash(row[2], password):
            user = User(row[0], row[1], row[3])
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    """
    Logout route.
    Ends user session and redirects to login page.
    """
    logout_user()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def dashboard():
    """
    Dashboard view.
    - Admin: sees all tickets
    - User: sees only their own tickets
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if current_user.role == "admin":
        # Join users table to show ticket owners
        c.execute("SELECT tickets.id, users.username, title, status FROM tickets JOIN users ON tickets.user_id=users.id")
    else:
        c.execute("SELECT id, title, status FROM tickets WHERE user_id=?", (current_user.id,))
    tickets = c.fetchall()
    conn.close()
    return render_template("dashboard.html", tickets=tickets, is_admin=current_user.role=="admin")

@app.route("/ticket", methods=["GET", "POST"])
@login_required
def ticket():
    """
    Submit a new ticket.
    Stores ticket title, description, and user_id.
    """
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["description"]
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO tickets (user_id, title, description) VALUES (?,?,?)",
                  (current_user.id, title, desc))
        conn.commit()
        conn.close()
        flash("Ticket submitted successfully!", "success")
        return redirect(url_for("dashboard"))
    return render_template("ticket.html")

@app.route("/ticket/<int:ticket_id>", methods=["GET", "POST"])
@login_required
def view_ticket(ticket_id):
    """
    View a ticket.
    - Admin: can reply and mark as resolved
    - User: can only view
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if current_user.role == "admin" and request.method == "POST":
        reply = request.form["reply"]
        c.execute("UPDATE tickets SET reply=?, status='Resolved' WHERE id=?", (reply, ticket_id))
        conn.commit()
        flash("Replied successfully.", "success")
    # Fetch ticket details with username
    c.execute("SELECT tickets.id, users.username, title, description, status, reply FROM tickets JOIN users ON tickets.user_id=users.id WHERE tickets.id=?", (ticket_id,))
    ticket_data = c.fetchone()
    conn.close()
    if not ticket_data:
        flash("Ticket not found.", "danger")
        return redirect(url_for("dashboard"))
    return render_template("admin.html", ticket=ticket_data, is_admin=current_user.role=="admin")

# ------------------- Run App -------------------
if __name__ == "__main__":
    # Debug=True for development; remove in production
    app.run(debug=True)

# By C4L
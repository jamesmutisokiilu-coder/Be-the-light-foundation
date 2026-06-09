from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# =========================
# CONFIGURATION
# =========================

app.secret_key = os.environ.get("SECRET_KEY", "btlf_secret_key")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "btlf.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================
# DATABASE TABLES
# =========================

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)


# =========================
# PUBLIC PAGES
# =========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/approach")
def approach():
    return render_template("approach.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/education")
def education():
    return render_template("education.html")


@app.route("/empowerment")
def empowerment():
    return render_template("empowerment.html")


@app.route("/mentalhealth")
def mental_health():
    return render_template("mentalhealth.html")


@app.route("/outreach")
def outreach():
    return render_template("outreach.html")


@app.route("/spiritual")
def spiritual():
    return render_template("spiritual.html")


@app.route("/assistant")
def assistant():
    return render_template("assistant.html")


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already registered."

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username

            return redirect(url_for("dashboard"))

        return "Invalid login details"

    return render_template("login.html")


# =========================
# USER DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


# =========================
# ASSISTANT MESSAGE SYSTEM
# =========================

@app.route("/send-message", methods=["POST"])
def send_message():

    new_message = Message(
        name=request.form.get("name"),
        email=request.form.get("email"),
        phone=request.form.get("phone"),
        content=request.form.get("message")
    )

    db.session.add(new_message)
    db.session.commit()

    return redirect(url_for("assistant"))


# =========================
# ADMIN LOGIN
# =========================

ADMIN_USERNAME = "kutosi123"
ADMIN_PASSWORD = "empowerment"


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))

        return "Invalid admin credentials"

    return render_template("admin_login.html")


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin-dashboard")
def admin_dashboard():

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    users = User.query.all()
    messages = Message.query.all()

    return render_template(
        "admin_dashboard.html",
        users=users,
        messages=messages
    )


# =========================
# ADMIN LOGOUT
# =========================

@app.route("/admin-logout")
def admin_logout():

    session.pop("admin", None)

    return redirect(url_for("admin_login"))


# =========================
# USER LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.pop("user_id", None)
    session.pop("username", None)

    return redirect(url_for("login"))


# =========================
# CREATE DATABASE
# =========================

with app.app_context():
    db.create_all()


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

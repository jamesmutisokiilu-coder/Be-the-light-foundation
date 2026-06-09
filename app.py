from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "btlf_secret_key"

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///btlf.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# DATABASE TABLES
# =========================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Message(db.Model):
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
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect("/dashboard")

        return "Invalid login details"

    return render_template("login.html")


# =========================
# DASHBOARD (USER)
# =========================

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


# =========================
# ASSISTANT MESSAGE SYSTEM
# =========================

@app.route("/send-message", methods=["POST"])
def send_message():
    new_msg = Message(
        name=request.form["name"],
        email=request.form["email"],
        phone=request.form["phone"],
        content=request.form["message"]
    )

    db.session.add(new_msg)
    db.session.commit()

    return redirect("/assistant")


# =========================
# ADMIN LOGIN
# =========================

ADMIN_USERNAME = "kutosi123"
ADMIN_PASSWORD = "empowerment"

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin-dashboard")

        return "Invalid admin credentials"

    return render_template("admin_login.html")


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin-dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin-login")

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
    return redirect("/admin-login")


# =========================
# LOGOUT USER
# =========================

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/login")


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
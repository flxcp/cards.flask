from flask import redirect, request, render_template, url_for, session, flash
from flask import current_app as app
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from .db import db, User
from flask_login import login_user, logout_user, login_required
from main import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None
        user = db.session.query(User).filter_by(
            username=username).first()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            login_user(user)
            return redirect(url_for('dashboard'))

        if error is not None:
            flash(error, 'danger')

    return render_template("auth/login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif (
            db.session.query(User).filter_by(
                username=username).first() is not None
        ):
            error = f"User {username} is already registered."

        if error is None:
            # the name is available, store it in the database and go to
            # the login page

            user = User(username=username,
                        password=generate_password_hash(password))

            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))

        if error is not None:
            flash(error, 'danger')

    return render_template("auth/register.html")

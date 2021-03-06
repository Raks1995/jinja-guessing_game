import random
import uuid
import hashlib
from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User, db

app = Flask(__name__)
db.create_all()


@app.route("/", methods=["GET"])
def index():
    session_token = request.cookies.get("session_token")
    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
    else:
        user = None

    return render_template("index.html", user=user)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")
    password = request.form.get("user-password")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    secret_number = random.randint(1, 30)

    user = db.query(User).filter_by(email=email).first()
    if not user:
        user = User(name=name, email=email, secret_number=secret_number, password=hashed_password)
        db.add(user)
        db.commit()

    if hashed_password != user.password:
        return "WRONG PASSWORD"
    elif hashed_password == user.password:
        session_token = str(uuid.uuid4())
        user.session_token = session_token
        db.add(user)
        db.commit()

    response = make_response(redirect(url_for("index")))
    response.set_cookie("session_token", session_token, httponly=True, samesite="Strict")

    return response


@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))
    session_token = request.cookies.get("session_token")

    user = db.query(User).filter_by(session_token=session_token).first()

    if guess == user.secret_number:
        message = "Correct! The secret number is {0}".format(str(user.secret_number))
        new_secret = random.randint(1, 30)
        user.secret_number = new_secret
        db.add(user)
        db.commit()
    elif guess > user.secret_number:
        message = "Your guess is not correct... try something smaller."
    elif guess < user.secret_number:
        message = "Your guess is not correct... try something bigger."

    return render_template("result.html", message=message)


if __name__ == '__main__':
    app.run()

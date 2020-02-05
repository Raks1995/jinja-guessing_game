from flask import Flask, render_template, request, make_response
import random

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        secret_number = request.cookies.get("secret_number")
        response = make_response(render_template("index.html"))
        if not secret_number:
            new_secret = random.randint(1, 30)
            response.set_cookie("secret_number", str(new_secret))

        return response
    if request.method == "POST":
        guess = int(request.form.get("guess"))
        secret_number = int(request.cookies.get("secret_number"))
        if guess == secret_number:
            message = "Correct, it is {0}".format(str(secret_number))
            response = make_response(render_template("index.html", message=message))
            response.set_cookie("secret_number", str(random.randint(1, 30)))
            return response
        elif guess > secret_number:
            message = "Incorrect..try sth smaller!"
            return render_template("index.html", message=message)
        elif guess < secret_number:
            message = "Incorrect..try sth bigger"
            return render_template("index.html", message=message)


if __name__ == '__main__':
    app.run()
# imports
from flask import Flask, render_template, request
import main


# vars
a = {"good": "-", "bad": "-"}


# main
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", a=a)

@app.route("/", methods=["POST"])
def search():
    a = main.analyse(request.form["url"], request.form["kw"])
    return render_template("index.html", a=a)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

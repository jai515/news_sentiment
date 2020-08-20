import flask
from flask import Flask, redirect, url_for, render_template, request
import graph

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def get_graph():
    if flask.request.method == "POST":
        domain = request.form.get('domain')
        topic = request.form.get('topic')
        graph.compare_news([topic], [domain])
        return redirect(url_for("show_graph"))
    else:
        return render_template("graph.html")


@app.route("/<name>")
def index(name):
    return render_template("basic.html", name=name)


@app.route('/graph')
def show_graph():
    return render_template("basic.html")


@app.route("/admin")
def hello_admin():
    return "Hello Admin"


@app.route("/guest/<guesty>")
def hello_guest(guesty):
    return f"Hello {guesty} Guest"


@app.route("/user/<name>")
def hello_user(name):
    if name == "admin":
        return redirect(url_for("hello_admin"))

    else:
        return redirect(url_for("hello_guest", guesty=name))


if __name__ == "__main__":
    app.run(host="localhost", port=3000)

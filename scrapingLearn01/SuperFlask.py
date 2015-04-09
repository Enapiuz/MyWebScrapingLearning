from flask import Flask, render_template
from helpers import db as dbhelper

app = Flask(__name__)


@app.route('/')
def hello_world():
    posts = dbhelper.get_entries()
    return render_template("index.html", posts=posts)


if __name__ == '__main__':
    app.run()



from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="empence",
    password="JJaOHH81TMC3",
    hostname="empence.mysql.pythonanywhere-services.com",
    databasename="empence$alerts",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route('/lurkerbot', methods=["GET", "POST"])
def lurkerbot():
    if request.method == "GET":
        return render_template("index.html")
    request.form["phrase"]
    request.form["subreddit"]
    request.form["email"]
    return redirect(url_for("lurkerbot"))





from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager

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

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True) # a user ID
    email = db.Column(db.String(256), nullable=False)
    alerts = db.relationship('Alert', backref='user', lazy=True)

class Alert(db.Model):
    __tablename__ = "alert"
    id = db.Column(db.Integer, primary_key=True) #an alert ID
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) # a user ID
    subreddits = db.relationship('Subreddit', backref='alert', lazy=True)
    phrases = db.relationship('Phrase', backref='alert', lazy=True)

class Subreddit(db.Model):
    __tablename__ = "subreddit"
    id = db.Column(db.Integer, primary_key=True) #entry ID
    alert = db.Column(db.Integer, db.ForeignKey("alert.id"), nullable=False) #the alert it's associated with
    subreddit = db.Column(db.String(20)) #subreddit name: the subreddit to watch

class Phrase(db.Model):
    id = db.Column(db.Integer, primary_key=True) #entry ID
    alert = db.Column(db.Integer, db.ForeignKey("alert.id"), nullable=False) #the alert it's associated with
    phrase = db.Column(db.String(256)) #the phrase to watch for

@app.route('/lurkerbot', methods=["GET", "POST"])
def lurkerbot():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "GET":
        request.form["phrase"]
        request.form["subreddit"]
        request.form["email"]
        return redirect(url_for("lurkerbot"))



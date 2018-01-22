import sys
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import flask_login
from flask_login import UserMixin, LoginManager, current_user, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
login = LoginManager(app)

app.config.from_object(Config)


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
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) # a user ID
    username = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(128))
    alerts = db.relationship('Alert', backref='users', lazy=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Alert(db.Model):
    __tablename__ = "alerts"
    id = db.Column(db.Integer, primary_key=True) #an alert ID
    user_id = db.Column(db.Integer, db.ForeignKey("users.id")) # a user ID
    subreddits = db.relationship('Subreddit', backref='alerts', lazy=True)
    phrases = db.relationship('Phrase', backref='alerts', lazy=True)

class Subreddit(db.Model):
    __tablename__ = "subreddits"
    id = db.Column(db.Integer, primary_key=True) #entry ID
    alert = db.Column(db.Integer, db.ForeignKey("alerts.id")) #the alert it's associated with
    subreddit = db.Column(db.String(20)) #subreddit name: the subreddit to watch

class Phrase(db.Model):
    __tablename__ = "phrases"
    id = db.Column(db.Integer, primary_key=True) #entry ID
    alert = db.Column(db.Integer, db.ForeignKey("alerts.id")) #the alert it's associated with
    phrase = db.Column(db.String(256)) #the phrase to watch for

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/base',)
def base():
    return render_template('base.html', title="Base")

@app.route('/lurkerbot/logout',)
def logout():
    logout_user()
    return redirect(url_for("lurkerbot"))

@app.route('/lurkerbot/edit',)
def edit():
    return ""

@app.route('/lurkerbot/', methods=["GET","POST"])
@app.route('/lurkerbot', methods=["GET", "POST"])
def lurkerbot():
    if request.method == "GET":
        return render_template("index.html",)
    elif request.method == "POST":
        #split phrase by commas, strip leading and trailing spaces, create a new phrase object for each
        new_phrases = [Phrase(phrase=x.strip()) for x in request.form["phrase"].split(",")]
        for p in new_phrases:
            db.session.add(p)
        new_subreddits = [Subreddit(subreddit=x.strip()) for x in request.form["subreddit"].split(",")]
        for s in new_subreddits:
            db.session.add(s)

        new_alert = Alert(subreddits=new_subreddits, phrases=new_phrases)

        user = User.query.filter_by(username=request.form["username"]).first()
        if user:
            if len(user.alerts) == 0:
                user.alerts = [new_alert]
            else:
                user.alerts.append(new_alert)
        else:
            user = User(username=request.form["username"].strip(), alerts=[new_alert])
            user.set_password(request.form["password"])
            db.session.add(user)
        db.session.add(new_alert)

        db.session.commit()

        return redirect(url_for("lurkerbot"))

@app.route('/lurkerbot/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", title="Login")
    elif request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user.check_password(request.form["password"]):
            login_user(user)
            return redirect(url_for("lurkerbot"))
        else:
            return redirect(url_for("login"))




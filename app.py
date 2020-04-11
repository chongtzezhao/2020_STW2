import os
from flask import Flask

# db imports
from flask_sqlalchemy import SQLAlchemy

# form imports
from wtforms.validators import InputRequired, Length
from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields.html5 import EmailField

# email imports (beta)
from flask_mail import Mail


'''
from flask_mysqldb import MySQL
import yaml


# Configure mysql
db_config = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db_config['mysql_host']
app.config['MYSQL_USER'] = db_config['mysql_user']
app.config['MYSQL_PASSWORD'] = db_config['mysql_password']
app.config['MYSQL_DB'] = db_config['mysql_db']

mysql = MySQL(app)
'''
app = Flask(__name__)

# --- SQLAlchemy ---

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(
    os.getenv("mysql_user"),
    os.getenv("mysql_password"),
    os.getenv("mysql_host"),
    os.getenv("mysql_db")
)
''' 
db_config = yaml.safe_load(open('db.yaml'))
(
    db_config['mysql_user'], 
    db_config['mysql_password'], 
    db_config['mysql_host'], 
    db_config['mysql_db']
    )'''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    UserID = db.Column(db.String(255), primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    Admin = db.Column(db.Boolean, nullable=False)

    def __init__(self, UserID, Name, Password, Email, Admin=False):
        self.UserID = UserID
        self.Name = Name
        self.Password = Password
        self.Email = Email
        self.Admin = Admin


class Question(db.Model):
    QuestionID = db.Column(db.Integer, primary_key=True)
    QuestionText = db.Column(db.String(255), nullable=False)
    Option1 = db.Column(db.String(255), nullable=False)
    Option2 = db.Column(db.String(255), nullable=False)
    Answer = db.Column(db.Integer, nullable=False)

    def __init__(self, QuestionText, Option1, Option2, Answer):
        self.QuestionText = QuestionText
        self.Option1 = Option1
        self.Option2 = Option2
        self.Answer = Answer


class Attempt(db.Model):
    AttemptID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.String(255), nullable=False)
    QuestionID = db.Column(db.Integer, nullable=False)
    Response = db.Column(db.String(255), nullable=False)

    def __init__(self, UserID, QuestionID, Response):
        self.UserID = UserID
        self.QuestionID = QuestionID
        self.Response = Response


class CountAttempt(db.Model):
    UserID = db.Column(db.String(255), primary_key=True)
    QuestionID = db.Column(db.Integer, primary_key=True)
    NumAttempts = db.Column(db.Integer, nullable=False, default=0)
    Correct = db.Column(db.Boolean, nullable=False, default=False)
    PracticeAttempts = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, UserID, QuestionID, NumAttempts=0, PracticeAttempts=0,  Correct=False):
        self.UserID = UserID
        self.QuestionID = QuestionID
        self.NumAttempts = NumAttempts
        self.Correct = Correct
        self.PracticeAttempts = PracticeAttempts


db.create_all()
db.session.commit()

# --- Flask_wtf and wtforms ---

app.config['SECRET_KEY'] = os.urandom(24)
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')


class SignUpForm(FlaskForm):
    user_name = StringField('Name:', validators=[
        InputRequired(),
        Length(max=40,
               message="Maximum of 40 characters.")])
    userid = StringField('UserID:', validators=[
        InputRequired(),
        Length(max=20,
               message="Maximum of 40 characters.")])
    password = PasswordField('Enter password:', validators=[
        InputRequired(),
        Length(min=8, max=40,
               message="Maximum of 40 characters.")])
    confirm = PasswordField('Re-enter password:', validators=[
        InputRequired(),
        Length(min=8, max=40,
               message="Maximum of 40 characters.")])
    email = EmailField('Email Address:', validators=[
        InputRequired()
        ])
    recaptcha = RecaptchaField()


class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email Address', validators=[
        InputRequired()
    ])
    recaptcha = RecaptchaField()

# --- Flask_mail ---

mail = Mail(app)

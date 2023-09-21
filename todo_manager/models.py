## models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def is_active(self):
        return True  
    
    @property
    def is_authenticated(self):
        return True  
    
    def get_id(self):
        return str(self.id)  #

    def __init__(self, username: str, password: str):
        self.username = username
        self.set_password(password)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title: str, user_id: int):
        self.title = title
        self.user_id = user_id

    def mark_as_completed(self):
        self.completed = True

    def __repr__(self):
        return '<Task {}>'.format(self.title)

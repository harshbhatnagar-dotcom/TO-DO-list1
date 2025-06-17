from app import db


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20),  default="pending")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False,unique=True)
    tasks = db.relationship('Tasks', backref='user', lazy=True)

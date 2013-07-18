from flask.ext.sqlalchemy import SQLAlchemy
from init import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:please@localhost/overtone'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80), unique=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Email %r>' % self.email

from flask.ext.sqlalchemy import SQLAlchemy
from init import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:please@localhost/overtone'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80), unique=False)
    addresses = db.relationship('Song', backref='users',
                                lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Email %r>' % self.email


class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, data, user_id):
        self.data = data
        self.user_id = user_id

    def __repr__(self):
        return self.data


class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return self.name

song_ownership = db.Table('song_ownership',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id'))
)

playlist_to_song = db.Table('palylist_to_song',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id'))
)

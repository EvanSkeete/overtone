from flask.ext.sqlalchemy import SQLAlchemy
from init import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:please@localhost/overtone'
db = SQLAlchemy(app)

song_ownership = db.Table('song_ownership',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id'))
)

playlist_to_song = db.Table('playlist_to_song',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id'))
)


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


class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    artist = db.Column(db.String(120))
    album = db.Column(db.String(120))
    time = db.Column(db.String(120))
    plays = db.Column(db.String(10))
    videoId = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, videoId, user_id, **kwargs):
        self.name = name
        self.videoId = videoId
        self.user_id = user_id
        self.artist = kwargs.get('artist', '')
        self.album = kwargs.get('album', '')
        self.time = kwargs.get('time', '')
        self.plays = kwargs.get('plays', '1')

    def __repr__(self):
        return self.name


class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    songs = db.relationship('Song', secondary=playlist_to_song,
        backref=db.backref('playlists', lazy='dynamic'))

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return self.name


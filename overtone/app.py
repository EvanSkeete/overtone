from flask import session, redirect, url_for, escape, request, render_template, json, flash
from init import app
from model import *
import sys, pdb


@app.route('/main')
def main():
    if 'email' in session:
        email = escape(session['email'])
        user_id = escape(session['user_id'])
        user = escape(session['email']).split('@')[0]

        playlists = Playlist.query.filter_by(user_id=user_id).all()
        app.logger.debug(playlists)

        songs = Song.query.filter_by(user_id=user_id).all()
        app.logger.debug(songs)


        return render_template('main.html', user=user, songs=songs, playlists=playlists)
    return 'You are not logged in'


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        app.logger.debug(email)
        app.logger.debug(password)

        stored_password = User.query.filter_by(email=email).one().password
        user_id = User.query.filter_by(email=email).one().id
        if(stored_password != password):
            return json.jsonify(status=False)

        session['email'] = email
        session['user_id'] = user_id
        return json.jsonify(status=True)

    if 'email' in session:
        return redirect(url_for('main'))

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    app.logger.debug(session)
    try:
        session.pop('email')
        session.pop('user_id')
    except KeyError:
        pass
    app.logger.debug(session)
    return redirect(url_for('login'))


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']

    user = User(email, password)

    try:
        db.session.add(user)
        db.session.commit()
    except:
        app.logger.debug(sys.exc_info()[0])
        return json.jsonify(status=False)

    app.logger.debug(User.query.all())
    user_id = User.query.filter_by(email=email).one().id
    session['email'] = email
    session['user_id'] = user_id

    flash('Thanks for registering')
    return json.jsonify(status=True)


@app.route('/add_song', methods=['POST'])
def add_song():
    app.logger.debug('adding song')
    name = request.form['name']
    videoId = request.form['videoId']
    user_id = session['user_id']
    artist = request.form['artist']

    song = Song(name, videoId, user_id, artist=artist)
    db.session.add(song)
    db.session.commit()
    from_db = Song.query.filter_by(user_id=user_id).all()
    app.logger.debug(from_db)
    return json.jsonify(status=True, name=name)

@app.route('/modify_song', methods=['POST'])
def modify_song():
    app.logger.debug('modifying song')
    app.logger.debug(request.form)
    videoId = request.form.get('videoId')
    song = Song.query.filter_by(videoId=videoId).one()
    for k in request.form.keys():
        setattr(song, k, request.form[k])
        db.session.commit()
    return json.jsonify(status=True)

@app.route('/add_playlist', methods=['POST'])
def add_playlist():
    name = request.form['name']
    user_id = session['user_id']

    playlist = Playlist(name, user_id)
    db.session.add(playlist)
    db.session.commit()

    playlist.songs.append(Song('generic song', user_id))
    db.session.commit()

    playlists = Playlist.query.filter_by(user_id=user_id).all()
    for i in playlists:
        app.logger.debug(i)
        app.logger.debug(i.songs)

    return json.jsonify(status=True, name=name)

#Secret key for session signing:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.debug = True
db.create_all()


if __name__ == "__main__":
    app.debug = True
    db.create_all()
    app.run()

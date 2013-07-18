from flask import session, redirect, url_for, escape, request
from flask import render_template
from init import app
from model import *


@app.route('/main')
def main():
    if 'email' in session:
        email = escape(session['email'])
        user = escape(session['email']).split('@')[0]
        return render_template('main.html', user=user)
    return 'You are not logged in'


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login(name=None):
    if request.method == 'POST':

        #TODO: Need to authenticate here before registering the session
        email = request.form['email']
        password = request.form['password']

        session['email'] = email

        app.logger.debug(email)
        app.logger.debug(password)

        return redirect(url_for('main'))
    return render_template('login.html', name=name)


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']

    user = User(email, password)
    db.session.add(user)
    db.session.commit()
    app.logger.debug(User.query.all())

    session['email'] = email

    return redirect(url_for('main'))


#Secret key for session signing:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.debug = True
    db.create_all()
    app.run()

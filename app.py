from urllib import request
import flask
import sqlite3
import jwt
import datetime
import passUtil

passutil = passUtil.passUtil('sha512')

current_tokens = []

db = 'main.db'

app = flask.Flask(__name__)

def randString(length):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def verify(request):
    if request.cookies.get('session_token') is None:
        return None
    else:
        jwt_token = request.cookies.get('session_token')
        decoded_jwt = jwt.decode(jwt_token, 'secret', algorithms=['HS256'])
        if decoded_jwt['ip'] != request.remote_addr:
            return None
        # if jwt_token not in current_tokens:
        #     return None

    return 0

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    else:
        username = flask.request.form['username']
        password = flask.request.form['password']
        
        ldbc = sqlite3.connect(db)
        dbC = ldbc.cursor()
        dbC.execute('SELECT * FROM users WHERE username=?', (username,))
        user = dbC.fetchone()
        ldbc.commit()
        ldbc.close()

        if user is None:
            return flask.render_template('login.html', error='Invalid email')
        else:
            salt = user[5]
            pepper = user[6]
            if passutil.verify(password, salt, pepper, user[4]):
                jwt_token = jwt.encode({'user_id': user[0], 'ip': flask.request.remote_addr, 'noise': randString(35)}, 'secret', algorithm='HS256')
                resp = flask.make_response(flask.redirect('/'))
                resp.set_cookie('session_token', jwt_token)
                current_tokens.append(jwt_token)

                return resp
            else:
                return flask.render_template('login.html', error='Invalid password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'GET':
        return flask.render_template('register.html')
    else:
        print('e')
        username = flask.request.form['username']
        student_id = flask.request.form['student_id']
        real_name = flask.request.form['real_name']
        salt = randString(10)
        pepper = randString(10)
        password = passutil.hash(flask.request.form['password'], salt, pepper)
        email = flask.request.form['email']
        time_created = datetime.datetime.now().timestamp()
        time_last_login = datetime.datetime.now().timestamp()
        time_last_logout = 0
        group_id = 0
        profile_picture = '' # TODO: make default pfp
        bio = "Hi :D I'm a new user!"

        ldbc = sqlite3.connect(db)
        dbC = ldbc.cursor()
        dbC.execute('INSERT INTO users (username, student_id, real_name, password, salt, pepper, email, time_created, time_last_login, time_last_logout, group_id, profile_picture, bio) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (username, student_id, real_name, password, salt, pepper, email, time_created, time_last_login, time_last_logout, group_id, profile_picture, bio))
        ldbc.commit()
        ldbc.close()

        return flask.redirect('/login')

@app.route('/logout')
def logout():
    resp = flask.make_response(flask.redirect('/'))
    resp.set_cookie('session_token', '', expires=0)
    return resp

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if verify(flask.request) is None:
        return flask.redirect('/login')
    
    if flask.request.method == 'GET':
        return flask.render_template('settings.html')
    else:
        username = flask.request.form['username']
        student_id = flask.request.form['student_id']
        real_name = flask.request.form['real_name']
        salt = randString(10)
        pepper = randString(10)
        password = passutil.hash(flask.request.form['password'], salt, pepper)
        email = flask.request.form['email']
        group_id = 0
        profile_picture = flask.request.form['profile_picture']
        bio = flask.request.form['bio']

        ldbc = sqlite3.connect(db)
        dbC = ldbc.cursor()
        dbC.execute('UPDATE users SET username=?, student_id=?, real_name=?, password=?, salt=?, pepper=?, email=?, group_id=?, profile_picture=?, bio=? WHERE user_id=?', (username, student_id, real_name, password, salt, pepper, email, group_id, profile_picture, bio, flask.request.cookies.get('session_token')['user_id']))
        ldbc.commit()
        ldbc.close()

        return flask.redirect('/settings')

@app.route('/getSettings', methods=['GET'])
def getSettings():
    if verify(flask.request) is None:
        return flask.jsonify({'error': 'Invalid session'})

    ldbc = sqlite3.connect(db)
    dbC = ldbc.cursor()
    token = flask.request.cookies.get('session_token')
    jwt_token = jwt.decode(token, 'secret', algorithms=['HS256'])
    print(jwt_token['user_id'])
    dbC.execute('SELECT * FROM users WHERE id=' + str(jwt_token['user_id']) + ';')
    user = dbC.fetchone()
    ldbc.commit()
    ldbc.close()

    return flask.jsonify({'username': user[1], 'student_id': user[2], 'real_name': user[3], 'password': user[4], 'email': user[7], 'group_id': user[8], 'profile_picture': user[9], 'bio': user[10]})

app.run(debug=True)
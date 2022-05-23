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
        profile_picture = 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wgARCACgAKADASIAAhEBAxEB/8QAGgABAQEBAQEBAAAAAAAAAAAAAAQDBQIBBv/EABsBAQACAwEBAAAAAAAAAAAAAAADBAIFBgcB/9oADAMBAAIQAxAAAAH8yKHQ39Dn9Ddefo7I2vCvMAAAsjssQuf0Oe2EA0voFSle4j7Xjtf1COyPDEK8wAACyOyxCkrxzygUqG3CTWbbRpo7IzH6EeYAACyNJhZjiy+BDITI9nSmFKYUphSmFKYUphSmFKYUphKKPbgAAAAAAAAdMbLzUBzOnzK3ShW6UAAB0+Z07PNBZ5oAABNSxszZXTQ7eUVeqA11U2uVmpJtQGVYAAABNTNHs5RR7cCqmam9xASawAA2SYYvfjDITYWqZiLZyqkO8lVBTMm0dKamXWD3nV8NmeOwuV8cdsadhzOnzKXUKpao9nSLvDgTS1S0u4dPmdOTWNsdrvL7C5X/AP/EACEQAAIBBAIDAQEAAAAAAAAAAAATAwISIDAEEAERM1Bg/9oACAEBAAEFAuuJv5ePE38vtQogpt3z03ChXce+TGPfJ+W0aNGjRo0aNGjRo0aNGjRo0b/LKFFdNuNFNwoVtnxg3z4wb58YN8+MGiwsKvHrto0+ooUKFHyGje6fHssLO5MYMZ8Y8ZMYMZ8Y+//EAC8RAAAEAgcHBAMBAAAAAAAAAAABAgQDEQUQFVKBodEGEhMgNEOxITEywUFR8TD/2gAIAQMBAT8BFN9cvDwQhcsUUJ1yMfB1Ww8v5FoHMZcaKa1+4hcsUNoy4MUlo9xbDy/kWlSoczCU7vKpO8Ew5HVY7y5mWosd5czLUWO8uZlqLHeXMy1FjvLmZaix3lzMtRY7y5mWosd5czLUWO8uZlqLHeXMy1/12e7mH3y7Q9vH65W7yM2nwjlMUbSTmM5ShavTD9V0lSTmC5UhCvTD9Bw8jOZcU5y5qH6xGPg66Y6xeHguTfSCOYbs4zmfCKcgzZxmcYo8cpJL+fgWwzv5HoLYZ38j0DxnGeRjjwCmk/5+Q4Zxm0uKUpgzkN9NSPiNnu5h9imOjXh5Kuh+jRj5MbQ9vH6C/jV//8QAIhEAAQMDBQEBAQAAAAAAAAAAAgABAxAREwQSIDJBMTMw/9oACAECAQE/AVpPyZT+cYPVq/yemIFC1gZmU/nGD1TNcHZ1iCgy7WsjPdxA9qKXc1qZQWUFlBZQWUFlBZQWUFlBZQ/rqPOOn94kDF9UkYsN2rHGLjd0IMPzlL0rF04YiTtZEbD9RmxtZliNYjQGwNZ0JsXxM11iKkvZajxRd6y91p/VF2p//8QAIBAAAgICAgMBAQAAAAAAAAAAADIBIDAxAhARIVFQYP/aAAgBAQAGPwLrln415Z+PbDE+88exhu5zxWc8flqKKKKKKKKKKKKKKKKKKL/LMMbrsYbLFZzxWc8VnPFZwbN0UU+eBhhhj75FFps33FZrFZrFZrFZ7//EAB4QAAMAAgMAAwAAAAAAAAAAAAAR8DDBECAhMVFg/9oACAEBAAE/IeNe8+/XXXvPv1zSKR9+az/XkykUvyIBTKZTKZTKZTKZTKZTKZTKZTKZTKZTKf5akUjz/J9ff8EUill29dOfb1059vXTn29dOCEQjx+vmmUyXpSKRSKRLwplPn1+ohELAaeu3OGnrtwH/9oADAMBAAIAAwAAABD+lXzzzylX8yFXzzzylEzwx3zzzy0zzDDDDDDDDDD/AP8A/wD/AP8A/wD/AP8APP8A/wD/AP8A/wA888tL/wDx3fPPPPKP/wBTzzzH3mLDBLX3EBX+jzxT+kD/xAAfEQEAAgIDAQEBAQAAAAAAAAABETEAIRBBUSBhMFD/2gAIAQMBAT8Q4q7fPT4qQZOVEuigOoKM7fPTGTgTDpsTuSnlDZTm9v51t5sp/wAJBBBBBBBBBCq8gk6Gpix9ckTKZIFJ6Bs5gTCIIVh7Ftz2CRoLiaDw/qgh+2AJM8gk7C5i08c2KfLIxIjSW0NHKCGhT4ZCYBaQ2Jsz2CRsaiaX0wBLn7cVfdIIVdx//8QAIBEAAQMEAwEBAAAAAAAAAAAAAAERsRAxYcEgIUHwMP/aAAgBAgEBPxAlypu46iHKUxSJ2x3Ju46hO2OpMU0bWHX6ZuPf6dx9ZTNJmkzSZpM0maTNJmkzSZp/XZrjo3xYmCiQ7qgkOxyZyvfe1tfe8MMC62W4xOFKu6qYoMUCFXZUHJwutkuYYpd+8Nmi195W994aNln7yn//xAAlEAACAQQBAgcBAAAAAAAAAAAA8PERIIHBMBBBMVBRYXGRsWD/2gAIAQEAAT8Q8oIiJJiTPzUpSlef81K1rQSYk+urfPu1bq3z7teVpESIkRIiREiJESIkRIiREiJESIkRIiREiJESP8skxJnzq7UpS341dq1qJMSfKzFrM87MWszzsxazPOzFrM8UnuBXt1SIkRPir9egkxJiTEmJ8FPv1EiJHr7AU7WybtWszazFurdu7VrM2sxbq31//9k='
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
    dbC.execute('SELECT * FROM users WHERE id=' + str(jwt_token['user_id']) + ';')
    user = dbC.fetchone()
    ldbc.commit()
    ldbc.close()

    return flask.jsonify({'username': user[1], 'student_id': user[2], 'real_name': user[3], 'password': user[4], 'email': user[7], 'group_id': user[8], 'profile_picture': user[9], 'bio': user[10]})

@app.route('/profile/<id>', methods=['GET'])
def profile(id):
    if verify(flask.request) is None:
        return flask.redirect('/login')

    ldbc = sqlite3.connect(db)
    dbC = ldbc.cursor()
    dbC.execute('SELECT * FROM users WHERE id=' + str(id) + ';')
    user = dbC.fetchone()
    ldbc.commit()
    ldbc.close()

    return flask.render_template('profile.html', user=user)

app.run(debug=True)
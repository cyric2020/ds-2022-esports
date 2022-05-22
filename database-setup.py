import sqlite3

mainDb = sqlite3.connect('main.db')

#
# users table
#

# usersDb = sqlite3.connect('users.db')
usersCursor = mainDb.cursor()

usersCursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    student_id INT,
    real_name TEXT,
    password TEXT,
    salt TEXT,
    pepper TEXT,
    email TEXT,
    time_created INT,
    time_last_login INT,
    time_last_logout INT,
    group_id INT,
    profile_picture TEXT,
    bio TEXT
)''')

usersCursor.close()
# usersDb.close()


#
# teams table
#

# teamsDb = sqlite3.connect('teams.db')
teamsCursor = mainDb.cursor()

teamsCursor.execute('''CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    members TEXT,
    admin_id INT
)''')

teamsCursor.close()


#
# groups table
#

groupsCursor = mainDb.cursor()

groupsCursor.execute('''CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    permissions TEXT
)''')

groupsCursor.close()


#
# Games table
#

gamesCursor = mainDb.cursor()

gamesCursor.execute('''CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game TEXT,
    description TEXT,
    time_created INT,
    teams TEXT,
    game_id INT,
    time_starting INT,
    time_ending INT
)''')

gamesCursor.close()


#
# Game table
#

gameCursor = mainDb.cursor()

gameCursor.execute('''CREATE TABLE IF NOT EXISTS game (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game TEXT,
    description TEXT,
    time_created INT,
    players TEXT
)''')

gameCursor.close()

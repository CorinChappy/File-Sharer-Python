import sqlite3
from flask import g, Flask
from pprint import pprint
app = Flask(__name__)

DATABASE = 'database.db'

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = make_dicts
    return db

def mutate_db(query, args=()):
    db = get_db()
    db.execute(query, args)
    db.commit()
    return True

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()




def checkLogin(username,password):
    user = query_db('select * from User where email = ? and password = ?',
                [username,password], one=True)
    if user is None:
        return False
    else:
        return user

def register(username,password,firstName,lastName):
    try:
        user = mutate_db("INSERT INTO User (email, password, firstName, lastName) VALUES (?,?,?,?)",
                    [username,password,firstName,lastName])
        return True
    except Exception as e:
        return False
    
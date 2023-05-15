import g
import os
import sqlite3

from flask import Flask, render_template

from FDataBase import FDataBase

#Конфигурация БД
DATABASE = '/tmp/fs.db'
DEBUS = True
SECRET_KEY  = 'ksflaghk2jlfg4hfd43gjkh'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fs.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    '''Соединение с базой данных если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.route('/')
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu())

@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с базой данных, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()

if __name__ == '__main__':
    app.run(debug=True)

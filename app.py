import os
import sqlite3

from flask import Flask, render_template, request, flash, abort, g, make_response, session

from FDataBase import FDataBase

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fs.db')))

#Конфигурация БД
DATABASE = '/tmp/fs.db'
DEBUG = True
SECRET_KEY = 'ksflaghk2jlfg4hfd43gjkh'

# Запустить из питон консоли
# import os
# os.urandom(20).hex()
# Взять ключ и подставить в секрет кей

def connect_db():  #Подключение к БД
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():   #Создание БД
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

@app.teardown_appcontext    #Разрывает соединение с БД
def close_db(error):
    '''Закрываем соединение с базой данных, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route('/')
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())



# @app.route('/')
# def index():
#     if 'visits' in session:
#         session['visits'] = session.get('visits') + 1  #обновление данных сессии
#     else:
#         session['visits'] = 1 #Запись данных в сессию
#
#     return f"<h1>Main Page</h1><p>Число просмотров: {session['visits']}"


@app.route('/add_post', methods=['POST', 'GET'])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_post.html', menu=dbase.getMenu(), title='Добавление статьи')

@app.route('/post/<alias>')
def showPost(alias):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)

@app.route('/login')
def login():
    log = ''
    if request.cookies.get('logged'):
        log = request.cookies.get('logged')

    res = make_response(f'<h1>Форма авторизации</h1><p>logged: {log}')
    res.set_cookie('logged', 'yes', 30*24*3600)
    return res

@app.route('/logout')
def logout():
    res = make_response('<p>Вы больше не авторизованы</p>')
    res.set_cookie('logged', '', 0)
    return res

if __name__ == '__main__':
    app.run(debug=True)

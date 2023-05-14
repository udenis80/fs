from flask import Flask, render_template, url_for, request, flash, redirect
from pip._internal.network import session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ksflaghk2jlfg4hfd43gjkh'
menu = [{ 'name': 'Установка', 'url': 'install-flask'},
        { 'name': 'Первое приложение', 'url': 'first-app'},
        { 'name': 'Обратная связь', 'url': 'contact'}]
@app.route('/')
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)

@app.route('/profile/<path:username>')
def profile(username):
    return f'Пользователь: {username}'


@app.route('/about')
def about():
    print(url_for('about'))
    return render_template('about.html', title='О сайте', menu=menu)

@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено')
        else:
            flash('Ошибка отправки')
        print(request.form['username'])
    return render_template('contact.html', title='Обратная свзь', menu=menu)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_logged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.form['username'] == 'abc' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', tittle='Авторизация', menu=menu)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='Страница не найдена', menu=menu), 404

if __name__ == '__main__':
    app.run(debug=True)
#
# with app.test_request_context():
#     print(url_for('about'))
#     print(url_for('index'))
#     print(url_for('profile', username='abc'))

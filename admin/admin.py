from flask import Blueprint, render_template, flash, redirect, url_for, request, session

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

def login_admin():
    session['admin_logged'] = 1

def islogged():
    return True if session.get('admin_logged') else False

def logout_admin():
    session.pop('admin_logged', None)

@admin.route('/')
def index():
    return 'admin'

@admin.route('/login', method=['POST', 'GET'])
def login():
    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == '12345':
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash('Неверная пара логин/пароль', "error")
    return render_template('admin/login.html', title='Админ-панель')

@admin.route('/logout', methods=['POST', 'GET'])
def logout():
    if not islogged():
        return redirect(url_for('.login'))
    logout_admin()
    return redirect(url_for('.login'))
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager
from app.models import User
from app.forms import RegistrationForm, LoginForm


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', title='Головна', current_user=current_user)
    else:
        return render_template('index.html', title='Головна')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    login_error = False 

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Успішний вхід!', 'success')
            return redirect(url_for('index'))
        else:
            login_error = True
            flash("Неправильне ім'я користувача або пароль.", 'error')

    return render_template('login.html', title='Вхід', form=form, login_error=login_error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Обліковий запис')

@app.route('/register', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    register_error = None 
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            register_error = 'Це ім\'я користувача вже зайняте. Виберіть інше ім\'я.' 
            flash(register_error, 'error') 
            return redirect(url_for('register'))

        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Обліковий запис успішно створено. Тепер ви можете увійти.', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', title='Реєстрація', form=form, register_error=register_error)
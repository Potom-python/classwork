import os

from flask import Flask, render_template, redirect
from flask_login import LoginManager
from flask_login import login_user

from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.user import LoginForm, RegisterForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/jobs.db")
    db_sess = db_session.create_session()

    if not os.path.isfile('db/jobs.db'):
        user = User()
        user.surname = "Scott"
        user.name = "Ridley"
        user.age = 21
        user.position = "captain"
        user.speciality = "research engineer"
        user.address = "module_1"
        user.email = "scott_chief@mars.org"
        db_sess.add(user)
        db_sess.commit()

        user = User()
        user.surname = "Karl"
        user.name = "Velikiy"
        user.age = 55
        user.position = "captain"
        user.speciality = "pilot"
        user.address = "module_2"
        user.email = "karl_chief@mars.org"
        db_sess.add(user)
        db_sess.commit()

        user = User()
        user.surname = "Pol"
        user.name = "Polov"
        user.age = 25
        user.position = "navigator"
        user.speciality = "admin"
        user.address = "module_3"
        user.email = "pol_admin@mars.org"
        db_sess.add(user)
        db_sess.commit()

        user = User()
        user.surname = "Kirill"
        user.name = "Ismagilov"
        user.age = 16
        user.position = "janitor"
        user.speciality = "programmer"
        user.address = "module_4"
        user.email = "kirill_janitor@mars.org"
        db_sess.add(user)
        db_sess.commit()

        job = Jobs()
        job.team_leader = 1
        job.job = 'deployment of residential modules 1 and 2'
        job.work_size = 15
        job.collaborators = '2, 3'
        job.is_finished = False
        db_sess.add(job)
        db_sess.commit()

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(user_id)

    @app.route("/")
    def table():
        jobs = db_sess.query(Jobs).all()
        return render_template('table.html', jobs=jobs)

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                surname=form.surname.data,
                email=form.email.data,
                age=form.age.data,
                position=form.position.data,
                speciality=form.speciality.data,
                address=form.address.data
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/')
        return render_template('register.html', title='Регистрация', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()

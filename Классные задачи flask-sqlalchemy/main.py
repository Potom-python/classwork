import os

from flask import Flask, render_template, redirect, make_response, jsonify, abort
from flask import request
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from flask_restful import Api

import users_resource
import jobs_resource
from data import db_session, jobs_api
from data.jobs import Jobs
from data.users import User
from forms.jobs import JobsForm
from forms.user import LoginForm, RegisterForm

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/jobs.db")
    db_sess = db_session.create_session()
    app.register_blueprint(jobs_api.blueprint)
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:users_id>')
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:jobs_id>')

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

        job = Jobs()
        job.team_leader = 3
        job.job = 'deployment of residential modules 2 and 3'
        job.work_size = 30
        job.collaborators = '3, 4'
        job.is_finished = True
        db_sess.add(job)
        db_sess.commit()

        job = Jobs()
        job.team_leader = 2
        job.job = 'deployment of residential modules 3 and 4'
        job.work_size = 30
        job.collaborators = '4, 5'
        job.is_finished = False
        db_sess.add(job)
        db_sess.commit()

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    @app.errorhandler(400)
    def bad_request(_):
        return make_response(jsonify({'error': 'Bad Request'}), 400)

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(user_id)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/jobs', methods=['GET', 'POST'])
    @login_required
    def add_job():
        form = JobsForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            jobs = Jobs()
            jobs.team_leader = form.team_leader.data
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            current_user.jobs.append(jobs)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/')
        return render_template('jobs.html', title='Добавление работы', form=form)

    @app.route('/jobs/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_jobs(id):
        form = JobsForm()
        if request.method == "GET":
            db_sess = db_session.create_session()
            jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                              ((Jobs.user == current_user) | (current_user.id == 1))
                                              ).first()
            if jobs:
                form.job.data = jobs.job
                form.team_leader.data = jobs.team_leader
                form.work_size.data = jobs.work_size
                form.collaborators.data = jobs.collaborators
                form.is_finished.data = jobs.is_finished
            else:
                abort(404)
            if form.validate_on_submit():
                db_sess = db_session.create_session()
                jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                                  ((Jobs.user == current_user) | (current_user.id == 1))
                                                  ).first()
                if jobs:
                    jobs.job = form.job.data
                    jobs.team_leader = form.team_leader.data
                    jobs.work_size = form.work_size.data
                    jobs.collaborators = form.collaborators.data
                    jobs.is_finished = form.is_finished.data
                    db_sess.commit()
                    return redirect('/')
                else:
                    abort(404)
            return render_template('jobs.html',
                                   title='Редактирование новости',
                                   form=form
                                   )

    @app.route("/")
    def table():
        jobs = db_sess.query(Jobs).all()
        users = db_sess.query(User).all()
        users_dict = {user.id: (user.name, user.surname) for user in users}
        return render_template('table.html', jobs=jobs, users_dict=users_dict)

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

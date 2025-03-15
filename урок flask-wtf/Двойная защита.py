from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    username_astro = StringField('id астронавта', validators=[DataRequired()])
    password_astro = PasswordField('Пароль астронавта', validators=[DataRequired()])
    username_captain = StringField('id капитана', validators=[DataRequired()])
    password_captain = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/training/<prof>')
def training(prof):
    if 'инженер' in prof.lower() or 'строитель' in prof.lower():
        text = "Инженерные тренажеры"
        image = url_for('static', filename='img/Инженерные тренажеры.jpg')
    else:
        text = "Научные симуляторы"
        image = url_for('static', filename='img/Научные симуляторы.png')
    return render_template('training.html', text=text, image=image)


@app.route('/list_prof/<list>')
def list_prof(list):
    s = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач', 'инженер по терраформированию',
         'климатолог', 'специалист по радиационной защите', 'астрогеолог', 'гляциолог', 'метеоролог']
    return render_template('list_prof.html', s=s, list=list)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    css = url_for('static', filename='css/style.css')
    slovar = {
        'title': 'Анкета', 'surname': 'Watny', 'name': 'Mark', 'education': 'выше среднего',
        'profession': 'климатолог', 'sex': 'male', 'motivation': 'Хочу жить на Марсе!', 'ready': 'True'
    }
    return render_template('auto_answer.html', slovar=slovar, css=css, title=slovar['title'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    image = url_for('static', filename='img/MARS-2-7.png')
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Аварийный доступ', form=form, image=image)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

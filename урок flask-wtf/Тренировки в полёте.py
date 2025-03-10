from flask import Flask, render_template, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

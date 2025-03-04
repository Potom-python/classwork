from flask import Flask

app = Flask(__name__)


@app.route('/results/<nickname>/<int:level>/<float:rating>')
def choise(nickname, level, rating):
    return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet" 
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                            crossorigin="anonymous">
                            <title>Варианты выбора</title>
                          </head>
                          <body>
                            <h1>Результаты отбора</h1>
                            <h2>Претендента на участие в миссии {nickname}:</h2>
                            <h3 class="alert alert-success" role="alert">
                                Поздравляем! Ваш рейтинг после {level} этапа отбора
                            </h3>
                            <h3>
                                составляет {rating}!
                            </h3>
                            <h3 class="alert alert-warning" role="alert">
                                Желаем удачи!
                            </h3>
                          </body>
                        </html>'''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

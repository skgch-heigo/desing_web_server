from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
@app.route('/main')
def main_title():
    return render_template('main.html', log_in=True)


@app.route('/register')
def register_title():
    return render_template('register.html', log_in=True)


@app.route('/clothes/boots')
def boots_title():
    return render_template('boots.html', count_cols=3, data=[(1, 'название', 'цвет', 'размер',
                                                              'материал', 'паттерн', 'картинка'),
                                                             (2, 'название2', 'цвет2', 'размер2',
                                                              'материал2', 'паттерн2', 'картинка2'),
                                                             (3, 'название3', 'цвет3', 'размер3',
                                                              'материал3', 'паттерн3', 'картинка3')],
                           log_in=True)


@app.route('/clothes/lower_body')
def lower_body_title():
    return render_template('lower_body.html', count_cols=3, data=[(1, 'название', 'цвет', 'размер',
                                                                   'материал', 'паттерн', 'картинка'),
                                                                  (2, 'название2', 'цвет2', 'размер2',
                                                                   'материал2', 'паттерн2', 'картинка2'),
                                                                  (3, 'название3', 'цвет3', 'размер3',
                                                                   'материал3', 'паттерн3', 'картинка3')],
                           log_in=True)


@app.route('/clothes/upper_body')
def upper_body_title():
    return render_template('upper_body.html', count_cols=3, data=[(1, 'название', 'цвет', 'размер',
                                                                   'материал', 'паттерн', 'картинка'),
                                                                  (2, 'название2', 'цвет2', 'размер2',
                                                                   'материал2', 'паттерн2', 'картинка2'),
                                                                  (3, 'название3', 'цвет3', 'размер3',
                                                                   'материал3', 'паттерн3', 'картинка3')],
                           log_in=True)


@app.route('/clothes/hats')
def hats_title():
    return render_template('hats.html', count_cols=3, data=[(1, 'название', 'цвет', 'размер',
                                                             'материал', 'паттерн', 'картинка'),
                                                            (2, 'название2', 'цвет2', 'размер2',
                                                             'материал2', 'паттерн2', 'картинка2'),
                                                            (3, 'название3', 'цвет3', 'размер3',
                                                             'материал3', 'паттерн3', 'картинка3')],
                           log_in=True)


@app.route('/clothes/add/hats')
def add_hats_title():
    return render_template('add_hats.html', log_in=True)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

from flask import Flask, request, url_for,  render_template, json,redirect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    user = "Ученик Яндекс.Лицея"
    return render_template('base.html', title='title')

@app.route('/answer', methods=['POST'])
def answer():
    # Здесь вы можете обработать данные формы
    data = request.form.to_dict()
    return render_template('auto_answer.html', **data)

@app.route('/auto_answer', methods=['GET'])
def auto_answer():
    return render_template('auto_answer.html', title='', surname='', name='', education='', profession='', sex='', motivation='', ready='')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
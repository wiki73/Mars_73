from flask import Flask, render_template, redirect
from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Замените на ваш секретный ключ

def add_test_data():
    db_sess = db_session.create_session()

    # Проверяем, существуют ли пользователи
    user1 = db_sess.query(User).filter(User.email == "alice@example.com").first()
    if not user1:
        user1 = User(name="Alice", email="alice@example.com", about="I love programming.")
        user1.set_password("password1")
        db_sess.add(user1)

    user2 = db_sess.query(User).filter(User.email == "bob@example.com").first()
    if not user2:
        user2 = User(name="Bob", email="bob@example.com", about="I enjoy hiking.")
        user2.set_password("password2")
        db_sess.add(user2)

    user3 = db_sess.query(User).filter(User.email == "charlie@example.com").first()
    if not user3:
        user3 = User(name="Charlie", email="charlie@example.com", about="I am a foodie.")
        user3.set_password("password3")
        db_sess.add(user3)

    db_sess.commit()  # Сохраняем пользователей в базе данных

    # Создаем задания
    job1 = Jobs(title="Alice's First Job", content="This is Alice's first job.", user_id=user1.id, is_private=False)
    job2 = Jobs(title="Bob's Adventure", content="Bob went hiking in the mountains.", user_id=user2.id, is_private=False)
    job3 = Jobs(title="Charlie's Food Review", content="Charlie reviews the best pizza in town.", user_id=user3.id, is_private=False)

    db_sess.add(job1)
    db_sess.add(job2)
    db_sess.add(job3)

    db_sess.commit()  # Сохраняем задания в базе данных

@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.is_private != True).all()  # Получаем все публичные записи
    return render_template("index.html", news=jobs)

@app.route('/register', methods=['GET', 'POST'])
def register():
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
            about=form.about.data,
            age=form.age.data,
            position=form.position.data,
            specialty=form.specialty.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')  # Замените на ваш маршрут для авторизации
    return render_template('register.html', title='Регистрация', form=form)

@app.route("/jobs")
def jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()  # Получаем все работы
    return render_template("jobs.html", jobs=jobs)

if __name__ == "__main__":
    db_session.global_init("db/blogs.db")  # Инициализация базы данных
    add_test_data()  # Добавляем тестовые данные
    app.run(debug=True)
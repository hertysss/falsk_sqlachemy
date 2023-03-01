from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Job
from forms.users import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def add_some_users():
    users = [('Scott', 'Ridley', 21, 'captain', 'research engineer', 'module_1', 'scott_chief@mars.org'),
             ('Kapoor', 'Venkat', 31, 'middle', 'research engineer', 'module_1', 'kapoor_venkat@mars.org'),
             ('Lui', 'Dji', 19, 'chief', 'research engineer', 'module_2', 'lui_dji@mars.org'),
             ('Sean', 'Bean', 19, 'chief', 'research engineer', 'module_1', 'sean_bean@mars.org')]
    for surname, name, age, position, speciality, address, email in users:
        user = User()
        user.surname = surname
        user.name = name
        user.age = age
        user.position = position
        user.speciality = speciality
        user.address = address
        user.email = email
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()


def add_job():
    job = Job()
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.is_finished = False
    db_sess = db_session.create_session()
    db_sess.add(job)
    db_sess.commit()


@app.route("/")
def index():
    return render_template("index.html")


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
                                   message="Почта занята")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            address=form.address.data,
            position=form.position.data,
            speciality=form.speciality.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return render_template('register.html', title='Регистрация',
                               form=form,
                               message="Вы успешно зарегистрировались")
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
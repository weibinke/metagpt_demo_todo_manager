## main.py

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Task, db
from forms import RegisterForm, LoginForm, TaskForm

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    return app, login_manager

app, login_manager = create_app()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    form = TaskForm() 
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', tasks=tasks,form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # hashed_password = generate_password_hash(form.password.data, method='sha256')
        # new_user = User(username=form.username.data, password=hashed_password)
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if not user or not user.check_password(form.password.data):
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/task', methods=['GET', 'POST'])
@login_required
def task():
    form = TaskForm()

    if form.validate_on_submit():
        new_task = Task(title=form.title.data, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('task.html', form=form)

@app.route('/task/<int:task_id>/complete')
@login_required
def complete_task(task_id):
    task = Task.query.get(task_id)

    if task and task.user_id == current_user.id:
        task.completed = True
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/task/<int:task_id>/delete')
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

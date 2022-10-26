from flask import render_template, url_for, request, redirect, session, flash

from flask_login import current_user, login_required, logout_user, login_user

from werkzeug.security import generate_password_hash, check_password_hash

from sandkasten_package import app, db
from sandkasten_package.models import User, Post, Project, Technology


menu = [{'name': 'Über mich', 'url': '/about'},
        {'name': 'Projekte', 'url': '/projects'},
        {'name': 'Technologie', 'url': '/technology'},
        {'name': 'Tagebuch', 'url': '/diary'},
        {'name': 'Anmelden', 'url': '/login', 'id': 'authorization'},
        {'name': 'Registrieren', 'url': '/register', 'id': 'authorization'}]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Sandkasten', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', title='Über die Webseite', menu=menu)


@app.route('/projects')
def projects():
    return render_template('projects.html', title='Projekte', menu=menu)


@app.route('/technology')
def technology():
    technologies = Technology.query.all()
    return render_template('technology.html', title='Technology', technologies=technologies, menu=menu)


@app.route('/diary')
def diary():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('diary.html', title='Tagebuch', posts=posts, menu=menu)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('/404.html', title='Die Seite wurde nicht gefunden', menu=menu), 404


@app.route('/login', methods=['POST', 'GET'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page)
        else:
            flash('E-Mail oder Passwort ist nicht korrekt. Versuchen Sie bitte wieder.')
    else:
        flash('Fühlen Sie bitte die Felder E-Mail und Passwort')
    return render_template('login_page.html', title='Anmeldung', menu=menu)


@app.route('/register', methods=['POST', 'GET'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    password_retype = request.form.get('password_retype')
    if request.method == 'POST':
        if not (login or password or password_retype):
            flash('Füllen Sie alle Felder korrekt.')
        elif password != password_retype:
            flash('Passwörter sind nicht gleich.')
        else:
            password_hash = generate_password_hash(password)
            new_user = User(email=email, password=password_hash, role='user')
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register_page.html', title='Registrieren', menu=menu)


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next' + request.url)

    return response


@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', title='Users', users=users, menu=menu)


@app.route('/new-technology', methods=['POST', 'GET'])
@login_required
def new_technology():
    if request.method == "POST":
        title = request.form['title']
        logo = request.form['logo']
        description = request.form['description']
        link = request.form['link']

        technology = Technology(title=title, logo=logo, description=description, link=link)
        print('Technologie wurde gespeichert')
        try:
            db.session.add(technology)
            db.session.commit()
            return redirect('/technology')
        except:
            print('Except')
            return "Es ist ein Fehler aufgetreten."

    else:
        print('Technologie wurde nicht gespeichert')
        return render_template('new_technology.html', title='Neue Technologie', menu=menu)


@app.route('/new-post', methods=['POST', 'GET'])
@login_required
def new_post():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        link = request.form['link']

        post = Post(title=title, text=text, link=link)
        print('Post wurde gespeichert')
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/diary')
        except:
            print('Except')
            return "Es ist ein Fehler aufgetreten."
    else:
        print('Post wurde nicht gespeichert')
        return render_template('new_post.html', title='Neues Post', menu=menu)

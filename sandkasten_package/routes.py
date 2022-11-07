import os

from flask import render_template, url_for, request, redirect, session, flash, send_from_directory

from flask_login import current_user, login_required, logout_user, login_user

from werkzeug.security import generate_password_hash, check_password_hash

from sandkasten_package import app, db
from sandkasten_package.models import User, Post, Project, Technology


menu = [{'name': 'Über mich', 'url': '/about'},
        {'name': 'Projekte', 'url': '/projects'},
        {'name': 'Technologie', 'url': '/technology'},
        {'name': 'Tagebuch', 'url': '/diary'},
        {'name': 'Anmelden', 'url': '/login', 'class': 'authorization'},
        {'name': 'Registrieren', 'url': '/register', 'class': 'authorization'}]


@app.route('/')
@app.route('/index')
def index():
    projects = Project.query.all()
    projects_number = len(projects)
    technologies = Technology.query.all()
    technologies_number = len(technologies)
    posts = Post.query.all()
    posts_number = len(posts)
    return render_template('index.html',
                           title='Sandkasten',
                           projects_number=projects_number,
                           technologies=technologies,
                           technologies_number=technologies_number,
                           posts_number=posts_number,
                           menu=menu)


@app.route('/about')
def about():
    return render_template('about.html',
                           title='Über die Webseite',
                           menu=menu)


@app.route('/projects')
def projects():
    projects = Project.query.order_by(Project.date.desc()).all()
    return render_template('projects.html',
                           title='Projekte',
                           projects=projects,
                           menu=menu)


@app.route('/projects/<int:id>')
def project_page(id):
    project = Project.query.get(id)
    return render_template('project_page.html',
                           title='Project',
                           project=project,
                           menu=menu)


@app.route('/technology')
def technology():
    technologies = Technology.query.all()
    return render_template('technology.html',
                           title='Technology',
                           technologies=technologies,
                           menu=menu)


@app.route('/diary')
def diary():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('diary.html',
                           title='Tagebuch',
                           posts=posts,
                           menu=menu)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('/404.html',
                           title='Die Seite wurde nicht gefunden',
                           menu=menu), 404


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
    return render_template('login_page.html',
                           title='Anmeldung',
                           menu=menu)


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
    return render_template('register_page.html',
                           title='Registrieren',
                           menu=menu)


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
    return render_template('users.html',
                           title='Users',
                           users=users,
                           menu=menu)


@app.route('/new-project', methods=['POST', 'GET'])
@login_required
def new_project():
    if request.method == "POST":
        title = request.form['title']
        capture = request.form['capture']
        description_1 = request.form['description_1']
        description_2 = request.form['description_2']
        description_3 = request.form['description_3']
        description_4 = request.form['description_4']
        description_5 = request.form['description_5']
        description_6 = request.form['description_6']
        result_1_title = request.form['result_1_title']
        result_1_css_class = request.form['result_1_css_class']
        result_1_body = request.form['result_1_body']
        result_2_title = request.form['result_2_title']
        result_2_css_class = request.form['result_2_css_class']
        result_2_body = request.form['result_2_body']
        result_3_title = request.form['result_3_title']
        result_3_css_class = request.form['result_3_css_class']
        result_3_body = request.form['result_3_body']
        result_4_title = request.form['result_4_title']
        result_4_css_class = request.form['result_4_css_class']
        result_4_body = request.form['result_4_body']
        result_5_title = request.form['result_5_title']
        result_5_css_class = request.form['result_5_css_class']
        result_5_body = request.form['result_5_body']
        result_6_title = request.form['result_6_title']
        result_6_css_class = request.form['result_6_css_class']
        result_6_body = request.form['result_6_body']
        github = request.form['github']

        project = Project(title=title,
                          capture=capture,
                          description_1=description_1,
                          description_2=description_2,
                          description_3=description_3,
                          description_4=description_4,
                          description_5=description_5,
                          description_6=description_6,
                          github=github,
                          result_1_title=result_1_title,
                          result_1_css_class=result_1_css_class,
                          result_1_body=result_1_body,
                          result_2_title=result_2_title,
                          result_2_css_class=result_2_css_class,
                          result_2_body=result_2_body,
                          result_3_title=result_3_title,
                          result_3_css_class=result_3_css_class,
                          result_3_body=result_3_body,
                          result_4_title=result_4_title,
                          result_4_css_class=result_4_css_class,
                          result_4_body=result_4_body,
                          result_5_title=result_5_title,
                          result_5_css_class=result_5_css_class,
                          result_5_body=result_5_body,
                          result_6_title=result_6_title,
                          result_6_css_class=result_6_css_class,
                          result_6_body=result_6_body)

        print('Projekt wurde gespeichert')
        try:
            db.session.add(project)
            db.session.commit()
            return redirect('/projects')
        except:
            return "Es ist ein Fehler aufgetreten."

    else:
        print('Projekt wurde nicht gespeichert')
        return render_template('new_project.html',
                               title='Neues Projekt',
                               menu=menu)


@app.route('/new-technology', methods=['POST', 'GET'])
@login_required
def new_technology():
    if request.method == "POST":
        title = request.form['title']
        logo = request.form['logo']
        description = request.form['description']
        link = request.form['link']

        technology = Technology(title=title,
                                logo=logo,
                                description=description,
                                link=link)
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
        return render_template('new_technology.html',
                               title='Neue Technologie',
                               menu=menu)


@app.route('/new-post', methods=['POST', 'GET'])
@login_required
def new_post():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        link = request.form['link']

        post = Post(title=title,
                    text=text,
                    link=link)
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
        return render_template('new_post.html',
                               title='Neues Post',
                               menu=menu)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

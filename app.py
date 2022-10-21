from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask import session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///dbsand.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


menu = [{'name': 'Über die Webseite', 'url': '/about'},
        {'name': 'Projekte', 'url': '/projects'},
        {'name': 'Tagebuch', 'url': '/diary'},
        {'name': 'Anmeldung', 'url': '/login'}]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(300), nullable=True)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return 'Post %r' % self.id


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    link_github = db.Column(db.String(300), nullable=True)
    link_video = db.Column(db.String(300), nullable=True)
    link_other = db.Column(db.String(300), nullable=True)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return 'Project %r' % self.id


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


@app.route('/diary')
def posts():
    return render_template('diary.html', title='Tagebuch', menu=menu)
    #posts = Post.query.order_by(Post.date).all()
    #return render_template('diary.html', posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('/404.html', title='Die Seite wurde nicht gefunden', menu=menu), 404


@app.route('/login')
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.form['username'] == 'nadia' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Anmeldung', menu=menu)


@app.route('/new-post', methods=['POST', 'GET'])
def create_post():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        link = request.form['link']

        post = Post(title=title, text=text, link=link)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return "Es ist ein Fehler aufgetreten."

    else:
        return render_template('new_post.html', title='Neues Post', menu=menu)

if __name__ == "__main__":
    app.run(debug=True)

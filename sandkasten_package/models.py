from flask_login import UserMixin

from datetime import datetime

from sandkasten_package import db, login


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    # def __repr__(self):
    # return f"User('{self.email}', '{self.password}', '{self.role}'')"


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    link_github = db.Column(db.String(300), nullable=True)
    link_video = db.Column(db.String(300), nullable=True)
    link_other = db.Column(db.String(300), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Project %r>' % self.id


class Technology(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return '<Technology %r>' % self.id

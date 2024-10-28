# models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserDetail(db.Model):
    __tablename__ = 'user_detail'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, default="new_user")
    email = db.Column(db.String(100), unique=True, nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('PostList', backref='author', lazy=True, cascade="all, delete")

class PostList(db.Model):
    __tablename__ = 'post_list'
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    partner_needed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user_detail.user_id'), nullable=False)

    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete")

class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post_list.post_id'), nullable=False)

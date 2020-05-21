import secrets
from datetime import datetime
from flaskBlog import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(50), unique=True, default=secrets.token_urlsafe)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    author =  db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'Post {self.title} written by {self.author}'
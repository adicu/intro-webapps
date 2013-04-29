from application import db
from pbkdf2 import pbkdf2_hex
import os
from binascii import hexlify, unhexlify

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    posts = db.relationship('Post', backref='author')
    comments = db.relationship('Comment', 
                    backref=db.backref('author', lazy='join'))

    def __init__(self, username, email):
        self.username = username
        self.email = email
    
    def set_password(self, password):
        salt = os.urandom(16)
        hashed = pbkdf2_hex(str(password), salt)
        self.password = hexlify(salt) + '$' + hashed

    def __repr__(self):
        return '<User %r>' % self.username 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    text = db.Column(db.Text())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post')

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return '<Post %r>' & self.title

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '<Comment %r>' & self.text

def check_login(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        return False
    [hexsalt, cmphash] = user.password.split('$')
    salt = unhexlify(hexsalt)
    hashed = pbkdf2_hex(str(password), salt)
    return hashed == cmphash

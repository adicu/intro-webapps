from application import app, db
from flask import session, redirect, request, render_template
from models import User, Post, Comment, check_login

@app.route('/')
def index():
    username = session.get('username', '')
    posts = Post.query.all()
    return render_template('index.html', posts=posts, username=username)

@app.route('/account/new', methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template('newaccount.html')
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username, email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        error = (request.args.get('error') == 'true')
        return render_template('login.html', error=error)
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not check_login(username, password):
            return redirect('/login?error=true')
        session['username'] = username
        return redirect('/')

@app.route('/post/new', methods=['GET', 'POST'])
def create_post():
    if request.method == 'GET':
        if 'username' not in session:
            return redirect('/login')
        return render_template('newpost.html')
    else:
        title = request.form['title']
        text = request.form['text']
        post = Post(title, text)
        user = User.query.filter_by(username=session['username']).first()
        post.author_id = user.id
        db.session.add(post)
        db.session.commit()
        return redirect('/post/' + str(post.id))

@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('post.html', post=post)

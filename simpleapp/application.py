from flask import Flask, render_template, redirect, request, session
app = Flask(__name__)

@app.route('/devfest')
def devfest():
    return redirect('http://devfe.st/')

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html',
                               name = session['username'])
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect('/')
    

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'l34GE0q1l1U+4D8c4S/1Yg=='
    app.run()

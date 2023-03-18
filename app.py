from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from db import add_user, init_db

client = MongoClient('localhost', 27017)
db = client.ntrack
init_db(db)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def index2():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginhandler', methods=['GET', 'POST'])
def loginhandler():
    if request.method == 'POST':
        id = request.form['inputId']
        password = request.form['inputPassword']
        user = db['users'].find_one({'id': id})
        if user is None:
            return redirect(url_for('login'))
        if user['password'] == password:
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registerhandler', methods=['GET', 'POST'])
def registerhandler():
    if request.method == 'POST':
        id = request.form['inputId']
        password = request.form['inputPassword']
        first_name = request.form['inputFirstName']
        last_name = request.form['inputLastName']
        user_inform = {'id': id, 'password': password, 'first_name': first_name, 'last_name': last_name}
        print('user_inform: ', user_inform)
        if add_user(db, user_inform=user_inform):
            return redirect(url_for('login'))
        else:
            return redirect(url_for('register'))

@app.route('/charts')
def charts():
    return render_template('ch5arts.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

if __name__ == '__main__':
    app.run(debug=True)
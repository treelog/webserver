from flask import Flask, render_template, request, redirect, url_for, make_response, session, send_from_directory
from pymongo import MongoClient
from db import add_user, init_db, add_user_projects, remove_user_projects, load_user_inform
from datetime import timedelta
import os

client = MongoClient('localhost', 27017)
db = client.ntrack
init_db(db)
IMAGE_DIR = 'C:/Users/최준영/Pictures/test'

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)

@app.route('/')
def index():
    if 'id' in session:
        id = session['id']
        user = db['users'].find_one({'id': id})
        return render_template('index.html', user=user, len=len(user['projects']))
    else:
        return render_template('index.html', user=None, len=0)

@app.route('/index')
def index2():
    if 'id' in session:
        id = session['id']
        user = db['users'].find_one({'id': id})
        return render_template('index.html', user=user, len=len(user['projects']))
    else:
        return render_template('index.html', user=None, len=0)


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
            session['id'] = id
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
        
@app.route('/password')
def password():
    return render_template('password.html')

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
        user_inform = {'id': id, 'password': password, 'first_name': first_name, 'last_name': last_name, 'projects': []}
        print('user_inform: ', user_inform)
        if add_user(db, user_inform=user_inform):
            return redirect(url_for('login'))
        else:
            return redirect(url_for('register'))
        
@app.route('/makeproject')
def makeproject():
    if 'id' in session:
        id = session['id']
        user = db['users'].find_one({'id': id})
        return render_template('makeproject.html', user=user)
    else:
        return redirect(url_for('login'))
    
@app.route('/makeprojecthandler', methods=['GET', 'POST'])
def makeprojecthandler():
    if request.method == 'POST':
        id = session['id']
        project_name = request.form['inputProjectName']
        project = {'project_name': project_name, 'tracked': False}
        add_user_projects(db, user_id=id, project=project)
        return redirect(url_for('index2'))

@app.route('/deleteprojecthandler', methods=['GET', 'POST'])
def deleteprojecthandler():
    if request.method == 'POST':
        id = session['id']
        print(id)
        print(request.form['project_name'])
        #project_name = request.form['inputProjectName']
        #project = {'project_name': project_name, 'tracked': False}
        return redirect(url_for('index2'))

@app.route('/projecthandler', methods=['GET', 'POST'])
def projecthandler():
    if request.method == 'POST':
        project_name = request.form['project_name']
        print(project_name)
        return redirect(url_for('project', project_name=project_name))

@app.route('/project/<project_name>')
def project(project_name):
    if 'id' in session:
        id = session['id']
        user = db['users'].find_one({'id': id})
        images = os.listdir(IMAGE_DIR)
        return render_template('project.html', user=user, project_name=project_name, images=images)

@app.route("/images/<path:path>")
def send_image(path):
    print(path)
    return send_from_directory(IMAGE_DIR, path)

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

@app.route('/layout-static')
def layout_static():
    return render_template('layout-static.html')

@app.route('/layout-sidenav-light')
def layout_sidenav_light():
    return render_template('layout-sidenav-light.html')

if __name__ == '__main__':
    app.run(debug=True)
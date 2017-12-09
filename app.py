from flask import *
import os, uuid
from database import init_db, checkLogin, register, addFile, collectFile, userUploads
app = Flask(__name__)

init_db()

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    if 'user' in session:
        return render_template('upload.html')
    else:
        return "You are not logged in. Please login." #put login at some point

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        success = register(request.form['username'],request.form['password'],request.form['firstName'],request.form['lastName'])
        if success is True:
            return "Signup successful!"
        else:
            return "Signup failed: Email already exists!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = checkLogin(request.form['username'], request.form['password'])
        if user is False:
            return "Invalid login. Please enter correct credentials"
        else:
            session["user"] = user
            return "Hello %s" % user['firstName']

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user', None)
    return "You have sucessfully logged out."

@app.route('/upload', methods=['POST'])
def upload_file():
    userID = session['user']['id']

    if request.method == 'POST' and 'files' in request.files:
        url_list = []
        for f in request.files.getlist('files'):
            if f and f.filename != '':
                id = str(uuid.uuid4())
                upload_dir = os.path.join(app.config['UPLOAD_FOLDER'],id)
                os.makedirs(upload_dir)
                upload_location = os.path.join(upload_dir,f.filename)
                f.save(upload_location) 
                addFile(id,f.filename, userID)
                url_list.append("http://localhost:5000%s" % url_for('download',id=id, filename=f.filename))
            else: 
                return "Please supply at least one file"
        return render_template('submit.html', **locals())

@app.route('/download/<id>/<filename>', methods=['GET'])
def download(id,filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'],id)
    collectFile(id) 
    return send_from_directory(directory=uploads, filename=filename, as_attachment=True)

@app.route('/upload_list', methods = ['GET'])
def uploadList():
    if 'user' not in session:
        return redirect(url_for('login')) #redirects user to login page
    else:
        username = session['user']['id']
        data = userUploads(username)
        return render_template('upload_list.html', **locals())
from flask import *
import os, uuid
from pprint import pprint
from database import init_db, checkLogin
app = Flask(__name__)

init_db()

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = checkLogin(request.form['username'], request.form['password'])
        if user is False:
            return "Invalid login. Please enter correct credentials"
        else:
            return "Hello %s" % user['firstName']


@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['file']
    if f and f.filename != '':
        id = str(uuid.uuid4())
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'],id)
        os.makedirs(upload_dir)
        upload_location = os.path.join(upload_dir,f.filename)
        f.save(upload_location) 
        return "Upload success: your unique URL is: http://localhost:5000%s" % url_for('download',id=id, filename=f.filename)
    else:
        return "Please supply a file"

@app.route('/download/<id>/<filename>', methods=['GET'])
def download(id,filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'],id)
    return send_from_directory(directory=uploads, filename=filename, as_attachment=True)


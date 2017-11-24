from flask import Flask, render_template, request, current_app, send_from_directory, url_for
import os, uuid
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')


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

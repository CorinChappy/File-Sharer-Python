from flask import Flask, render_template, request, current_app, send_from_directory
import os
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['file']
    if f:
        f.save('uploads/file.txt') 
        return "Success!"
    else:
        return "Please supply a file"

@app.route('/download', methods=['GET'])
def download():
    uploads = os.path.join(current_app.root_path,'uploads')
    return send_from_directory(directory=uploads, filename='file.txt', as_attachment=True)

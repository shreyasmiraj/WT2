import os
from flask import Flask, flash, request, redirect, url_for, render_template, json, session
from werkzeug.utils import secure_filename
from flask import send_from_directory
from DiseaseClassification import *
import shutil
import glob


UPLOAD_FOLDER = 'imagedata/result'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploadajax', methods=['GET', 'POST'])
def uploadajax():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			print("file not in request.files")
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			print("no selected files")
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			files = glob.glob(str(app.config['UPLOAD_FOLDER'])+'/*')
			for f in files:
				os.remove(f)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			classValue = predictValue()
			print(classValue)
			return json.dumps({'status':2})


@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template("upload.html")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],
							   filename)


if __name__ == '__main__':
	app.run(debug="true")

from flask import Flask, flash, request, redirect, url_for, render_template, json, session,jsonify,abort
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import os
import json
import pyotp
from werkzeug.utils import secure_filename
from flask import send_from_directory
from DiseaseClassification import *
import shutil
import glob


UPLOAD_FOLDER = 'imagedata/result'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["MONGO_URI"] = "mongodb://localhost:27017/disease_detection"
mongo = PyMongo(app)



@app.route('/checkuser',methods=['POST'])
def check_user(email):
    user1=mongo.db.users.find_one({'email':email})
    if user1:
        return 1
    else:
        return 0

@app.route('/adduser',methods=['POST'])
def adduser():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    location = request.form['location']
    if(check_user(email) == 1):
        return render_template('login.html',data="already registered")
    print(name)
    userdata = {'name':name ,'password':password,'email':email,'location':location}
    user=mongo.db.users.insert_one(userdata)
    if user:
        query={
            'email':email,
            'password':password
        }
        session['logged_in'] = True
        user=mongo.db.users.find_one(query)
        user['_id']=str(user['_id'])
    return render_template('dashboard.html')


@app.route('/auth',methods=['POST'])
def auth_user():
    email=request.form['email']
    password=request.form['password']
    query={
		'email':email,
		'password':password
	}
    #return jsonify(query)
    user=mongo.db.users.find_one(query)
    user1=mongo.db.users.find_one({'email':email})
    if user:
        user['_id']=str(user['_id'])
        session['logged_in'] = True
        session['user_name'] = user['name']
        session['user_id'] = user['_id']

        return render_template('dashboard.html')
        return jsonify({'user_id':user['_id'],'uname':user['name'],'result':'Success'})
    elif user1:
        return jsonify({'result':"failure"})
    else:
        return jsonify({'result':"failure"})

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/dash_render')
def dashboard():
    return render_template('dashboard.html')

@app.route('/user_render')
def user():
    return render_template('user.html')

@app.route('/rss_render')
def rss():
    return render_template('rss.html')

@app.route('/consult_render')
def consult():
    return render_template('consult.html')

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
			session['classValue'] = classValue
			params = {'classValue' : classValue, 'div1status' : 'none', 'div2status' : 'block'}
			return jsonify(params)


@app.route('/consult', methods=['GET', 'POST'])
def uploadForm():
	classValue = 'NA'
	if 'classValue' in session:
		classValue = session['classValue']
	return render_template("upload.html", classValue = classValue, div1status="block", div2status="none")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],
							   filename)


if __name__ == '__main__':
	app.secret_key = 'super secret key'
	app.run(debug="true", threaded=True)

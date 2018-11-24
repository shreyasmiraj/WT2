from flask import Flask, redirect, url_for,jsonify,request,flash,abort,render_template
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import os
import json
import pyotp


app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["MONGO_URI"] = "mongodb://localhost:27017/disease_detection"
mongo = PyMongo(app)

@app.route('/')
def launch():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/checkuser',methods=['POST'])
def check_user():
    data=request.get_json()
    print(data)
    user1=mongo.db.users.find_one({'email':data['email']})
    if user1:
        return jsonify({'result':"Already registered"})
    else:
        return jsonify({'result':"New User"})

@app.route('/adduser',methods=['POST'])
def adduser():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    location = request.form['location']
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
    data=request.get_json()
    query={
		'email':data['email'] ,
		'password':data['password']
	}
    #return jsonify(query)
    user=mongo.db.users.find_one(query)
    user1=mongo.db.users.find_one({'email':data['email']})
    if user:
        user['_id']=str(user['_id'])
        session['logged_in'] = True
        return jsonify({'user_id':user['_id'],'uname':user['name'],'result':'Success','is_student':user['is_student']})
    elif user1:
        return jsonify({'result':"failure"})
    else:
        return jsonify({'result':"failure"})

if __name__ == '__main__':
   app.run(debug = True)

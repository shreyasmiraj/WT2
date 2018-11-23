from flask import Flask, redirect, url_for,jsonify,request,flash,abort
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

@app.route('/checkuser',methods=['POST'])
def check_user():
    data=request.get_json()
    user1=mongo.db.users.find_one({'email':data['email']})
    if user1:
        return jsonify({'result':"Already registered"})
    else:
        return jsonify({'result':"New User"})

@app.route('/signup',methods=['POST'])
def adduser():
    data=request.get_json()
    userdata = {'name':data['username'] ,'password':data['password'],'email': data['email']}
    user=mongo.db.users.insert_one(userdata)
    if user:
        query={
            'email':data['email'] ,
            'password':data['password']
        }
        user=mongo.db.users.find_one(query)
        user['_id']=str(user['_id'])
        return jsonify({'user_id':user['_id'],'uname':data['username'],'result':'Success','is_student':is_student})
    else:
        return jsonify({'result':"Something went wrong"})

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
        return jsonify({'user_id':user['_id'],'uname':user['name'],'result':'Success','is_student':user['is_student']})
    elif user1:
        return jsonify({'result':"Invalid password"})
    else:
        return jsonify({'result':"Invalid user"})


if __name__ == '__main__':
   app.run(debug = True)

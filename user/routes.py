from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from passlib.handlers.pbkdf2 import pbkdf2_sha256
import uuid

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'
from app import app
from user.models import User
import requests
from bs4 import BeautifulSoup

# Database
client = MongoClient('mongodb+srv://test:sparta@cluster0.9cihgwo.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

# 로그인/로그아웃/회원가입 routes================================================================================================

#로그인페이지
@app.route('/')
def home():
    return render_template('login.html')

#로그인 routes
@app.route('/user/login', methods=['POST'])
def login():
    return User().login()   # 로그인 함수 실행

#로그아웃 routes
@app.route('/user/signout')
def signout():
    return User().signout()

#회원가입 routes GET 요청
@app.route('/user/signup', methods=['GET'])
def signup_get():
    input_list = list(db.users.find({}, {'_id': False}))
    from flask import jsonify
    return jsonify({'result': 'success', 'msg': '회원가입 완료', 'input_list': input_list})

#회원가입 routes
@app.route('/user/signup', methods=['POST'])
def signup():
    from flask import request
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']

    doc = {
        'email': email_receive,
        'pw': pw_receive

    }
    db.users.insert_one(doc)
    print(doc, '회원가입 완료')

    return jsonify({'result': 'success', 'msg': '회원가입이 완료되었습니다.'})






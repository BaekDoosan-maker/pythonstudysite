from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
#sha256 암호화를 위한 passlib 라이브러리 설치
from app import db
import uuid
#uuid란, 네트워크 상에서 고유성이 보장되는 id를 만들기 위한 표준 규약

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.9cihgwo.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

class User:
    def start_session(self, user):
        # 세션을 시작하는 함수
        del user['pw']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

        # 회원가입 영역 ==================================================================================================
    def signup(self):
        print(request.form)
        # 유저 오브젝트 생성
        user = {
            "email": request.form.get('email'),
            "pw": request.form.get('pw')
        }
        # 비밀번호 암호화 sha256 해시 암호화 사용 'Secure Hash Algorithm의 한 종류'
        user['pw'] = pbkdf2_sha256.encrypt(user['pw'])

        # 이메일 계정 중복 체크
        # 웹개발 종합반 강의 중 python prac 내용을 참조, db에서 찾을때
        if db.user.find_one({"email": user['email']}):
            return jsonify({"error": "이미 사용중인 이메일 계정입니다."}), 400
        # db에 저장
        if db.user.insert_one(user):
            return self.start_session(user)
        # 세션 시작
        return jsonify({"error": "Signup failed"}), 400
        # 세션을 시작하는 함수 끝
        # 회원가입 함수 끝
# =================================================로그아웃 영역==============================================================
    # 로그아웃 함수
    def signout(self):
            session.clear()
            return redirect('/')
    # 로그아웃 함수 끝
# =================================================로그인 영역==============================================================
    # 로그인 함수
    def login(self):
        user = db.user.find_one({
            "email": request.form.get('email')
        })
        if user and pbkdf2_sha256.verify(request.form.get('pw'), user['pw']):
            return self.start_session(user)
        return jsonify({"error": "Invalid login credentials"}), 401
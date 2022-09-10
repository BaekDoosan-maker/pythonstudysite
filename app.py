import self as self
from flask import Flask, render_template, request, jsonify
import flask
import passlib
from flask import Flask, render_template, session, redirect, jsonify, request, url_for
from functools import wraps
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from pythonstudysite import user

app = Flask(__name__)
# 플라스크 설치
import requests
from bs4 import BeautifulSoup
# 웹크롤링용 bs4 추가

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'
# 몽고디비계정연결
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.9cihgwo.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap

@app.route('/')
def home():
    return render_template('login.html')

# 회원가입페이지로 이동하기
@app.route('/signup')
def signup():
    return render_template('signup.html')
#signup GET API 요청
@app.route('/api/signup', methods=['GET'])
def api_signup():
    # 클라이언트로부터 데이터를 받음
    email_receive = request.args.get('email_give')
    pw_receive = request.args.get('pw_give')
    # 비밀번호 암호화
    pw_hash = pbkdf2_sha256.hash(pw_receive)
    # DB에 삽입할 user 만들기
    doc = {
        'email': email_receive,
        'pw': pw_hash
    }
    # DB에 삽입하기
    db.user.insert_one(doc)
    # 성공 여부 & 성공 메시지 반환
    print(doc, 'get성공')
    return jsonify({'result': 'success', 'msg': '회원가입이 완료되었습니다.'})


@app.route('/api/signup', methods=['POST'])
def api_signup_post():
    # 클라이언트로부터 데이터를 받음
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']
    # 비밀번호 암호화
    pw_hash = pbkdf2_sha256.hash(pw_receive)
    # DB에 삽입할 user 만들기
    doc = {
        'email': email_receive,
        'pw': pw_hash
    }
    # DB에 삽입하기
    db.user.insert_one(doc)
    # 성공 여부 & 성공 메시지 반환

    print(doc, '회원가입이 완료되었습니다.')
    return jsonify({'result': 'success', 'msg': '회원가입이 완료되었습니다.'})
# 로그인페이지로 이동하기
@app.route('/login')
def login():
    return render_template('login.html')
# 로그인페이지에서 로그인버튼 누르면
@app.route('/api/login', methods=['POST'])
def api_login(self):


    # email이 해당하는 데이터 찾기 & pw 확인
    result = db.user.find_one({
        'email': request.form.get('email')
    })
    # 비밀번호가 일치하는 경우 로그인 성공 처리
    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
        return self.start_session(user)
    return jsonify({"error": "Invalid login credentials"}), 401

# 로그아웃
@app.route('/logout')
def logout():
    # 세션에서 유저 정보 삭제
    session.pop('user', None)
    return redirect(url_for('home'))




# Decorators
def login_required(f):
    # wraps는 데코레이터를 사용할 때, 데코레이터가 적용된 함수의 이름과 docstring을 데코레이터가 적용되기 전의 함수의 이름과 docstring으로 바꿔주는 역할을 한다.
    # 데코레이터를 사용하면 함수의 이름과 docstring이 데코레이터 함수의 이름과 docstring으로 바뀌기 때문에, 이를 방지하기 위해 사용한다.
    @wraps(f)
    # 로그인이 되어있는지 확인하는 함수
    def wrap(*args, **kwargs):
        # 세션에 email이 있는지 확인
        if 'logged_in' in session:
            # 세션에 email이 있으면 함수 실행
            return f(*args, **kwargs)
        # 세션에 email이 없으면 로그인 페이지로 리다이렉트
        else:
            # 세션에 email이 없으면 로그인 페이지로 리다이렉트
            return redirect('/')
    return wrap
    # 로그인이 되어있는지 확인하는 함수 끝

#=================================================로그인 영역 끝=============================================================


# 파이썬테마피디아
@app.route('/main')
def main():
    return render_template('pythonthema.html')
#파이썬테마 - POST요청
# ajax POST 방식으로 /pythonthema 경로로 ,
# data{url_give: url, star_give:star, comment_give:comment }를 받는다.
@app.route("/pythonthema",methods=["POST"])
def pythonthema_post():  # pythonthema_post() 함수 실행 // count = len(pythonthema_list) + 1 추가
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text,'html.parser')
    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']
    pythonthema_list = list(db.pythonthema.find({}, {'_id': False}))
    count = len(pythonthema_list) + 1
    # print(count)
    doc = {  # dac안에 title, image, desc, star, comment값을 넣는다.
        'num': count,
        'title': title,
        'image': image,
        'desc': desc,
        'star': star_receive,
        'comment': comment_receive
    }
    db.pythonthema.insert_one(doc)  # doc에 담긴것을db에  insert 한다.

    return jsonify({'msg': '저장 완료!'}) # 저장완료 메시지를 노출함


#pythonthema 기록하기 - GET요청
@app.route("/pythonthema", methods=["GET"])
def pythonthema_get():
    pythonthema_list = list(db.pythonthema.find({}, {'_id':False}))
    return jsonify({'pythonthema':pythonthema_list})


#pythonthema 수정 GET요청 API 구성
@app.route("/open/edit", methods=["GET"])
def edit_get():
    num_receive = request.args.get('num_give')
    pythonthema_list = list(db.pythonthema.find({'num': int(num_receive)}, {'_id': False}))
    print(pythonthema_list)
    return jsonify({'pythonthema': pythonthema_list})


#pythonthema - 수정 POST요청, title, 별점, 코멘트 데이터 수정용 POST API 구성
@app.route("/save/edit", methods=["POST"])
def edit_post():
    num_receive = request.form['num_give']
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    db.pythonthema.update_one({'num': int(num_receive)}, {'$set': {'url': url_receive, 'star': star_receive, 'comment': comment_receive}})
    return jsonify({'msg': '수정 완료!'})

#pythonthema - 삭제 요청 API 구성
@app.route("/delete", methods=["POST"])
def delete_post():
    num_receive = request.form['num_give'];
    db.pythonthema.delete_one({'num': int(num_receive)})
    print(num_receive)  # num값이 들어오는것을 확인
    return jsonify({'msg': '삭제 완료!'})


# 포트 8080 실행 ====================================================================================================================
if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)   # debug=True로 설정하면 코드 수정시 자동으로 서버가 재시작된다.


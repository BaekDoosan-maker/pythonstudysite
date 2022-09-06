from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
# 플라스크 설치
import requests
from bs4 import BeautifulSoup
# 웹크롤링용 bs4 추가

# 몽고디비계정연결
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.9cihgwo.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

# 파이썬테마피디아
@app.route('/')
def home():
    return render_template('pythonthema.html')

#파이썬테마 - POST요청
# ajax POST 방식으로 /pythonthema 경로로 ,
#
# data{url_give: url, star_give:star, comment_give:comment }를 받는다.
@app.route("/pythonthema",methods=["POST"])
def pythonthema_post():  # pythonthema_post() 함수 실행 // count = len(pythonthema_list) + 1 추가    2022-09-06-오후8:48분
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
    print(count)
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

#pythonthema- post 저장 id 값 len으로 저장 ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
        # title_receive = request.form["title_give"];
        # posts = list(db.posts.find({}));
        # db.pythonthema.insert_one({"title": title_receive, "id": len(posts)});

#pythonthema 기록하기 - GET요청
@app.route("/pythonthema", methods=["GET"])
def pythonthema_get():
    pythonthema_list = list(db.pythonthema.find({}, {'_id':False}))
    return jsonify({'pythonthema':pythonthema_list})


#pythonthema 수정 GET요청 - edit요청, title, 별점, 코멘트 데이터 수정용 GET API 구성
@app.route("/open/edit", methods=["GET"])
def edit_get():
    edit_list = list(db.pythonthema.find({},{'_id':False}))
    return jsonify({'/open/edit':edit_list})

#pythonthema - 수정 POST요청, title, 별점, 코멘트 데이터 수정용 POST API 구성
@app.route("/saveedit", methods=["POST"])
def edit_post():
    num_receive = request.form['num_give']

    star_image_receive = request.form['star_image_give'] #새로운 별점
    title_receive = request.form["title_give"];
    posts = list(db.posts.find({}));
    db.posts.insert_one({"title": title_receive, "id": len(posts)});
    # db.movies.update_one({'num':int(num_receive),'title': old_title_receive}, {"$set": {'title': title_receive}});  # 업데이트쿼리문
    return jsonify({'msg': '저장완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
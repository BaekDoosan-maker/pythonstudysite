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
@app.route("/pythonthema",methods=["POST"])
def pythonthema_post():
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

    doc = {
        'title': title,
        'image': image,
        'desc': desc,
        'star': star_receive,
        'comment': comment_receive
    }
    db.pythonthema.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

#pythonthema - GET요청
@app.route("/pythonthema", methods=["GET"])
def pythonthema_get():
    pythonthema_list = list(db.pythonthema.find({}, {'_id':False}))
    return jsonify({'pythonthema':pythonthema_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
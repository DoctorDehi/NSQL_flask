import os
import redis
from pymongo import MongoClient
import time
import json

from flask import Flask, request, redirect, session, g as app_ctx
from flask import render_template,  url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Fakulta, Katedra
#from chatbot import bot
from clanky_dict import *


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config["SECRET_KEY"] = "C02FFVUEe58qbZ2MPqoSax3ej8PsOyQq4npyXgWEU8D6AmRzvcMHFjGklPDQHD58g1VRbrcbBSGx6MU6fZzj6dc3eXgm7bJD"
db.init_app(app)


redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:50001')
redis_conn = redis.from_url(redis_url)

mongo_client = MongoClient('mongodb://localhost:50002')
db = mongo_client.test_database
posts = db.posts
#posts.insert_many(clanky_dicts)

def add_clanek(name):
    global next_id
    clanky_dicts.append({
        "id": next_id,
        "nazev": name,
        "text": ""
    })
    next_id += 1


@app.before_request
def logging_before():
    # Store the start time for the request
    app_ctx.start_time = time.perf_counter()


@app.after_request
def logging_after(response):
    # Get total time in milliseconds
    total_time = time.perf_counter() - app_ctx.start_time
    time_in_ms = int(total_time * 1000)
    # Log the time taken for the endpoint
    print('%s ms %s %s' % (time_in_ms, request.method, request.path))
    return response

@app.route('/', methods = ['POST', 'GET'])
def index():  # put application's code here
    failed = False
    if request.method == "POST":
        login = request.form["login"].strip()
        heslo = request.form["heslo"]
        user = db.session.execute(db.select(User).filter_by(login=login)).scalars().first()
        if not user:
            failed = True
        else:
            if user.password == heslo:
                session.permanent = True
                session["user"] = login
                return redirect('/clanky')

            else:
                failed = True

    return render_template('index.html', failed=failed)

@app.route('/logout')
def logout():
    if "user" in session:
        session.pop("user", None)
    return redirect(url_for("index"))

@app.route('/clanky', methods = ['POST', 'GET'])
def clanky_all():
    if request.method == "POST":
        add_clanek(request.form["nazev_clanku"])
    return render_template('clanky.html', clanky=clanky_dicts)

@app.route('/clanky/<int:clanekID>')
def clanek(clanekID):
    return 'ID clanku %d' % clanekID

@app.route('/katedry')
def katedry():
    katedry = db.session.execute(db.select(Katedra)).scalars()
    return render_template("katedry.html", katedry=katedry)

@app.route('/katedra/<int:katedraID>')
def katedra(katedraID):
    key = "katedra%i" %katedraID
    redis_result = redis_conn.get(key)
    if redis_result:
        data = json.loads(redis_result)
    else:
        katedra = db.session.execute(db.select(Katedra).filter_by(id=katedraID)).scalars().first()
        fakulta = db.session.execute(db.select(Fakulta).filter_by(id=katedra.fakulta)).scalars().first()
        data = {"katedra": katedra.name,
                "fakulta": fakulta.name
        }
        redis_conn.set(key, json.dumps(data))
        redis_conn.expire(key, 60)
    return render_template("katedra.html", katedra=data["katedra"], fakulta=data["fakulta"])

@app.route("/posts-mongo/")
def posts_mongo():
    collection = db['posts']
    cursor = collection.find({})
    posts = []
    for document in cursor:
        posts.append(document)
    return render_template("clanky.html", clanky=posts)


if __name__ == '__main__':
    app.run(debug=True)

import os
import redis
import time
import json

from flask import Flask, request, redirect, session, g as app_ctx
from flask import render_template,  url_for, jsonify
from models import db, User, Fakulta, Katedra
from mongo_models import mongo_db, Clanek


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config["SECRET_KEY"] = "C02FFVUEe58qbZ2MPqoSax3ej8PsOyQq4npyXgWEU8D6AmRzvcMHFjGklPDQHD58g1VRbrcbBSGx6MU6fZzj6dc3eXgm7bJD"
db.init_app(app)


redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:50001')
redis_conn = redis.from_url(redis_url)


app.config['MONGODB_SETTINGS'] = {
        'db': 'novinky',
        'host': 'localhost',
        'port': 50002
}
mongo_db.init_app(app)


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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods = ['POST', 'GET'])
def login():  # put application's code here
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
                return redirect('/')

            else:
                failed = True

    return render_template('login.html', failed=failed)


@app.route('/logout')
def logout():
    if "user" in session:
        session.pop("user", None)
    return redirect(url_for("login"))


@app.route('/clanky')
def clanky_all():
    clanky = Clanek.objects
    return render_template('clanky_list.html', clanky=clanky)


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

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import User


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)


next_id = 4
clanky_dicts = [
    {
    "id": 1,
    "nazev": "Bla",
    "text": "lorem ipsum"
    },
    {
        "id": 2,
        "nazev": "Blabla",
        "text": "lorem ipsum"
    },
    {
        "id": 3,
        "nazev": "Dlspdfú",
        "text": "lorem ipsum"
    },
]


def add_clanek(name):
    global next_id
    clanky_dicts.append({
        "id": next_id,
        "nazev": name,
        "text": ""
    })
    next_id += 1


@app.route('/', methods = ['POST', 'GET'])
def index():  # put application's code here
    if request.method == "POST":
        login = request.form["login"]
        heslo = request.form["heslo"]
    return render_template('index.html')


@app.route('/clanky', methods = ['POST', 'GET'])
def clanky_all():
    if request.method == "POST":
        add_clanek(request.form["nazev_clanku"])
    return render_template('clanky.html', clanky=clanky_dicts)

@app.route('/clanky/<int:clanekID>')
def clanek(clanekID):
    return 'ID clanku %d' % clanekID


if __name__ == '__main__':
    app.run(debug=True)

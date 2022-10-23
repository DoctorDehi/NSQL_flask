from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, User


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

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config["SECRET_KEY"] = "C02FFVUEe58qbZ2MPqoSax3ej8PsOyQq4npyXgWEU8D6AmRzvcMHFjGklPDQHD58g1VRbrcbBSGx6MU6fZzj6dc3eXgm7bJD"
db.init_app(app)


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


if __name__ == '__main__':
    app.run(debug=True)

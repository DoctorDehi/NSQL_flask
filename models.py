from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

class Fakulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

class Katedra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    fakulta = db.Column(db.Integer, db.ForeignKey("fakulta.id"))



if __name__ == "__main__":
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # fse = Fakulta(name="Fakulta sociálně ekonomická")
        # db.session.add(fse)
        katedry = [
            ("Katedra fyzioterapie", 8),
            ("Katedra záchranářství a radiologie", 8),
            ("Katedra psychologie", 6),
            ("Katedra cizích jazyků", 1),
            ("Katedra matematiky a informatiky", 1)
        ]
        for katedra in katedry:
            db.session.add(Katedra(name=katedra[0], fakulta=katedra[1]))

        #db.session.add(User(login="test2@test.cz", password="test"))
        db.session.commit()

        users = db.session.execute(db.select(User)).scalars()
        print(users)

from mongoengine import ListField, StringField, URLField
from flask_mongoengine import MongoEngine
from flask import Flask


mongo_db = MongoEngine()


class Clanek(mongo_db.Document):
    nadpis = StringField(required=True, max_length=70)
    autor = StringField(required=True, max_length=20)
    klicova_slova = ListField(StringField(max_length=50))
    url = URLField(required=True)


if __name__ == "__main__":
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        'db': 'novinky',
        'host': 'localhost',
        'port': 50002
    }
    # db = MongoEngine()
    mongo_db.init_app(app)


    clanek1 = Clanek(
        nadpis="Dezoláti a milovníci Ruska se sešli. A moc jich nebylo",
        autor="Johana Hovorková",
        klicova_slova=["dezoláti", "max dva zuby", "flákanec", "za Babiše bylo lépe", "USA žere děti za živa"],
        url="https://www.forum24.cz/dezolati-a-milovnici-ruska-se-sesli-a-moc-jich-nebylo/"
    )


    clanek1.save()

    for dokument in Clanek.objects(autor="Johana Hovorková"):
        print(dokument.url)

    for dokument in Clanek.objects:
        print(dokument.nadpis)

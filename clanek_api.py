import json
from app import app
from flask import request, jsonify
from mongo_models import Clanek


@app.route('/api/clanek', methods=['GET'])
def clanek_read():
    nadpis = request.args.get('nadpis')
    clanek = Clanek.objects(nadpis=nadpis).first()
    if not clanek:
        return jsonify({'chyba': 'clanek se zadanym nazvem nebyl nalezen'})
    else:
        return jsonify(clanek.to_json())


@app.route('/api/clanek', methods=['PUT'])
def clanek_create():
    zaznam = json.loads(request.data)
    clanek = Clanek(
                nadpis=zaznam["nadpis"],
                autor=zaznam["autor"],
                klicova_slova=zaznam["klicova slova"],
                url=zaznam["url"]
             )
    clanek.save()
    return jsonify(clanek.to_json())

@app.route('/api/clanek', methods=['POST'])
def clanek_update():
    zaznam = json.loads(request.data)
    nadpis = zaznam['nadpis']
    autor = zaznam["autor"]
    klicova_slova = zaznam["klicova slova"]
    url = zaznam["url"]
    clanek = Clanek.objects(nadpis=nadpis).first()
    if not clanek:
        return jsonify({'chyba': 'clanek se zadanym nadpisem nebyl nalezen'})
    else:
        clanek.update(autor=zaznam['autor'])
        clanek.update(klicova_slova=zaznam['klicova slova'])
        clanek.update(url=zaznam['url'])
    return jsonify(clanek.to_json())

@app.route('/api/clanek', methods=['DELETE'])
def delete_clanek():
    zaznam = json.loads(request.data)
    clanek = Clanek.objects(nadpis=zaznam['nadpis']).first()
    if not clanek:
        return jsonify({'chyba': 'clanek se zadanym nadpisem nebyl nalezen'})
    else:
        clanek.delete()
    return jsonify(clanek.to_json())

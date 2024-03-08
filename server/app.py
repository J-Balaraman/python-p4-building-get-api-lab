#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc
from sqlalchemy.orm import load_only
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_json = [bakery.to_dict() for bakery in bakeries]
    return jsonify(bakeries_json)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    bakery_data = bakery.to_dict()
    bakery_data['baked_goods'] = [good.to_dict() for good in bakery.baked_goods]
    
    return jsonify(bakery_data)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
    baked_goods_json = [good.to_dict() for good in baked_goods]
    return jsonify(baked_goods_json)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_good = BakedGood.query.options(load_only(BakedGood.name, BakedGood.price)).order_by(desc(BakedGood.price)).first()
    return jsonify(most_expensive_good.to_dict())

if __name__ == '__main__':
    app.run(port=5555, debug=True)

from flask import Blueprint, request, jsonify
from app import mongo

shopping_bp = Blueprint('shopping', __name__)

@shopping_bp.route('/list', methods=['GET'])
def get_list():
    items = mongo.db.items.find()
    return jsonify([{'_id': str(item['_id']), 'name': item['name'], 'bought': item['bought']} for item in items])

@shopping_bp.route('/list', methods=['POST'])
def add_item():
    data = request.json
    item_id = mongo.db.items.insert_one({'name': data['name'], 'bought': False}).inserted_id
    return jsonify({'_id': str(item_id), 'name': data['name'], 'bought': False})

@shopping_bp.route('/list/<item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    mongo.db.items.update_one({'_id': mongo.db.ObjectId(item_id)}, {'$set': {'name': data['name'], 'bought': data['bought']}})
    return jsonify({'message': 'Item updated'})

@shopping_bp.route('/list/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    mongo.db.items.delete_one({'_id': mongo.db.ObjectId(item_id)})
    return jsonify({'message': 'Item deleted'})
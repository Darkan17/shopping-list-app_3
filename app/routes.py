from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi
from dotenv import load_dotenv
import os

shopping = Blueprint('shopping', __name__)


load_dotenv()
uri = os.getenv("MONGO_URI")

client = MongoClient(
    uri,
    tls=True,
    tlsCAFile=certifi.where()
)
db = client["shopping"]
shopping_lists = db["shopping"]

@shopping.route("/items", methods=["GET"])
def get_items():
    items = list(shopping_lists.find())
    for item in items:
        item["_id"] = str(item["_id"])
    return jsonify(items)

@shopping.route("/items", methods=["POST"])
def add_item():
    data = request.json
    result = shopping_lists.insert_one(data)
    return jsonify({"_id": str(result.inserted_id)}), 201

@shopping.route("/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.json
    data.pop("_id", None)
    shopping_lists.update_one({"_id": ObjectId(item_id)}, {"$set": data})
    return jsonify({"msg": "Updated"})

@shopping.route("/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    shopping_lists.delete_one({"_id": ObjectId(item_id)})
    return jsonify({"msg": "Deleted"})

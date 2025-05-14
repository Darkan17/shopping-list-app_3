from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import certifi
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv("MONGO_URI")
auth = Blueprint('auth', __name__)

client = MongoClient(
    uri,
    tls=True,
    tlsCAFile=certifi.where()
)

db = client["user"]
users = db["user"]

@auth.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = generate_password_hash(password)
    users.insert_one({"email": email, "password": hashed_pw})
    return jsonify({"msg": "User registered successfully"}), 201

@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users.find_one({"email": email})
    if user and check_password_hash(user["password"], password):
        return jsonify({"msg": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401


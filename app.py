from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)

from pymongo import MongoClient

client = client = MongoClient(os.getenv("MONGO_URI"))
db = client["finance_dashboard"]
collection = db["transactions"]

@app.route('/transactions', methods=['GET'])
def get_transactions():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.json

    new_transaction = {
        "id": int(time.time()),
        "date": data.get("date"),
        "amount": data.get("amount"),
        "category": data.get("category"),
        "type": data.get("type"),
        "description": data.get("description", data.get("category"))
    }

    collection.insert_one(new_transaction)
    return jsonify(new_transaction)

@app.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    global transactions
    transactions = [t for t in transactions if t["id"] != id]
    return jsonify({"message": "Deleted"})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
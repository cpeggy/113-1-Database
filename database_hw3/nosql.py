from flask import Blueprint, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

# Initialize Blueprint
create_bp = Blueprint('create_bp', __name__, url_prefix='/api')

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['project_db']
posts_collection = db['posts']

@create_bp.route('/create_post', methods=['POST'])
def create_post():
    data = request.form  # Retrieve data from the form
    title = data.get('title')
    content = data.get('content')
    partner_needed = data.get('partner_needed') == 'on'  # Checkbox handling

    # Insert data into MongoDB
    post = {
        "title": title,
        "content": content,
        "partner_needed": partner_needed,
        "created_at": datetime.utcnow(),
        "comments": []
    }
    result = posts_collection.insert_one(post)

    if result.inserted_id:
        return jsonify({"success": True, "message": "Post created"}), 201
    else:
        return jsonify({"success": False, "message": "Failed to create post"}), 500

@create_bp.route('/create', methods=['GET'])
def create_form():
    return render_template('create.html')
from flask import Flask, Blueprint, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId, InvalidId
from datetime import datetime

# Initialize main Blueprint
app_bp = Blueprint('app_bp', __name__)
update_bp = Blueprint('update_bp', __name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['project_db']
collection = db['posts']

# Route for reading and displaying posts
@app_bp.route('/read')
def read_posts():
    show_all = request.args.get('show_all', 'false').lower() == 'true'
    data = list(collection.find({})) if show_all else []
    for doc in data:
        doc['_id'] = str(doc['_id'])
    return render_template('index.html', data=data, results=None, show_all=show_all)

# Route for creating a new post
@app_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        partner_needed = request.form.get('partner_needed') == 'on'

        # Insert new post
        new_post = {
            "title": title,
            "content": content,
            "partner_needed": partner_needed,
            "created_at": datetime.utcnow()
        }
        collection.insert_one(new_post)
        return redirect(url_for('app_bp.read_posts'))
    return render_template('create.html')

# Route for searching posts
@app_bp.route('/search', methods=['POST'])
def search_posts():
    query_text = request.form.get("query", "")
    regex_query = {"$regex": query_text, "$options": "i"}
    query = {"$or": [{"title": regex_query}, {"content": regex_query}]}

    results = list(collection.find(query))
    for result in results:
        result['_id'] = str(result['_id'])

    return render_template('index.html', data=[], results=results, show_all=False)

# Route for toggling the display of all posts
@app_bp.route('/toggle_show_all', methods=['GET'])
def toggle_show_all():
    show_all = request.args.get('show_all', 'false').lower() == 'true'
    return redirect(url_for('app_bp.read_posts', show_all=not show_all))


# Create a separate Blueprint for the update functionality
@update_bp.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    try:
        # Determine if the ID is an ObjectId or a string
        try:
            object_id = ObjectId(id)
        except InvalidId:
            object_id = id  # Use as a string if not an ObjectId

        if request.method == 'POST':
            # Collect updated data from form
            update_data = {key: value for key, value in request.form.items() if key != '_id'}
            collection.update_one({"_id": object_id}, {"$set": update_data})
            return redirect(url_for('app_bp.read_posts'))

        # Fetch the document to pre-fill the form
        entry = collection.find_one({"_id": object_id})
        if not entry:
            return "Document not found", 404

        entry['_id'] = str(entry['_id'])  # Ensure _id is a string for template compatibility
        return render_template('update.html', entry=entry)

    except Exception as e:
        return str(e), 400
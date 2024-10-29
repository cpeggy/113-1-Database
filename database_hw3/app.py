from flask import Flask, render_template
from nosql import create_bp  # Import the create_bp Blueprint from nosql.py
from pymongo import MongoClient

app = Flask(__name__)
app.register_blueprint(create_bp)  # Register the Blueprint

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['project_db']
collection = db['posts']

# Define the home route to list all entries
@app.route('/')
def index():
    posts = list(collection.find({}))
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
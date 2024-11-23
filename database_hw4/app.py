from flask import Flask, redirect, url_for
from nosql import app_bp, update_bp, delete_bp  # Import the Blueprints

app = Flask(__name__)
app.register_blueprint(app_bp)  # Register the main Blueprint
app.register_blueprint(update_bp)  # Register the update Blueprint
app.register_blueprint(delete_bp)  # Register the delete Blueprint

# Redirect the root URL to /read
@app.route('/')
def home():
    return redirect(url_for('app_bp.read_posts'))

if __name__ == '__main__':
    app.run(debug=True)
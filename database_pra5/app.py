from flask import Flask, redirect, url_for
from nosql import app_bp  # Import the Blueprint

app = Flask(__name__)
app.register_blueprint(app_bp)  # Register the Blueprint

# Redirect the root URL to /read
@app.route('/')
def home():
    return redirect(url_for('app_bp.read_posts'))

if __name__ == '__main__':
    app.run(debug=True)
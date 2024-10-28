from flask import Flask, render_template
import create, read, update, delete, join

# Initialize the Flask app
app = Flask(__name__)

@app.route('/')
def home():
    # Fetch posts and comments data
    posts = read.get_posts()
    comments = read.get_comments()
    
    # 將 comments 分組到各個 post 下
    posts_with_comments = []
    for post in posts:
        post_comments = [comment for comment in comments if comment['post_id'] == post['post_id']]
        post['comments'] = post_comments
        posts_with_comments.append(post)

    users = read.get_users()
    joined_data = join.get_joined_data()

    return render_template('posts.html', posts=posts_with_comments, users=users, joined_data=joined_data)

# Register CRUD and JOIN blueprints
app.register_blueprint(create.create_bp)
app.register_blueprint(read.read_bp)
app.register_blueprint(update.update_bp)  # 確保這裡註冊了 update_bp
app.register_blueprint(delete.delete_bp)
app.register_blueprint(join.join_bp)

if __name__ == '__main__':
    app.run(debug=True)
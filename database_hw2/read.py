from flask import Blueprint, render_template
import mysql.connector
import os

# 定義 Blueprint
read_bp = Blueprint('read_bp', __name__)

# 資料庫連線配置
db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB')
}

def get_posts():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    try:
        # 使用 LEFT JOIN 和 COALESCE 確保所有貼文顯示，即使 author_id 為 NULL
        cursor.execute("""
            SELECT Post_list.*, 
                   COALESCE(User_detail.username, 'Unknown') AS user_name,
                   User_detail.email,
                   User_detail.registered_at
            FROM Post_list
            LEFT JOIN User_detail ON Post_list.author_id = User_detail.user_id
        """)
        posts = cursor.fetchall()
        print(posts)
    finally:
        cursor.close()
        conn.close()
    return posts

def get_comments():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Comment")
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return comments

def get_users():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM User_detail")
        users = cursor.fetchall()
        print(users)  # 打印用戶資料以便調試
    except mysql.connector.Error as err:
        print("Error: {}".format(err))  # 打印錯誤
        users = []  # 如果有錯誤，返回空列表
    finally:
        cursor.close()
        conn.close()
    return users

@read_bp.route('/users', methods=['GET'])
def read_users():
    users = get_users()  # 獲取用戶資料
    return render_template('posts.html', users=users)  # 確保用 `users` 變數名稱

@read_bp.route('/posts', methods=['GET'])
def read_posts():
    posts = get_posts()
    comments = get_comments()
    users = get_users()  # 獲取用戶資料

    posts_with_comments = []
    for post in posts:
        post_comments = [comment for comment in comments if comment['post_id'] == post['post_id']]
        post['comments'] = post_comments

        posts_with_comments.append(post)

    return render_template('posts.html', posts=posts_with_comments, users=users)  # 傳遞用戶資料到模板

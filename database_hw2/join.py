from flask import Blueprint, render_template
import mysql.connector
import os

join_bp = Blueprint('join_bp', __name__)

db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB')
}

def get_joined_data():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.post_id, p.title, p.content, COALESCE(u.username, 'Unknown') AS user_name, 
               p.created_at AS post_created_at, c.comment_id, c.comment_content, c.created_at AS comment_created_at
        FROM Post_list p
        LEFT JOIN User_detail u ON p.author_id = u.user_id    -- 取得貼文的作者
        LEFT JOIN Comment c ON p.post_id = c.post_id          -- 取得貼文的評論（包括無評論的貼文）
        ORDER BY p.post_id, c.created_at
    """)
    joined_result = cursor.fetchall()
    cursor.close()
    conn.close()

    # 將查詢結果組合成每篇貼文的字典格式，包含貼文的相關評論
    posts = {}
    for row in joined_result:
        post_id = row['post_id']
        if post_id not in posts:
            posts[post_id] = {
                'post_id': row['post_id'],
                'title': row['title'],
                'content': row['content'],
                'user_name': row['user_name'],
                'created_at': row['post_created_at'],
                'comments': []
            }
        # 將評論加入對應的貼文中
        if row['comment_id']:
            posts[post_id]['comments'].append({
                'comment_id': row['comment_id'],
                'comment_content': row['comment_content'],
                'comment_created_at': row['comment_created_at']
            })
    
    return list(posts.values())

@join_bp.route('/joined_data', methods=['GET'])
def joined_data():
    posts = get_joined_data()  # 使用 get_joined_data 函數獲取數據
    print("Joined Data:", posts)  # 在控制台打印輸出
    return render_template('posts.html', posts=posts)
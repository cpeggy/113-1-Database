from flask import Blueprint, render_template, request, redirect, url_for
import mysql.connector
import os

read_bp = Blueprint('read_bp', __name__)

# MySQL configuration
db_config = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DB')
}

@read_bp.route('/', methods=['GET', 'POST'])
def read_index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # 處理搜尋請求
    search_query = request.args.get('search_query')  # Get search query from URL parameters

    if search_query:
        # 如果有搜尋詞，根據標題和內容來搜尋
        cursor.execute("""
            SELECT post_id, title, content, partner_needed, created_at 
            FROM post_list 
            WHERE title LIKE %s OR content LIKE %s
        """, ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        # 如果沒有搜尋詞，顯示所有帖子
        cursor.execute("SELECT post_id, title, content, partner_needed, created_at FROM post_list")

    tables = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('new_post.html', tables=tables, search_query=search_query)
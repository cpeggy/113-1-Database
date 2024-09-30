from flask import Blueprint, request, redirect, url_for
import mysql.connector
import os

delete_bp = Blueprint('delete_bp', __name__)

# MySQL configuration
db_config = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DB')
}

@delete_bp.route('/delete', methods=['POST'])
def delete_posts():
    # 確保從表單獲取單個 post_id 而不是列表
    selected_id = request.form.get('post_id')  # 接收單個 post_id

    if selected_id:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 生成並執行刪除查詢
        delete_query = "DELETE FROM post_list WHERE post_id = %s"
        cursor.execute(delete_query, (selected_id,))  # 注意元組格式

        conn.commit()
        cursor.close()
        conn.close()

    # 刪除後重新導向到主頁
    return redirect(url_for('read_bp.read_index'))
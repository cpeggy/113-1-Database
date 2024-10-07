from flask import Blueprint, request, redirect, url_for
import mysql.connector
import os

delete_bp = Blueprint('delete_bp', __name__)

# MySQL 配置
db_config = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DB')
}

@delete_bp.route('/delete', methods=['POST'])
def delete_posts():
    post_id = request.form.get('post_id')

    # 刪除 MySQL 資料庫中的帖子
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    delete_query = "DELETE FROM post_list WHERE post_id = %s"
    cursor.execute(delete_query, (post_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('read_bp.read_index'))
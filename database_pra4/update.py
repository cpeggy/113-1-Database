from flask import Blueprint, request, redirect, url_for
import mysql.connector
import os

update_bp = Blueprint('update_bp', __name__)

# MySQL 配置
db_config = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DB')
}

@update_bp.route('/update', methods=['POST'])
def update_posts():
    post_id = request.form.get('post_id')
    new_title = request.form.get('title')
    new_content = request.form.get('content')
    new_partner_needed = 1 if request.form.get('partner_needed') == 'on' else 0

    # 更新 MySQL 資料庫中的帖子
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    update_query = """
        UPDATE post_list 
        SET title = %s, content = %s, partner_needed = %s 
        WHERE post_id = %s
    """
    cursor.execute(update_query, (new_title, new_content, new_partner_needed, post_id))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('read_bp.read_index'))
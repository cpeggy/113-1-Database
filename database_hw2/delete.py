from flask import Blueprint, request, jsonify
import mysql.connector
import os

delete_bp = Blueprint('delete_bp', __name__)

db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB')
}

@delete_bp.route('/posts/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Post_list WHERE post_id = %s", (post_id,))
        conn.commit()
        success = cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()
    return jsonify({'success': success})

@delete_bp.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM User_detail WHERE user_id = %s", (user_id,))
        conn.commit()
        success = cursor.rowcount > 0  # 判斷是否成功刪除
    finally:
        cursor.close()
        conn.close()
    
    return jsonify({'success': success})

@delete_bp.route('/comments/delete/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Comment WHERE comment_id = %s", (comment_id,))
        conn.commit()
        success = cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()
    return jsonify({'success': success})
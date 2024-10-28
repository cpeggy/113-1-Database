from flask import Blueprint, request, jsonify, redirect, url_for, render_template, flash
import mysql.connector
import os

update_bp = Blueprint('update_bp', __name__)

db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB')
}

@update_bp.route('/posts/update/<int:post_id>', methods=['POST'])
def update_post(post_id):
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Request must be JSON'}), 400

    data = request.json
    title = data.get('title')
    content = data.get('content')
    partner_needed = data.get('partner_needed', False)

    if not title or not content:
        return jsonify({'success': False, 'error': 'Title and content are required'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE post_list SET title = %s, content = %s, partner_needed = %s WHERE post_id = %s",
            (title, content, partner_needed, post_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()

    return jsonify({'success': success})


@update_bp.route('/users/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    data = request.json  # 確保使用 JSON 格式來提取數據
    username = data.get('username')
    email = data.get('email')

    if not username or not email:
        return jsonify({'success': False, 'error': 'Username and email are required'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE User_detail SET username = %s, email = %s WHERE user_id = %s", (username, email, user_id))
        conn.commit()
        success = cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()
    
    return jsonify({'success': True})

@update_bp.route('/comments/update/<int:comment_id>', methods=['POST'])
def update_comment(comment_id):
    data = request.json
    comment_content = data.get('comment_content')

    if not comment_content:
        return jsonify({'success': False, 'error': 'No content provided'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Comment SET comment_content = %s WHERE comment_id = %s", (comment_content, comment_id))
        conn.commit()
        success = cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()

    return jsonify({'success': success})
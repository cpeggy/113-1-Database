from flask import Blueprint, request, jsonify, redirect, url_for, render_template
import mysql.connector
import os
import datetime

create_bp = Blueprint('create_bp', __name__)

db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB')
}

@create_bp.route('/posts/create', methods=['POST'])
def create_post():
    title = request.form['title']
    content = request.form['content']
    partner_needed = request.form.get('partner_needed') == 'on'

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Post_list (title, content, partner_needed) VALUES (%s, %s, %s)",
            (title, content, partner_needed)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('read_bp.read_posts'))  # 返回 posts 頁面

@create_bp.route('/users/create', methods=['POST'])
def create_user():
    username = request.form['username']
    email = request.form['email']
    registered_at = request.form.get('registered_at', datetime.datetime.now())  # 如果沒有指定，默認為當前時間
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 檢查 email 是否已存在
        cursor.execute("SELECT * FROM User_detail WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            print(f"Error: Email {email} already exists.")
            return redirect(url_for('read_bp.read_users'))  # 返回使用者列表頁面

        # 插入新的使用者
        cursor.execute("""
            INSERT INTO User_detail (username, email, registered_at)
            VALUES (%s, %s, %s)
        """, (username, email, registered_at))
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('read_bp.read_users'))  # 返回使用者列表頁面

@create_bp.route('/comments/create', methods=['POST'])
def create_comment():
    # 使用 JSON 來接收數據
    data = request.json
    comment_content = data.get('comment_content')
    post_id = data.get('post_id')
    user_id = data.get('user_id')

    # 檢查必須的欄位是否存在
    if not comment_content or not post_id or not user_id:
        return jsonify({'success': False, 'error': 'Missing data'}), 400

    created_at = datetime.datetime.now()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Comment (comment_content, post_id, user_id, created_at) VALUES (%s, %s, %s, %s)",
            (comment_content, post_id, user_id, created_at)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    # 返回 JSON 響應
    return jsonify({'success': True})
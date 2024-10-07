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
    if request.method == 'POST':
        # 從表單中獲取資料
        title = request.form['title']
        content = request.form['content']
        partner_needed = request.form.get('partner_needed')
        partner_needed_value = 1 if partner_needed == 'on' else 0

        # 連接到 MySQL 資料庫
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 插入資料到 post_list 表中
        insert_query = """
        INSERT INTO post_list (title, content, partner_needed)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (title, content, partner_needed_value))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('read_bp.read_index'))

    # 如果是 GET 請求
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # 查詢所有的帖子，包含 created_at 欄位
    cursor.execute("SELECT post_id, title, content, partner_needed, created_at FROM post_list")
    tables = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('new_post.html', tables=tables)
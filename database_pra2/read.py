from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from create import create_bp
import os

app = Flask(__name__)
app.register_blueprint(create_bp)

# MySQL configuration
db_config = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DB')
}

@app.route('/', methods=['GET', 'POST'])
def index():
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

        return redirect(url_for('index'))

    # 如果是 GET 請求
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM post_list")
    tables = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('new_post.html', tables=tables)

if __name__ == '__main__':
    app.run(debug=True)

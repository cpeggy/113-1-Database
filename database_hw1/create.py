from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from dotenv import load_dotenv
import os

# 加載環境變量
load_dotenv()

app = Flask(__name__)

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
        partner_needed = request.form.get('partner_needed')  # 從 checkbox 中獲取值
        
        # 如果勾選了 "尋找夥伴"，設為 1，否則設為 0
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
        
        # 關閉游標和連接
        cursor.close()
        conn.close()
        
        # 重新導向到主頁
        return redirect(url_for('index'))
    
    # 渲染新的發文頁面
    return render_template('new_post.html')

if __name__ == '__main__':
    app.run(debug=True)
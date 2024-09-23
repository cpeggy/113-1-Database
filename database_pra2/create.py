from flask import Flask, request, redirect, url_for, Blueprint
import mysql.connector
from dotenv import load_dotenv
import os

create_bp = Blueprint('create_bp', __name__)

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

@create_bp.route('/add', methods=['POST'])
def add_post():
    post_content = request.form['post']
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    insert_query = "INSERT INTO example_table (post) VALUES (%s)"
    cursor.execute(insert_query, (post_content,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return redirect(url_for('index'))

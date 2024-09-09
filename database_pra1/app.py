from flask import Flask, render_template
import mysql.connector
from dotenv import load_dotenv
import os

app = Flask(__name__)

# MySQL configuration
db_config = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DB')
}

# Home route to show the data from the employees table
@app.route('/')
def show_employees():
    # Connect to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Execute the SQL query to retrieve employee data
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()  # Fetch all rows

    # Close the database connection
    cursor.close()
    conn.close()

    # Render the data using a template
    return render_template('employees.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True)
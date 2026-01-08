# app.py - Main Flask Application
# Import required libraries
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

# Initialize Flask app
app = Flask(__name__)

# Database configuration
DATABASE = 'market.db'

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize database tables
def init_db():
    conn = get_db_connection()
    
    # Create farmers table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            crop_type TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL,
            contact TEXT NOT NULL
        )
    ''')
    
    # Create buyers table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS buyers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            required_crop TEXT NOT NULL,
            quantity REAL NOT NULL,
            contact TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database when app starts
init_db()

# Route: Home page
@app.route('/')
def index():
    return render_template('index.html')

# Route: Farmer registration page (GET)
@app.route('/farmer-register')
def farmer_register():
    return render_template('farmer_register.html')

# Route: Farmer registration submission (POST)
@app.route('/farmer-register', methods=['POST'])
def farmer_register_post():
    # Get form data
    name = request.form['name']
    crop_type = request.form['crop_type']
    quantity = request.form['quantity']
    price = request.form['price']
    contact = request.form['contact']
    
    # Insert into database
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO farmers (name, crop_type, quantity, price, contact) VALUES (?, ?, ?, ?, ?)',
        (name, crop_type, quantity, price, contact)
    )
    conn.commit()
    conn.close()
    
    # Redirect to view farmers page
    return redirect(url_for('view_farmers'))

# Route: Buyer registration page (GET)
@app.route('/buyer-register')
def buyer_register():
    return render_template('buyer_register.html')

# Route: Buyer registration submission (POST)
@app.route('/buyer-register', methods=['POST'])
def buyer_register_post():
    # Get form data
    name = request.form['name']
    required_crop = request.form['required_crop']
    quantity = request.form['quantity']
    contact = request.form['contact']
    
    # Insert into database
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO buyers (name, required_crop, quantity, contact) VALUES (?, ?, ?, ?)',
        (name, required_crop, quantity, contact)
    )
    conn.commit()
    conn.close()
    
    # Redirect to view buyers page
    return redirect(url_for('view_buyers'))

# Route: View all farmers
@app.route('/view-farmers')
def view_farmers():
    conn = get_db_connection()
    farmers = conn.execute('SELECT * FROM farmers').fetchall()
    conn.close()
    return render_template('view_farmers.html', farmers=farmers)

# Route: View all buyers
@app.route('/view-buyers')
def view_buyers():
    conn = get_db_connection()
    buyers = conn.execute('SELECT * FROM buyers').fetchall()
    conn.close()
    return render_template('view_buyers.html', buyers=buyers)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request,jsonify
import sqlite3

app = Flask(__name__)

# Function to create the database table if it doesn't exist
def create_db():
    conn = sqlite3.connect('product.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    P_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    price REAL,
                    category TEXT,
                    contact INTEGER
                )''')
    conn.commit()
    conn.close()

create_db()

@app.route('/')
def home():
    conn = sqlite3.connect('product.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/sub', methods=['POST'])
def sub():
    title = request.form['title']
    description = request.form['description']
    price = request.form['price']
    category = request.form['category']
    contact = request.form['contact']

    conn = sqlite3.connect('product.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (title, description, price, category, contact) VALUES (?, ?, ?, ?, ?)", 
                   (title, description, price, category, contact))
    conn.commit()
    conn.close()
    
    Details = {
        'title': title,
        'Price': price,
        'category': category,
        'Contact': contact
    }
    return jsonify(Details)

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('query', '')
    with sqlite3.connect('product.db') as conn:
        results = conn.execute('SELECT * FROM products WHERE title LIKE ? OR category LIKE ?', 
                               (f'%{search_query}%', f'%{search_query}%')).fetchall()
    return jsonify(results)

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('product.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE P_ID=?", (id,))
    conn.commit()
    conn.close()
    return home()

if __name__ == '__main__':
    app.run(port=6001, debug=True)

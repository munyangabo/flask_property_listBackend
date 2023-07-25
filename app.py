from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS properties
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 location TEXT NOT NULL,
                 price INTEGER NOT NULL,
                 description TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Endpoint to add a new property
@app.route('/add_property', methods=['POST'])
def add_property():
    data = request.get_json()
    title = data.get('title')
    location = data.get('location')
    price = data.get('price')
    description = data.get('description')

    if not title or not location or not price or not description:
        return jsonify({'error': 'All fields are required.'}), 400

    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    c.execute("INSERT INTO properties (title, location, price, description) VALUES (?, ?, ?, ?)",
              (title, location, price, description))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Property added successfully!'}), 201

# Endpoint to search for properties by location and price range
@app.route('/search_properties', methods=['GET'])
def search_properties():
    location = request.args.get('location')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    conn = sqlite3.connect('properties.db')
    c = conn.cursor()

    query = "SELECT * FROM properties WHERE location LIKE ? AND price >= ? AND price <= ?"
    c.execute(query, ('%' + location + '%', min_price, max_price))
    properties = c.fetchall()
    conn.close()

    if not properties:
        return jsonify({'message': 'No properties found.'}), 404

    property_list = []
    for prop in properties:
        property_dict = {
            'id': prop[0],
            'title': prop[1],
            'location': prop[2],
            'price': prop[3],
            'description': prop[4]
        }
        property_list.append(property_dict)

    return jsonify(property_list), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


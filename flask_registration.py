# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # In a real-world application, you should hash the password before storing it.
    # For simplicity, we'll store it directly in the database.

    if not username or not password:
        return jsonify({'error': 'Username and password are required fields.'}), 400

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Username already exists. Please choose a different one.'}), 400

    conn.close()
    return jsonify({'message': 'Registration successful!'}), 201

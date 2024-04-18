from flask import Flask, render_template, request, redirect, url_for, session# type: ignore
import sqlite3

app = Flask(__name__)

app.secret_key = 'key'  

def get_db_connection():
    conn = sqlite3.connect('eatease.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT rest_id, name, location FROM restaurants')
    restaurants = cur.fetchall()
    conn.close()
    return render_template('land.html',restaurants=[dict(row) for row in restaurants])



@app.route('/restaurant/<int:rest_id>')
def restaurant_details(rest_id):
    conn = get_db_connection()
    cur = conn.cursor()
    # Query for the specific restaurant
    cur.execute('SELECT name, location FROM restaurants WHERE rest_id = ?', (rest_id,))
    restaurant = cur.fetchone()
    
    # Query for the menu of the restaurant
    cur.execute('SELECT name, price FROM menu_items WHERE rest_id = ?', (rest_id,))
    menu_items = cur.fetchall()
    conn.close()
    
    return render_template('restaurant_details.html', restaurant=restaurant, menu_items=menu_items)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cur.fetchone()
        conn.close()

        try:    
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = user['id']  # Storing user ID in session
            session['user_role'] = user['role']  # Assuming 'role' is a column in your users table
            if user and session['user_role'] == 2:
                return redirect(url_for('owner_dashboard'))
            elif user:
                return redirect(url_for('home'))
        except:
            return render_template('login.html')
    else:
        return render_template('login.html')



@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        conn = get_db_connection()
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email,))
        conn.commit()
        conn.close()
        session['logged_in'] = True  # Set session as logged in
        session['username'] = username  # Optionally store the username
        return redirect(url_for('home'))

    else:
        return render_template('signup.html')



@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Clear the logged_in flag in session
    session.pop('username', None)  # Clear the stored username, if any
    return redirect(url_for('home'))




@app.route('/order/<int:rest_id>')
def order(rest_id):
    if 'logged_in' in session and session['logged_in']:
        # Simulate order processing
        return render_template('order_confirmation.html', rest_id=rest_id)
    else:
        # Redirect to login if not logged in
        return redirect(url_for('login'))



@app.route('/owner_dashboard')
def owner_dashboard():
    if 'logged_in' in session and session['user_role'] == 2:  # Assuming '2' is for restaurant owners
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT rest_id, name, location FROM restaurants WHERE owner = ?', (session['user_id'],))
        restaurants = cur.fetchall()
        conn.close()
        return render_template('owner_dashboard.html', restaurants=[dict(row) for row in restaurants])
    else:
        return redirect(url_for('login'))  # Redirect non-owners to the login page




@app.route('/edit_menu/<int:rest_id>', methods=['GET', 'POST'])
def edit_menu(rest_id):
    if request.method == 'POST':
        # Handle form submission for updating menu items
        pass
    elif request.method == 'GET':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT name, price FROM menu_items WHERE rest_id = ?', (rest_id,))
        menu_items = cur.fetchall()
        conn.close()
        return render_template('edit_menu.html', menu_items=[dict(item) for item in menu_items], rest_id=rest_id)



if __name__ == '__main__':
    app.run(debug=True)

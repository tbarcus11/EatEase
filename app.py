from flask import Flask, render_template, request, redirect, url_for, session, flash, g# type: ignore
import sqlite3

app = Flask(__name__)

app.secret_key = 'key'  

def get_db_connection():
    conn = sqlite3.connect('eatease.db')
    conn.row_factory = sqlite3.Row
    return conn 

# A global flag to ensure session clearing happens only once
session_cleared = False

@app.before_request
def handle_session_clearing():
    global session_cleared
    if not session_cleared:
        session.clear()
        session_cleared = True


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





@app.route('/signup')
def signup():
    return render_template('signup.html')
    
@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

@app.route('/signup_owner', methods=['GET','POST'])
def signup_owner():
    if request.method == 'POST':
        conn = get_db_connection()
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)', (username, password, email, 2,))
        cur.close()

        cur2 =  conn.cursor()
        cur2.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cur2.fetchone()
        session['logged_in'] = True  # Set session as logged in
        session['username'] = username  # Optionally store the username
        session['user_id'] = user['id']  # Storing user ID in session
        session['user_role'] = user['role']  # Assuming 'role' is a column in your users table
        conn.commit()
        conn.close()


        session['logged_in'] = True  # Set session as logged in
        session['username'] = username  # Optionally store the username
        session['user_id'] = user['id']  # Storing user ID in session
        session['user_role'] = user['role']  # Assuming 'role' is a column in your users table
        return redirect(url_for('owner_dashboard'))

    else:
        return render_template('signup_owner.html')
    

@app.route('/signup_user', methods=['GET','POST'])
def signup_user():
    if request.method == 'POST':
        conn = get_db_connection()
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)', (username, password, email, 1,))
        conn.commit()
        conn.close()
        session['logged_in'] = True  # Set session as logged in
        session['username'] = username  # Optionally store the username
        return redirect(url_for('home'))

    else:
        return render_template('signup_user.html')



@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Clear the logged_in flag in session
    session.pop('username', None)  # Clear the stored username, if any
    return redirect(url_for('home'))




@app.route('/customer_menu/<int:rest_id>', methods=['GET', 'POST'])
def view_menu(rest_id):
    if 'logged_in' in session and session['logged_in']:
        conn = get_db_connection()
        cur = conn.cursor()

        if request.method == 'POST':
            # Process the order
            user_id = session['user_id']  # Assuming you store user_id in session
            menu_item_id = request.form['menu_item_id']
            # Insert order into the order table
            print("User_ID: ", user_id)
            print("rest_ID: ", rest_id)
            print("menu_id:", menu_item_id)


            cur.execute('INSERT INTO orders (rest_id, user_id, menu_item_id) VALUES (?, ?, ?)', (rest_id, user_id, menu_item_id,))
            conn.commit()

            # Optionally, redirect to a confirmation page or back to the menu
            return redirect(url_for('order_confirmation'))
        else:
            # Query for the specific restaurant
            cur.execute('SELECT name, location, rest_id FROM restaurants WHERE rest_id = ?', (rest_id,))
            restaurant = cur.fetchone()

            cur.execute('SELECT menu_item_id, name, price FROM menu_items WHERE rest_id = ?', (rest_id,))
            menu_items = cur.fetchall()
            conn.close()
            return render_template('customer_menu.html', restaurant=restaurant, menu_items=menu_items)
    else:
        # Redirect to login if not logged in
        return redirect(url_for('login.html'))



@app.route('/owner_dashboard')
def owner_dashboard():
    if 'logged_in' in session and session['user_role'] == 2:  # Assuming '2' is for restaurant owners
        conn = get_db_connection()
        cur = conn.cursor()

        print("id check: ", session['user_id'])
        cur.execute('SELECT rest_id, name, location FROM restaurants WHERE owner = ?', (session['user_id'],))
        restaurants = cur.fetchall()
        print(restaurants)
        conn.close()
        return render_template('owner_dashboard.html', restaurants=[dict(row) for row in restaurants])
    else:
        return redirect(url_for('login'))  # Redirect non-owners to the login page



#done
@app.route('/edit_menu/<int:rest_id>', methods=['GET', 'POST'])
def edit_menu(rest_id):
    if request.method == 'POST':
        # Determine action type from form data
        action = request.form.get('action')

        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()


        # Handling based on action type
        if action == 'add':
            item_name = request.form['item_name']
            item_price = request.form['item_price']
            cur.execute('INSERT INTO menu_items (name, price, rest_id) VALUES (?, ?, ?)', (item_name, float(item_price), rest_id))
        
        elif action == 'edit':
            item_name = request.form['item_name']
            item_price = request.form['item_price']
            # Assuming there is a unique identifier to locate the item
            item_id = request.form['menu_item_id']
            cur.execute('UPDATE menu_items SET name = ?, price = ? WHERE menu_item_id = ? AND rest_id = ?', (item_name, float(item_price), item_id, rest_id))
        
        elif action == 'delete':
            menu_item_id = request.form['menu_item_id']
            cur.execute('DELETE FROM menu_items WHERE menu_item_id = ?', (menu_item_id,))

        # Commit changes and close connection
        conn.commit()
        conn.close()

        # Redirect to the same page to see changes
        return redirect(url_for('edit_menu', rest_id=rest_id))
    
    elif request.method == 'GET':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT name, price, menu_item_id FROM menu_items WHERE rest_id = ?', (rest_id,))
        menu_items = cur.fetchall()
        conn.close()
        return render_template('edit_menu.html', menu_items=[dict(item) for item in menu_items], rest_id=rest_id)


@app.route('/leave_review/<int:rest_id>', methods=['GET', 'POST'])
def leave_review(rest_id):
    if 'logged_in' not in session:
        flash("Log in first")
        return redirect(url_for('login'))

    if request.method == 'POST':
        rating = request.form['rating']
        description = request.form['description']
        
        if not rating or not description:
            flash("All fields are required.")
            return render_template('leave_review.html', rest_id=rest_id)

        user_id = session['user_id']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO reviews (user_id, rest_id, rating, description) VALUES (?, ?, ?, ?)', (user_id, rest_id, rating, description))
        conn.commit()
        conn.close()
        flash('Your review has been successfully submitted.')
        return redirect(url_for('restaurant_details', rest_id=rest_id))
    else:
        return render_template('leave_review.html', rest_id=rest_id)


if __name__ == '__main__':
    app.run(debug=True)

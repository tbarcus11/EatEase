import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('eatease.db')

# Create cursor object
c = conn.cursor()


c.execute("DROP TABLE IF EXISTS menu_items")
c.execute("DROP TABLE IF EXISTS users")
c.execute("DROP TABLE IF EXISTS restaurants")

# Create tables
c.execute('''
CREATE TABLE IF NOT EXISTS restaurants (
    rest_id INTEGER,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    owner INTEGER
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role INTEGER
)
''')

c.execute('''
CREATE TABLE menu_items (
    menu_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rest_id INTEGER,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    FOREIGN KEY (rest_id) REFERENCES restaurants(rest_id)
);


''')

c.execute("INSERT INTO users (username, password, email, role) VALUES ('reg-customer', 'reg-customer', 'reg@gmail.com', 1)")
c.execute("INSERT INTO users (username, password, email, role) VALUES ('m-owner', 'm-owner', 'mainowner@gmail.com', 2)")
c.execute("INSERT INTO users (username, password, email, role) VALUES ('mcds-owner', 'mcds-owner', 'mcdsowner@gmail.com', 2)")

# Insert mock data
c.execute("INSERT INTO restaurants (rest_id, name, location, owner) VALUES (1, 'The Great Pizza', '123 Main St', 2)")
c.execute("INSERT INTO restaurants (rest_id, name, location, owner) VALUES (2, 'Burger House', '456 Side Ave', 2)")
c.execute("INSERT INTO restaurants (rest_id, name, location, owner) VALUES (3, 'McDonalds', '789 Des St', 3)")


c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (1, 'Margherita Pizza', 'Classic Margherita with fresh mozzarella and basil.', 12.99)")
c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (1, 'Pepperoni Pizza', 'Pepperoni with a blend of cheeses.', 14.99)")


c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (2, 'Classic Burger', 'Beef burger with lettuce, tomato, and onion.', 10.99)")
c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (2, 'Cheese Burger', 'Beef burger with cheese, lettuce, and tomato.', 11.99)")

c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (3, 'McDouble', 'McDub', 3.99)")
c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (3, 'Fries', 'Fries', 4.99)")
# Commit changes and close the connection
conn.commit()
conn.close()

print("Database initialized and mock data added!")

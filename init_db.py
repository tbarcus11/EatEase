import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('eatease.db')

# Create cursor object
c = conn.cursor()


c.execute("DROP TABLE IF EXISTS menu_items")
c.execute("DROP TABLE IF EXISTS users")
c.execute("DROP TABLE IF EXISTS restaurants")
c.execute("DROP TABLE IF EXISTS reviews")
c.execute("DROP TABLE IF EXISTS orders")

# Create tables
c.execute('''
CREATE TABLE IF NOT EXISTS restaurants (
    rest_id INTEGER PRIMARY KEY AUTOINCREMENT,
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

c.execute('''
    CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    rest_id INTEGER,
    rating INTEGER,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (rest_id) REFERENCES restaurants(rest_id)
);
''')

c.execute('''
    CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    rest_id INTEGER,
    menu_item_id
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (rest_id) REFERENCES restaurants(rest_id)
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(menu_item_id)
);
''')
#Starting user count at 10000

c.execute("INSERT INTO users (id, username, password, email) VALUES (9999, 'dummy', 'dummy', 'dummy@example.com');")
c.execute("DELETE FROM users WHERE id = 9999;")

#Inserting base users

c.execute("INSERT INTO users (username, password, email, role) VALUES ('customer', 'customer', 'reg@gmail.com', 1)")
c.execute("INSERT INTO users (username, password, email, role) VALUES ('owner', 'owner', 'mainowner@gmail.com', 2)")
c.execute("INSERT INTO users (username, password, email, role) VALUES ('mcds-owner', 'mcds-owner', 'mcdsowner@gmail.com', 2)")

# Inserting restraunts

c.execute("INSERT INTO restaurants (name, location, owner) VALUES ('The Great Pizza', '123 Main St', 10001)")
c.execute("INSERT INTO restaurants (name, location, owner) VALUES ('Burger House', '456 Side Ave', 10001)")
c.execute("INSERT INTO restaurants (name, location, owner) VALUES ('Tans Tacos', '246 KU Ave', 10001)")
c.execute("INSERT INTO restaurants (name, location, owner) VALUES ('McDonalds', '789 Des St', 10002)")

# Inserting menu items

c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (1, 'Margherita Pizza', 'Classic Margherita with fresh mozzarella and basil.', 12.99)")
c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (1, 'Pepperoni Pizza', 'Pepperoni with a blend of cheeses.', 14.99)")
c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (1, 'Sausage Pizza', 'Pizza with sausage topping', 12.99)")


c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (2, 'Classic Burger', 'Beef burger with lettuce, tomato, and onion.', 10.99)")
c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (2, 'Cheese Burger', 'Beef burger with cheese, lettuce, and tomato.', 11.99)")
c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (2, 'Buffalo Wings', 'Classing wings with Ranch as a side', 12.99)")

c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (3, 'Steak Tacos', 'Grilled steak tacos, comes with 4 tacos', 10.99)")
c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (3, 'Chicken Tacos', 'Grilled chicken tacos, comes with 4 tacos', 11.99)")
c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (3, 'Pork Tacos', 'Roasted pork tacos, comes with 4 tacos', 12.99)")


c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (4, 'McDouble', 'McDub', 3.99)")
c.execute("INSERT INTO menu_items (rest_id, name, description, price) VALUES (4, 'Fries', 'Fries', 4.99)")

# Inserting starter review
c.execute("INSERT INTO reviews (user_id, rest_id, rating, description) VALUES (10000, 1, 1, 'Pizza is just not good.')")
# Commit changes and close the connection
conn.commit()
conn.close()

print("Database initialized and mock data added!")

-- Start of SQL script to initialize the MySQL database for 'eatease'

-- Drop existing tables if they exist to start fresh
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS restaurants;

-- Creating the restaurants table
CREATE TABLE restaurants (
    rest_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    owner VARCHAR(255) NOT NULL
);

-- Creating the users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Creating the menu_items table
CREATE TABLE menu_items (
    menu_item_id INT AUTO_INCREMENT PRIMARY KEY,
    rest_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (rest_id) REFERENCES restaurants(rest_id)
);

-- Inserting mock data into restaurants
INSERT INTO restaurants (name, location, owner) VALUES ('The Great Pizza', '123 Main St', 'tanown');
INSERT INTO restaurants (name, location, owner) VALUES ('Burger House', '456 Side Ave', 'guy1');
INSERT INTO restaurants (name, location, owner) VALUES ('McDonalds', '789 Des St', 'guy2');

-- Inserting mock data into menu_items
INSERT INTO menu_items (rest_id, name, description, price) VALUES (1, 'Margherita Pizza', 'Classic Margherita with fresh mozzarella and basil.', 12.99);
INSERT INTO menu_items (rest_id, name, description, price) VALUES (1, 'Pepperoni Pizza', 'Pepperoni with a blend of cheeses.', 14.99);
INSERT INTO menu_items (rest_id, name, description, price) VALUES (2, 'Classic Burger', 'Beef burger with lettuce, tomato, and onion.', 10.99);
INSERT INTO menu_items (rest_id, name, description, price) VALUES (2, 'Cheese Burger', 'Beef burger with cheese, lettuce, and tomato.', 11.99);

-- End of SQL script

-- DE LEON, Richard Emmanuel 
-- GALIDO, Alyanna Nicole
-- LEONCIO, Kathleen Kate
-- REYES, Mark Andrei 
-- CMSC 127 S7l 
-- Project milestone 3

DROP DATABASE IF EXISTS 127Project;
CREATE DATABASE IF NOT EXISTS 127Project;
USE 127project;

-- USER(User id, Username, Password)
    CREATE TABLE users(
        userid INT(7) AUTO_INCREMENT,
        username VARCHAR(50) NOT NULL,
        userpassword LONGTEXT NOT NULL,
        CONSTRAINT user_userid_pk PRIMARY KEY(userid)
    );

    INSERT INTO users (username, userpassword) VALUES
        ('john_doe', 'password123'),
        ('jane_smith', 'securepass'),
        ('mike_jackson', 'p@ssw0rd!'),
        ('sara_williams', 'qwerty123'),
        ('chris_brown', 'letmein');

-- FOOD_ESTABLISHMENT(Food establishment id, Name, Location, Type,  Average rating)
    CREATE TABLE food_establishment(
        foodEst_id INT(7) AUTO_INCREMENT,
        foodEst_name VARCHAR(50) NOT NULL,
        foodEst_loc VARCHAR(50) NOT NULL,
        foodEst_type ENUM('Restaurant', 'Cafe', 'Fast Food', 'Other') NOT NULL,
        foodEst_rating DOUBLE,
        CONSTRAINT foodEstablisment_foodEst_id_pk PRIMARY KEY(foodEst_id)
    );
-- Insert dummy data
    INSERT INTO food_establishment (foodEst_name, foodEst_loc, foodEst_type) VALUES
        ('Tasty Bites', '123 Main Street', 'Restaurant'),
        ('Spice Garden', '456 Elm Street', 'Cafe'),
        ('Pizza Palace', '789 Oak Street', 'Fast Food');


-- FOOD_ITEM(Food item id, Name, Type, Price, Description, Average rating)
    CREATE TABLE food_item(
        foodItem_id INT(7) AUTO_INCREMENT,
        foodItem_name VARCHAR(50) NOT NULL,
        foodItem_price DECIMAL(6,2) NOT NULL,
        foodItem_type ENUM('Meat', 'Vegetables', 'Seafood', 'Burger', 'Pizza', 'Salad', 'Noodles', 'Sushi', 'Indian', 'Vietnamese', 'Italian', 'Middle Eastern') NOT NULL,
        foodItem_desc VARCHAR(100) NOT NULL,
        foodItem_rating DOUBLE,
        CONSTRAINT food_item_foodItem_id_pk PRIMARY KEY(foodItem_id)
    );

    INSERT INTO food_item (foodItem_name, foodItem_price, foodItem_type, foodItem_desc) VALUES
        ('Cheeseburger', 9.99, 'Burger', 'A classic cheeseburger with lettuce, tomato, and pickles.'),
        ('Margherita Pizza', 12.99, 'Pizza', 'Traditional pizza topped with tomato sauce, fresh mozzarella, and basil.'),
        ('Chicken Caesar Salad', 8.49, 'Salad', 'Fresh romaine lettuce topped with grilled chicken, croutons, and Caesar dressing.'),
        ('Pad Thai', 10.99, 'Noodles', 'Stir-fried rice noodles with tofu, bean sprouts, peanuts, and a tangy sauce.'),
        ('Sushi Combo', 15.99, 'Sushi', 'Assorted sushi rolls including tuna, salmon, and California rolls.'),
        ('Grilled Salmon', 16.99, 'Seafood', 'Fresh Atlantic salmon grilled to perfection served with steamed vegetables.'),
        ('Chicken Tikka Masala', 13.99, 'Indian', 'Tender chicken pieces cooked in a creamy tomato sauce with Indian spices.'),
        ('Pho Soup', 11.49, 'Vietnamese', 'Traditional Vietnamese soup with rice noodles, beef broth, and herbs.'),
        ('Pasta Carbonara', 14.99, 'Italian', 'Spaghetti pasta with creamy egg sauce, pancetta, and Parmesan cheese.'),
        ('Falafel Wrap', 7.99, 'Middle Eastern', 'Falafel balls wrapped in pita bread with lettuce, tomato, and tahini sauce.');

-- REVIEW(Review id, Date of review, Content, Rating, User id, Food establishment id, Food item id)
    CREATE TABLE review(
        review_id INT(7) AUTO_INCREMENT,
        review_date DATE NOT NULL,
        content VARCHAR(100) NOT NULL,
        rating INT(1),
        userid INT(7),
        foodEst_id INT(7),
        foodItem_id INT(7),
        CONSTRAINT review_review_id_pk PRIMARY KEY(review_id),
        CONSTRAINT review_userid_fk FOREIGN KEY(userid) REFERENCES users(userid),
        CONSTRAINT review_foodEstid_fk FOREIGN KEY(foodEst_id) REFERENCES food_establishment(foodEst_id),
        CONSTRAINT review_foodItemid_fk FOREIGN KEY(foodItem_id) REFERENCES food_item(foodItem_id)
    );

    INSERT INTO review (review_date, content, rating, userid, foodest_id, fooditem_id) VALUES
        ('2024-05-01', 'Great food and service!', 5, 1, 1, 1),
        ('2024-05-02', 'Delicious pizza!', 4, 2, 3, 2),
        ('2024-05-03', 'Average experience.', 3, 3, 2, 3),
        ('2024-05-04', 'Best pho I''ve ever had!', 5, 4, 3, 8),
        ('2024-05-05', 'Not impressed with the burger.', 2, 5, 1, 1),
        ('2024-05-06', 'Excellent service but the sushi was mediocre.', 4, 1, 2, 5),
        ('2024-05-07', 'Very tasty falafel!', 5, 2, 3, 10),
        ('2024-05-08', 'Disappointing experience overall.', 1, 3, 1, 8);

-- REVIEWS_FOOD_ESTABLISHMENT(Food establishment id,  Review id)
    CREATE TABLE reviews_foodest(
        foodEst_id INT(7) NOT NULL,
        review_id INT(7) NOT NULL,
        PRIMARY KEY(foodEst_id, review_id),
        CONSTRAINT reviewsFoodEst_foodEstId_fk FOREIGN KEY(foodEst_id) REFERENCES food_establishment(foodEst_id),
        CONSTRAINT reviewsFoodEst_reviewId_fk FOREIGN KEY(review_id) REFERENCES review(review_id)
    );

-- REVIEWS_FOOD_ITEM(User id, Food item id)
    CREATE TABLE reviews_fooditem(
        userid INT(7) NOT NULL,
        foodItem_id INT(7) NOT NULL,
        CONSTRAINT PRIMARY KEY(userid, foodItem_id),
        CONSTRAINT reviewsFoodItem_userid_fk FOREIGN KEY(userid) REFERENCES users(userid),
        CONSTRAINT reviewsFoodItem_foodItemId_fk FOREIGN KEY(foodItem_id) REFERENCES food_item(foodItem_id)
    );

-- SERVES(Food establishment id, Food item id)
    CREATE TABLE serves(
        foodEst_id INT(7) NOT NULL,
        foodItem_id INT(7) NOT NULL,
        CONSTRAINT PRIMARY KEY(foodest_id, fooditem_id),
        CONSTRAINT serves_foodEstId_fk FOREIGN KEY(foodEst_id) REFERENCES food_establishment(foodEst_id),
        CONSTRAINT serves_foodItemId_fk FOREIGN KEY(foodItem_id) REFERENCES food_item(foodItem_id)
    );

    INSERT INTO serves(foodEst_id, foodItem_id) VALUES 
    (1, 1), -- Tasty Bites serves Cheeseburger
    (1, 3), -- Tasty Bites serves Chicken Caesar Salad
    (1, 10), -- Tasty Bites serves Falafel Wrap
    (2, 2), -- Spice Garden serves Margherita Pizza
    (3, 2); -- Pizza Palace serves Margherita Pizza




-- View all food establishments;
    SELECT * FROM food_establishment;

-- View all food reviews for an establishment or a food item;
    SELECT * FROM review;

-- View all food items from an establishment;
    SELECT * FROM food_item;

-- View all food items from an establishment that belong to a food type {meat | veg | etc.};
    SELECT fi.foodItem_id, fi.foodItem_name, fi.foodItem_type, fi.foodItem_price, fi.foodItem_desc, fi.foodItem_rating
    FROM food_item FI
    JOIN serves s ON fi.foodItem_id = s.foodItem_id
    JOIN food_establishment fe ON s.foodEst_id = fe.foodEst_id
    WHERE fe.foodEst_name = 'Spice Garden'
    AND fi.foodItem_type = 'Pizza';     JOIN serves s ON fi.foodItem_id = s.foodItem_id
    JOIN food_establishment fe ON s.foodEst_id = fe.foodEst_id
    WHERE fe.foodEst_name = 'Spice Garden'
    AND fi.foodItem_type = 'Pizza'; 

-- View all reviews made within a month for an establishment or a food item;

    SELECT r.review_id, r.review_date, r.content, r.rating, u.username,
        fe.foodEst_name, fi.foodItem_name
    FROM review r
    JOIN users u ON r.userid = u.userid
    LEFT JOIN food_establishment fe ON r.foodEst_id = fe.foodEst_id
    LEFT JOIN food_item fi ON r.foodItem_id = fi.foodItem_id
    WHERE (fe.foodEst_id = 1 OR fi.foodItem_id = 1)
        AND r.review_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE();


-- View all food items from an establishment arranged according to price;
    SELECT fi.foodItem_id, fi.foodItem_name, fi.foodItem_price, fi.foodItem_type, fi.foodItem_desc, fi.foodItem_rating
    FROM serves s
    JOIN food_item fi ON s.foodItem_id = fi.foodItem_id
    WHERE s.foodEst_id = 1
    ORDER BY fi.foodItem_price ASC;

-- Search food items from any establishment based on a given price range and/or food type.
    SELECT fi.foodItem_id, fi.foodItem_name, fi.foodItem_price, fi.foodItem_type, fi.foodItem_desc, fi.foodItem_rating, fe.foodEst_name AS establishment_name
    FROM serves s
    JOIN food_item fi ON s.foodItem_id = fi.foodItem_id
    JOIN food_establishment fe ON s.foodEst_id = fe.foodEst_id
    WHERE 
        (fi.foodItem_price BETWEEN 10.00 AND 15.00) -- Specify the price range
        AND (fi.foodItem_type = 'Pizza') -- Specify the food type
    ORDER BY fi.foodItem_price ASC;

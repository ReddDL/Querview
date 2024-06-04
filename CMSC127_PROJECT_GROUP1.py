import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# Database connection function
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='127projectV3',
            user='root',
            password='052508'  # replace ng password niyo 
        )
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror("Error", f"Error connecting to MySQL: {e}")
        return None
    

# R - Reports to be generated
# F - Features

# ===== VIEW TAB =====

# 1R -- Function to view all food establishments
def view_food_establishments(view_right_frame):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT
                        fe.foodEst_name, 
                        fe.foodEst_loc, 
                        fe.foodEst_type, 
                        COALESCE(AVG(rating), 0) AS 'AVERAGE RATING' 
                        FROM food_establishment fe
                        LEFT JOIN review r 
                        ON fe.foodEst_id=r.foodEst_id
                        GROUP BY fe.foodEst_id; 
                        """)
        records = cursor.fetchall()
        display_records(records, ["Name", "Location", "Type", "Average Rating"], view_right_frame)
        cursor.close()
        connection.close()

# 2R -- Function to view all reviews for an establishment
def view_reviews_establishment(view_right_frame):
    connection = connect_to_db()
    if connection: 
        cursor = connection.cursor()
        cursor.execute("""SELECT 
                       fe.foodEst_id,
                       fe.foodEst_name, 
                       fe.foodEst_loc, 
                       fe.foodEst_type, 
                       AVG(rating) AS 'AVERAGE RATING' 
                       FROM review r 
                       JOIN food_establishment fe 
                       ON r.foodEst_id=fe.foodEst_id 
                       WHERE r.foodEst_id IS NOT NULL 
                       GROUP BY r.foodEst_id;""")
        records = cursor.fetchall()
        cursor.close()
        connection.close()

        # Clear previous records in the right frame
        for widget in view_right_frame.winfo_children():
            widget.destroy()

        # Create two frames for the two Treeviews
        top_frame = tk.Frame(view_right_frame)
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        bottom_frame = tk.Frame(view_right_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # Create a Treeview to display the records in the top frame
        tree = ttk.Treeview(top_frame, columns=("ID", "Name", "Location", "Type", "Rating"), show='headings')
        tree.pack(expand=True, fill=tk.BOTH)

        # Define columns
        tree.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree.column("ID", anchor=tk.W, width=100)
        tree.column("Name", anchor=tk.W, width=100)
        tree.column("Location", anchor=tk.W, width=100)
        tree.column("Type", anchor=tk.W, width=100)
        tree.column("Rating", anchor=tk.W, width=100)

        # Create headings
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Location", text="Location")
        tree.heading("Type", text="Type")
        tree.heading("Rating", text="Rating")

        # Add records to the Treeview
        for record in records:
            tree.insert("", tk.END, values=record)

        # Function to handle the selection
        def on_select(event):
            selected_item = tree.focus()
            if selected_item:
                selected_food_establishment = tree.item(selected_item)["values"][0]
                
                connection = connect_to_db()
                if connection: 
                    cursor = connection.cursor()
                    cursor.execute("""SELECT r.review_date, 
                                    r.content, 
                                    r.rating 
                                    FROM review r 
                                    JOIN food_establishment fe ON r.foodEst_id=fe.foodEst_id 
                                    WHERE r.foodItem_id IS NULL AND fe.foodEst_id = %s 
                                    ORDER BY r.review_date;""", (selected_food_establishment,))
                    reviews = cursor.fetchall()
                    cursor.close()
                    connection.close()

                    for widget in bottom_frame.winfo_children():
                        widget.destroy()

                    # Add a horizontal scrollbar to the reviews Treeview
                    tree_reviews_xscroll = ttk.Scrollbar(bottom_frame, orient=tk.HORIZONTAL)
                    tree_reviews_xscroll.pack(side=tk.BOTTOM, fill=tk.X)

                    tree_reviews = ttk.Treeview(bottom_frame, columns=("Review date", "Content", "Rating"), show='headings', xscrollcommand=tree_reviews_xscroll.set)
                    tree_reviews.heading("Review date", text="Review date")
                    tree_reviews.heading("Content", text="Content")
                    tree_reviews.heading("Rating", text="Rating")

                    tree_reviews.column("Review date", anchor=tk.W, width=100)
                    tree_reviews.column("Content", anchor=tk.W, width=250)
                    tree_reviews.column("Rating", anchor=tk.W, width=100)

                    for review in reviews:
                        tree_reviews.insert("", tk.END, values=review)

                    tree_reviews.pack(fill=tk.BOTH, expand=True)
                    tree_reviews_xscroll.config(command=tree_reviews.xview)

        tree.bind("<ButtonRelease-1>", on_select)

# 2R -- Function to view all reviews for a food item
def view_reviews_food(view_right_frame):
    connection = connect_to_db()
    if connection: 
        cursor = connection.cursor()
        cursor.execute("""SELECT
                            fi.foodItem_id, 
                            fi.foodItem_name, 
                            fi.foodItem_price, 
                            fi.foodItem_type, 
                            fi.foodItem_desc, 
                            AVG(rating) AS 'AVERAGE RATING' 
                            FROM review r 
                            JOIN food_item fi ON r.foodItem_id=fi.foodItem_id 
                            WHERE r.foodItem_id IS NOT NULL 
                            GROUP BY r.foodItem_id;""")
        records = cursor.fetchall()
        cursor.close()
        connection.close()

        # Clear previous records in the right frame
        for widget in view_right_frame.winfo_children():
            widget.destroy()

        # Create two frames for the two Treeviews
        top_frame = tk.Frame(view_right_frame)
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        bottom_frame = tk.Frame(view_right_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # Create a Treeview to display the records in the top frame
        tree = ttk.Treeview(top_frame, columns=("ID", "Name", "Price", "Type", "Description", "Rating"), show='headings')
        tree.pack(expand=True, fill=tk.BOTH)

        # Define columns
        tree.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree.column("ID", anchor=tk.W, width=100)
        tree.column("Name", anchor=tk.W, width=100)
        tree.column("Price", anchor=tk.W, width=100)
        tree.column("Type", anchor=tk.W, width=100)
        tree.column("Description", anchor=tk.W, width=150)
        tree.column("Rating", anchor=tk.W, width=100)

        # Create headings
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Price", text="Price")
        tree.heading("Type", text="Type")
        tree.heading("Description", text="Description")
        tree.heading("Rating", text="Rating")

        # Add records to the Treeview
        for record in records:
            tree.insert("", tk.END, values=record)

        # Function to handle the selection of food items and display reviews
        def on_item_select(event):
            selected_item = tree.focus()
            if selected_item:
                selected_food_item_id = tree.item(selected_item)["values"][0]
                
                connection = connect_to_db()
                if connection: 
                    cursor = connection.cursor()
                    cursor.execute("""SELECT review_date, 
                                    content, 
                                    rating 
                                    FROM review 
                                    WHERE foodItem_id = %s;""", (selected_food_item_id,))
                    food_reviews = cursor.fetchall()
                    cursor.close()
                    connection.close()

                    for widget in bottom_frame.winfo_children():
                        widget.destroy()

                    # Create a new Treeview to display reviews in the bottom frame
                    tree_food_reviews = ttk.Treeview(bottom_frame, columns=("Review date", "Content", "Rating"), show='headings')
                    tree_food_reviews.pack(expand=True, fill=tk.BOTH)

                    # Define columns for reviews
                    tree_food_reviews.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
                    tree_food_reviews.column("Review date", anchor=tk.W, width=100)
                    tree_food_reviews.column("Content", anchor=tk.W, width=250)
                    tree_food_reviews.column("Rating", anchor=tk.W, width=100)

                    # Create headings for reviews
                    tree_food_reviews.heading("Review date", text="Review date")
                    tree_food_reviews.heading("Content", text="Content")
                    tree_food_reviews.heading("Rating", text="Rating")

                    for review in food_reviews:
                        tree_food_reviews.insert("", tk.END, values=review)

        tree.bind("<ButtonRelease-1>", on_item_select)

# 3R -- Function to view all food items from an establishment
def view_items_from_estab(view_right_frame):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT 
                fe.foodEst_id,
                fe.foodEst_name, 
                fe.foodEst_loc, 
                fe.foodEst_type, 
                AVG(r.rating) AS 'AVERAGE RATING' 
            FROM review r 
            JOIN food_establishment fe 
            ON r.foodEst_id = fe.foodEst_id 
            WHERE r.foodEst_id IS NOT NULL 
            GROUP BY r.foodEst_id;
        """)
        records = cursor.fetchall()
        cursor.close()
        connection.close()

        # Clear previous records in the right frame
        for widget in view_right_frame.winfo_children():
            widget.destroy()

        # Create two frames for the two Treeviews
        top_frame = tk.Frame(view_right_frame)
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        bottom_frame = tk.Frame(view_right_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # Create a Treeview to display the records in the top frame
        tree = ttk.Treeview(top_frame, columns=("ID", "Name", "Location", "Type", "Rating"), show='headings')
        tree.pack(expand=True, fill=tk.BOTH)

        # Define columns
        tree.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree.column("ID", anchor=tk.W, width=100)
        tree.column("Name", anchor=tk.W, width=100)
        tree.column("Location", anchor=tk.W, width=100)
        tree.column("Type", anchor=tk.W, width=100)
        tree.column("Rating", anchor=tk.W, width=100)

        # Create headings
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Location", text="Location")
        tree.heading("Type", text="Type")
        tree.heading("Rating", text="Rating")

        # Add records to the Treeview
        for record in records:
            tree.insert("", tk.END, values=record)

        # Function to handle the selection
        def on_select(event):
            for child in tree_reviews.get_children():
                tree_reviews.delete(child)

            selected_item = tree.focus()
            if selected_item:
                selected_food_establishment_id = tree.item(selected_item)["values"][0]

                connection = connect_to_db()
                if connection:
                    cursor = connection.cursor()
                    cursor.execute("""
                        UPDATE food_item fi
                            SET foodItem_rating = (
                                SELECT AVG(rating)
                                FROM review
                                WHERE foodItem_id = fi.foodItem_id
                            );
                    """)
                    cursor.execute("""
                        SELECT 
                            fi.foodItem_id, 
                            fi.foodItem_name, 
                            fi.foodItem_price, 
                            fi.foodItem_type, 
                            fi.foodItem_desc, 
                            fi.foodItem_rating
                        FROM food_item fi  
                        WHERE fi.foodEst_id = %s 
                    """, (selected_food_establishment_id,))
                    items = cursor.fetchall()
                    cursor.close()
                    connection.close()

                    for item in items:
                        tree_reviews.insert("", tk.END, values=item)

        tree.bind("<ButtonRelease-1>", on_select)

        # Create a Treeview to display the reviews in the bottom frame
        global tree_reviews
        tree_reviews = ttk.Treeview(bottom_frame, columns=("ID", "Name", "Price", "Type", "Description", "Rating"), show='headings')
        tree_reviews.pack(expand=True, fill=tk.BOTH)

        tree_reviews.column("#0", width=0, stretch=tk.NO)
        tree_reviews.column("ID", anchor=tk.W, width=10)
        tree_reviews.column("Name", anchor=tk.W, width=100)
        tree_reviews.column("Price", anchor=tk.W, width=100)
        tree_reviews.column("Type", anchor=tk.W, width=100)
        tree_reviews.column("Description", anchor=tk.W, width=150)
        tree_reviews.column("Rating", anchor=tk.W, width=100)

        tree_reviews.heading("ID", text="ID")
        tree_reviews.heading("Name", text="Name")
        tree_reviews.heading("Price", text="Price")
        tree_reviews.heading("Type", text="Type")
        tree_reviews.heading("Description", text="Description")
        tree_reviews.heading("Rating", text="Rating")

# 4R -- View all food items from an establishment that belong to a food type {meat | veg | etc.};
def view_items_from_type(view_right_frame):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SHOW COLUMNS FROM food_item LIKE 'foodItem_type'")
        records = cursor.fetchone()[1]
        cursor.close()
        connection.close()

        food_types = records.replace("enum(", "").replace(")", "").replace("'", "").split(",")

        # Clear previous records in the right frame
        for widget in view_right_frame.winfo_children():
            widget.destroy()

        # Create two frames for the two Treeviews
        top_frame = tk.Frame(view_right_frame)
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        bottom_frame = tk.Frame(view_right_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # Create a Treeview to display the food types in the top frame
        tree = ttk.Treeview(top_frame, columns=("Type"), show='headings')
        tree.pack(expand=True, fill=tk.BOTH)

        # Define columns
        tree.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree.column("Type", anchor=tk.W, width=100)

        # Create headings
        tree.heading("Type", text="Type")

        # Add records to the Treeview
        for food_type in food_types:
            tree.insert("", tk.END, values=(food_type,))

        # Create a Treeview to display the items in the bottom frame
        tree_reviews = ttk.Treeview(bottom_frame, columns=("ID", "Name", "Price", "Type", "Description", "Rating"), show='headings')
        tree_reviews.pack(expand=True, fill=tk.BOTH)

        # Define columns for items
        tree_reviews.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree_reviews.column("ID", anchor=tk.W, width=50)
        tree_reviews.column("Name", anchor=tk.W, width=100)
        tree_reviews.column("Price", anchor=tk.W, width=100)
        tree_reviews.column("Type", anchor=tk.W, width=100)
        tree_reviews.column("Description", anchor=tk.W, width=150)
        tree_reviews.column("Rating", anchor=tk.W, width=100)

        # Create headings for items
        tree_reviews.heading("ID", text="ID")
        tree_reviews.heading("Name", text="Name")
        tree_reviews.heading("Price", text="Price")
        tree_reviews.heading("Type", text="Type")
        tree_reviews.heading("Description", text="Description")
        tree_reviews.heading("Rating", text="Rating")

        # Function to handle the selection
        def on_select(event):
            # Clear previous reviews
            for child in tree_reviews.get_children():
                tree_reviews.delete(child)

            # Get the selected item
            selected_item = tree.focus()
            if selected_item:
                # Extract the food type from the selected item
                selected_food_type = tree.item(selected_item)["values"][0]

                # Execute another query based on the selected food type
                connection = connect_to_db()
                if connection:
                    cursor = connection.cursor()
                    cursor.execute("""
                        UPDATE food_item fi
                            SET foodItem_rating = (
                                SELECT AVG(rating)
                                FROM review
                                WHERE foodItem_id = fi.foodItem_id
                            );
                    """)
                    cursor.execute("""
                        SELECT 
                            fi.foodItem_id, 
                            fi.foodItem_name, 
                            fi.foodItem_price, 
                            fi.foodItem_type, 
                            fi.foodItem_desc, 
                            fi.foodItem_rating
                        FROM food_item fi  
                        WHERE fi.foodItem_type = %s 
                    """, (selected_food_type,))
                    items = cursor.fetchall()
                    cursor.close()
                    connection.close()

                    # Add items to the Treeview
                    for item in items:
                        tree_reviews.insert("", tk.END, values=item)

        # Bind the selection event to the function
        tree.bind("<ButtonRelease-1>", on_select)

# 5R -- Function to view all reviews made within a month for an establishment
def view_reviews_establishment_month(view_right_frame):
    connection = connect_to_db()
    if connection: 
        cursor = connection.cursor()
        cursor.execute("""SELECT 
                       fe.foodEst_id,
                       fe.foodEst_name, 
                       fe.foodEst_loc, 
                       fe.foodEst_type, 
                       AVG(rating) AS 'AVERAGE RATING' 
                       FROM review r 
                       JOIN food_establishment fe 
                       ON r.foodEst_id=fe.foodEst_id 
                       WHERE r.foodEst_id IS NOT NULL 
                       GROUP BY r.foodEst_id;""")
        records = cursor.fetchall()
        cursor.close()
        connection.close()

        # Clear previous records in the right frame
        for widget in view_right_frame.winfo_children():
            widget.destroy()

        # Create two frames for the two Treeviews
        top_frame = tk.Frame(view_right_frame)
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        bottom_frame = tk.Frame(view_right_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # Create a Treeview to display the records in the top frame
        tree = ttk.Treeview(top_frame, columns=("ID", "Name", "Location", "Type", "Rating"), show='headings')
        tree.pack(expand=True, fill=tk.BOTH)

        # Define columns
        tree.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree.column("ID", anchor=tk.W, width=100)
        tree.column("Name", anchor=tk.W, width=100)
        tree.column("Location", anchor=tk.W, width=100)
        tree.column("Type", anchor=tk.W, width=100)
        tree.column("Rating", anchor=tk.W, width=100)

        # Create headings
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Location", text="Location")
        tree.heading("Type", text="Type")
        tree.heading("Rating", text="Rating")

        # Add records to the Treeview
        for record in records:
            tree.insert("", tk.END, values=record)

        # Function to handle the selection
        def on_select(event):
            # Clear previous reviews
            for child in tree_reviews.get_children():
                tree_reviews.delete(child)

            # Get the selected item
            selected_item = tree.focus()
            if selected_item:
                # Extract the food establishment name from the selected item
                selected_food_establishment = tree.item(selected_item)["values"][0]
                
                # Execute another query based on the selected food establishment
                connection = connect_to_db()
                if connection: 
                    cursor = connection.cursor()
                    cursor.execute("""SELECT review_date, 
                                   content, 
                                   rating from review 
                                   WHERE foodEst_id = (SELECT foodEst_id FROM
                                                       food_establishment WHERE foodEst_id = %s) AND review_date BETWEEN 
                                                       ADDDATE(CURDATE(), INTERVAL -1 MONTH) AND CURDATE();""", (selected_food_establishment,))
                    reviews = cursor.fetchall()
                    cursor.close()
                    connection.close()

                    # Add reviews to the Treeview for reviews
                    for review in reviews:
                        tree_reviews.insert("", tk.END, values=review)

        # Bind the selection event to the function
        tree.bind("<ButtonRelease-1>", on_select)

        # Create a new Treeview to display reviews in the bottom frame
        tree_reviews = ttk.Treeview(bottom_frame, columns=("Review date", "Content", "Rating"), show='headings')
        tree_reviews.pack(expand=True, fill=tk.BOTH)

        # Define columns for reviews
        tree_reviews.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree_reviews.column("Review date", anchor=tk.W, width=100)
        tree_reviews.column("Content", anchor=tk.W, width=250)
        tree_reviews.column("Rating", anchor=tk.W, width=100)

        # Create headings for reviews
        tree_reviews.heading("Review date", text="Review date")
        tree_reviews.heading("Content", text="Content")
        tree_reviews.heading("Rating", text="Rating")

# 5R -- Function to view all reviews made within a month for an establishment
def view_reviews_food_month(view_right_frame):
    connection = connect_to_db()
    if connection: 
        cursor = connection.cursor()
        cursor.execute("""SELECT foodItem_id, 
                       foodItem_name, 
                       foodItem_price,
                       foodItem_type,
                       foodItem_desc, 
                       foodItem_rating 
                       FROM food_item""")
        records = cursor.fetchall()
        cursor.close()
        connection.close()

        # Clear previous records in the right frame
        for widget in view_right_frame.winfo_children():
            widget.destroy()

        # Create two frames for the two Treeviews
        top_frame = tk.Frame(view_right_frame)
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        bottom_frame = tk.Frame(view_right_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # Create a Treeview to display the records in the top frame
        tree = ttk.Treeview(top_frame, columns=("ID", "Name", "Price", "Type", "Description", "Rating"), show='headings')
        tree.pack(expand=True, fill=tk.BOTH)

        # Define columns
        tree.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree.column("ID", anchor=tk.W, width=100)
        tree.column("Name", anchor=tk.W, width=100)
        tree.column("Price", anchor=tk.W, width=100)
        tree.column("Type", anchor=tk.W, width=100)
        tree.column("Description", anchor=tk.W, width=150)
        tree.column("Rating", anchor=tk.W, width=100)

        # Create headings
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Price", text="Price")
        tree.heading("Type", text="Type")
        tree.heading("Description", text="Description")
        tree.heading("Rating", text="Rating")

        # Add records to the Treeview
        for record in records:
            tree.insert("", tk.END, values=record)

        # Function to handle the selection
        def on_select(event):
            for child in tree_reviews.get_children():
                tree_reviews.delete(child)

            selected_item = tree.focus()
            if selected_item:
                selected_food_item_id = tree.item(selected_item)["values"][0]

                connection = connect_to_db()
                if connection: 
                    cursor = connection.cursor()
                    cursor.execute("""
                        SELECT review_date, content, rating 
                        FROM review 
                        WHERE foodItem_id = %s 
                        AND review_date BETWEEN ADDDATE(CURDATE(), INTERVAL -1 MONTH) AND CURDATE()
                    """, (selected_food_item_id,))
                    reviews = cursor.fetchall()
                    cursor.close()
                    connection.close()

                    for review in reviews:
                        tree_reviews.insert("", tk.END, values=review)
        
        tree.bind("<ButtonRelease-1>", on_select)

        # Create a Treeview to display the reviews in the bottom frame
        tree_reviews = ttk.Treeview(bottom_frame, columns=("Review date", "Content", "Rating"), show='headings')
        tree_reviews.pack(expand=True, fill=tk.BOTH)

        tree_reviews.column("#0", width=0, stretch=tk.NO)
        tree_reviews.column("Review date", anchor=tk.W, width=100)
        tree_reviews.column("Content", anchor=tk.W, width=250)
        tree_reviews.column("Rating", anchor=tk.W, width=100)

        tree_reviews.heading("Review date", text="Review date")
        tree_reviews.heading("Content", text="Content")
        tree_reviews.heading("Rating", text="Rating")

# 6R -- Function to view establishments with high rating (>=4)
def view_estab_high_rating(view_right_frame):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT fe.foodEst_name, 
                       fe.foodEst_loc, 
                       fe.foodEst_type,
                       AVG(rating) 'AVERAGE RATING' 
                       FROM review r 
                       JOIN food_establishment fe ON r.foodEst_id=fe.foodEst_id 
                       WHERE r.foodEst_id IS NOT NULL 
                       GROUP BY r.foodEst_id 
                       HAVING `AVERAGE RATING` >= 4;""")
        records = cursor.fetchall()
        display_records(records, ["Name", "Location", "Type", "Average Rating"], view_right_frame)
        cursor.close()
        connection.close()

# 7R -- View all food items from an establishment arranged according to price
def view_items_by_price(view_right_frame):
    connection = connect_to_db()
    if connection: 
        cursor = connection.cursor()
        cursor.execute("""SELECT 
                           fe.foodEst_id,
                           fe.foodEst_name, 
                           fe.foodEst_loc, 
                           fe.foodEst_type, 
                           AVG(rating) AS 'AVERAGE RATING' 
                           FROM review r 
                           JOIN food_establishment fe 
                           ON r.foodEst_id=fe.foodEst_id 
                           WHERE r.foodEst_id IS NOT NULL 
                           GROUP BY r.foodEst_id;""")
        records = cursor.fetchall()
        cursor.close()
        connection.close()

        # Clear previous records in the right frame
        for widget in view_right_frame.winfo_children():
            widget.destroy()

        # Create two frames for the two Treeviews
        top_frame = tk.Frame(view_right_frame)
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        bottom_frame = tk.Frame(view_right_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # Create a Treeview to display the records in the top frame
        tree = ttk.Treeview(top_frame, columns=("ID", "Name", "Location", "Type", "Rating"), show='headings')
        tree.pack(expand=True, fill=tk.BOTH)

        # Define columns
        tree.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree.column("ID", anchor=tk.W, width=100)
        tree.column("Name", anchor=tk.W, width=100)
        tree.column("Location", anchor=tk.W, width=100)
        tree.column("Type", anchor=tk.W, width=100)
        tree.column("Rating", anchor=tk.W, width=100)

        # Create headings
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Location", text="Location")
        tree.heading("Type", text="Type")
        tree.heading("Rating", text="Rating")

        # Add records to the Treeview
        for record in records:
            tree.insert("", tk.END, values=record)
        
        # Function to handle the selection
        def on_select(event):
            for child in tree_reviews.get_children():
                tree_reviews.delete(child)

            selected_item = tree.focus()
            if selected_item:
                selected_food_establishment_id = tree.item(selected_item)["values"][0]

                connection = connect_to_db()
                if connection: 
                    cursor = connection.cursor()
                    cursor.execute("""
                        SELECT fi.foodItem_id 'ID', 
                           foodItem_name 'Name', 
                           foodItem_price 'Price', 
                           foodItem_type 'Type', 
                           foodItem_desc 'Description', 
                           AVG(r.rating) 'Rating' 
                           FROM food_item fi 
                           JOIN review r ON fi.foodItem_id=r.foodItem_id WHERE fi.foodEst_id = %s 
                           GROUP BY r.foodItem_id
                           ORDER BY foodItem_price DESC;
                    """, (selected_food_establishment_id,))
                    items = cursor.fetchall()
                    cursor.close()
                    connection.close()

                    for item in items:
                        tree_reviews.insert("", tk.END, values=item)
        
        tree.bind("<ButtonRelease-1>", on_select)

        # Create a Treeview to display the items in the bottom frame
        tree_reviews = ttk.Treeview(bottom_frame, columns=("ID", "Name", "Price", "Type", "Description", "Rating"), show='headings')
        tree_reviews.pack(expand=True, fill=tk.BOTH)

        tree_reviews.column("#0", width=0, stretch=tk.NO)
        tree_reviews.column("ID", anchor=tk.W, width=50)
        tree_reviews.column("Name", anchor=tk.W, width=100)
        tree_reviews.column("Price", anchor=tk.W, width=100)
        tree_reviews.column("Type", anchor=tk.W, width=100)
        tree_reviews.column("Description", anchor=tk.W, width=150)
        tree_reviews.column("Rating", anchor=tk.W, width=100)

        tree_reviews.heading("ID", text="ID")
        tree_reviews.heading("Name", text="Name")
        tree_reviews.heading("Price", text="Price")
        tree_reviews.heading("Type", text="Type")
        tree_reviews.heading("Description", text="Description")
        tree_reviews.heading("Rating", text="Rating")

# ===== SEARCH TAB =====

# 8R -- Search food items from any establishment based on type
def search_food_items_bytype(type_entry, search_right_frame):
    food_type = type_entry.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
                        UPDATE food_item fi
                            SET foodItem_rating = (
                                SELECT AVG(rating)
                                FROM review
                                WHERE foodItem_id = fi.foodItem_id
                            );
                    """)
        query = """
        SELECT fi.foodItem_id, fi.foodItem_name, fi.foodItem_price, fi.foodItem_type, fi.foodItem_desc, fi.foodItem_rating, fe.foodEst_name
        FROM serves s
        JOIN food_item fi ON s.foodItem_id = fi.foodItem_id
        JOIN food_establishment fe ON s.foodEst_id = fe.foodEst_id
        WHERE fi.foodItem_type = %s
        """
        cursor.execute(query, (food_type,))
        records = cursor.fetchall()
        display_records(records, ["ID", "Name", "Price", "Type", "Description", "Rating", "Establishment"], search_right_frame)
        cursor.close()
        connection.close()

# 8R -- Search food items from any establishment based on a given price range
def search_food_items_byprice(price_min_entry, price_max_entry, search_right_frame):
    price_min = price_min_entry.get()
    price_max = price_max_entry.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
                        UPDATE food_item fi
                            SET foodItem_rating = (
                                SELECT AVG(rating)
                                FROM review
                                WHERE foodItem_id = fi.foodItem_id
                            );
                    """)
        query = """
        SELECT fi.foodItem_id, fi.foodItem_name, fi.foodItem_price, fi.foodItem_type, fi.foodItem_desc, fi.foodItem_rating, fe.foodEst_name
        FROM serves s
        JOIN food_item fi ON s.foodItem_id = fi.foodItem_id
        JOIN food_establishment fe ON s.foodEst_id = fe.foodEst_id
        WHERE fi.foodItem_price BETWEEN %s AND %s
        """
        cursor.execute(query, (price_min, price_max))
        records = cursor.fetchall()
        display_records(records, ["ID", "Name", "Price", "Type", "Description", "Rating", "Establishment"], search_right_frame)
        cursor.close()
        connection.close()

# 2F -- Search a food establishment
def search_food_establishments(food_est_entry, search_right_frame):
    # Get the food establishment name from the entry widget
    food_est = food_est_entry.get()

    # Connect to the database
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        
        # Execute the SQL query to retrieve food establishment records
        cursor.execute("SELECT foodEst_name, foodEst_loc, foodEst_type, foodEst_rating FROM food_establishment WHERE foodEst_name LIKE %s", (f'%{food_est}%',))
        records = cursor.fetchall()
        
        # Display the retrieved records in the search_right_frame
        display_records(records, ["Name", "Location", "Type", "Average Rating"], search_right_frame)
        
        cursor.close()
        connection.close()


# 2F -- Search a food item
def search_food_items(food_item_entry, search_right_frame):
    # Get the food item name from the entry widget
    food_item = food_item_entry.get()

    # Connect to the database
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT fi.foodItem_id, fi.foodItem_name, fi.foodItem_price, fi.foodItem_type, fi.foodItem_desc, fi.foodItem_rating, fe.foodEst_name 
            FROM food_item fi 
            JOIN food_establishment fe ON fi.foodEst_id = fe.foodEst_id 
            WHERE fi.foodItem_name LIKE %s
        """, (f'%{food_item}%',))
        records = cursor.fetchall()
        
        # Display the retrieved records in the search_right_frame
        display_records(records, ["ID", "Name", "Price", "Type", "Description", "Rating"], search_right_frame)
        
        cursor.close()
        connection.close()

# ===== ADD/UPDATE TAB =====
# Helper to fetch food establishments
def fetch_food_establishments():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT foodEst_id, foodEst_name, foodEst_loc, foodEst_type, foodEst_rating FROM food_establishment")
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records
    
# Helper to fetch food items
def fetch_food_items(est_id):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM food_item WHERE foodEst_id = %s;", (est_id,))
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records

#Helper to fetch food types
def fetch_food_types():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SHOW COLUMNS FROM food_item LIKE 'foodItem_type'")
    result = cursor.fetchone()[1]
    cursor.close()
    conn.close()
    food_types = result.replace("enum(", "").replace(")", "").replace("'", "").split(",")
    return food_types

# Helper to get food item reviews for a specific user
def get_food_reviews_by_user(userid):
    connection = connect_to_db()
    if connection: 
        cursor = connection.cursor()
        cursor.execute("""
            SELECT r.review_id, 
                   r.review_date, 
                   r.content, 
                   r.rating, 
                   fi.foodItem_name 
            FROM review r 
            LEFT JOIN food_item fi ON r.foodItem_id = fi.foodItem_id 
            WHERE r.userid = %s AND r.foodItem_id IS NOT NULL;
        """, (userid,))
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records

# Helper to get food establishment reviews for a specific user
def get_establishment_reviews_by_user(userid):
    connection = connect_to_db()
    if connection: 
        cursor = connection.cursor()
        cursor.execute("""
            SELECT r.review_id, 
                   r.review_date, 
                   r.content, 
                   r.rating, 
                   fe.foodEst_name 
            FROM review r 
            LEFT JOIN food_establishment fe ON r.foodEst_id = fe.foodEst_id
            WHERE r.userid = %s AND r.foodEst_id IS NOT NULL;
        """, (userid,))
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records
    
# 1F -- Add a food review on a food establishment or a food item
def make_review(userid, addupdate_right_frame):
    def choose_review_type():
        for widget in addupdate_right_frame.winfo_children():
            widget.destroy()
        choice = review_type.get()
        if choice == "Food Item":
            establishments = fetch_food_establishments()
            show_establishments(establishments, "Food Item")
        elif choice == "Establishment":
            establishments = fetch_food_establishments()
            show_establishments(establishments, "Establishment")

    def show_establishments(establishments, review_type):
        ttk.Label(addupdate_right_frame, text="Select Establishment:").grid(row=0, column=0, padx=10, pady=10)
        selected_est = tk.StringVar()
        ttk.Combobox(addupdate_right_frame, textvariable=selected_est, values=[f'{est[0]} - {est[1]}' for est in establishments]).grid(row=0, column=1, padx=10, pady=10)

        def next_step():
            selected_est_str = selected_est.get()
            est_id = selected_est_str.split(' - ')[0]
            if est_id:
                if review_type == "Food Item":
                    items = fetch_food_items(est_id)
                    show_review_form(items, "Food Item", selected_est_str)
                else:
                    show_review_form([est for est in establishments if est[0] == est_id], "Establishment", selected_est_str)

        ttk.Button(addupdate_right_frame, text="Next", command=next_step).grid(row=1, columnspan=2, pady=10)

    def show_review_form(items, review_type, est_name=None):
        for widget in addupdate_right_frame.winfo_children():
            widget.destroy()

        if review_type == "Food Item":
            ttk.Label(addupdate_right_frame, text="Select Food Item:").grid(row=0, column=0, padx=10, pady=10)
            selected_item = tk.StringVar()
            ttk.Combobox(addupdate_right_frame, textvariable=selected_item, values=[item[1] for item in items]).grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(addupdate_right_frame, text="Rating(1-5):").grid(row=1, column=0, padx=10, pady=10)
        rating_entry = ttk.Entry(addupdate_right_frame)
        rating_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(addupdate_right_frame, text="Content:").grid(row=2, column=0, padx=10, pady=10)
        content_entry = ttk.Entry(addupdate_right_frame)
        content_entry.grid(row=2, column=1, padx=10, pady=10)

        def submit_review():
            if review_type == "Food Item":
                selected_id = None
                for item in items:
                    if item[1] == selected_item.get():
                        selected_id = item[0]
                        break
                foodEst_id = None
                foodItem_id = selected_id
            else:
                selected_id = est_name.split(' - ')[0]
                foodEst_id = selected_id
                foodItem_id = None

            rating = rating_entry.get()
            content = content_entry.get()

            # Validate rating
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid rating between 1 and 5")
                return

            if selected_id and rating and content:
                connection = connect_to_db()
                if connection:
                    cursor = connection.cursor()
                    cursor.execute(
                        "INSERT INTO review (review_date, content, rating, userid, foodEst_id, foodItem_id) VALUES (CURDATE(), %s, %s, %s, %s, %s);",
                        (content, rating, userid, foodEst_id, foodItem_id)
                    )
                    connection.commit()
                    
                    # Get the last inserted review_id
                    review_id = cursor.lastrowid

                    if foodEst_id is not None:
                        cursor.execute("INSERT INTO reviews_foodest (foodEst_id, review_id) VALUES (%s, %s);", (foodEst_id, review_id))

                    if foodItem_id is not None:
                        cursor.execute("INSERT INTO reviews_fooditem (userid, foodItem_id) VALUES (%s, %s);", (userid, foodItem_id))

                    connection.commit()
                    cursor.close()
                    connection.close()
                messagebox.showinfo("Success", "Review submitted successfully")
            else:
                messagebox.showerror("Error", "Please fill all fields")

        ttk.Button(addupdate_right_frame, text="Submit", command=submit_review).grid(row=3, columnspan=2, pady=10)

    for widget in addupdate_right_frame.winfo_children():
        widget.destroy()

    review_type = tk.StringVar(value="Food Item")
    ttk.Radiobutton(addupdate_right_frame, text="Food Item", variable=review_type, value="Food Item").grid(row=0, column=0, padx=10, pady=10)
    ttk.Radiobutton(addupdate_right_frame, text="Establishment", variable=review_type, value="Establishment").grid(row=0, column=1, padx=10, pady=10)
    ttk.Button(addupdate_right_frame, text="Next", command=choose_review_type).grid(row=1, columnspan=2, pady=10)


# Update Helper
def update_review(review_id, new_content, new_rating):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE review 
            SET content = %s, rating = %s 
            WHERE review_id = %s
        """, (new_content, new_rating, review_id))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Food item updated successfully")

# 1F -- Update a food review on a food establishment or a food item
def update_own_review(userid, right_frame):
    food_records = get_food_reviews_by_user(userid)
    establishment_records = get_establishment_reviews_by_user(userid)

    # Clear right frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Create frames for food and establishment reviews
    review_frame = tk.Frame(right_frame)
    review_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    update_fields_frame = tk.Frame(right_frame)

    # Create a Treeview to display the food reviews
    tree_items = ttk.Treeview(review_frame)
    tree_items.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=5, pady=(5, 2))

    # Define columns for food reviews
    tree_items["columns"] = ("ID", "Date", "Content", "Rating", "Food Item")

    # Format columns for food reviews
    tree_items.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
    tree_items.column("ID", anchor=tk.W, width=50)
    tree_items.column("Date", anchor=tk.W, width=100)
    tree_items.column("Content", anchor=tk.W, width=400)
    tree_items.column("Rating", anchor=tk.W, width=50)
    tree_items.column("Food Item", anchor=tk.W, width=200)

    # Create headings for food reviews
    tree_items.heading("ID", text="ID")
    tree_items.heading("Date", text="Date")
    tree_items.heading("Content", text="Content")
    tree_items.heading("Rating", text="Rating")
    tree_items.heading("Food Item", text="Food Item")

    # Add food review records to the Treeview
    for record in food_records:
        tree_items.insert("", tk.END, values=record)

    # Create a Treeview to display the establishment reviews
    tree_establishments = ttk.Treeview(review_frame)
    tree_establishments.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, padx=5, pady=(2, 5))

    # Define columns for establishment reviews
    tree_establishments["columns"] = ("ID", "Date", "Content", "Rating", "Establishment")

    # Format columns for establishment reviews
    tree_establishments.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
    tree_establishments.column("ID", anchor=tk.W, width=50)
    tree_establishments.column("Date", anchor=tk.W, width=100)
    tree_establishments.column("Content", anchor=tk.W, width=400)
    tree_establishments.column("Rating", anchor=tk.W, width=50)
    tree_establishments.column("Establishment", anchor=tk.W, width=200)

    # Create headings for establishment reviews
    tree_establishments.heading("ID", text="ID")
    tree_establishments.heading("Date", text="Date")
    tree_establishments.heading("Content", text="Content")
    tree_establishments.heading("Rating", text="Rating")
    tree_establishments.heading("Establishment", text="Establishment")

    # Add establishment review records to the Treeview
    for record in establishment_records:
        tree_establishments.insert("", tk.END, values=record)

    def on_item_double_click(event, tree, is_food):
        selected_item = tree.selection()
        if not selected_item:
            return
        selected_item = selected_item[0]
        values = tree.item(selected_item, "values")
        review_id = values[0]
        current_content = values[2]
        current_rating = values[3]

        # Clear update_fields_frame
        for widget in update_fields_frame.winfo_children():
            widget.destroy()

        ttk.Label(update_fields_frame, text=f"Update Review {review_id}").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(update_fields_frame, text="Rating(1-5):").grid(row=1, column=0, padx=10, pady=10)
        rating_entry = ttk.Entry(update_fields_frame)
        rating_entry.grid(row=1, column=1, padx=10, pady=10)
        rating_entry.insert(0, current_rating)

        ttk.Label(update_fields_frame, text="Content:").grid(row=2, column=0, padx=10, pady=10)
        content_entry = ttk.Entry(update_fields_frame)
        content_entry.grid(row=2, column=1, padx=10, pady=10)
        content_entry.insert(0, current_content)

        def save_review():
            new_rating = rating_entry.get()
            new_content = content_entry.get()
            
            # Validate rating
            try:
                new_rating = int(new_rating)
                if new_rating < 1 or new_rating > 5:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid rating between 1 and 5")
                return

            update_review(review_id, new_content, new_rating)

            # Refresh the Treeview
            tree.item(selected_item, values=(review_id, values[1], new_content, new_rating, values[4]))

        ttk.Button(update_fields_frame, text="Save", command=save_review).grid(row=3, column=0, columnspan=2, pady=10)

        # Pack the update_fields_frame on the right side when an item is selected
        update_fields_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Bind double-click event to the Treeview for food reviews
    tree_items.bind("<Double-1>", lambda event: on_item_double_click(event, tree_items, True))

    # Bind double-click event to the Treeview for establishment reviews
    tree_establishments.bind("<Double-1>", lambda event: on_item_double_click(event, tree_establishments, False))

# Delete Helper
def delete_review(review_id):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM review
            WHERE review_id = %s
        """, (review_id,))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Review deleted successfully")

# 1F -- Delete a food review on a food establishment or a food item
def delete_own_review(userid, right_frame):
    records = get_food_reviews_by_user(userid)

    # Clear right frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Create a frame for the review deletion
    delete_frame = tk.Frame(right_frame)
    delete_frame.pack(expand=True, fill=tk.BOTH)

    # Create a Treeview to display the records
    tree = ttk.Treeview(delete_frame)
    tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    # Define columns
    tree["columns"] = ("ID", "Date", "Content", "Rating", "Item/Establishment")

    # Format columns
    tree.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
    tree.column("ID", anchor=tk.W, width=50)
    tree.column("Date", anchor=tk.W, width=100)
    tree.column("Content", anchor=tk.W, width=200)
    tree.column("Rating", anchor=tk.W, width=50)
    tree.column("Item/Establishment", anchor=tk.W, width=100)

    # Create headings
    tree.heading("ID", text="ID")
    tree.heading("Date", text="Date")
    tree.heading("Content", text="Content")
    tree.heading("Rating", text="Rating")
    tree.heading("Item/Establishment", text="Item/Establishment")

    # Add records to the Treeview
    for record in records:
        tree.insert("", tk.END, values=record)

    def on_double_click(event):
        selected_item = tree.selection()
        if not selected_item:
            return
        selected_item = selected_item[0]
        values = tree.item(selected_item, "values")
        review_id = values[0]
        current_content = values[2]
        current_rating = values[3]

        def delete_review_record():
            confirmed = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this review?")
            if confirmed:
                delete_review(review_id)
                tree.delete(selected_item)

        # Call the delete_review_record function
        delete_review_record()

    # Bind double-click event to the Treeview
    tree.bind("<Double-1>", on_double_click)

# 2F - Add a food establishment
def add_food_establishment_form(right_frame):
    def fetch_food_types():
        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SHOW COLUMNS FROM food_establishment LIKE 'foodEst_type'")
                result = cursor.fetchone()[1]
                food_types = result.replace("enum(", "").replace(")", "").replace("'", "").split(",")
                return food_types
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to fetch food types: {e}")
            finally:
                connection.close()
        return []

    def add_food_establishment():
        name = est_name_entry.get()
        location = est_location_entry.get()
        type_ = est_type_combobox.get()
        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO food_establishment (foodEst_name, foodEst_loc, foodEst_type) VALUES (%s, %s, %s)", (name, location, type_))
                connection.commit()
                cursor.close()
                messagebox.showinfo("Success", "Food establishment added successfully")
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to add food establishment: {e}")
            finally:
                connection.close()

    # Clear the right_frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Fetch food types
    food_types = fetch_food_types()

    # Create input fields and labels in the right_frame
    tk.Label(right_frame, text="Food Establishment Name:").grid(row=0, column=0, padx=10, pady=10)
    est_name_entry = tk.Entry(right_frame)
    est_name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(right_frame, text="Location:").grid(row=1, column=0, padx=10, pady=10)
    est_location_entry = tk.Entry(right_frame)
    est_location_entry.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(right_frame, text="Estab Type:").grid(row=2, column=0, padx=10, pady=10)
    selected_est_type = tk.StringVar()
    est_type_combobox = ttk.Combobox(right_frame, textvariable=selected_est_type, values=food_types)
    est_type_combobox.grid(row=2, column=1, padx=10, pady=10)

    add_button = tk.Button(right_frame, text="Add Food Establishment", command=add_food_establishment)
    add_button.grid(row=3, columnspan=2, pady=20)

# 2F -- Delete a food establishment
def delete_food_establishment(right_frame):
    # Clear the right_frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Create a new Treeview to display items
    tree_items = ttk.Treeview(right_frame)
    tree_items.pack(expand=True, fill=tk.BOTH)

    # Define columns for items
    tree_items["columns"] = ("ID", "Name", "Location", "Type", "Rating")

    # Format columns for items
    tree_items.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
    tree_items.column("ID", anchor=tk.W, width=50)
    tree_items.column("Name", anchor=tk.W, width=100)
    tree_items.column("Location", anchor=tk.W, width=100)
    tree_items.column("Type", anchor=tk.W, width=100)
    tree_items.column("Rating", anchor=tk.W, width=100)

    # Create headings for items
    tree_items.heading("ID", text="ID")
    tree_items.heading("Name", text="Name")
    tree_items.heading("Location", text="Location")
    tree_items.heading("Type", text="Type")
    tree_items.heading("Rating", text="Rating")

    # Function to populate the TreeView with food establishments
    def populate_tree():
        # Clear previous items
        for child in tree_items.get_children():
            tree_items.delete(child)

        # Fetch and display food establishments
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT foodEst_id, foodEst_name, foodEst_loc, foodEst_type, foodEst_rating FROM food_establishment")
            items = cursor.fetchall()
            cursor.close()
            connection.close()

            # Add items to the Treeview
            for item in items:
                tree_items.insert("", tk.END, values=item)

    # Function to handle the deletion of a food establishment
    def delete_food_est():
        selected_item = tree_items.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a food establishment to delete.")
            return

        selected_item = selected_item[0]
        values = tree_items.item(selected_item, "values")
        food_est_id = values[0]

        confirmed = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the food establishment '{values[1]}'?")
        if confirmed:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor()
                try:
                    # Delete related entries in the review table first
                    cursor.execute("DELETE FROM review WHERE foodItem_id IN (SELECT foodItem_id FROM food_item WHERE foodEst_id = %s)", (food_est_id,))
                    cursor.execute("DELETE FROM review WHERE foodEst_id = %s", (food_est_id,))
                    # Delete related entries in other tables
                    cursor.execute("DELETE FROM serves WHERE foodEst_id = %s", (food_est_id,))
                    cursor.execute("DELETE FROM food_item WHERE foodEst_id = %s", (food_est_id,))
                    cursor.execute("DELETE FROM food_establishment WHERE foodEst_id = %s", (food_est_id,))
                    connection.commit()
                    tree_items.delete(selected_item)
                    messagebox.showinfo("Success", "Food establishment deleted successfully.")
                except mysql.connector.Error as err:
                    connection.rollback()
                    messagebox.showerror("Error", f"Error deleting food establishment: {err}")
                finally:
                    cursor.close()
                    connection.close()

    # Populate the TreeView initially
    populate_tree()

    # Bind double-click event to delete the selected food establishment
    tree_items.bind("<Double-1>", lambda event: delete_food_est())

# 2F -- Update a food establishment
def update_food_establishment(right_frame):
    # Clear the right_frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT foodEst_id, foodEst_name, foodEst_loc, foodEst_type FROM food_establishment")
        establishments = cursor.fetchall()
        cursor.execute("SHOW COLUMNS FROM food_establishment LIKE 'foodEst_type'")
        result = cursor.fetchone()[1]
        cursor.close()
        connection.close() 
    
        food_types = result.replace("enum(", "").replace(")", "").replace("'", "").split(",")

    # Establishments Dropdown
    tk.Label(right_frame, text="Select Establishment:").grid(row=0, column=0, padx=10, pady=5)
    establishment_var = tk.StringVar()
    establishment_dropdown = ttk.Combobox(right_frame, textvariable=establishment_var)
    establishment_dropdown['values'] = [f"{est[0]} - {est[1]}" for est in establishments]
    establishment_dropdown.grid(row=0, column=1, padx=10, pady=5)
    
    # Name Entry
    tk.Label(right_frame, text="Name:").grid(row=1, column=0, padx=10, pady=5)
    name_entry = tk.Entry(right_frame)
    name_entry.grid(row=1, column=1, padx=10, pady=5)
    
    # Location Entry
    tk.Label(right_frame, text="Location:").grid(row=2, column=0, padx=10, pady=5)
    location_entry = tk.Entry(right_frame)
    location_entry.grid(row=2, column=1, padx=10, pady=5)
    
    # Type Dropdown
    tk.Label(right_frame, text="Type:").grid(row=3, column=0, padx=10, pady=5)
    type_var = tk.StringVar()
    type_dropdown = ttk.Combobox(right_frame, textvariable=type_var)
    type_dropdown['values'] = food_types
    type_dropdown.grid(row=3, column=1, padx=10, pady=5)

    def on_establishment_select(event, establishment_var, name_entry, location_entry, type_var, establishments):
        selected_establishment = establishment_var.get()
        est_id = int(selected_establishment.split(' - ')[0])
        for est in establishments:
            if est[0] == est_id:
                name_entry.delete(0, tk.END)
                name_entry.insert(0, est[1])
                location_entry.delete(0, tk.END)
                location_entry.insert(0, est[2])
                type_var.set(est[3])
                break
    
    # Bind the selection event to update other text boxes
    establishment_dropdown.bind("<<ComboboxSelected>>", lambda event: on_establishment_select(event, establishment_var, name_entry, location_entry, type_var, establishments))

    def update_entry(establishment_var, name_entry, location_entry, type_var, establishments):
        selected_establishment = establishment_var.get()
        est_id = int(selected_establishment.split(' - ')[0])
        for est in establishments:
            if est[0] == est_id:
                name = name_entry.get()
                location = location_entry.get()
                type_ = type_var.get()

                connection = connect_to_db()
                if connection:
                    cursor = connection.cursor()
                    cursor.execute("UPDATE food_establishment SET foodEst_name = %s, foodEst_loc = %s, foodEst_type = %s WHERE foodEst_id = %s", (name, location, type_, est_id))
                    connection.commit()
                    cursor.close()
                    connection.close() 
                
                # Print or perform the actual update operation here
                print(f"Updating: {selected_establishment}, Name: {name}, Location: {location}, Type: {type_}")
                break
    
    # Submit Button
    submit_button = tk.Button(right_frame, text="Update", command=lambda: update_entry(establishment_var, name_entry, location_entry, type_var, establishments))
    submit_button.grid(row=4, column=0, columnspan=2, pady=10)


# 3F -- Add a food item
def add_food_item_form(right_frame):
    establishments = fetch_food_establishments()
    food_types = fetch_food_types()

    def add_food_item():
        name = item_name_entry.get()
        price = item_price_entry.get()
        type_ = item_type_combobox.get()
        desc = item_desc_entry.get()
        # Extracting the ID of the selected establishment
        est_id = item_estid_combobox.get().split(',')[0]
        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO food_item (foodItem_name, foodItem_price, foodItem_type, foodItem_desc, foodEst_id) VALUES (%s, %s, %s, %s, %s)",
                    (name, price, type_, desc, est_id)
                )
                cursor.execute(
                    """
                    INSERT INTO serves (foodEst_id, foodItem_id)
                    VALUES (%s, (SELECT foodItem_id FROM food_item WHERE foodItem_name = %s))
                    """, (est_id, name)
                )
                connection.commit()
                cursor.close()
                messagebox.showinfo("Success", "Food item added successfully")
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to add food item: {e}")
            finally:
                connection.close()

    # Clear the right_frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Create input fields and labels in the right_frame
    tk.Label(right_frame, text="Food Item Name:").grid(row=0, column=0, padx=10, pady=10)
    item_name_entry = tk.Entry(right_frame)
    item_name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(right_frame, text="Price:").grid(row=1, column=0, padx=10, pady=10)
    item_price_entry = tk.Entry(right_frame)
    item_price_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(right_frame, text="Type:").grid(row=2, column=0, padx=10, pady=10)
    item_type_combobox = ttk.Combobox(right_frame, values=food_types)
    item_type_combobox.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(right_frame, text="Description:").grid(row=3, column=0, padx=10, pady=10)
    item_desc_entry = tk.Entry(right_frame)
    item_desc_entry.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(right_frame, text="Establishment:").grid(row=4, column=0, padx=10, pady=10)
    item_estid_combobox = ttk.Combobox(right_frame, values=[f'{est[0]}, {est[1]}' for est in establishments])
    item_estid_combobox.grid(row=4, column=1, padx=10, pady=10)

    add_button = tk.Button(right_frame, text="Add Food Item", command=add_food_item)
    add_button.grid(row=5, columnspan=2, pady=20)

# 3F -- Delete a food item
def delete_food_item(right_frame):
    # Clear the right_frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Create a new Treeview to display items
    tree_items = ttk.Treeview(right_frame)
    tree_items.pack(expand=True, fill=tk.BOTH)

    # Define columns for items
    tree_items["columns"] = ("ID", "Name", "Price", "Type", "Description", "Rating")

    # Format columns for items
    tree_items.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
    tree_items.column("ID", anchor=tk.W, width=50)
    tree_items.column("Name", anchor=tk.W, width=100)
    tree_items.column("Price", anchor=tk.W, width=100)
    tree_items.column("Type", anchor=tk.W, width=100)
    tree_items.column("Description", anchor=tk.W, width=150)
    tree_items.column("Rating", anchor=tk.W, width=100)

    # Create headings for items
    tree_items.heading("ID", text="ID")
    tree_items.heading("Name", text="Name")
    tree_items.heading("Price", text="Price")
    tree_items.heading("Type", text="Type")
    tree_items.heading("Description", text="Description")
    tree_items.heading("Rating", text="Rating")

    # Function to populate the TreeView with food items
    def populate_tree():
        # Clear previous items
        for child in tree_items.get_children():
            tree_items.delete(child)

        # Fetch and display food items
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE food_item fi
                SET foodItem_rating = (
                    SELECT AVG(rating)
                    FROM review
                    WHERE foodItem_id = fi.foodItem_id
                );
            """)
            cursor.execute("""
                SELECT 
                    fi.foodItem_id, 
                    fi.foodItem_name, 
                    fi.foodItem_price, 
                    fi.foodItem_type, 
                    fi.foodItem_desc, 
                    fi.foodItem_rating
                FROM food_item fi
            """)
            items = cursor.fetchall()
            cursor.close()
            connection.close()

            # Add items to the Treeview
            for item in items:
                tree_items.insert("", tk.END, values=item)

    # Function to handle the deletion of a food item
    def delete_food_item():
        selected_item = tree_items.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a food item to delete.")
            return

        selected_item = selected_item[0]
        values = tree_items.item(selected_item, "values")
        food_item_id = values[0]

        confirmed = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the food item '{values[1]}'?")
        if confirmed:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor()
                try:
                    # Delete associated reviews first
                    cursor.execute("DELETE FROM review WHERE foodItem_id = %s", (food_item_id,))
                    # Delete associated entries in the serves table
                    cursor.execute("DELETE FROM serves WHERE foodItem_id = %s", (food_item_id,))
                    # Then delete the food item
                    cursor.execute("DELETE FROM food_item WHERE foodItem_id = %s", (food_item_id,))
                    connection.commit()
                    tree_items.delete(selected_item)
                    messagebox.showinfo("Success", "Food item deleted successfully.")
                except mysql.connector.Error as err:
                    connection.rollback()
                    messagebox.showerror("Error", f"Error deleting food item: {err}")
                finally:
                    cursor.close()
                    connection.close()

    # Populate the TreeView initially
    populate_tree()

    # Bind double-click event to delete the selected food item
    tree_items.bind("<Double-1>", lambda event: delete_food_item())

# 3F -- Update a food item
def update_food_item(right_frame):
    # Clear the right_frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Function to fetch establishments from the database
    def fetch_establishments():
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT foodEst_id, foodEst_name FROM food_establishment")
        establishments = cursor.fetchall()
        cursor.close()
        conn.close()
        return establishments
    
    # Function to fetch food items from the database for a given establishment
    def fetch_food_items(establishment_id):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT foodItem_id, foodItem_name, foodItem_price, foodItem_type, foodItem_desc FROM food_item WHERE foodEst_id = %s", (establishment_id,))
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return items
    
    # Function to fetch food types from the database
    def fetch_food_types():
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SHOW COLUMNS FROM food_item LIKE 'foodItem_type'")
        result = cursor.fetchone()[1]
        cursor.close()
        conn.close()
        food_types = result.replace("enum(", "").replace(")", "").replace("'", "").split(",")
        return food_types

    establishments = fetch_establishments()
    food_types = fetch_food_types()

    # Establishments Dropdown
    tk.Label(right_frame, text="Select Establishment:").grid(row=0, column=0, padx=10, pady=5)
    establishment_var = tk.StringVar()
    establishment_dropdown = ttk.Combobox(right_frame, textvariable=establishment_var)
    establishment_dropdown['values'] = [f"{est[0]} - {est[1]}" for est in establishments]
    establishment_dropdown.grid(row=0, column=1, padx=10, pady=5)
    
    # Items Dropdown
    tk.Label(right_frame, text="Select Food Item:").grid(row=1, column=0, padx=10, pady=5)
    item_var = tk.StringVar()
    item_dropdown = ttk.Combobox(right_frame, textvariable=item_var)
    item_dropdown.grid(row=1, column=1, padx=10, pady=5)

    # Function to handle selection of a food item
    def on_item_select(event, item_var, name_entry, price_entry, type_var, description_text, items):
        selected_item = item_var.get()
        item_id = int(selected_item.split(' - ')[0])
        for item in items:
            if item[0] == item_id:
                name_entry.delete(0, tk.END)
                name_entry.insert(0, item[1])
                price_entry.delete(0, tk.END)
                price_entry.insert(0, item[2])
                type_var.set(item[3])
                description_text.delete(1.0, tk.END)
                description_text.insert(tk.END, item[4])
                break

    # Function to handle selection of an establishment
    def on_establishment_select(event, establishment_var, item_var, name_entry, price_entry, type_var, description_text, item_dropdown):
        selected_establishment = establishment_var.get()
        est_id = int(selected_establishment.split(' - ')[0])
        items = fetch_food_items(est_id)
        item_dropdown['values'] = [f"{item[0]} - {item[1]}" for item in items]
        item_dropdown.bind("<<ComboboxSelected>>", lambda event: on_item_select(event, item_var, name_entry, price_entry, type_var, description_text, items))
    
    # Bind the selection event to update item dropdown
    establishment_dropdown.bind("<<ComboboxSelected>>", lambda event: on_establishment_select(event, establishment_var, item_var, name_entry, price_entry, type_var, description_text, item_dropdown))
    
    # Name Entry
    tk.Label(right_frame, text="Name:").grid(row=2, column=0, padx=10, pady=5)
    name_entry = tk.Entry(right_frame)
    name_entry.grid(row=2, column=1, padx=10, pady=5)
    
    # Price Entry
    tk.Label(right_frame, text="Price:").grid(row=3, column=0, padx=10, pady=5)
    price_entry = tk.Entry(right_frame)
    price_entry.grid(row=3, column=1, padx=10, pady=5)
    
    # Type Dropdown
    tk.Label(right_frame, text="Type:").grid(row=4, column=0, padx=10, pady=5)
    type_var = tk.StringVar()
    type_dropdown = ttk.Combobox(right_frame, textvariable=type_var)
    type_dropdown['values'] = food_types
    type_dropdown.grid(row=4, column=1, padx=10, pady=5)

    # Description Entry (using tk.Text for a larger input area)
    tk.Label(right_frame, text="Description:").grid(row=5, column=0, padx=10, pady=5)
    description_text = tk.Text(right_frame, height=6, width=40)
    description_text.grid(row=5, column=1, padx=10, pady=5)

    def update_entry(establishment_var, item_var, name_entry, price_entry, type_var, description_text):
        selected_item = item_var.get()
        item_id = int(selected_item.split(' - ')[0])
        name = name_entry.get()
        price = price_entry.get()
        type_ = type_var.get()
        description = description_text.get(1.0, tk.END).strip()

        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE food_item SET foodItem_name = %s, foodItem_price = %s, foodItem_type = %s, foodItem_desc = %s WHERE foodItem_id = %s", (name, price, type_, description, item_id))
            connection.commit()
            cursor.close()
            connection.close() 
        
        # Print or perform the actual update operation here
        print(f"Updating: {selected_item}, Name: {name}, Price: {price}, Type: {type_}, Description: {description}")
    
    # Submit Button
    submit_button = tk.Button(right_frame, text="Update", command=lambda: update_entry(establishment_var, item_var, name_entry, price_entry, type_var, description_text))
    submit_button.grid(row=6, column=0, columnspan=2, pady=10)



# USER LOGIN PAGE
def login():
    def check_credentials():
        username = username_entry.get()
        password = password_entry.get()
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT userid FROM users WHERE username = %s AND userpassword = %s;", (username, password))
            result = cursor.fetchone()
            if result:
                userid = result[0]
                login_window.destroy()
                show_main_app(userid)
            else:
                messagebox.showerror("Error", "Invalid username or password")
            cursor.close()
            connection.close()
        else:
            messagebox.showerror("Error", "Database connection failed")

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.configure(bg="#EAE2B7")

    # Initial size
    initial_width = 1280
    initial_height = 720

    # Frame to hold the login window with border radius
    container_frame = tk.Frame(login_window)
    container_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Header frame with application name
    header_frame = tk.Frame(container_frame, bg='#003049')
    header_frame.pack(side=tk.TOP, fill=tk.X)

    header_label = tk.Label(header_frame, text="querview", bg='#003049', fg='#EAE2B7', font=('Arial', 24))
    header_label.pack(pady=10)

    # Create a frame for the login form
    login_frame = ttk.Frame(container_frame, padding="20 20 20 20", style="Container.TFrame")
    login_frame.pack(expand=True, fill=tk.BOTH)

    # Create and place the widgets within the frame
    ttk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    username_entry = ttk.Entry(login_frame, width=40, style="Thick.TEntry")
    username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = ttk.Entry(login_frame, show="*", width=40, style="Thick.TEntry")  
    password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    style = ttk.Style()
    style.configure("List.TButton", relief="flat", foreground="#003049", padding=10) 
    style.configure("Thick.TEntry", padding=10) 
    style.configure("Container.TFrame", borderwidth=2, relief=tk.SOLID, bordercolor="#003049")

    # Fixed width for all buttons
    button_width = 20

    ttk.Button(login_frame, text="Login", command=check_credentials, style="List.TButton", width=button_width).grid(row=2, column=1, columnspan=2, pady=20)

    login_window.geometry(f"{initial_width}x{initial_height}")
    login_window.mainloop()

# Function to display records in a frame on the right side of the main window
def display_records(records, columns, view_right_frame):
    for widget in view_right_frame.winfo_children():
        widget.destroy()

    global tree
    tree = ttk.Treeview(view_right_frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')
    for record in records:
        tree.insert('', tk.END, values=record)
    tree.pack(fill=tk.BOTH, expand=True)


# MAIN APP
def show_main_app(userid):
    # Main application
    root = tk.Tk()
    root.title("querview")

    # Initial size
    initial_width = 1280
    initial_height = 720
    root.geometry(f"{initial_width}x{initial_height}")

    # Header frame with application name
    header_frame = tk.Frame(root, bg='#003049')
    header_frame.pack(side=tk.TOP, fill=tk.X)

    header_label = tk.Label(header_frame, text="querview", bg='#003049', fg='#EAE2B7', font=('Arial', 24))
    header_label.pack(pady=10)

    style = ttk.Style()
    style.configure("TNotebook.Tab", background="#c0c0c0", foreground="black", padding=[10, 5]) 
    style.map("TNotebook.Tab", foreground=[("selected", "#003049")])  

    tab_control = ttk.Notebook(root)
    tab_control.pack(expand=1, fill="both")
    view_tab = ttk.Frame(tab_control)
    add_update_tab = ttk.Frame(tab_control)
    search_tab = ttk.Frame(tab_control)

    tab_control.add(view_tab, text='View')
    tab_control.add(add_update_tab, text='Add/Update')
    tab_control.add(search_tab, text='Search')

    # ===== VIEW TAB ======
    view_left_frame = tk.Frame(view_tab)
    view_left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    style = ttk.Style()
    style.configure("List.TButton", relief="flat", background="#f0f0f0", padding=10, borderwidth=0, bordercolor="#003049")

    # fixed width for all buttons
    button_width = 50

    # 1R
    view_button = ttk.Button(view_left_frame, text="View Food Establishments", command=lambda: view_food_establishments(view_right_frame), style="List.TButton", width=button_width)
    view_button.pack(pady=2, anchor="w", padx=1)

    # 2R
    view_reviews_button = ttk.Button(view_left_frame, text="View Reviews for Establishment", command=lambda: view_reviews_establishment(view_right_frame), style="List.TButton", width=button_width)
    view_reviews_button.pack(pady=2, anchor="w", padx=1)

    view_reviews_food_button = ttk.Button(view_left_frame, text="View Reviews for Food Item", command=lambda: view_reviews_food(view_right_frame), style="List.TButton", width=button_width)
    view_reviews_food_button.pack(pady=2, anchor="w", padx=1)

    # 3R
    view_items_from_estab_button = ttk.Button(view_left_frame, text="View Items from Establishment", command=lambda: view_items_from_estab(view_right_frame), style="List.TButton", width=button_width)
    view_items_from_estab_button.pack(pady=2, anchor="w", padx=1)

    # 4R
    view_food_items_from_type_btn = ttk.Button(view_left_frame, text="View Food Items based on Type", command=lambda: view_items_from_type(view_right_frame), style="List.TButton", width=button_width)
    view_food_items_from_type_btn.pack(pady=2, anchor="w", padx=1)

    # 5R
    view_reviews_month_estab_btn = ttk.Button(view_left_frame, text="View Reviews for Food Establishments in the past month", command=lambda: view_reviews_establishment_month(view_right_frame), style="List.TButton", width=button_width)
    view_reviews_month_estab_btn.pack(pady=2, anchor="w", padx=1)

    view_reviews_month_food_btn = ttk.Button(view_left_frame, text="View Reviews for Food Items in the past month", command=lambda: view_reviews_food_month(view_right_frame), style="List.TButton", width=button_width)
    view_reviews_month_food_btn.pack(pady=2, anchor="w", padx=1)

    # 6R 
    view_estab_high_rating_btn = ttk.Button(view_left_frame, text="View Establishments with high rating", command=lambda: view_estab_high_rating(view_right_frame), style="List.TButton", width=button_width)
    view_estab_high_rating_btn.pack(pady=2, anchor="w", padx=1)

    # 7R
    view_food_by_price = ttk.Button(view_left_frame, text="View Food Items sorted by price", command=lambda: view_items_by_price(view_right_frame), style="List.TButton", width=button_width)
    view_food_by_price.pack(pady=2, anchor="w", padx=1)

    view_right_frame = tk.Frame(view_tab)
    view_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Right frame with an empty Treeview
    tree = ttk.Treeview(view_right_frame, show='headings')
    tree.pack(fill=tk.BOTH, expand=True)

    # ===== ADD OR UPDATE TAB =====
    addupdate_left_frame = tk.Frame(add_update_tab)
    addupdate_left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # Buttons in the left frame
    button_width = 30

    # 1F
    make_review_btn = ttk.Button(addupdate_left_frame, text="Make a Review", command=lambda: make_review(userid, addupdate_right_frame), style="List.TButton", width=button_width)
    make_review_btn.pack(pady=2, anchor="w", padx=1)

    update_review_btn = ttk.Button(addupdate_left_frame, text="Update a Review", command=lambda: update_own_review(userid, addupdate_right_frame), style="List.TButton", width=button_width)
    update_review_btn.pack(pady=2, anchor="w", padx=1)

    delete_review_btn = ttk.Button(addupdate_left_frame, text="Delete a Review", command=lambda: delete_own_review(userid, addupdate_right_frame), style="List.TButton", width=button_width)
    delete_review_btn.pack(pady=2, anchor="w", padx=1)

    # 2F
    add_est_btn = ttk.Button(addupdate_left_frame, text="Add a Food Establishment", command=lambda: add_food_establishment_form(addupdate_right_frame), style="List.TButton", width=button_width)
    add_est_btn.pack(pady=2, anchor="w", padx=1)

    delete_est_btn = ttk.Button(addupdate_left_frame, text="Delete a Food Establishment", command=lambda: delete_food_establishment(addupdate_right_frame), style="List.TButton", width=button_width)
    delete_est_btn.pack(pady=2, anchor="w", padx=1)

    update_est_btn = ttk.Button(addupdate_left_frame, text="Update a Food Establishment", command=lambda: update_food_establishment(addupdate_right_frame), style="List.TButton", width=button_width)
    update_est_btn.pack(pady=2, anchor="w", padx=1)

    # 3F
    add_item_btn = ttk.Button(addupdate_left_frame, text="Add a Food Item", command=lambda: add_food_item_form(addupdate_right_frame), style="List.TButton", width=button_width)
    add_item_btn.pack(pady=2, anchor="w", padx=1)

    delete_item_btn = ttk.Button(addupdate_left_frame, text="Delete a Food Item", command=lambda: delete_food_item(addupdate_right_frame), style="List.TButton", width=button_width)
    delete_item_btn.pack(pady=2, anchor="w", padx=1)

    update_item_btn = ttk.Button(addupdate_left_frame, text="Update a Food Item", command=lambda: update_food_item(addupdate_right_frame), style="List.TButton", width=button_width)
    update_item_btn.pack(pady=2, anchor="w", padx=1)

    addupdate_right_frame = tk.Frame(add_update_tab)
    addupdate_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Right frame with an empty Treeview
    tree = ttk.Treeview(addupdate_right_frame, show='headings')
    tree.pack(fill=tk.BOTH, expand=True)

    # ====== SEARCH TAB ======
    style = ttk.Style()
    style.configure("Search.TButton", padding=6)
    style.configure("Search.TEntry", padding=(10, 10))
    style.configure("TEntry", font=("Helvetica", 14)) 

    search_left_frame = ttk.LabelFrame(search_tab, text="Search Food Items or Establishments")
    search_left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # 8F
    ttk.Label(search_left_frame, text="Food Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    type_entry = ttk.Entry(search_left_frame, width=20, style="Search.TEntry")
    type_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    ttk.Button(search_left_frame, text="Search by Type", command=lambda:search_food_items_bytype(type_entry, search_right_frame), style="List.TButton", width=40).grid(row=1, columnspan=2)

    # 8F
    ttk.Label(search_left_frame, text="Min Price:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    price_min_entry = ttk.Entry(search_left_frame, width=20, style="Search.TEntry")
    price_min_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    ttk.Label(search_left_frame, text="Max Price:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    price_max_entry = ttk.Entry(search_left_frame, width=20, style="Search.TEntry")
    price_max_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
    ttk.Button(search_left_frame, text="Search by Price", command=lambda:search_food_items_byprice(price_min_entry, price_max_entry, search_right_frame), style="List.TButton", width=40).grid(row=4, columnspan=2)

    # 2F
    ttk.Label(search_left_frame, text="Food Establisment:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
    food_est_entry = ttk.Entry(search_left_frame, width=20, style="Search.TEntry")
    food_est_entry.grid(row=5, column=1, padx=10, pady=10, sticky="ew")
    ttk.Button(search_left_frame, text="Search by Establishment", command=lambda:search_food_establishments(food_est_entry, search_right_frame), style="List.TButton", width=40).grid(row=6, columnspan=2)

    # 3F
    ttk.Label(search_left_frame, text="Food Item:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
    food_item_entry = ttk.Entry(search_left_frame, width=20, style="Search.TEntry")
    food_item_entry.grid(row=7, column=1, padx=10, pady=10, sticky="ew")
    ttk.Button(search_left_frame, text="Search by Food Item", command=lambda:search_food_items(food_item_entry, search_right_frame), style="List.TButton", width=40).grid(row=8, columnspan=2)

    search_right_frame = tk.Frame(search_tab)
    search_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    root.mainloop()

login()

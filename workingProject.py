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
            password='052508' # replace ng password niyo 
        )
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror("Error", f"Error connecting to MySQL: {e}")
        return None


# 1
# Function to view all food establishments
def view_food_establishments():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT foodEst_name, foodEst_loc, foodEst_type, foodEst_rating FROM food_establishment")
        records = cursor.fetchall()
        display_records(records, ["Name", "Location", "Type", "Average Rating"])
        cursor.close()
        connection.close()

# 2
# Function to view all reviews for an establishment
def view_reviews_establishment():
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

        # Create a Tkinter window
        root = tk.Tk()
        root.title("Food Establishments")

        # Create a Treeview to display the records
        tree = ttk.Treeview(root)
        tree.pack(expand=True, fill=tk.BOTH)

        # Define columns
        tree["columns"] = ("ID", "Name", "Location", "Type", "Rating")

        # Format columns
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

                    # Add reviews to the Treeview for reviews
                    for review in reviews:
                        tree_reviews.insert("", tk.END, values=review)

        # Bind the selection event to the function
        tree.bind("<ButtonRelease-1>", on_select)

        # Create a new Treeview to display reviews
        tree_reviews = ttk.Treeview(root)
        tree_reviews.pack(expand=True, fill=tk.BOTH)

        # Define columns for reviews
        tree_reviews["columns"] = ("Review date", "Content", "Rating")

        # Format columns for reviews
        tree_reviews.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree_reviews.column("Review date", anchor=tk.W, width=100)
        tree_reviews.column("Content", anchor=tk.W, width=250)
        tree_reviews.column("Rating", anchor=tk.W, width=100)

        # Create headings for reviews
        tree_reviews.heading("Review date", text="Review date")
        tree_reviews.heading("Content", text="Content")
        tree_reviews.heading("Rating", text="Rating")

        root.mainloop()

# 2
# Function to view all reviews for a food item
def view_reviews_food():
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

        # Create a Tkinter window
        root = tk.Tk()
        root.title("Food Establishments")

        # Create a Treeview to display the records
        tree = ttk.Treeview(root)
        tree.pack(expand=True, fill=tk.BOTH)

        # Define columns
        tree["columns"] = ("ID", "Name", "Location", "Type", "Rating")

        # Format columns
        tree.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree.column("ID", anchor=tk.W, width=150)
        tree.column("Name", anchor=tk.W, width=150)
        tree.column("Location", anchor=tk.W, width=150)
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

        # Function to handle the selection of food establishments
        def on_estab_select(event):
            # Clear previous food items
            for child in tree_food_items.get_children():
                tree_food_items.delete(child)

            # Get the selected item
            selected_item = tree.selection()
            if selected_item:
                selected_item = selected_item[0]
                # Extract the food establishment name from the selected item
                selected_food_establishment_id = tree.item(selected_item)["values"][0]

                # Execute another query based on the selected food establishment
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
                                WHERE r.foodItem_id IS NOT NULL AND fi.foodEst_id = %s 
                                GROUP BY r.foodItem_id;""", (selected_food_establishment_id,))
                    food_items = cursor.fetchall()
                    cursor.close()
                    connection.close()

                    # Add food items to the Treeview
                    for item in food_items:
                        tree_food_items.insert("", tk.END, values=item)

        # Bind the selection event of food establishments to the function
        tree.bind("<ButtonRelease-1>", on_estab_select)

        # Create a new Treeview to display food items
        tree_food_items = ttk.Treeview(root)
        tree_food_items.pack(expand=True, fill=tk.BOTH)

        # Define columns for food items
        tree_food_items["columns"] = ("ID", "Name", "Price", "Type", "Description", "Rating")

        # Format columns for food items
        tree_food_items.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree_food_items.column("ID", anchor=tk.W, width=50)
        tree_food_items.column("Name", anchor=tk.W, width=100)
        tree_food_items.column("Price", anchor=tk.W, width=100)
        tree_food_items.column("Type", anchor=tk.W, width=100)
        tree_food_items.column("Description", anchor=tk.W, width=150)
        tree_food_items.column("Rating", anchor=tk.W, width=100)

        # Create headings for food items
        tree_food_items.heading("ID", text="ID")
        tree_food_items.heading("Name", text="Name")
        tree_food_items.heading("Price", text="Price")
        tree_food_items.heading("Type", text="Type")
        tree_food_items.heading("Description", text="Description")
        tree_food_items.heading("Rating", text="Rating")

        # Function to handle the selection of food items and display reviews
        def on_item_select(event):
            # Clear previous food reviews
            for child in tree_food_reviews.get_children():
                tree_food_reviews.delete(child)

            # Get the selected item
            selected_item = tree_food_items.focus()
            if selected_item:
                # Extract the food item ID from the selected item
                selected_food_item_id = tree_food_items.item(selected_item)["values"][0]
                
                # Execute another query based on the selected food item ID
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

                    # Add food reviews to the Treeview
                    for review in food_reviews:
                        tree_food_reviews.insert("", tk.END, values=review)

        # Bind the selection event of food items to the function
        tree_food_items.bind("<ButtonRelease-1>", on_item_select)

        # Create a new Treeview to display food reviews
        tree_food_reviews = ttk.Treeview(root)
        tree_food_reviews.pack(expand=True, fill=tk.BOTH)

        # Define columns for food reviews
        tree_food_reviews["columns"] = ("Review date", "Content", "Rating")

        # Format columns for food reviews
        tree_food_reviews.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree_food_reviews.column("Review date", anchor=tk.W, width=100)
        tree_food_reviews.column("Content", anchor=tk.W, width=100)
        tree_food_reviews.column("Rating", anchor=tk.W, width=100)

        # Create headings for food reviews
        tree_food_reviews.heading("Review date", text="Review date")
        tree_food_reviews.heading("Content", text="Content")
        tree_food_reviews.heading("Rating", text="Rating")

        root.mainloop()

# 3
# Function to view all food items from an establishment
def view_items_from_estab():
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

        # Create a Tkinter window
        root = tk.Tk()
        root.title("Food Establishments")

        # Create a Treeview to display the records
        tree = ttk.Treeview(root)
        tree.pack(expand=True, fill=tk.BOTH)

        # Define columns
        tree["columns"] = ("ID", "Name", "Location", "Type", "Rating")

        # Format columns
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

        # Create a new Treeview to display items
        tree_reviews = ttk.Treeview(root)
        tree_reviews.pack(expand=True, fill=tk.BOTH)

        # Define columns for items
        tree_reviews["columns"] = ("ID", "Name", "Price", "Type", "Description", "Rating")

        # Format columns for items
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
                # Extract the food establishment ID from the selected item
                selected_food_establishment_id = tree.item(selected_item)["values"][0]

                # Execute another query based on the selected food establishment
                connection = connect_to_db()
                if connection:
                    cursor = connection.cursor()
                    # cursor.execute("""
                    #     SELECT 
                    #         fi.foodItem_id, 
                    #         fi.foodItem_name, 
                    #         fi.foodItem_price, 
                    #         fi.foodItem_type, 
                    #         fi.foodItem_desc, 
                    #         AVG(r.rating) AS 'Rating' 
                    #     FROM review r 
                    #     RIGHT JOIN food_item fi 
                    #     ON r.foodItem_id = fi.foodItem_id 
                    #     WHERE r.foodItem_id IS NOT NULL 
                    #     AND fi.foodEst_id = %s 
                    #     GROUP BY r.foodItem_id;
                    # """, (selected_food_establishment_id,))
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

                    # Add items to the Treeview
                    for item in items:
                        tree_reviews.insert("", tk.END, values=item)

        # Bind the selection event to the function
        tree.bind("<ButtonRelease-1>", on_select)

        root.mainloop()

# 4 

# 5
# Function to view all reviews made within a month for an establishment
def view_reviews_establishment_month():
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

        # Create a Tkinter window
        root = tk.Tk()
        root.title("Food Establishments")

        # Create a Treeview to display the records
        tree = ttk.Treeview(root)
        tree.pack(expand=True, fill=tk.BOTH)

        # Define columns
        tree["columns"] = ("ID", "Name", "Location", "Type", "Rating")

        # Format columns
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

        # Create a new Treeview to display reviews
        tree_reviews = ttk.Treeview(root)
        tree_reviews.pack(expand=True, fill=tk.BOTH)

        # Define columns for reviews
        tree_reviews["columns"] = ("Review date", "Content", "Rating")

        # Format columns for reviews
        tree_reviews.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree_reviews.column("Review date", anchor=tk.W, width=100)
        tree_reviews.column("Content", anchor=tk.W, width=250)
        tree_reviews.column("Rating", anchor=tk.W, width=100)

        # Create headings for reviews
        tree_reviews.heading("Review date", text="Review date")
        tree_reviews.heading("Content", text="Content")
        tree_reviews.heading("Rating", text="Rating")

        root.mainloop()

# 5
# Function to view all reviews made within a month for a food item 
def view_reviews_food_month():
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

        # Create a Tkinter window
        root = tk.Tk()
        root.title("Food Item")

        # Create a Treeview to display the records
        tree = ttk.Treeview(root)
        tree.pack(expand=True, fill=tk.BOTH)

        # Define columns
        tree["columns"] = ("ID", "Name", "Price", "Type", "Description", "Rating")

        # Format columns
        tree.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree.column("ID", anchor=tk.W, width=50)
        tree.column("Name", anchor=tk.W, width=100)
        tree.column("Price", anchor=tk.W, width=50)
        tree.column("Type", anchor=tk.W, width=100)
        tree.column("Description", anchor=tk.W, width=100)
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
            # Clear previous reviews
            for child in tree_reviews.get_children():
                tree_reviews.delete(child)

            # Get the selected item
            selected_item = tree.focus()
            if selected_item:
                # Extract the food establishment name from the selected item
                selected_food_item = tree.item(selected_item)["values"][0]
                
                # Execute another query based on the selected food establishment
                connection = connect_to_db()
                if connection: 
                    cursor = connection.cursor()
                    cursor.execute("""    SELECT review_date, content, rating from review WHERE foodItem_id = (SELECT foodItem_id FROM food_item WHERE foodItem_id = %s) AND review_date BETWEEN ADDDATE(CURDATE(), INTERVAL -1 MONTH) AND CURDATE()""", (selected_food_item,))
                    reviews = cursor.fetchall()
                    cursor.close()
                    connection.close()

                    # Add reviews to the Treeview for reviews
                    for review in reviews:
                        tree_reviews.insert("", tk.END, values=review)

        # Bind the selection event to the function
        tree.bind("<ButtonRelease-1>", on_select)

        # Create a new Treeview to display reviews
        tree_reviews = ttk.Treeview(root)
        tree_reviews.pack(expand=True, fill=tk.BOTH)

        # Define columns for reviews
        tree_reviews["columns"] = ("Review date", "Content", "Rating")

        # Format columns for reviews
        tree_reviews.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
        tree_reviews.column("Review date", anchor=tk.W, width=100)
        tree_reviews.column("Content", anchor=tk.W, width=250)
        tree_reviews.column("Rating", anchor=tk.W, width=100)

        # Create headings for reviews
        tree_reviews.heading("Review date", text="Review date")
        tree_reviews.heading("Content", text="Content")
        tree_reviews.heading("Rating", text="Rating")

        root.mainloop()

# 6 
# Function to view establishments with high rating (>=4)
def view_estab_high_rating():
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
        display_records(records, ["Name", "Location", "Type", "Average Rating"])
        cursor.close()
        connection.close()

# 7
def view_items_by_price():
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

        # Create a Tkinter window
        root = tk.Tk()
        root.title("Food Establishments")

        # Create a Treeview to display the records
        tree = ttk.Treeview(root)
        tree.pack(expand=True, fill=tk.BOTH)

        # Define columns
        tree["columns"] = ("ID", "Name", "Location", "Type", "Rating")

        # Format columns
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
                # Extract the food establishment ID from the selected item
                selected_food_establishment_id = tree.item(selected_item)["values"][0]
                
                # Execute another query based on the selected food establishment
                connection = connect_to_db()
                if connection: 
                    cursor = connection.cursor()
                    cursor.execute("""SELECT fi.foodItem_id 'ID', 
                                   foodItem_name 'Name', 
                                   foodItem_price 'Price', 
                                   foodItem_type 'Type', 
                                   foodItem_desc 'Description', 
                                   AVG(r.rating) 'Rating' 
                                   FROM food_item fi 
                                   JOIN review r ON fi.foodItem_id=r.foodItem_id WHERE fi.foodEst_id = (SELECT foodEst_id FROM food_establishment 
                                   WHERE foodEst_id = %s)  
                                   GROUP BY r.foodItem_id
                                   ORDER BY foodItem_price DESC;""", (selected_food_establishment_id,))
                    items = cursor.fetchall()
                    cursor.close()
                    connection.close()

                    # Add items to the Treeview
                    for item in items:
                        tree_reviews.insert("", tk.END, values=item)

        # Bind the selection event to the function
        tree.bind("<ButtonRelease-1>", on_select)

        # Create a new Treeview to display items
        tree_reviews = ttk.Treeview(root)
        tree_reviews.pack(expand=True, fill=tk.BOTH)

        # Define columns for items
        tree_reviews["columns"] = ("ID", "Name", "Price", "Type", "Description", "Rating")

        # Format columns for items
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

        root.mainloop()

# Function to search food items based on type
def search_food_items_bytype(type_entry):
    food_type = type_entry.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = """
        SELECT fi.foodItem_id, fi.foodItem_name, fi.foodItem_price, fi.foodItem_type, fi.foodItem_desc, fi.foodItem_rating, fe.foodEst_name
        FROM serves s
        JOIN food_item fi ON s.foodItem_id = fi.foodItem_id
        JOIN food_establishment fe ON s.foodEst_id = fe.foodEst_id
        WHERE fi.foodItem_type = %s
        """
        cursor.execute(query, (food_type,))
        records = cursor.fetchall()
        display_records(records, ["ID", "Name", "Price", "Type", "Description", "Rating", "Establishment"])
        cursor.close()
        connection.close()

# Function to search food items based on price range
def search_food_items_byprice(price_min_entry, price_max_entry):
    price_min = price_min_entry.get()
    price_max = price_max_entry.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = """
        SELECT fi.foodItem_id, fi.foodItem_name, fi.foodItem_price, fi.foodItem_type, fi.foodItem_desc, fi.foodItem_rating, fe.foodEst_name
        FROM serves s
        JOIN food_item fi ON s.foodItem_id = fi.foodItem_id
        JOIN food_establishment fe ON s.foodEst_id = fe.foodEst_id
        WHERE fi.foodItem_price BETWEEN %s AND %s
        """
        cursor.execute(query, (price_min, price_max))
        records = cursor.fetchall()
        display_records(records, ["ID", "Name", "Price", "Type", "Description", "Rating", "Establishment"])
        cursor.close()
        connection.close()

# Function to search food item reviews based on food name
def search_food_item_reviews(food_item_name_entry):
    food_item_name = food_item_name_entry.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = """SELECT 
                    r.review_date, 
                    r.content, 
                    r.rating, 
                    fi.foodItem_name, 
                    fi.foodItem_price, 
                    fi.foodItem_type, 
                    fe.foodEst_name AS "Food Establishment"
                    FROM review r
                    JOIN food_item fi ON r.foodItem_id = fi.foodItem_id
                    JOIN food_establishment fe ON fi.foodEst_id = fe.foodEst_id
                    WHERE fi.foodItem_name = %s"""
        cursor.execute(query, (food_item_name,))
        records = cursor.fetchall()
        display_records(records, ["Review Date", "Content", "Rating", "Food Item Name", "Price", "Type", "Food Establishment"])
        cursor.close()
        connection.close()

def search_establishment_food_items(establishment_name_entry):
    establishment_name = establishment_name_entry.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = """
        SELECT fi.foodItem_id, fi.foodItem_name, fi.foodItem_price, fi.foodItem_type, fi.foodItem_desc, fi.foodItem_rating
        FROM food_item fi
        JOIN food_establishment fe ON fi.foodEst_id = fe.foodEst_id
        WHERE fe.foodEst_name = %s
        """
        cursor.execute(query, (establishment_name,))
        records = cursor.fetchall()
        display_records(records, ["ID", "Name", "Price", "Type", "Description", "Rating"])
        cursor.close()
        connection.close()


# Function to display records in a new window
def display_records(records, columns):
    record_window = tk.Toplevel()
    record_window.title("Records")
    tree = ttk.Treeview(record_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')  
    for record in records:
        tree.insert('', tk.END, values=record)
    tree.pack(fill=tk.BOTH, expand=True)

# Function to add a food establishment
def add_food_establishment(est_name_entry, est_location_entry, est_type_entry):
    name = est_name_entry.get()
    location = est_location_entry.get()
    type_ = est_type_entry.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO food_establishment (foodEst_name, foodEst_loc, foodEst_type) VALUES (%s, %s, %s)", (name, location, type_))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Food establishment added successfully")

# Function to update a food establishment
def update_food_establishment(est_name_entry, est_location_entry, est_type_entry, est_id_entry):
    id_ = est_id_entry.get()
    name = est_name_entry.get()
    location = est_location_entry.get()
    type_ = est_type_entry.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE food_establishment SET foodEst_name = %s, foodEst_loc = %s, foodEst_type = %s WHERE foodEst_id = %s", (name, location, type_, id_))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Food establishment updated successfully")

# Function to delete a food establishment
def delete_food_establishment(est_id_entry):
    id_ = est_id_entry.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM food_establishment WHERE foodEst_id = %s", (id_,))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Food establishment deleted successfully")

# Function to add a food item
def add_food_item(item_name_entry, item_price_entry, item_type_entry, item_desc_entry, item_estid_entry):
    name = item_name_entry.get()
    price = item_price_entry.get()
    type_ = item_type_entry.get()
    desc = item_desc_entry.get()
    est_id = item_estid_entry.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO food_item (foodItem_name, foodItem_price, foodItem_type, foodItem_desc, foodEst_id) VALUES (%s, %s, %s, %s, %s)", (name, price, type_, desc, est_id))
        cursor.execute("""
            INSERT INTO serves (foodEst_id, foodItem_id)
               VALUE(%s, (SELECT foodItem_id FROM food_item WHERE foodItem_name = %s));
        """, (est_id, name))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Food item added successfully")

# Function to update a food item
def update_food_item(item_name_entry, item_price_entry, item_type_entry, item_desc_entry, item_id_entry):
    id_ = item_id_entry.get()
    name = item_name_entry.get()
    price = item_price_entry.get()
    type_ = item_type_entry.get()
    desc = item_desc_entry.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE food_item SET foodItem_name = %s, foodItem_price = %s, foodItem_type = %s, foodItem_desc = %s WHERE foodItem_id = %s", (name, price, type_, desc, id_))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Food item updated successfully")

# Function to delete a food item
def delete_food_item(item_id_entry):
    id_ = item_id_entry.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM food_item WHERE foodItem_id = %s", (id_,))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Food item deleted successfully")

# Function to add a food review
def add_food_review(review_date_entry, review_content_entry, review_rating_entry, review_user_id_entry, review_food_est_id_entry, review_food_item_id_entry):
    date = review_date_entry.get()
    content = review_content_entry.get()
    rating = review_rating_entry.get()
    user_id = review_user_id_entry.get()
    food_est_id = review_food_est_id_entry.get()
    food_item_id = review_food_item_id_entry.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO review (review_date, content, rating, userid, foodEst_id, foodItem_id) VALUES (%s, %s, %s, %s, %s, %s)", (date, content, rating, user_id, food_est_id, food_item_id))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Food review added successfully")

# Function to update a food review
def update_food_review(review_date_entry, review_content_entry, review_rating_entry, review_user_id_entry, review_food_est_id_entry, review_food_item_id_entry, review_id_entry):
    id_ = review_id_entry.get()
    date = review_date_entry.get()
    content = review_content_entry.get()
    rating = review_rating_entry.get()
    user_id = review_user_id_entry.get()
    food_est_id = review_food_est_id_entry.get()
    food_item_id = review_food_item_id_entry.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE review SET review_date = %s, content = %s, rating = %s, userid = %s, foodEst_id = %s, foodItem_id = %s WHERE review_id = %s", (date, content, rating, user_id, food_est_id, food_item_id, id_))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Food review updated successfully")

# Function to delete a food review
def delete_food_review(review_id_entry):
    id_ = review_id_entry.get()
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM review WHERE review_id = %s", (id_,))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Food review deleted successfully")

def fetch_food_establishments():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT foodEst_id, foodEst_name, foodEst_loc, foodEst_type, foodEst_rating FROM food_establishment")
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records
    

def fetch_food_items(est_id):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM food_item WHERE foodEst_id = %s;", (est_id,))
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records

# Function to get food reviews for a specific user
def get_food_reviews_by_user(userid):
    connection = connect_to_db()
    if connection: 
        cursor = connection.cursor()
        cursor.execute("""
                        SELECT r.review_id, 
                r.review_date, 
                r.content, 
                r.rating, 
                COALESCE(fi.foodItem_name, fe.foodEst_name) 
            FROM review r 
            LEFT JOIN food_item fi ON r.foodItem_id = fi.foodItem_id 
            LEFT JOIN food_establishment fe ON r.foodEst_id = fe.foodEst_id
            WHERE r.userid = %s;
        """, (userid,))
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records

# Function to update a review in the database
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

# Function to handle updating reviews
def update_own_review(userid):
    records = get_food_reviews_by_user(userid)

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Update a Review")

    # Create a Treeview to display the food items
    tree_items = ttk.Treeview(root)
    tree_items.pack(expand=True, fill=tk.BOTH)

    # Define columns for food items
    tree_items["columns"] = ("ID", "Date", "Content", "Rating", "Food Item")

    # Format columns for food items
    tree_items.column("#0", width=0, stretch=tk.NO)  # Hide first empty column
    tree_items.column("ID", anchor=tk.W, width=50)
    tree_items.column("Date", anchor=tk.W, width=100)
    tree_items.column("Content", anchor=tk.W, width=200)
    tree_items.column("Rating", anchor=tk.W, width=50)
    tree_items.column("Food Item", anchor=tk.W, width=100)

    # Create headings for food items
    tree_items.heading("ID", text="ID")
    tree_items.heading("Date", text="Date")
    tree_items.heading("Content", text="Content")
    tree_items.heading("Rating", text="Rating")
    tree_items.heading("Food Item", text="Food Item")

    # Add food item records to the Treeview
    for record in records:
        tree_items.insert("", tk.END, values=record)

    # Define a function to handle double-click events on food items
    def on_item_double_click(event):
        selected_item = tree_items.selection()
        if not selected_item:
            return
        selected_item = selected_item[0]
        values = tree_items.item(selected_item, "values")
        review_id = values[0]
        current_content = values[2]
        current_rating = values[3]

        review_window = tk.Toplevel(root)
        review_window.title(f"Update Review {review_id}")

        ttk.Label(review_window, text="Rating:").grid(row=1, column=0, padx=10, pady=10)
        rating_entry = ttk.Entry(review_window)
        rating_entry.grid(row=1, column=1, padx=10, pady=10)
        rating_entry.insert(0, current_rating)

        ttk.Label(review_window, text="Content:").grid(row=2, column=0, padx=10, pady=10)
        content_entry = ttk.Entry(review_window)
        content_entry.grid(row=2, column=1, padx=10, pady=10)
        content_entry.insert(0, current_content)

        def save_review():
            new_rating = rating_entry.get()
            new_content = content_entry.get()
            update_review(review_id, new_content, new_rating)

            # Refresh the Treeview
            tree_items.item(selected_item, values=(review_id, values[1], new_content, new_rating, values[4]))
            messagebox.showinfo("Success", "Review updated successfully.")
            review_window.destroy()

        ttk.Button(review_window, text="Save", command=save_review).grid(row=3, column=0, columnspan=2, pady=10)

    # Bind double-click event to the Treeview for food items
    tree_items.bind("<Double-1>", on_item_double_click)

    root.mainloop()

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

def delete_own_review(userid):
    records = get_food_reviews_by_user(userid)

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Delete a Review")

    # Create a Treeview to display the records
    tree = ttk.Treeview(root)
    tree.pack(expand=True, fill=tk.BOTH)

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
                messagebox.showinfo("Success", "Review deleted successfully.")

        # Call the delete_review_record function
        delete_review_record()

    # Bind double-click event to the Treeview
    tree.bind("<Double-1>", on_double_click)

    root.mainloop()

# Function to make a review
def make_review(userid):
    def choose_review_type():
        choice = review_type.get()
        if choice == "Food Item":
            establishments = fetch_food_establishments()
            show_establishments(establishments, "Food Item")
        elif choice == "Establishment":
            establishments = fetch_food_establishments()
            show_review_form(establishments, "Establishment")

    def show_establishments(establishments, review_type):
        est_window = tk.Toplevel()
        est_window.title(f"Select Establishment for {review_type} Review")

        ttk.Label(est_window, text="Select Establishment:").grid(row=0, column=0, padx=10, pady=10)
        selected_est = tk.StringVar()
        ttk.Combobox(est_window, textvariable=selected_est, values=[f'{est[0]} - {est[1]}' for est in establishments]).grid(row=0, column=1, padx=10, pady=10)

        def next_step():
            selected_est_str = selected_est.get()
            est_id = selected_est_str.split(' - ')[0]
            if est_id:
                if review_type == "Food Item":
                    items = fetch_food_items(est_id)
                    # print(items)
                    show_review_form(items, "Food Item", selected_est_str)
                else:
                    show_review_form([est for est in establishments if est[0] == selected_est_str], "Establishment", selected_est_str)


        ttk.Button(est_window, text="Next", command=next_step).grid(row=1, columnspan=2, pady=10)

    def show_review_form(items, review_type, est_name=None):
        review_window = tk.Toplevel()
        review_window.title(f"Review {review_type}")

        if review_type == "Food Item":
            ttk.Label(review_window, text="Select Food Item:").grid(row=0, column=0, padx=10, pady=10)
            selected_item = tk.StringVar()
            ttk.Combobox(review_window, textvariable=selected_item, values=[item[1] for item in items]).grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(review_window, text="Rating:").grid(row=1, column=0, padx=10, pady=10)
        rating_entry = ttk.Entry(review_window)
        rating_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(review_window, text="Content:").grid(row=2, column=0, padx=10, pady=10)
        content_entry = ttk.Entry(review_window)
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
                selected_id = est_name
                foodEst_id = selected_id
                foodItem_id = None

            rating = rating_entry.get()
            content = content_entry.get()
            if selected_id and rating and content:
                print(f"""
                        === TEST ===
                        userid: {userid}
                        foodEstId: {foodEst_id}
                        foodItemId: {foodItem_id}
""")
                connection = connect_to_db()
                if connection:
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO review (review_date, content, rating, userid, foodEst_id, foodItem_id) VALUES (CURDATE(), %s, %s, %s, %s, %s);", (content, rating, userid, foodEst_id, foodItem_id))
                    # cursor.execute("INSERT INTO review (review_date, content, rating, userid, foodEst_id, foodItem_id) VALUES (CURDATE(), 'test rev', 3, 1, NULL, 1)")
                    connection.commit()
                    cursor.close()
                    connection.close()
                print(f"Review for {review_type} ID {selected_id}: Rating {rating}, Content {content}")
                messagebox.showinfo("Success", "Review submitted successfully")
                review_window.destroy()
            else:
                messagebox.showerror("Error", "Please fill all fields")



        ttk.Button(review_window, text="Submit", command=submit_review).grid(row=3, columnspan=2, pady=10)

    review_window = tk.Toplevel()
    review_window.title("Make a Review")

    review_type = tk.StringVar(value="Food Item")
    ttk.Radiobutton(review_window, text="Food Item", variable=review_type, value="Food Item").grid(row=0, column=0, padx=10, pady=10)
    ttk.Radiobutton(review_window, text="Establishment", variable=review_type, value="Establishment").grid(row=0, column=1, padx=10, pady=10)
    ttk.Button(review_window, text="Next", command=choose_review_type).grid(row=1, columnspan=2, pady=10)


# Define the login function
def login():
    def check_credentials():
        username = username_entry.get()
        password = password_entry.get()
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT userid FROM users WHERE username = %s AND userpassword = %s;", (username, password))
            result = cursor.fetchone()
            userid = result[0]
            if result:
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

    ttk.Label(login_window, text="Username:").grid(row=0, column=0)
    username_entry = ttk.Entry(login_window)
    username_entry.grid(row=0, column=1)

    ttk.Label(login_window, text="Password:").grid(row=1, column=0)
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1)

    ttk.Button(login_window, text="Login", command=check_credentials).grid(row=2, columnspan=2)

    login_window.mainloop()


# Call the login function to start the application

def show_main_app(userid):
    # GUI Setup
    root = tk.Tk()
    root.title("Food Review System")

    tab_control = ttk.Notebook(root)
    view_tab = ttk.Frame(tab_control)
    add_update_tab = ttk.Frame(tab_control)
    search_tab = ttk.Frame(tab_control)
    tab_control.add(view_tab, text='View')
    tab_control.add(add_update_tab, text='Add/Update')
    tab_control.add(search_tab, text='Search')
    tab_control.pack(expand=1, fill="both")

    # View tab
    view_frame = ttk.LabelFrame(view_tab, text="View Records")
    view_frame.pack(padx=10, pady=10)

    # 1
    view_food_est_btn = ttk.Button(view_frame, text="View Food Establishments", command=view_food_establishments)
    view_food_est_btn.pack(fill='x')
    # 2
    view_reviews_est_btn = ttk.Button(view_frame, text="View Reviews for Establishments", command=view_reviews_establishment)
    view_reviews_est_btn.pack(fill='x')

    view_reviews_food_btn = ttk.Button(view_frame, text="View Reviews for Food Items", command=view_reviews_food)
    view_reviews_food_btn.pack(fill='x')

    # 3 
    view_food_items_btn = ttk.Button(view_frame, text="View Food items", command=view_items_from_estab)
    view_food_items_btn.pack(fill='x')

    # 5
    view_reviews_month_estab_btn = ttk.Button(view_frame, text="View Reviews for Food Establishments in the past month", command=view_reviews_establishment_month)
    view_reviews_month_estab_btn.pack(fill='x')

    view_reviews_month_food_btn = ttk.Button(view_frame, text="View Reviews for Food Items in the past month", command=view_reviews_food_month)
    view_reviews_month_food_btn.pack(fill='x')

    # 6
    view_estab_high_rating_btn = ttk.Button(view_frame, text="View Establishments with high rating", command=view_estab_high_rating)
    view_estab_high_rating_btn.pack(fill='x')

    # 7 
    view_food_by_price = ttk.Button(view_frame, text="View Food Items sorted by price", command=view_items_by_price)
    view_food_by_price.pack(fill='x')

    # Add/Update tab
    add_update_frame = ttk.LabelFrame(add_update_tab, text="Add/Update Records")
    add_update_frame.pack(padx=10, pady=10)

    # Food Establishment
    est_frame = ttk.LabelFrame(add_update_frame, text="Food Establishment")
    est_frame.grid(row=0, column=0, padx=5, pady=5)

    ttk.Label(est_frame, text="ID:").grid(row=0, column=0)
    est_id_entry = ttk.Entry(est_frame)
    est_id_entry.grid(row=0, column=1)

    ttk.Label(est_frame, text="Name:").grid(row=1, column=0)
    est_name_entry = ttk.Entry(est_frame)
    est_name_entry.grid(row=1, column=1)

    ttk.Label(est_frame, text="Location:").grid(row=2, column=0)
    est_location_entry = ttk.Entry(est_frame)
    est_location_entry.grid(row=2, column=1)

    ttk.Label(est_frame, text="Type:").grid(row=3, column=0)
    est_type_entry = ttk.Entry(est_frame)
    est_type_entry.grid(row=3, column=1)

    ttk.Button(est_frame, text="Add", command=lambda:add_food_establishment(est_name_entry, est_location_entry, est_type_entry)).grid(row=4, column=0)
    ttk.Button(est_frame, text="Update", command=lambda:update_food_establishment(est_name_entry, est_location_entry, est_type_entry, est_id_entry)).grid(row=4, column=1)
    ttk.Button(est_frame, text="Delete", command=lambda:delete_food_establishment(est_id_entry)).grid(row=4, column=2)

    # Food Item
    item_frame = ttk.LabelFrame(add_update_frame, text="Food Item")
    item_frame.grid(row=1, column=0, padx=5, pady=5)

    ttk.Label(item_frame, text="ID:").grid(row=0, column=0)
    item_id_entry = ttk.Entry(item_frame)
    item_id_entry.grid(row=0, column=1)

    ttk.Label(item_frame, text="Name:").grid(row=1, column=0)
    item_name_entry = ttk.Entry(item_frame)
    item_name_entry.grid(row=1, column=1)

    ttk.Label(item_frame, text="Price:").grid(row=2, column=0)
    item_price_entry = ttk.Entry(item_frame)
    item_price_entry.grid(row=2, column=1)

    ttk.Label(item_frame, text="Type:").grid(row=3, column=0)
    item_type_entry = ttk.Entry(item_frame)
    item_type_entry.grid(row=3, column=1)

    ttk.Label(item_frame, text="Description:").grid(row=4, column=0)
    item_desc_entry = ttk.Entry(item_frame)
    item_desc_entry.grid(row=4, column=1)

    ttk.Label(item_frame, text="Food Establishment ID:").grid(row=5, column=0)
    item_estid_entry = ttk.Entry(item_frame)
    item_estid_entry.grid(row=5, column=1)

    ttk.Button(item_frame, text="Add", command=lambda:add_food_item(item_name_entry, item_price_entry, item_type_entry, item_desc_entry, item_estid_entry)).grid(row=6, column=0)
    ttk.Button(item_frame, text="Update", command=lambda:update_food_item(item_name_entry, item_price_entry, item_type_entry, item_desc_entry, item_id_entry)).grid(row=6, column=1)
    ttk.Button(item_frame, text="Delete", command=lambda:delete_food_item(item_id_entry)).grid(row=6, column=2)

    # Food Review
    review_frame = ttk.LabelFrame(add_update_frame, text="Food Review")
    review_frame.grid(row=2, column=0, padx=5, pady=5)

    ttk.Label(review_frame, text="ID:").grid(row=0, column=0)
    review_id_entry = ttk.Entry(review_frame)
    review_id_entry.grid(row=0, column=1)

    ttk.Label(review_frame, text="Date:").grid(row=1, column=0)
    review_date_entry = ttk.Entry(review_frame)
    review_date_entry.grid(row=1, column=1)

    ttk.Label(review_frame, text="Content:").grid(row=2, column=0)
    review_content_entry = ttk.Entry(review_frame)
    review_content_entry.grid(row=2, column=1)

    ttk.Label(review_frame, text="Rating:").grid(row=3, column=0)
    review_rating_entry = ttk.Entry(review_frame)
    review_rating_entry.grid(row=3, column=1)

    ttk.Label(review_frame, text="User ID:").grid(row=4, column=0)
    review_user_id_entry = ttk.Entry(review_frame)
    review_user_id_entry.grid(row=4, column=1)

    ttk.Label(review_frame, text="Food Est ID:").grid(row=5, column=0)
    review_food_est_id_entry = ttk.Entry(review_frame)
    review_food_est_id_entry.grid(row=5, column=1)

    ttk.Label(review_frame, text="Food Item ID:").grid(row=6, column=0)
    review_food_item_id_entry = ttk.Entry(review_frame)
    review_food_item_id_entry.grid(row=6, column=1)

    ttk.Button(est_frame, text="Add", command=lambda: add_food_establishment(est_name_entry, est_location_entry, est_type_entry)).grid(row=4, column=0)
    ttk.Button(est_frame, text="Update", command=lambda: update_food_establishment(est_id_entry, est_name_entry, est_location_entry, est_type_entry)).grid(row=4, column=1)
    ttk.Button(est_frame, text="Delete", command=lambda: delete_food_establishment(est_id_entry)).grid(row=4, column=2)

    ttk.Button(add_update_frame, text="Make a Review", command=lambda: make_review(userid)).grid(row=8, column=0, pady=10)
    
    ttk.Button(add_update_frame, text="Update a Review", command=lambda: update_own_review(userid)).grid(row=8, column=1, pady=10)

    ttk.Button(add_update_frame, text="Delete a Review", command=lambda: delete_own_review(userid)).grid(row=8, column=2, pady=10)


    # Search tab
    search_frame = ttk.LabelFrame(search_tab, text="Search Food Items")
    search_frame.pack(padx=10, pady=10)

    ttk.Label(search_frame, text="Type:").grid(row=0, column=0)
    type_entry = ttk.Entry(search_frame)
    type_entry.grid(row=0, column=1)
    ttk.Button(search_frame, text="Search by Type", command=lambda:search_food_items_bytype(type_entry)).grid(row=0, column=2)

    ttk.Label(search_frame, text="Min Price:").grid(row=1, column=0)
    price_min_entry = ttk.Entry(search_frame)
    price_min_entry.grid(row=1, column=1)
    ttk.Label(search_frame, text="Max Price:").grid(row=1, column=2)
    price_max_entry = ttk.Entry(search_frame)
    price_max_entry.grid(row=1, column=3)
    ttk.Button(search_frame, text="Search by Price", command=lambda:search_food_items_byprice(price_min_entry, price_max_entry)).grid(row=1, column=4)

    # Search Reviews by Food Item Name
    food_item_name_label = ttk.Label(search_tab, text="Search Reviews by Food Item Name")
    food_item_name_label.pack()
    food_item_name_entry = ttk.Entry(search_tab)
    food_item_name_entry.pack()
    food_item_name_button = ttk.Button(search_tab, text="Search", command=lambda:search_food_item_reviews(food_item_name_entry))
    food_item_name_button.pack(pady=5)

    search_frame = ttk.LabelFrame(search_tab, text="Search Food Items by Establishment")
    search_frame.pack(padx=10, pady=10)

    ttk.Label(search_frame, text="Establishment Name:").grid(row=0, column=0)
    establishment_name_entry = ttk.Entry(search_frame)
    establishment_name_entry.grid(row=0, column=1)
    ttk.Button(search_frame, text="Search", command=lambda:search_establishment_food_items(establishment_name_entry)).grid(row=0, column=2)

    root.mainloop()

login()
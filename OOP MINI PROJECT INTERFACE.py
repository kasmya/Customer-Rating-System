import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import string
import random

# Step 1: Generate random ratings between 1 and 5
def generate_rating():
    return round(random.uniform(1, 5), 1)

# Step 2: Generate customer names
def generate_customer_names(num_customers, name_length=50):
    base_string = ''.join(random.choices(string.ascii_letters, k=name_length))
    return [base_string[:random.randint(3, 10)] for _ in range(num_customers)]

# Step 3: Generate other customer details
def generate_customer_details(num_customers):
    customer_ids = [random.randint(1000, 9999) for _ in range(num_customers)]
    ages = [random.randint(18, 70) for _ in range(num_customers)]
    mobile_numbers = [random.randint(7000000000, 9999999999) for _ in range(num_customers)]
    ratings = [generate_rating() for _ in range(num_customers)]
    return customer_ids, ages, mobile_numbers, ratings

# Step 4: Store data in a DataFrame and save it as a CSV file
def create_customer_data(num_customers=10):
    names = generate_customer_names(num_customers)
    ids, ages, mobiles, ratings = generate_customer_details(num_customers)
    data = pd.DataFrame({
        "Customer ID": ids,
        "Name": names,
        "Age": ages,
        "Mobile No.": mobiles,
        "Rating": ratings
    })
    data.to_csv("customer_data.csv", index=False)
    return data

# Step 5: Load data from the CSV into a list of objects (using classes)
class Customer:
    def __init__(self, customer_id, name, age, mobile, rating):
        self.customer_id = customer_id
        self.name = name
        self.age = age
        self.mobile = mobile
        self.rating = rating

def load_customer_data(filename="customer_data.csv"):
    try:
        data = pd.read_csv(filename)
        customers = [
            Customer(row["Customer ID"], row["Name"], row["Age"], row["Mobile No."], row["Rating"])
            for _, row in data.iterrows()
        ]
        return customers
    except FileNotFoundError:
        messagebox.showerror("Error", f"{filename} not found!")
        return []

# Step 6: Filter customers with an average rating >= 3.5
def filter_customers_by_rating(customers, threshold=3.5):
    return [customer for customer in customers if customer.rating >= threshold]

# Tkinter GUI Implementation
def create_interface():
    # Main window
    root = tk.Tk()
    root.title("Customer Management")
    root.geometry("800x600")

    # Label
    tk.Label(root, text="Customer Management System", font=("Arial", 16)).pack(pady=10)

    # Treeview to display data
    tree = ttk.Treeview(root, columns=("ID", "Name", "Age", "Mobile", "Rating"), show="headings")
    tree.heading("ID", text="Customer ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Mobile", text="Mobile No.")
    tree.heading("Rating", text="Rating")
    tree.pack(fill=tk.BOTH, expand=True, pady=20)

    # Generate customer data
    def generate_data():
        create_customer_data(num_customers=15)
        messagebox.showinfo("Success", "Customer data generated and saved to 'customer_data.csv'.")

    # Load customer data
    def load_data():
        customers = load_customer_data()
        tree.delete(*tree.get_children())  # Clear existing data
        for customer in customers:
            tree.insert("", tk.END, values=(customer.customer_id, customer.name, customer.age, customer.mobile, customer.rating))

    # Filter high-rating customers
    def filter_data():
        customers = load_customer_data()
        filtered = filter_customers_by_rating(customers)
        tree.delete(*tree.get_children())  # Clear existing data
        for customer in filtered:
            tree.insert("", tk.END, values=(customer.customer_id, customer.name, customer.age, customer.mobile, customer.rating))
        messagebox.showinfo("Filter Applied", f"Filtered {len(filtered)} customers with rating >= 3.5.")

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Generate Data", command=generate_data, width=20).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Load Data", command=load_data, width=20).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Filter by Rating", command=filter_data, width=20).pack(side=tk.LEFT, padx=5)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_interface()

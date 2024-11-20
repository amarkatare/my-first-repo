import tkinter as tk
from tkinter import messagebox
import pymysql
# Function to connect to MySQL database
def connect_to_db():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Amar@12345',  
            database='MoneyTransferSystem'
        )
        return connection
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None
# Function to check if the user has sufficient balance
def check_sufficient_balance(username, amount):
    connection = connect_to_db()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT balance FROM users WHERE username = %s", (username,))
        balance = cursor.fetchone()
        if balance is None or balance[0] < amount:
            return False
        return True
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return False
    finally:
        connection.close()
# Function to update balance after a transaction
def update_balance(username, amount, operation):
    connection = connect_to_db()
    if connection is None:
        return
    try:
        cursor = connection.cursor()
        if operation == "deposit":
            cursor.execute("UPDATE users SET balance = balance + %s WHERE username = %s", (amount, username))
        elif operation == "withdraw":
            cursor.execute("UPDATE users SET balance = balance - %s WHERE username = %s", (amount, username))
        elif operation == "transfer_sender":
            cursor.execute("UPDATE users SET balance = balance - %s WHERE username = %s", (amount, username))
        elif operation == "transfer_receiver":
            cursor.execute("UPDATE users SET balance = balance + %s WHERE username = %s", (amount, username))
        connection.commit()
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        connection.close()
# Function to transfer money
def transfer_money(sender, receiver, amount):
    if not check_sufficient_balance(sender, amount):
        messagebox.showerror("Error", "Sender has insufficient funds.")
        return
    connection = connect_to_db()
    if connection is None:
        return    
    try:
        cursor = connection.cursor()
        # Update sender's balance
        update_balance(sender, amount, "transfer_sender")
        # Update receiver's balance
        update_balance(receiver, amount, "transfer_receiver")
        messagebox.showinfo("Success", f"Transferred {amount} from {sender} to {receiver}.")
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        connection.close()
# Function to create a new user
def create_user(username, password):
    connection = connect_to_db()
    if connection is None:
        return
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password, balance) VALUES (%s, %s, 0)", (username, password))
        connection.commit()
        messagebox.showinfo("Success", f"User {username} created successfully.")
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        connection.close()

# Function to check balance of the user
def check_balance(username):
    connection = connect_to_db()
    if connection is None:
        return
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT balance FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None
    finally:
        connection.close()

# Function to display Admin Dashboard
def admin_dashboard():
    for widget in root.winfo_children():
        widget.destroy()
    frame = tk.Frame(root)
    frame.pack(pady=20)
    tk.Label(frame, text="Admin Dashboard", font=("Arial", 26)).grid(row=0, columnspan=20, pady=80)

    # Admin buttons
    tk.Button(frame, text="Create New User",fg="white", bg="steelblue",height=3, width=25, command=create_user_interface).grid(row=1, columnspan=20, pady=15)
    tk.Button(frame, text="Deposit Money", bg="green", height=3, width=25, command=deposit_money_interface).grid(row=2, columnspan=20, pady=15)
    tk.Button(frame, text="Transfer Money", fg="white",bg="blue", height=3, width=25, command=transfer_money_interface).grid(row=3, columnspan=20, pady=15)
    tk.Button(frame, text="Withdraw Money",fg="white", bg="orange", height=3, width=25, command=withdraw_money_interface).grid(row=4, columnspan=20, pady=15)
    tk.Button(frame, text="Check Balance", bg="yellow", height=3, width=25, command=check_balance_interface).grid(row=5, columnspan=20, pady=15)
    tk.Button(frame, text="Exit",fg="white", bg="red", height=1, width=10, command=root.quit).grid(row=6, columnspan=10, pady=30)

# Function to handle creating a user interface
def create_user_interface():
    for widget in root.winfo_children():
        widget.destroy()
    frame = tk.Frame(root)
    frame.pack(pady=20)
    tk.Label(frame, text="Create New User", font=("Arial", 16)).grid(row=0, columnspan=2, pady=10)
    tk.Label(frame, text="Username:").grid(row=1, column=0, pady=5)
    tk.Label(frame, text="Password:").grid(row=2, column=0, pady=5)

    user_username_entry = tk.Entry(frame, width=30)
    user_password_entry = tk.Entry(frame, show="*", width=30)

    user_username_entry.grid(row=1, column=1, pady=5)
    user_password_entry.grid(row=2, column=1, pady=5)

    def submit_create_user():
        username = user_username_entry.get()
        password = user_password_entry.get()
        create_user(username, password)

    tk.Button(frame, text="Create User", command=submit_create_user).grid(row=3, columnspan=2, pady=10)
    tk.Button(frame, text="Back", command=admin_dashboard).grid(row=4, columnspan=2, pady=10)
# Function to handle Deposit Money Interface
def deposit_money_interface():
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root)
    frame.pack(pady=20)

    tk.Label(frame, text="Deposit Money", font=("Arial", 16)).grid(row=0, columnspan=2, pady=10)

    tk.Label(frame, text="Username:").grid(row=1, column=0, pady=5)
    tk.Label(frame, text="Amount:").grid(row=2, column=0, pady=5)

    username_entry = tk.Entry(frame, width=40)
    amount_entry = tk.Entry(frame, width=40)

    username_entry.grid(row=1, column=1, pady=5)
    amount_entry.grid(row=2, column=1, pady=5)

    def submit_deposit():
        username = username_entry.get()
        amount = float(amount_entry.get())
        if amount <= 0:
                messagebox.showerror("Invalid Amount", "Amount should be greater than 0.")
                return
        update_balance(username, amount, "deposit")
        messagebox.showinfo("Success", f"{amount} deposited to {username}'s account.")

    tk.Button(frame, text="Deposit", command=submit_deposit).grid(row=3, columnspan=2, pady=10)
    tk.Button(frame, text="Back", command=admin_dashboard).grid(row=4, columnspan=2, pady=10)

# Function to handle Withdraw Money Interface
def withdraw_money_interface():
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root)
    frame.pack(pady=20)

    tk.Label(frame, text="Withdraw Money", font=("Arial", 16)).grid(row=0, columnspan=2, pady=10)

    tk.Label(frame, text="Username:").grid(row=1, column=0, pady=5)
    tk.Label(frame, text="Amount:").grid(row=2, column=0, pady=5)

    username_entry = tk.Entry(frame, width=40)
    amount_entry = tk.Entry(frame, width=40)

    username_entry.grid(row=1, column=1, pady=5)
    amount_entry.grid(row=2, column=1, pady=5)

    def submit_withdraw():
        username = username_entry.get()
        amount = float(amount_entry.get())
        if amount <= 0:
                messagebox.showerror("Invalid Amount", "Amount should be greater than 0.")
                return
        if check_sufficient_balance(username, amount):
            update_balance(username, amount, "withdraw")
            messagebox.showinfo("Success", f"{amount} withdrawn from {username}'s account.")
        else:
            messagebox.showerror("Error", "Insufficient funds.")

    tk.Button(frame, text="Withdraw", command=submit_withdraw).grid(row=3, columnspan=2, pady=10)
    tk.Button(frame, text="Back", command=admin_dashboard).grid(row=4, columnspan=2, pady=10)

# Function to handle Transfer Money Interface
def transfer_money_interface():
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root)
    frame.pack(pady=20)

    tk.Label(frame, text="Transfer Money", font=("Arial", 16)).grid(row=0, columnspan=2, pady=10)

    tk.Label(frame, text="Sender Username:").grid(row=1, column=0, pady=5)
    tk.Label(frame, text="Receiver Username:").grid(row=2, column=0, pady=5)
    tk.Label(frame, text="Amount:").grid(row=3, column=0, pady=5)

    sender_entry = tk.Entry(frame, width=40)
    receiver_entry = tk.Entry(frame, width=40)
    amount_entry = tk.Entry(frame, width=40)

    sender_entry.grid(row=1, column=1, pady=5)
    receiver_entry.grid(row=2, column=1, pady=5)
    amount_entry.grid(row=3, column=1, pady=5)

    def submit_transfer():
        sender = sender_entry.get()
        receiver = receiver_entry.get()
        amount = float(amount_entry.get())
        if amount <= 0:
                messagebox.showerror("Invalid Amount", "Amount should be greater than 0.")
                return            
        transfer_money(sender, receiver, amount)

    tk.Button(frame, text="Transfer", command=submit_transfer).grid(row=4, columnspan=2, pady=10)
    tk.Button(frame, text="Back", command=admin_dashboard).grid(row=5, columnspan=2, pady=10)

# Function to handle Check Balance Interface
def check_balance_interface():
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root)
    frame.pack(pady=20)
    tk.Label(frame, text="Check Balance", font=("Arial", 16)).grid(row=0, columnspan=2, pady=10)
    tk.Label(frame, text="Username:").grid(row=1, column=0, pady=5)
    username_entry = tk.Entry(frame, width=40)
    username_entry.grid(row=1, column=1, pady=5)
    def submit_check_balance():
        username = username_entry.get()
        balance = check_balance(username)
        if balance is not None:
            messagebox.showinfo("Balance", f"{username} has a balance of {balance}.")
        else:
            messagebox.showerror("Error", "User not found.")

    tk.Button(frame, text="Check Balance", command=submit_check_balance).grid(row=2, columnspan=2, pady=10)
    tk.Button(frame, text="Back", command=admin_dashboard).grid(row=3, columnspan=2, pady=10)

# Function to handle Admin Login
def admin_login_interface():
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root)
    frame.pack(pady=80)
    tk.Label(frame, text="Admin Login", font=("Arial", 16)).grid(row=0, columnspan=2, pady=10)
    tk.Label(frame, text="Username:").grid(row=1, column=0, pady=10)
    tk.Label(frame, text="Password:").grid(row=2, column=0, pady=10)
    admin_username_entry = tk.Entry(frame, width=20)
    admin_password_entry = tk.Entry(frame, show="*", width=20)
    admin_username_entry.grid(row=1, column=1, pady=5)
    admin_password_entry.grid(row=2, column=1, pady=5)
    def submit_admin_login():
        if admin_username_entry.get() == "amar" and admin_password_entry.get() == "pass":
            admin_dashboard()
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

    tk.Button(frame, text="Login", command=submit_admin_login).grid(row=3, columnspan=2, pady=10)
    tk.Button(frame, text="Exit", command=root.quit).grid(row=4, columnspan=2, pady=10)
# Main GUI loop
root = tk.Tk()
root.title("Online Money Transfer System")
admin_login_interface()
root.mainloop()

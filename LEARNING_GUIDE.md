# Learning Guide - Accounting System Project

This guide will help you understand every part of the accounting system from basic Python concepts to advanced features.

## Table of Contents
1. [Python Basics](#python-basics)
2. [Database Fundamentals](#database-fundamentals)
3. [GUI Development](#gui-development)
4. [Project Architecture](#project-architecture)
5. [Advanced Features](#advanced-features)

---

## Python Basics

### Variables and Data Types
```python
# Strings
name = "John Doe"
print(name)  # Output: John Doe

# Numbers
balance = 1000.50
quantity = 5

# Lists (arrays)
accounts = ["Bank", "Cash", "Inventory"]
accounts.append("Receivables")  # Add to list

# Dictionaries (key-value pairs)
account = {
    "name": "Bank Account",
    "balance": 5000,
    "type": "Asset"
}
print(account["balance"])  # Output: 5000

# Boolean
is_active = True
```

### Functions
```python
# Define a function
def calculate_interest(principal, rate, years):
    """Calculate simple interest"""
    interest = principal * rate * years / 100
    return interest

# Call the function
result = calculate_interest(1000, 5, 2)
print(result)  # Output: 100
```

### Loops
```python
# For loop
accounts = ["Bank", "Cash", "Inventory"]
for account in accounts:
    print(account)

# While loop
counter = 0
while counter < 5:
    print(counter)
    counter += 1
```

### Conditional Statements
```python
balance = 500

if balance > 1000:
    print("High balance")
elif balance > 100:
    print("Medium balance")
else:
    print("Low balance")
```

### Classes and Objects
```python
class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Insufficient funds")

# Create an object
my_account = Account("Bank", 1000)
my_account.deposit(500)
print(my_account.balance)  # Output: 1500
```

---

## Database Fundamentals

### What is SQLite?
SQLite is a lightweight, file-based database. No server needed!

### Basic SQL Commands

#### CREATE TABLE
```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    account_type TEXT,
    balance REAL DEFAULT 0,
    created_date DATE
);
```

#### INSERT
```sql
INSERT INTO accounts (name, account_type, balance, created_date)
VALUES ('Bank Account', 'Asset', 5000, '2025-01-15');
```

#### SELECT
```sql
-- Get all accounts
SELECT * FROM accounts;

-- Get specific columns
SELECT name, balance FROM accounts;

-- With conditions
SELECT * FROM accounts WHERE balance > 1000;

-- Order by
SELECT * FROM accounts ORDER BY balance DESC;
```

#### UPDATE
```sql
UPDATE accounts 
SET balance = 6000 
WHERE name = 'Bank Account';
```

#### DELETE
```sql
DELETE FROM accounts WHERE id = 1;
```

### Python SQLite Example
```python
import sqlite3

# Connect to database
conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,
        name TEXT,
        balance REAL
    )
''')

# Insert data
cursor.execute(
    "INSERT INTO accounts (name, balance) VALUES (?, ?)",
    ("Bank", 5000)
)

# Query data
cursor.execute("SELECT * FROM accounts")
accounts = cursor.fetchall()
for account in accounts:
    print(account)

# Commit and close
conn.commit()
conn.close()
```

---

## GUI Development

### Tkinter Basics

#### Simple Window
```python
import tkinter as tk

root = tk.Tk()
root.title("My App")
root.geometry("400x300")

label = tk.Label(root, text="Hello, World!")
label.pack()

root.mainloop()
```

#### Widgets
```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Label
label = tk.Label(root, text="Name:")
label.pack()

# Entry (text input)
entry = tk.Entry(root, width=30)
entry.pack()

# Button
def on_click():
    print(entry.get())

button = tk.Button(root, text="Submit", command=on_click)
button.pack()

# Combobox
combo = ttk.Combobox(root, values=["Option 1", "Option 2"])
combo.pack()

root.mainloop()
```

#### Frames and Layout
```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Create frames
top_frame = ttk.Frame(root)
top_frame.pack(fill=tk.X, padx=10, pady=10)

bottom_frame = ttk.Frame(root)
bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Add widgets to frames
label = ttk.Label(top_frame, text="Input:")
label.pack(side=tk.LEFT)

entry = ttk.Entry(top_frame)
entry.pack(side=tk.LEFT, padx=5)

text = tk.Text(bottom_frame, height=10)
text.pack(fill=tk.BOTH, expand=True)

root.mainloop()
```

---

## Project Architecture

### Understanding the Accounting System Structure

#### 1. Database Layer (db_handler.py)
Responsible for all database operations.

```python
class DatabaseHandler:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()
```

#### 2. Business Logic Layer (modules/)
Each module handles specific business operations.

```python
class AccountingManager:
    def __init__(self, db_handler):
        self.db = db_handler
    
    def create_account(self, name, account_type):
        # Business logic here
        pass
```

#### 3. GUI Layer (gui/)
User interface for each module.

```python
class AccountingGUI:
    def __init__(self, parent, db_handler, manager):
        self.db = db_handler
        self.manager = manager
        # Create GUI here
```

### Data Flow
```
GUI (User Input)
  ↓
Business Logic (Processing)
  ↓
Database (Storage)
  ↓
GUI (Display Results)
```

---

## Advanced Features

### 1. Error Handling
```python
try:
    amount = float(input("Enter amount: "))
    if amount < 0:
        raise ValueError("Amount cannot be negative")
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 2. File Operations
```python
# Write to file
with open('data.txt', 'w') as file:
    file.write("Account Data\n")
    file.write("Balance: 5000")

# Read from file
with open('data.txt', 'r') as file:
    content = file.read()
    print(content)
```

### 3. DateTime Operations
```python
from datetime import datetime, timedelta

# Current date
today = datetime.now()
print(today.strftime('%Y-%m-%d'))  # 2025-05-09

# Add days
future = today + timedelta(days=30)

# Calculate difference
diff = (future - today).days
```

### 4. List Comprehensions
```python
# Traditional loop
balances = []
for account in accounts:
    balances.append(account['balance'])

# List comprehension (shorter)
balances = [account['balance'] for account in accounts]

# With condition
high_balances = [acc['balance'] for acc in accounts if acc['balance'] > 1000]
```

### 5. Decorators
```python
def validate_input(func):
    def wrapper(*args, **kwargs):
        if not args[0]:
            print("Input required")
            return
        return func(*args, **kwargs)
    return wrapper

@validate_input
def process_account(data):
    print(f"Processing: {data}")
```

---

## Practice Exercises

### Exercise 1: Create an Account Class
Create a class that represents a bank account with:
- Balance tracking
- Deposit method
- Withdraw method
- Interest calculation

### Exercise 2: Database Query
Write queries to:
- Get total balance across all accounts
- Find highest balance account
- Get accounts by type

### Exercise 3: GUI Form
Create a form to:
- Input account details
- Display account balance
- Update balance

### Exercise 4: Financial Calculation
Implement:
- Compound interest calculation
- Loan amortization
- Depreciation calculation

---

## Resources
- [Python Official Docs](https://docs.python.org/3/)
- [SQLite Tutorial](https://www.sqlite.org/docs.html)
- [Tkinter Reference](https://docs.python.org/3/library/tkinter.html)
- [Real Python Tutorials](https://realpython.com/)


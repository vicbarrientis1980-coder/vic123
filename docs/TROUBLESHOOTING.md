# Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: Application Won't Start

**Error:** `ModuleNotFoundError: No module named 'tkinter'`

**Cause:** Tkinter is not installed

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk

# Windows
# Tkinter is included with Python by default
# Reinstall Python and ensure "tcl/tk" is checked
```

---

### Issue 2: Database Error

**Error:** `sqlite3.OperationalError: no such table: accounts`

**Cause:** Database not initialized

**Solution:**
```python
# Delete the old database file
import os
if os.path.exists('accounting_system.db'):
    os.remove('accounting_system.db')

# Restart the application - it will create a new database
```

---

### Issue 3: Duplicate Accounts

**Problem:** Same account appearing multiple times

**Solution:**
```python
# Check for duplicates
query = """
    SELECT name, COUNT(*) as count
    FROM accounts
    GROUP BY name
    HAVING count > 1
"""
cursor.execute(query)
duplicates = cursor.fetchall()

# Delete duplicates manually or merge them
```

---

### Issue 4: Balance Doesn't Match

**Problem:** Account balance is wrong

**Solution:**
```python
# Verify transactions
def verify_balance(account_id):
    # Get recorded balance
    query = "SELECT balance FROM accounts WHERE id = ?"
    cursor.execute(query, (account_id,))
    recorded = cursor.fetchone()[0]
    
    # Calculate from transactions
    query = """
        SELECT SUM(CASE WHEN to_account_id = ? THEN amount ELSE -amount END)
        FROM transactions
        WHERE from_account_id = ? OR to_account_id = ?
    """
    cursor.execute(query, (account_id, account_id, account_id))
    calculated = cursor.fetchone()[0] or 0
    
    if recorded != calculated:
        print(f"Balance mismatch! Recorded: {recorded}, Calculated: {calculated}")
        # Fix it
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", 
                      (calculated, account_id))
        conn.commit()
```

---

### Issue 5: GUI Elements Not Showing

**Problem:** Buttons, labels, or tables not visible

**Solution:**
```python
# Common causes:
# 1. Widgets not packed/gridded
widget.pack()  # Add this

# 2. Widgets placed outside visible area
widget.pack(fill=tk.BOTH, expand=True)

# 3. Frame not expanding
frame.pack(fill=tk.BOTH, expand=True)

# 4. Text color same as background
widget = tk.Label(root, text="Text", fg="black", bg="white")
```

---

### Issue 6: Calculations Wrong

**Problem:** Depreciation, interest, or payments incorrect

**Solution:**
```python
# Check formula
# Example: Depreciation

# WRONG
depreciation = cost / years  # Missing residual value

# CORRECT
depreciation = (cost - residual_value) / years

# Test with known values
cost = 10000
years = 10
residual = 1000
expected = 900  # (10000 - 1000) / 10
calculated = (cost - residual) / years
assert calculated == expected, f"Expected {expected}, got {calculated}"
```

---

### Issue 7: Data Lost After Restart

**Problem:** Data not saved

**Solution:**
```python
# Ensure you call commit()
connection.commit()  # This saves data!

# Without this, data is not persisted

# Check in database_handler:
def save_data(self):
    self.conn.commit()  # Must be called
```

---

### Issue 8: Slow Performance

**Problem:** Application running slowly

**Solution:**
```python
# Add indexes to frequently searched columns
cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_account_type 
    ON accounts(account_type)
""")

# Limit result sets
query = "SELECT * FROM transactions LIMIT 1000"  # Get 1000 not all

# Use efficient queries
# INEFFICIENT
for account in get_all_accounts():
    if account['type'] == 'Asset':
        process(account)

# EFFICIENT
query = "SELECT * FROM accounts WHERE account_type = 'Asset'"
assets = cursor.execute(query).fetchall()
for account in assets:
    process(account)
```

---

## Debugging Tips

### 1. Print Debugging
```python
def record_transaction(from_account, to_account, amount):
    print(f"DEBUG: Recording transaction from {from_account} to {to_account}, amount: {amount}")
    
    try:
        # Your code
        pass
    except Exception as e:
        print(f"DEBUG: Error occurred: {e}")
        raise
```

### 2. Check Database Directly
```bash
# Open SQLite CLI
sqlite3 accounting_system.db

# Query your data
sqlite> SELECT * FROM accounts;
sqlite> SELECT COUNT(*) FROM transactions;
sqlite> .exit
```

### 3. Logging
```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.debug("Application started")
logging.info("Account created: Bank")
logging.error("Failed to save transaction")
```

### 4. Exception Handling
```python
try:
    amount = float(entry.get())
except ValueError as e:
    print(f"ValueError: {e}")
    messagebox.showerror("Error", "Please enter a valid number")
except Exception as e:
    print(f"Unexpected error: {e}")
    logging.exception("Unexpected error")
```

---

## Testing Your Code

### Unit Tests
```python
import unittest

class TestAccountingModule(unittest.TestCase):
    def setUp(self):
        # Setup before each test
        self.db = DatabaseHandler(':memory:')
    
    def test_create_account(self):
        account_id = self.db.create_account("Bank", "Asset")
        self.assertIsNotNone(account_id)
    
    def test_account_balance(self):
        account_id = self.db.create_account("Bank", "Asset")
        balance = self.db.get_balance(account_id)
        self.assertEqual(balance, 0)
    
    def tearDown(self):
        # Cleanup after each test
        self.db.close()

if __name__ == '__main__':
    unittest.main()
```

---

## Performance Monitoring

```python
import time

def time_function(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

@time_function
def get_all_transactions():
    # This will show how long it takes
    query = "SELECT * FROM transactions"
    return cursor.execute(query).fetchall()
```


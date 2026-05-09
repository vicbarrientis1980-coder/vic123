# Database Guide

## Database Schema

Your accounting system uses 10 interconnected tables:

### 1. Accounts Table
```
accounts
├── id (Primary Key)
├── name (Account name)
├── account_type (Asset, Liability, Equity, Income, Expense)
├── balance (Current balance)
└── created_date (Creation date)
```

**Purpose:** Stores all general ledger accounts.

### 2. Transactions Table
```
transactions
├── id (Primary Key)
├── from_account_id (FK)
├── to_account_id (FK)
├── amount (Transaction amount)
├── transaction_type (Debit/Credit)
├── description (Transaction details)
└── transaction_date (Date of transaction)
```

**Purpose:** Records all accounting transactions.

### 3. Fixed Assets Table
```
fixed_assets
├── id (Primary Key)
├── asset_name
├── asset_type (Building, Equipment, Vehicle, etc.)
├── purchase_price
├── purchase_date
├── useful_life (years)
├── depreciation_method (Straight-line, Declining-balance)
├── accumulated_depreciation
├── book_value
└── status (Active, Disposed)
```

**Purpose:** Tracks company assets and their depreciation.

### 4. Depreciation Records Table
```
depreciation_records
├── id (Primary Key)
├── asset_id (FK)
├── depreciation_month
├── depreciation_amount
└── accumulated_depreciation
```

**Purpose:** Records monthly depreciation calculations.

### 5. Inventory Items Table
```
inventory_items
├── id (Primary Key)
├── item_name
├── category
├── unit_price
├── quantity_on_hand
├── reorder_level
├── reorder_quantity
└── last_updated
```

**Purpose:** Maintains inventory catalog.

### 6. Inventory Movements Table
```
inventory_movements
├── id (Primary Key)
├── item_id (FK)
├── movement_type (Purchase, Sale, Adjustment, Transfer, Return, Damage)
├── quantity_moved
├── unit_cost
├── total_cost
├── reference_number
└── movement_date
```

**Purpose:** Tracks inventory in/out movements.

### 7. Loans Table
```
loans
├── id (Primary Key)
├── borrower_name
├── principal_amount
├── interest_rate
├── loan_term_months
├── monthly_payment
├── start_date
├── end_date
├── status (Active, Closed, Defaulted)
└── notes
```

**Purpose:** Records loan details.

### 8. Loan Payments Table
```
loan_payments
├── id (Primary Key)
├── loan_id (FK)
├── payment_date
├── principal_payment
├── interest_payment
├── total_payment
├── outstanding_balance
└── notes
```

**Purpose:** Tracks loan payment history.

### 9. Deposit Accounts Table
```
deposit_accounts
├── id (Primary Key)
├── account_holder_name
├── account_type (Time Deposit, Savings, Fixed Deposit)
├── opening_date
├── initial_deposit
├── current_balance
├── interest_rate
├── term_months
├── maturity_date
├── status (Active, Closed, Matured)
└── last_interest_credited
```

**Purpose:** Manages deposit accounts.

### 10. Deposit Transactions Table
```
deposit_transactions
├── id (Primary Key)
├── deposit_account_id (FK)
├── transaction_type (Deposit, Withdrawal, Interest, Tax, Penalty)
├── amount
├── transaction_date
└── notes
```

**Purpose:** Records deposit account transactions.

---

## Database Relationships

```
Accounts ──1:N──> Transactions
   ↓
   └─── Used for: Recording all financial transactions

Fixed Assets ──1:N──> Depreciation Records
   ↓
   └─── Used for: Tracking asset depreciation over time

Inventory Items ──1:N──> Inventory Movements
   ↓
   └─── Used for: Tracking stock movements

Loans ──1:N──> Loan Payments
   ↓
   └─── Used for: Tracking loan payments

Deposit Accounts ──1:N──> Deposit Transactions
   ↓
   └─── Used for: Tracking deposit activities
```

---

## Common Database Queries

### Get Account Balance
```python
query = "SELECT balance FROM accounts WHERE id = ?"
cursor.execute(query, (account_id,))
balance = cursor.fetchone()[0]
```

### Get Total Deposits
```python
query = "SELECT SUM(current_balance) FROM deposit_accounts WHERE status = 'Active'"
cursor.execute(query)
total = cursor.fetchone()[0]
```

### Get Asset Book Value
```python
query = """
    SELECT purchase_price - accumulated_depreciation as book_value
    FROM fixed_assets
    WHERE id = ?
"""
cursor.execute(query, (asset_id,))
book_value = cursor.fetchone()[0]
```

### Get Loan Outstanding Balance
```python
query = """
    SELECT outstanding_balance
    FROM loan_payments
    WHERE loan_id = ?
    ORDER BY payment_date DESC
    LIMIT 1
"""
cursor.execute(query, (loan_id,))
balance = cursor.fetchone()[0]
```

---

## Best Practices

### 1. Always Use Parameterized Queries
```python
# GOOD - Prevents SQL injection
cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))

# BAD - Security risk
cursor.execute(f"SELECT * FROM accounts WHERE id = {account_id}")
```

### 2. Use Transactions for Multiple Operations
```python
try:
    cursor.execute("INSERT INTO accounts ...")
    cursor.execute("UPDATE accounts ...")
    conn.commit()  # Save all changes
except Exception as e:
    conn.rollback()  # Undo all changes if error
    print(f"Error: {e}")
```

### 3. Create Indexes for Better Performance
```python
# For frequently searched columns
cursor.execute("CREATE INDEX idx_account_type ON accounts(account_type)")
```

### 4. Use Foreign Keys
```python
# Define relationships between tables
cursor.execute("""
    CREATE TABLE transactions (
        ...,
        from_account_id INTEGER,
        FOREIGN KEY (from_account_id) REFERENCES accounts(id)
    )
""")
```

---

## Database Optimization Tips

1. **Use appropriate data types** - TEXT for strings, INTEGER for whole numbers, REAL for decimals
2. **Add NOT NULL constraints** - Force required fields
3. **Use UNIQUE constraints** - Prevent duplicate entries
4. **Regular backups** - Save your database files regularly
5. **Query optimization** - Use WHERE clauses to filter data efficiently


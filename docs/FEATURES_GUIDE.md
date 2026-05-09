# Complete Features Guide

## Module 1: Accounting System

### Features
- Create accounts (Assets, Liabilities, Equity, Income, Expenses)
- Record transactions with automatic balance updates
- View general ledger
- Generate trial balance
- Account reconciliation
- Transaction history

### Key Calculations
```python
# Debit Entry
from_account.balance -= amount
to_account.balance += amount

# Trial Balance Verification
sum(debit_accounts) == sum(credit_accounts)
```

### How to Use
1. Create accounts for your business
2. Record transactions between accounts
3. View balance after each transaction
4. Generate reports

---

## Module 2: Fixed Assets Management

### Features
- Add fixed assets (buildings, equipment, vehicles)
- Calculate depreciation (straight-line & declining-balance methods)
- Track accumulated depreciation
- Calculate book value
- Record asset disposals
- Generate asset reports

### Depreciation Methods

#### Straight-Line Depreciation
```python
# Formula: (Cost - Salvage Value) / Useful Life
annual_depreciation = (100000 - 10000) / 10  # = $9000/year
monthly_depreciation = annual_depreciation / 12  # = $750/month
```

#### Declining-Balance Depreciation
```python
# Formula: Book Value × Depreciation Rate
# Depreciation Rate = 2 / Useful Life
rate = 2 / 10  # = 20% for 10-year asset
year1_depreciation = 100000 * 0.20  # = $20000
year2_depreciation = (100000 - 20000) * 0.20  # = $16000
```

### How to Use
1. Add asset with purchase price and useful life
2. Select depreciation method
3. System automatically calculates monthly depreciation
4. View depreciation schedule
5. Record disposal when asset is sold

---

## Module 3: Inventory Management

### Features
- Track inventory items by category
- Monitor stock levels and reorder points
- Record inventory movements (Purchase, Sale, Transfer, Adjustment, Return, Damage)
- Calculate inventory valuation
- Generate low-stock alerts
- Inventory aging reports

### Inventory Valuation Methods
```python
# FIFO (First In, First Out)
# Last purchase prices increase = Higher COGS, Lower Profit

# LIFO (Last In, First Out)
# Recent purchase prices = Lower COGS, Higher Profit

# Weighted Average
# Average cost across all units
```

### How to Use
1. Create inventory items with categories
2. Set reorder levels and quantities
3. Record purchases (inventory increase)
4. Record sales (inventory decrease)
5. Adjust for shrinkage or damage
6. View current stock levels
7. Generate reorder reports

---

## Module 4: Loan Management

### Features
- Create loan records with interest rates
- Calculate monthly payments (amortization)
- Record loan payments
- Breakdown payments into principal and interest
- Generate amortization schedules
- Track overdue loans
- Calculate loan status

### Loan Calculations

#### Monthly Payment (PMT Formula)
```python
# Formula: P × [r(1+r)^n] / [(1+r)^n - 1]
# P = Principal
# r = Monthly interest rate
# n = Number of payments

from math import pow

P = 100000  # Principal
annual_rate = 0.12  # 12%
months = 60  # 5 years

r = annual_rate / 12  # Monthly rate
monthly_payment = P * (r * pow(1 + r, months)) / (pow(1 + r, months) - 1)
```

#### Interest Portion of Payment
```python
outstanding_balance = 100000
monthly_rate = 0.01  # 1% monthly
interest_payment = outstanding_balance * monthly_rate
principal_payment = monthly_payment - interest_payment
```

### How to Use
1. Create loan with principal, interest rate, and term
2. System calculates monthly payment automatically
3. Record each payment
4. View amortization schedule
5. Track loan progress
6. Get alerts for overdue payments

---

## Module 5: Time & Savings Deposits

### Features
- Create deposit accounts (Fixed Term, Savings)
- Calculate and credit interest
- Record deposits and withdrawals
- Track accrued interest
- Automatic maturity notifications
- Close accounts with final calculations

### Interest Calculations

#### Simple Interest
```python
# Formula: P × R × T / 100
# P = Principal
# R = Annual interest rate
# T = Time in years

interest = 10000 * 5 * 1 / 100  # = $500 for 1 year at 5%
```

#### Compound Interest
```python
# Formula: P × (1 + r/n)^(n×t)
# P = Principal
# r = Annual rate
# n = Compounding frequency
# t = Time in years

from math import pow

P = 10000
r = 0.05  # 5%
n = 12  # Monthly
t = 1  # 1 year

final_amount = P * pow(1 + r/n, n*t)
interest = final_amount - P
```

### How to Use
1. Open deposit account with initial deposit
2. Set interest rate and term
3. Make additional deposits as needed
4. Interest accrues automatically
5. View accrued interest anytime
6. Close account at maturity

---

## Module 6: Financial Reports

### Reports Available

#### Income Statement (P&L)
```
Sales Revenue           $100,000
- Cost of Goods Sold   -$40,000
= Gross Profit         $60,000
- Operating Expenses   -$20,000
= Operating Income     $40,000
- Interest Expense     -$5,000
= Net Income           $35,000
```

#### Balance Sheet
```
ASSETS
Current Assets
  Cash                  $10,000
  Receivables          $20,000
  Inventory            $30,000
Total Current Assets   $60,000

Fixed Assets
  Equipment           $50,000
  - Depreciation     -$10,000
Net Fixed Assets       $40,000
TOTAL ASSETS          $100,000

LIABILITIES
Current Liabilities
  Payables            $15,000
Long-term Liabilities
  Loans               $30,000
Total Liabilities      $45,000

EQUITY
Capital              $55,000
TOTAL LIABILITY & EQUITY $100,000
```

#### Trial Balance
```
Account Name              Debit       Credit
Bank                    $10,000
Cash                     $5,000
Sales                              $40,000
Expenses                 $8,000
Assets                  $25,000
                       --------    --------
TOTALS                 $48,000    $40,000
```

---

## Data Validation Examples

### Account Creation
```python
def validate_account(name, account_type):
    if not name or len(name) < 3:
        return False, "Account name must be at least 3 characters"
    
    if account_type not in ['Asset', 'Liability', 'Equity', 'Income', 'Expense']:
        return False, "Invalid account type"
    
    return True, "Valid"
```

### Transaction Recording
```python
def validate_transaction(from_account, to_account, amount):
    if from_account == to_account:
        return False, "Cannot transfer to same account"
    
    if amount <= 0:
        return False, "Amount must be positive"
    
    if from_account_balance < amount:
        return False, "Insufficient funds"
    
    return True, "Valid"
```

---

## Integration Examples

### Complete Accounting Cycle
```python
# 1. Create accounts
accounting.create_account("Sales", "Income")
accounting.create_account("Expenses", "Expense")

# 2. Record transaction
accounting.record_transaction("Sales", "Expenses", 1000, "Daily sales")

# 3. View balance
balance = accounting.get_account_balance("Sales")

# 4. Generate report
report = accounting.generate_trial_balance()
```

### Asset Depreciation Tracking
```python
# 1. Add asset
assets.add_asset("Computer", 5000, "Equipment", 5)

# 2. Calculate monthly depreciation
depreciation = assets.calculate_depreciation(asset_id)

# 3. Update accounting ledger
accounting.record_transaction("Depreciation Expense", "Accumulated Depreciation", depreciation)

# 4. View book value
book_value = assets.get_book_value(asset_id)
```

---

## Tips for Success

1. **Always reconcile** - Verify transactions match your records
2. **Backup regularly** - Save your database daily
3. **Document transactions** - Add clear descriptions
4. **Review reports monthly** - Monitor financial health
5. **Validate inputs** - Prevent data entry errors
6. **Keep audit trail** - Record who made changes and when


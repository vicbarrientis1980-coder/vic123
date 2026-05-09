# Accounting System

A comprehensive desktop accounting system built with Python, Tkinter, and SQLite. This system manages:
- Accounting (General Ledger, Accounts, Transactions)
- Fixed Assets (Asset Tracking, Depreciation)
- Inventory Management (Stock Tracking, Movements)
- Loan Management (Loan Records, Payments, Interest)
- Time & Savings Deposits (Deposit Tracking, Interest Calculation)

## Tech Stack
- **Language:** Python 3.8+
- **GUI:** Tkinter (built-in)
- **Database:** SQLite
- **Version Control:** Git/GitHub

## Project Structure
```
accounting_system/
├── main.py                    # Application entry point
├── database/
│   └── db_handler.py         # Database initialization and operations
├── modules/
│   ├── accounting.py         # Accounting module logic
│   ├── fixed_assets.py       # Fixed assets module logic
│   ├── inventory.py          # Inventory module logic
│   ├── loans.py              # Loans module logic
│   └── deposits.py           # Deposits module logic
├── gui/
│   ├── main_window.py        # Main application window
│   ├── accounting_gui.py     # Accounting GUI
│   ├── fixed_assets_gui.py   # Fixed assets GUI
│   ├── inventory_gui.py      # Inventory GUI
│   ├── loans_gui.py          # Loans GUI
│   └── deposits_gui.py       # Deposits GUI
├── utils/
│   └── helpers.py            # Utility functions
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/vicbarrientis1980-coder/vic123.git
cd vic123
```

2. Run the application:
```bash
python main.py
```

## Features

### 1. Accounting Module
- Create and manage accounts (Assets, Liabilities, Equity, Income, Expenses)
- Record transactions
- View general ledger
- Generate financial reports

### 2. Fixed Assets Module
- Track fixed assets
- Calculate depreciation
- Maintain asset history

### 3. Inventory Management
- Track inventory items
- Monitor stock levels
- Record inventory movements (in/out)

### 4. Loan Management
- Create and track loans
- Record loan payments
- Calculate interest
- Track loan status

### 5. Time & Savings Deposits
- Manage deposit accounts
- Track deposits and withdrawals
- Calculate interest

## Usage
Run the main application and navigate through the menu to access different modules.

## Learning Resources
- [Python Official Documentation](https://docs.python.org/)
- [Tkinter Tutorial](https://docs.python.org/3/library/tkinter.html)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## License
MIT

## Author
vicbarrientis1980-coder

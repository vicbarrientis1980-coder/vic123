"""
Main Application - Accounting System
Complete business management system with accounting, fixed assets, inventory, loans, and deposits
"""

import tkinter as tk
from tkinter import ttk
import os

# Import database handler
from database.db_handler import DatabaseHandler

# Import all modules
from modules.accounting import AccountingManager
from modules.fixed_assets import FixedAssetsManager
from modules.inventory import InventoryManager
from modules.loans import LoanManager
from modules.deposits import DepositManager

# Import all GUI modules
from gui.main_window import MainWindow
from gui.accounting_gui import AccountingGUI
from gui.fixed_assets_gui import FixedAssetsGUI
from gui.inventory_gui import InventoryGUI
from gui.loans_gui import LoansGUI
from gui.deposits_gui import DepositsGUI

class AccountingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Integrated Accounting & Business Management System")
        self.root.geometry("1200x700")
        
        # Initialize database
        self.db = DatabaseHandler('accounting_system.db')
        
        # Initialize all managers
        self.accounting_manager = AccountingManager(self.db)
        self.assets_manager = FixedAssetsManager(self.db)
        self.inventory_manager = InventoryManager(self.db)
        self.loans_manager = LoanManager(self.db)
        self.deposits_manager = DepositManager(self.db)
        
        # Create main notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs for each module
        self.create_tabs()
    
    def create_tabs(self):
        """Create tabs for each module"""
        
        # Accounting Tab
        accounting_frame = ttk.Frame(self.notebook)
        self.notebook.add(accounting_frame, text="📊 Accounting")
        AccountingGUI(accounting_frame, self.db, self.accounting_manager)
        
        # Fixed Assets Tab
        assets_frame = ttk.Frame(self.notebook)
        self.notebook.add(assets_frame, text="🏗️ Fixed Assets")
        FixedAssetsGUI(assets_frame, self.db, self.assets_manager)
        
        # Inventory Tab
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text="📦 Inventory")
        InventoryGUI(inventory_frame, self.db, self.inventory_manager)
        
        # Loans Tab
        loans_frame = ttk.Frame(self.notebook)
        self.notebook.add(loans_frame, text="💰 Loans")
        LoansGUI(loans_frame, self.db, self.loans_manager)
        
        # Deposits Tab
        deposits_frame = ttk.Frame(self.notebook)
        self.notebook.add(deposits_frame, text="🏦 Deposits")
        DepositsGUI(deposits_frame, self.db, self.deposits_manager)

def main():
    root = tk.Tk()
    app = AccountingSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()

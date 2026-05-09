"""
Deposits GUI Module
Provides graphical interface for time & savings deposits management
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class DepositsGUI:
    def __init__(self, parent, db_handler, deposits_manager):
        self.parent = parent
        self.db = db_handler
        self.deposits_manager = deposits_manager
        
        # Create frame
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title = ttk.Label(self.frame, text="Time & Savings Deposits Management", 
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tabs
        self.create_new_account_tab()
        self.create_accounts_list_tab()
        self.create_transaction_tab()
        self.create_deposits_report_tab()
    
    def create_new_account_tab(self):
        """Create tab for opening new deposit accounts"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="New Account")
        
        # Form fields
        fields = [
            ("Account Holder Name:", "holder_name"),
            ("Account Type:", "account_type"),
            ("Opening Date (YYYY-MM-DD):", "opening_date"),
            ("Initial Deposit:", "initial_deposit"),
            ("Annual Interest Rate (%):", "interest_rate"),
            ("Term (months, 0 for savings):", "term_months"),
        ]
        
        self.account_entries = {}
        
        for label_text, key in fields:
            frame = ttk.Frame(tab)
            frame.pack(fill=tk.X, pady=5, padx=10)
            
            label = ttk.Label(frame, text=label_text, width=30)
            label.pack(side=tk.LEFT)
            
            entry = ttk.Entry(frame, width=30)
            entry.pack(side=tk.LEFT, padx=5)
            self.account_entries[key] = entry
        
        # Pre-fill date
        self.account_entries['opening_date'].insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Buttons
        button_frame = ttk.Frame(tab)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Create Account", 
                  command=self.create_account).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_account_form).pack(side=tk.LEFT, padx=5)
    
    def create_account(self):
        """Create a new deposit account"""
        try:
            term_months = int(self.account_entries['term_months'].get())
            
            # Calculate maturity date if term is specified
            maturity_date = None
            if term_months > 0:
                from datetime import timedelta
                opening = datetime.strptime(self.account_entries['opening_date'].get(), '%Y-%m-%d')
                maturity_date = (opening + timedelta(days=term_months*30)).strftime('%Y-%m-%d')
            
            account_id = self.deposits_manager.create_deposit_account(
                self.account_entries['holder_name'].get(),
                self.account_entries['account_type'].get(),
                self.account_entries['opening_date'].get(),
                float(self.account_entries['initial_deposit'].get()),
                float(self.account_entries['interest_rate'].get()),
                term_months,
                maturity_date
            )
            
            if account_id:
                messagebox.showinfo("Success", f"Account created successfully! ID: {account_id}")
                self.clear_account_form()
                self.refresh_accounts_list()
            else:
                messagebox.showerror("Error", "Failed to create account")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def clear_account_form(self):
        """Clear account form fields"""
        for entry in self.account_entries.values():
            if isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)
        self.account_entries['opening_date'].insert(0, datetime.now().strftime('%Y-%m-%d'))
    
    def create_accounts_list_tab(self):
        """Create tab showing all deposit accounts"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Accounts List")
        
        # Treeview
        columns = ("ID", "Holder", "Type", "Balance", "Interest Rate", "Accrued Interest", "Status")
        self.accounts_tree = ttk.Treeview(tab, columns=columns, height=15)
        self.accounts_tree.heading("#0", text="")
        self.accounts_tree.column("#0", width=0)
        
        for col in columns:
            self.accounts_tree.heading(col, text=col)
            self.accounts_tree.column(col, width=110)
        
        self.accounts_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=self.accounts_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.accounts_tree.configure(yscroll=scrollbar.set)
        
        # Refresh button
        ttk.Button(tab, text="Refresh", command=self.refresh_accounts_list).pack(pady=10)
        
        self.refresh_accounts_list()
    
    def refresh_accounts_list(self):
        """Refresh accounts list display"""
        for item in self.accounts_tree.get_children():
            self.accounts_tree.delete(item)
        
        accounts = self.deposits_manager.get_all_accounts(status=None)
        
        for account in accounts:
            account_id = account[0]
            accrued_interest = self.deposits_manager.calculate_interest(account_id)
            
            values = (
                account_id,
                account[1],
                account[2],
                f"${account[4]:,.2f}",
                f"{account[5]:.2f}%",
                f"${accrued_interest:,.2f}",
                account[6]
            )
            self.accounts_tree.insert("", tk.END, values=values)
    
    def create_transaction_tab(self):
        """Create tab for recording account transactions"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Transactions")
        
        # Account selection
        frame = ttk.Frame(tab)
        frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Label(frame, text="Select Account:", width=15).pack(side=tk.LEFT)
        
        self.transaction_account_var = tk.StringVar()
        self.transaction_combo = ttk.Combobox(frame, textvariable=self.transaction_account_var,
                                             width=40)
        self.transaction_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame, text="Load Account", 
                  command=self.load_transaction_account).pack(side=tk.LEFT, padx=5)
        
        # Account details
        self.transaction_details_text = tk.Text(tab, height=6, width=80)
        self.transaction_details_text.pack(pady=10, padx=10)
        self.transaction_details_text.config(state=tk.DISABLED)
        
        # Transaction form
        form_frame = ttk.LabelFrame(tab, text="Record Transaction")
        form_frame.pack(fill=tk.X, pady=10, padx=10)
        
        frame = ttk.Frame(form_frame)
        frame.pack(fill=tk.X, pady=5, padx=10)
        ttk.Label(frame, text="Transaction Type:").pack(side=tk.LEFT)
        self.transaction_type_combo = ttk.Combobox(frame, 
                                                  values=["Deposit", "Withdrawal", "Interest", "Tax", "Penalty"],
                                                  width=20)
        self.transaction_type_combo.pack(side=tk.LEFT, padx=5)
        
        frame = ttk.Frame(form_frame)
        frame.pack(fill=tk.X, pady=5, padx=10)
        ttk.Label(frame, text="Amount:").pack(side=tk.LEFT)
        self.transaction_amount_entry = ttk.Entry(frame, width=20)
        self.transaction_amount_entry.pack(side=tk.LEFT, padx=5)
        
        frame = ttk.Frame(form_frame)
        frame.pack(fill=tk.X, pady=5, padx=10)
        ttk.Label(frame, text="Transaction Date (YYYY-MM-DD):").pack(side=tk.LEFT)
        self.transaction_date_entry = ttk.Entry(frame, width=20)
        self.transaction_date_entry.pack(side=tk.LEFT, padx=5)
        self.transaction_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        frame = ttk.Frame(form_frame)
        frame.pack(fill=tk.X, pady=5, padx=10)
        ttk.Label(frame, text="Notes:").pack(side=tk.LEFT)
        self.transaction_notes_entry = ttk.Entry(frame, width=60)
        self.transaction_notes_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(form_frame, text="Record Transaction",
                  command=self.record_transaction).pack(pady=10)
        
        # Transaction history
        ttk.Label(tab, text="Transaction History:").pack(pady=10, padx=10)
        
        columns = ("Type", "Amount", "Date", "Notes")
        self.transaction_tree = ttk.Treeview(tab, columns=columns, height=10)
        self.transaction_tree.heading("#0", text="")
        self.transaction_tree.column("#0", width=0)
        
        for col in columns:
            self.transaction_tree.heading(col, text=col)
            self.transaction_tree.column(col, width=150)
        
        self.transaction_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Populate account combo
        self.update_transaction_combo()
    
    def update_transaction_combo(self):
        """Update account dropdown"""
        accounts = self.deposits_manager.get_all_accounts(status='Active')
        account_list = [f"{a[0]}: {a[1]}" for a in accounts]
        self.transaction_combo['values'] = account_list
    
    def load_transaction_account(self):
        """Load selected account for transactions"""
        selection = self.transaction_account_var.get()
        if not selection:
            messagebox.showwarning("Warning", "Please select an account")
            return
        
        account_id = int(selection.split(":")[0])
        details = self.deposits_manager.get_account_details(account_id)
        
        if details:
            _, holder, acc_type, opening_date, initial, balance, rate, term, maturity, status, last_credited = details
            
            accrued = self.deposits_manager.calculate_interest(account_id)
            
            text = f"Holder: {holder} | Type: {acc_type} | Balance: ${balance:,.2f} | Accrued Interest: ${accrued:,.2f} | Status: {status}"
            
            self.transaction_details_text.config(state=tk.NORMAL)
            self.transaction_details_text.delete(1.0, tk.END)
            self.transaction_details_text.insert(tk.END, text)
            self.transaction_details_text.config(state=tk.DISABLED)
            
            # Load transaction history
            for item in self.transaction_tree.get_children():
                self.transaction_tree.delete(item)
            
            history = self.deposits_manager.get_transaction_history(account_id, limit=20)
            for record in history:
                self.transaction_tree.insert("", tk.END, values=(
                    record[0],
                    f"${record[1]:,.2f}",
                    record[2],
                    record[3]
                ))
    
    def record_transaction(self):
        """Record deposit transaction"""
        selection = self.transaction_account_var.get()
        if not selection:
            messagebox.showwarning("Warning", "Please select an account")
            return
        
        account_id = int(selection.split(":")[0])
        
        try:
            transaction_id = self.deposits_manager.record_transaction(
                account_id,
                self.transaction_type_combo.get(),
                float(self.transaction_amount_entry.get()),
                self.transaction_date_entry.get(),
                self.transaction_notes_entry.get()
            )
            
            if transaction_id:
                messagebox.showinfo("Success", "Transaction recorded successfully")
                self.transaction_amount_entry.delete(0, tk.END)
                self.transaction_notes_entry.delete(0, tk.END)
                self.load_transaction_account()
                self.refresh_accounts_list()
            else:
                messagebox.showerror("Error", "Failed to record transaction")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def create_deposits_report_tab(self):
        """Create tab for deposit reports"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Reports")
        
        # Report text area
        self.deposits_report_text = tk.Text(tab, height=25, width=90)
        self.deposits_report_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.deposits_report_text.config(state=tk.DISABLED)
        
        # Buttons
        frame = ttk.Frame(tab)
        frame.pack(pady=10)
        
        ttk.Button(frame, text="Deposits Summary",
                  command=self.generate_deposits_summary).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Interest Report",
                  command=self.generate_interest_report).pack(side=tk.LEFT, padx=5)
    
    def generate_deposits_summary(self):
        """Generate deposits summary report"""
        summary = self.deposits_manager.get_deposits_summary()
        
        report = "DEPOSITS SUMMARY REPORT\n"
        report += "=" * 90 + "\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += f"Active Accounts: {summary.get('active_accounts', 0)}\n"
        report += f"Total Deposits: ${summary.get('total_deposits', 0):,.2f}\n"
        report += f"Total Accrued Interest: ${summary.get('total_interest_accrued', 0):,.2f}\n\n"
        
        report += f"{'ID':<5} {'Account Holder':<25} {'Type':<15} {'Balance':<15} {'Rate':<8} {'Interest':<15}\n"
        report += "-" * 90 + "\n"
        
        for account in summary.get('accounts', []):
            report += f"{account['id']:<5} {account['holder']:<25} {account['type']:<15} "
            report += f"${account['balance']:>13,.2f} {account['interest_rate']:>6.2f}% ${account['accrued_interest']:>13,.2f}\n"
        
        self.deposits_report_text.config(state=tk.NORMAL)
        self.deposits_report_text.delete(1.0, tk.END)
        self.deposits_report_text.insert(tk.END, report)
        self.deposits_report_text.config(state=tk.DISABLED)
    
    def generate_interest_report(self):
        """Generate interest report"""
        accounts = self.deposits_manager.get_all_accounts(status='Active')
        
        report = "DEPOSIT INTEREST REPORT\n"
        report += "=" * 80 + "\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += f"{'Holder':<25} {'Type':<15} {'Balance':<15} {'Rate':<8} {'Accrued':<15}\n"
        report += "-" * 80 + "\n"
        
        total_accrued = 0
        
        for account in accounts:
            account_id = account[0]
            accrued = self.deposits_manager.calculate_interest(account_id)
            total_accrued += accrued
            
            report += f"{account[1]:<25} {account[2]:<15} ${account[4]:>13,.2f} "
            report += f"{account[5]:>6.2f}% ${accrued:>13,.2f}\n"
        
        report += "-" * 80 + "\n"
        report += f"{'TOTAL ACCRUED INTEREST':<55} ${total_accrued:>13,.2f}\n"
        
        self.deposits_report_text.config(state=tk.NORMAL)
        self.deposits_report_text.delete(1.0, tk.END)
        self.deposits_report_text.insert(tk.END, report)
        self.deposits_report_text.config(state=tk.DISABLED)

# GUI Development Guide

## Tkinter Fundamentals

### 1. Main Application Window
```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Accounting System")
root.geometry("1200x700")

# Set minimum window size
root.minsize(800, 600)

# Run the application
root.mainloop()
```

### 2. Widgets Overview

#### Label
```python
label = tk.Label(root, text="Account Name:", font=("Arial", 12))
label.pack(pady=5)
```

#### Entry (Text Input)
```python
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Get value
value = entry.get()

# Set value
entry.insert(0, "Default Value")

# Clear value
entry.delete(0, tk.END)
```

#### Button
```python
def on_click():
    print("Button clicked!")

button = tk.Button(root, text="Submit", command=on_click)
button.pack(pady=5)
```

#### Combobox (Dropdown)
```python
combo = ttk.Combobox(root, values=["Option 1", "Option 2", "Option 3"])
combo.pack(pady=5)

# Get selected value
selected = combo.get()
```

#### Treeview (Table)
```python
columns = ("ID", "Name", "Balance")
tree = ttk.Treeview(root, columns=columns, height=10)

# Set column headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

# Add rows
tree.insert("", tk.END, values=(1, "Bank", "$5000"))

tree.pack(fill=tk.BOTH, expand=True)
```

#### Text (Multi-line Text)
```python
text = tk.Text(root, height=10, width=50)
text.pack(fill=tk.BOTH, expand=True)

# Get all text
content = text.get(1.0, tk.END)

# Insert text
text.insert(tk.END, "New text")

# Delete text
text.delete(1.0, tk.END)
```

#### Frame (Container)
```python
frame = ttk.Frame(root)
frame.pack(fill=tk.X, padx=10, pady=10)

# Add widgets to frame
label = ttk.Label(frame, text="Name:")
label.pack(side=tk.LEFT)

entry = ttk.Entry(frame)
entry.pack(side=tk.LEFT, padx=5)
```

### 3. Layout Managers

#### Pack
```python
# Simple stacking layout
widget.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
```

#### Grid
```python
# Table-like layout
label = tk.Label(root, text="Name:")
label.grid(row=0, column=0, padx=5, pady=5)

entry = tk.Entry(root)
entry.grid(row=0, column=1, padx=5, pady=5)
```

#### Place
```python
# Absolute positioning
button = tk.Button(root, text="Submit")
button.place(x=100, y=50, width=100, height=30)
```

---

## Building Forms

### Simple Form Example
```python
import tkinter as tk
from tkinter import ttk, messagebox

class AccountForm:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title = ttk.Label(self.frame, text="Create Account", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Form fields
        self.create_field("Account Name:", "name_entry")
        self.create_field("Account Type:", "type_combo")
        self.create_field("Initial Balance:", "balance_entry")
        
        # Buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Submit", command=self.submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=5)
    
    def create_field(self, label_text, field_name):
        frame = ttk.Frame(self.frame)
        frame.pack(fill=tk.X, pady=5)
        
        label = ttk.Label(frame, text=label_text, width=20)
        label.pack(side=tk.LEFT)
        
        if field_name.endswith("_combo"):
            widget = ttk.Combobox(frame, values=["Asset", "Liability", "Equity"])
        else:
            widget = ttk.Entry(frame)
        
        widget.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        setattr(self, field_name, widget)
    
    def submit(self):
        # Validate and process
        messagebox.showinfo("Success", "Account created!")
    
    def clear(self):
        self.name_entry.delete(0, tk.END)
        self.balance_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Account Form")
root.geometry("400x300")

form = AccountForm(root)

root.mainloop()
```

---

## Creating Tabs

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Tabbed Interface")

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Tab 1
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Accounts")
label1 = ttk.Label(tab1, text="Account Management")
label1.pack()

# Tab 2
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Transactions")
label2 = ttk.Label(tab2, text="Transaction Records")
label2.pack()

root.mainloop()
```

---

## Data Validation

```python
from tkinter import messagebox

def validate_amount(amount_str):
    """Validate that input is a positive number"""
    try:
        amount = float(amount_str)
        if amount < 0:
            messagebox.showerror("Error", "Amount must be positive")
            return False
        return True
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number")
        return False

def validate_required_fields(*fields):
    """Check that all fields have values"""
    for field, name in fields:
        if not field.get().strip():
            messagebox.showwarning("Warning", f"{name} is required")
            return False
    return True
```

---

## Event Handling

```python
import tkinter as tk

root = tk.Tk()

def on_button_click():
    print("Button clicked")

def on_entry_change(event):
    print(f"Entry value: {entry.get()}")

def on_key_press(event):
    print(f"Key pressed: {event.char}")

button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack()

entry = tk.Entry(root)
entry.bind("<KeyRelease>", on_entry_change)  # Triggered on every key
entry.bind("<Return>", on_key_press)  # Triggered on Enter key
entry.pack()

root.mainloop()
```

---

## Styling

### Colors and Fonts
```python
import tkinter as tk

root = tk.Tk()

# Text formatting
label = tk.Label(
    root,
    text="Accounting System",
    font=("Arial", 16, "bold"),
    fg="white",  # Foreground (text) color
    bg="blue"    # Background color
)
label.pack(padx=10, pady=10)

# Button styling
button = tk.Button(
    root,
    text="Submit",
    font=("Arial", 12),
    fg="white",
    bg="green",
    padx=20,
    pady=10
)
button.pack()

root.mainloop()
```

### Themes with ttk
```python
from tkinter import ttk

root = tk.Tk()

# Available styles
style = ttk.Style()
print(style.theme_names())  # ['clam', 'alt', 'default', 'classic']

style.theme_use('clam')

button = ttk.Button(root, text="Submit")
button.pack()

root.mainloop()
```

---

## Advanced: Custom Widgets

```python
import tkinter as tk
from tkinter import ttk

class CurrencyEntry(ttk.Entry):
    """Custom entry widget for currency input"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<KeyRelease>", self.format_currency)
    
    def format_currency(self, event=None):
        value = self.get().replace('$', '').replace(',', '')
        if value:
            try:
                formatted = f"${float(value):,.2f}"
                self.delete(0, tk.END)
                self.insert(0, formatted)
            except ValueError:
                pass
    
    def get_value(self):
        """Get numeric value without formatting"""
        return float(self.get().replace('$', '').replace(',', ''))

root = tk.Tk()
currency = CurrencyEntry(root, width=20)
currency.pack(padx=10, pady=10)

root.mainloop()
```

---

## Common GUI Patterns in Your App

### Pattern 1: List with Actions
```python
# Treeview for displaying data
# Buttons for Create, Edit, Delete
# Status bar for feedback
```

### Pattern 2: Master-Detail
```python
# Left side: List of items
# Right side: Details of selected item
```

### Pattern 3: Modal Dialogs
```python
from tkinter import simpledialog, filedialog

# Input dialog
name = simpledialog.askstring("Input", "Enter account name:")

# File dialog
filename = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
```


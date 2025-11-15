# PyQt5 Conversion Guide - CMMS_NEON2.2

## Overview
Complete conversion of Tkinter application to PyQt5 for modern, professional appearance and better functionality.

## Key Conversion Mappings

### 1. Application Structure

#### Tkinter
```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

root = tk.Tk()
app = AITCMMSSystem(root)
root.mainloop()
```

#### PyQt5
```python
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
import sys

app = QApplication(sys.argv)
app.setStyle('Fusion')  # Modern look
window = AITCMMSSystem()
window.show()
sys.exit(app.exec_())
```

### 2. Window Types

| Tkinter | PyQt5 | Notes |
|---------|-------|-------|
| `tk.Tk()` | `QApplication()` + `QMainWindow()` | Main application window |
| `tk.Toplevel()` | `QDialog()` or `QMainWindow()` | Modal dialogs |
| `tk.Frame` | `QWidget()` with layout | Container |
| `ttk.Notebook` | `QTabWidget()` | Tab interface |
| `ttk.Treeview` | `QTableWidget()` or `QTreeWidget()` | Data tables |

### 3. Widget Mapping

| Tkinter | PyQt5 | Usage |
|---------|-------|-------|
| `tk.Label` | `QLabel()` | Static text |
| `tk.Button` | `QPushButton()` | Clickable button |
| `ttk.Entry` / `tk.Entry` | `QLineEdit()` | Single line input |
| `tk.Text` | `QPlainTextEdit()` or `QTextEdit()` | Multi-line text |
| `ttk.Combobox` | `QComboBox()` | Dropdown selection |
| `ttk.Checkbutton` | `QCheckBox()` | Boolean option |
| `ttk.Radiobutton` | `QRadioButton()` | Mutually exclusive options |
| `tk.Listbox` | `QListWidget()` | List of items |
| `tk.Canvas` | `QGraphicsView()` | Drawing surface |
| `ttk.Progressbar` | `QProgressBar()` | Progress indication |
| `tk.Menu` | `QMenuBar()` | Menu bar |
| `ttk.Spinbox` | `QSpinBox()` / `QDoubleSpinBox()` | Numeric input |
| `ttk.Scale` | `QSlider()` | Value slider |
| `tk.Scrollbar` | Built-in to containers | Automatic scrolling |

### 4. Layout Management

#### Tkinter
```python
frame.grid(row=0, column=0, sticky='nsew')
button.pack(side='left', fill='x', expand=True)
label.place(x=10, y=10)
```

#### PyQt5
```python
layout = QVBoxLayout()  # Vertical stacking
layout.addWidget(button)
layout.addSpacing(10)
layout.addStretch()  # Like expand=True
widget.setLayout(layout)

# Or QHBoxLayout for horizontal
h_layout = QHBoxLayout()
```

### 5. Styling & Colors

#### Tkinter
```python
button.config(bg='#3498db', fg='white', font=('Arial', 10))
button.configure(width=20, height=2)
```

#### PyQt5
```python
# Using stylesheets (CSS-like)
button.setStyleSheet("""
    QPushButton {
        background-color: #3498db;
        color: white;
        font-size: 10pt;
        padding: 10px;
        border-radius: 5px;
        border: none;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
    QPushButton:pressed {
        background-color: #1f618d;
    }
""")

# Or using QPalette
palette = QPalette()
palette.setColor(QPalette.Button, QColor('#3498db'))
```

### 6. Signal/Slot Connections (Events)

#### Tkinter
```python
button.config(command=self.on_button_clicked)
entry.bind('<Return>', self.on_enter)
```

#### PyQt5
```python
button.clicked.connect(self.on_button_clicked)
entry.returnPressed.connect(self.on_enter)
```

### 7. Message Boxes

#### Tkinter
```python
from tkinter import messagebox
messagebox.showinfo("Title", "Message")
messagebox.showerror("Error", "Error message")
result = messagebox.askyesno("Confirm", "Are you sure?")
```

#### PyQt5
```python
from PyQt5.QtWidgets import QMessageBox
QMessageBox.information(self, "Title", "Message")
QMessageBox.critical(self, "Error", "Error message")
reply = QMessageBox.question(self, "Confirm", "Are you sure?",
                             QMessageBox.Yes | QMessageBox.No)
```

### 8. File Dialogs

#### Tkinter
```python
from tkinter import filedialog
filename = filedialog.askopenfilename()
path = filedialog.askdirectory()
```

#### PyQt5
```python
from PyQt5.QtWidgets import QFileDialog
filename, _ = QFileDialog.getOpenFileName(self, "Open File")
path = QFileDialog.getExistingDirectory(self, "Select Folder")
```

### 9. Threading & Long Operations

#### Tkinter
```python
def long_operation():
    # Does blocking work
    root.after(100, long_operation)  # Poor solution

# Better: Use threading
threading.Thread(target=worker, daemon=True).start()
```

#### PyQt5
```python
from PyQt5.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        # Do work
        self.progress.emit(50)
        self.finished.emit()

worker = WorkerThread()
worker.finished.connect(self.on_work_finished)
worker.start()
```

### 10. Data Display Tables

#### Tkinter with Treeview
```python
tree = ttk.Treeview(parent, columns=('col1', 'col2'))
tree.insert('', 'end', values=(val1, val2))
tree.bind('<<TreeviewSelect>>', on_select)
```

#### PyQt5 with QTableWidget
```python
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

table = QTableWidget()
table.setColumnCount(2)
table.setRowCount(10)
table.setItem(0, 0, QTableWidgetItem("Value"))
table.itemSelectionChanged.connect(on_select)
```

### 11. DPI Scaling (High Resolution Support)

#### Tkinter
```python
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)
scaling_factor = 1.6  # Manual adjustment

font = tk.Font(family="Arial", size=int(10 * scaling_factor))
```

#### PyQt5
```python
# PyQt5 handles DPI scaling automatically
# Use relative sizes:
font = QFont("Arial", 10)  # Points are DPI-aware

# For pixel-based measurements, use device-independent coordinates
self.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)
```

### 12. Consistent Application Styling

```python
def setup_application_style(app):
    """Apply consistent styling across entire application"""
    app.setStyle('Fusion')

    # Define color palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor('#f0f0f0'))
    palette.setColor(QPalette.WindowText, QColor('#2c3e50'))
    palette.setColor(QPalette.Base, QColor('white'))
    palette.setColor(QPalette.Button, QColor('#ecf0f1'))
    palette.setColor(QPalette.ButtonText, QColor('#2c3e50'))
    palette.setColor(QPalette.Highlight, QColor('#3498db'))
    palette.setColor(QPalette.HighlightedText, QColor('white'))
    app.setPalette(palette)

    # Define global stylesheet
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QLabel {
            color: #2c3e50;
            font-size: 10pt;
        }
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 15px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #1f618d;
        }
        QLineEdit, QComboBox, QTextEdit {
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            padding: 5px;
            background-color: white;
            color: #2c3e50;
        }
        QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
            border: 2px solid #3498db;
        }
    """)
```

### 13. Dialog Implementation Pattern

#### Tkinter
```python
def show_login_dialog(self):
    dialog = tk.Toplevel(self.root)
    dialog.title("Login")
    # Create widgets directly
    tk.Label(dialog, text="Username:").pack()
    entry = tk.Entry(dialog)
    entry.pack()
    # ...
```

#### PyQt5
```python
class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        layout.addWidget(username_label)
        layout.addWidget(self.username_input)

        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

# Usage
dialog = LoginDialog(self)
if dialog.exec_() == QDialog.Accepted:
    username = dialog.username_input.text()
```

## Key Principles for Conversion

1. **Maintain Business Logic** - Only change UI layer, keep all business logic identical
2. **Consistent Styling** - Use unified stylesheet for professional appearance
3. **Better Performance** - PyQt5 is generally faster, especially with large datasets
4. **DPI Aware by Default** - No special scaling needed
5. **Modern Features** - Use signals/slots instead of bindings
6. **Thread Safe** - Proper use of QThread for long operations
7. **Modular Structure** - Keep modules separated and independent

## File Conversion Order

1. `AIT_CMMS_REV3.py` - Main application (18,996 lines)
2. `AIT_CMMS_Visual.py` - Alternate main (15,122 lines)
3. `mro_stock_module.py` - MRO inventory (2,130 lines)
4. `equipment_history.py` - Equipment tracking (756 lines)
5. `cm_parts_integration.py` - Parts integration (528 lines)
6. `kpi_trend_analyzer.py` - KPI analysis (674 lines)
7. `user_management_ui.py` - User management (446 lines)
8. `password_change_ui.py` - Password dialog (181 lines)
9. `kpi_ui.py` - Ensure full integration (1,081 lines)
10. Test all features

## Testing Checklist

- [ ] Application launches without errors
- [ ] Login functionality works
- [ ] All tabs display correctly
- [ ] Equipment management CRUD operations
- [ ] PM scheduling and assignment
- [ ] Corrective maintenance workflow
- [ ] MRO inventory management
- [ ] KPI dashboard and reporting
- [ ] User management (for managers)
- [ ] Database connectivity and sync
- [ ] File import/export (CSV, PDF, Excel)
- [ ] High-DPI display support
- [ ] All dialogs open and function correctly
- [ ] Data integrity maintained
- [ ] Performance acceptable for large datasets

## Notes

- PyQt5 requires `pip install PyQt5`
- Keep PostgreSQL connection code unchanged
- Maintain all database logic
- Preserve all validation and business rules
- Test on Windows, Linux, and macOS if possible

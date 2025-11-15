# Equipment History Tab - Integration Guide

## Quick Start

### Step 1: Import the Module

Add to your main application file (e.g., `AIT_CMMS_REV3_PyQt5.py`):

```python
from equipment_history_tab_pyqt5 import EquipmentHistoryTab
```

### Step 2: Create the Tab

In your main window's tab initialization:

```python
# Create equipment history tab
self.equipment_history_tab = EquipmentHistoryTab(self.conn)

# Connect signals
self.equipment_history_tab.status_updated.connect(self.update_status_bar)

# Add to tab widget
self.tabs.addTab(self.equipment_history_tab, "Equipment History")
```

### Step 3: Complete Integration Example

```python
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from equipment_history_tab_pyqt5 import EquipmentHistoryTab
import psycopg2
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMMS NEON 2.2")
        self.resize(1400, 900)

        # Create database connection
        self.conn = self.create_connection()

        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Add equipment history tab
        self.equipment_history_tab = EquipmentHistoryTab(self.conn)
        self.equipment_history_tab.status_updated.connect(
            lambda msg: self.statusBar().showMessage(msg)
        )
        self.tabs.addTab(self.equipment_history_tab, "Equipment History")

    def create_connection(self):
        """Create database connection"""
        return psycopg2.connect(
            dbname="cmms_db",
            user="your_user",
            password="your_password",
            host="your_host",
            port="5432"
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
```

## Integration with Existing Tabs

### Equipment Tab Integration

Add a "View History" button to the Equipment Tab:

```python
# In equipment_tab_pyqt5.py

def create_controls_group(self):
    # ... existing code ...

    # Add history button
    history_btn = QPushButton("View History")
    history_btn.clicked.connect(self.view_equipment_history)
    layout.addWidget(history_btn)

def view_equipment_history(self):
    """Open equipment history for selected equipment"""
    selected_rows = self.equipment_table.selectionModel().selectedRows()
    if not selected_rows:
        QMessageBox.warning(self, "No Selection",
                          "Please select an equipment item first.")
        return

    row = selected_rows[0].row()
    bfm_no = self.equipment_table.item(row, 0).text()

    # Switch to history tab and select equipment
    main_window = self.window()
    tabs = main_window.findChild(QTabWidget)

    # Find history tab
    for i in range(tabs.count()):
        if tabs.tabText(i) == "Equipment History":
            tabs.setCurrentIndex(i)
            history_tab = tabs.widget(i)

            # Select equipment in combo box
            index = history_tab.equipment_combo.findData(bfm_no)
            if index >= 0:
                history_tab.equipment_combo.setCurrentIndex(index)
            break
```

### PM Completion Tab Integration

Add equipment history context menu:

```python
# In pm_completion_tab_pyqt5.py

def create_context_menu(self):
    """Create right-click context menu"""
    menu = QMenu(self)

    view_history_action = menu.addAction("View Equipment History")
    view_history_action.triggered.connect(self.view_equipment_history_from_pm)

    return menu

def view_equipment_history_from_pm(self):
    """View equipment history from PM completion context"""
    # Get selected PM's BFM number
    bfm_no = self.bfm_combo.currentData()

    if not bfm_no:
        return

    # Navigate to history tab
    main_window = self.window()
    tabs = main_window.findChild(QTabWidget)

    for i in range(tabs.count()):
        if tabs.tabText(i) == "Equipment History":
            tabs.setCurrentIndex(i)
            history_tab = tabs.widget(i)

            index = history_tab.equipment_combo.findData(bfm_no)
            if index >= 0:
                history_tab.equipment_combo.setCurrentIndex(index)
            break
```

### CM Management Tab Integration

Link CM records to equipment history:

```python
# In cm_management_tab_pyqt5.py

def add_history_button(self):
    """Add equipment history button to CM details"""
    self.history_btn = QPushButton("View Equipment History")
    self.history_btn.clicked.connect(self.view_equipment_history_from_cm)
    # Add to your layout

def view_equipment_history_from_cm(self):
    """Navigate to equipment history from CM"""
    # Get BFM number from selected CM
    selected_rows = self.cm_table.selectionModel().selectedRows()
    if not selected_rows:
        return

    row = selected_rows[0].row()
    bfm_no = self.cm_table.item(row, 1).text()  # Assuming column 1 is BFM

    # Navigate to history tab
    self.navigate_to_history(bfm_no)
```

## Advanced Features

### 1. Direct Equipment History Dialog

Create a standalone dialog for quick history viewing:

```python
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from equipment_history_tab_pyqt5 import EquipmentHistoryTab

class QuickHistoryDialog(QDialog):
    """Quick view dialog for equipment history"""

    def __init__(self, conn, bfm_no, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Equipment History - {bfm_no}")
        self.resize(1200, 800)

        layout = QVBoxLayout()

        # Create history tab
        self.history_widget = EquipmentHistoryTab(conn)
        layout.addWidget(self.history_widget)

        self.setLayout(layout)

        # Auto-select equipment
        index = self.history_widget.equipment_combo.findData(bfm_no)
        if index >= 0:
            self.history_widget.equipment_combo.setCurrentIndex(index)

# Usage
def show_quick_history(conn, bfm_no):
    dialog = QuickHistoryDialog(conn, bfm_no)
    dialog.exec_()
```

### 2. Custom Health Score Thresholds

Override health score calculation:

```python
class CustomEquipmentHistoryTab(EquipmentHistoryTab):
    """Custom implementation with different health scoring"""

    def calculate_health_score(self):
        """Custom health score with different weights"""
        # Your custom implementation
        pass
```

### 3. Export Automation

Automatically export history on schedule:

```python
from PyQt5.QtCore import QTimer

class ScheduledHistoryExport:
    """Automated history export"""

    def __init__(self, history_tab):
        self.history_tab = history_tab
        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_export)

    def start_daily_export(self):
        """Export history daily at midnight"""
        # Calculate milliseconds until midnight
        now = QDateTime.currentDateTime()
        midnight = now.addDays(1).date().startOfDay()
        msecs = now.msecsTo(midnight)

        self.timer.start(msecs)

    def auto_export(self):
        """Perform automatic export"""
        file_path = f"auto_export_{QDate.currentDate().toString('yyyyMMdd')}.csv"
        # Export logic here
```

## Database Schema Requirements

Ensure your database has these tables with proper columns:

### equipment table
```sql
CREATE TABLE equipment (
    bfm_equipment_no VARCHAR(50) PRIMARY KEY,
    short_description TEXT,
    status VARCHAR(50),
    monthly_pm CHAR(1),
    annual_pm CHAR(1)
    -- other columns...
);
```

### pm_completions table
```sql
CREATE TABLE pm_completions (
    id SERIAL PRIMARY KEY,
    bfm_equipment_no VARCHAR(50) REFERENCES equipment(bfm_equipment_no),
    completion_date DATE,
    pm_type VARCHAR(50),
    technician_name VARCHAR(100),
    labor_hours DECIMAL(10,2),
    notes TEXT,
    special_equipment TEXT
    -- other columns...
);
```

### corrective_maintenance table
```sql
CREATE TABLE corrective_maintenance (
    cm_number VARCHAR(50) PRIMARY KEY,
    bfm_equipment_no VARCHAR(50) REFERENCES equipment(bfm_equipment_no),
    reported_date DATE,
    closed_date DATE,
    description TEXT,
    priority VARCHAR(50),
    status VARCHAR(50),
    assigned_technician VARCHAR(100),
    labor_hours DECIMAL(10,2),
    notes TEXT,
    root_cause TEXT,
    corrective_action TEXT
    -- other columns...
);
```

### cm_parts_requests table
```sql
CREATE TABLE cm_parts_requests (
    id SERIAL PRIMARY KEY,
    cm_number VARCHAR(50) REFERENCES corrective_maintenance(cm_number),
    requested_date DATE,
    part_number VARCHAR(100),
    model_number VARCHAR(100),
    requested_by VARCHAR(100),
    notes TEXT
    -- other columns...
);
```

## Performance Optimization

### 1. Add Database Indexes

```sql
-- Indexes for faster queries
CREATE INDEX idx_pm_completions_bfm ON pm_completions(bfm_equipment_no);
CREATE INDEX idx_pm_completions_date ON pm_completions(completion_date);
CREATE INDEX idx_cm_bfm ON corrective_maintenance(bfm_equipment_no);
CREATE INDEX idx_cm_reported_date ON corrective_maintenance(reported_date);
CREATE INDEX idx_parts_requests_cm ON cm_parts_requests(cm_number);
```

### 2. Use Connection Pooling

```python
from database_utils import DatabaseConnectionPool

# In main application
pool = DatabaseConnectionPool()
pool.initialize(db_config)

# Get connection for history tab
conn = pool.get_connection()
history_tab = EquipmentHistoryTab(conn)

# Return connection when done
pool.return_connection(conn)
```

### 3. Lazy Loading

The tab already implements lazy loading - history is only loaded when equipment is selected.

## Testing

### Unit Test Example

```python
import unittest
from PyQt5.QtWidgets import QApplication
from equipment_history_tab_pyqt5 import EquipmentHistoryTab

class TestEquipmentHistoryTab(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        # Create test database connection
        self.conn = create_test_connection()
        self.tab = EquipmentHistoryTab(self.conn)

    def test_load_equipment_list(self):
        """Test loading equipment list"""
        self.tab.load_equipment_list()
        self.assertGreater(self.tab.equipment_combo.count(), 0)

    def test_filter_by_date(self):
        """Test date filtering"""
        self.tab.current_bfm = "TEST-001"
        self.tab.load_equipment_history()
        initial_count = len(self.tab.all_events)

        # Apply narrower date range
        self.tab.start_date.setDate(QDate.currentDate().addDays(-30))
        self.tab.apply_filters()

        # Should have same or fewer events
        self.assertLessEqual(
            self.tab.events_table.rowCount(),
            initial_count
        )

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
```

## Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Tab doesn't load | Check database connection and table permissions |
| Timeline blank | Verify events have valid dates in YYYY-MM-DD format |
| Health score shows "--" | Equipment needs monthly_pm or annual_pm flags set |
| Export fails | Check file write permissions and available disk space |
| Slow performance | Add database indexes (see Performance Optimization) |
| Signal not connecting | Ensure parent window has status bar or handle signal |

## Best Practices

1. **Always use connection pooling** in production
2. **Handle database errors gracefully** with rollback
3. **Commit after read operations** to prevent long transactions
4. **Use date pickers** for user input instead of text fields
5. **Provide visual feedback** for long operations
6. **Test with production data** before deployment

## Support

For integration support:
1. Review this integration guide
2. Check main README documentation
3. Review example code snippets
4. Contact development team

---

**Last Updated**: 2025-11-15
**Version**: 1.0.0

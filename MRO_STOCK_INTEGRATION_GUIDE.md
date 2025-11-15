# MRO Stock Tab Integration Guide

## Quick Integration Steps

### Step 1: Import the Module

Add this import to your main application file:

```python
from mro_stock_tab_pyqt5 import MROStockTab
```

### Step 2: Add to Tab Widget

In your main window class, add the MRO Stock tab to your tab widget:

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ... your existing initialization code ...

        # Create MRO Stock tab
        self.mro_stock_tab = MROStockTab(
            conn=self.conn,              # Your PostgreSQL connection
            current_user=self.username,   # Current logged-in user
            parent=self
        )

        # Connect signals
        self.mro_stock_tab.status_updated.connect(self.update_status_bar)

        # Add to tab widget
        self.tab_widget.addTab(self.mro_stock_tab, "MRO Stock")
```

### Step 3: Database Connection

Ensure you have a PostgreSQL connection with RealDictCursor:

```python
import psycopg2
from psycopg2.extras import RealDictCursor

self.conn = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_user",
    password="your_password",
    cursor_factory=RealDictCursor  # Important!
)
```

### Step 4: Status Bar (Optional)

If you want to receive status updates:

```python
def update_status_bar(self, message):
    """Update status bar with message from MRO tab"""
    self.statusBar().showMessage(message, 5000)  # Show for 5 seconds
```

## Complete Integration Example

```python
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
import psycopg2
from psycopg2.extras import RealDictCursor

# Import your other tabs
from equipment_tab_pyqt5 import EquipmentTab
from pm_completion_tab_pyqt5 import PMCompletionTab
from mro_stock_tab_pyqt5 import MROStockTab  # Add this


class CMMSMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AIT CMMS NEON 2.2")
        self.setGeometry(100, 100, 1400, 900)

        # Database connection
        self.conn = psycopg2.connect(
            host="localhost",
            database="cmms_db",
            user="cmms_user",
            password="your_password",
            cursor_factory=RealDictCursor
        )

        # Current user (from login)
        self.username = "John Doe"
        self.technicians = ["John Doe", "Jane Smith", "Bob Wilson"]

        # Create central widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create tabs
        self.create_tabs()

        # Status bar
        self.statusBar().showMessage("Ready")

    def create_tabs(self):
        """Create all application tabs"""

        # Equipment Tab
        self.equipment_tab = EquipmentTab(
            conn=self.conn,
            technicians=self.technicians,
            parent=self
        )
        self.equipment_tab.status_updated.connect(self.update_status_bar)
        self.tab_widget.addTab(self.equipment_tab, "Equipment")

        # PM Completion Tab
        self.pm_tab = PMCompletionTab(
            conn=self.conn,
            technicians=self.technicians,
            parent=self
        )
        self.pm_tab.status_updated.connect(self.update_status_bar)
        self.tab_widget.addTab(self.pm_tab, "PM Completion")

        # MRO Stock Tab (NEW!)
        self.mro_stock_tab = MROStockTab(
            conn=self.conn,
            current_user=self.username,
            parent=self
        )
        self.mro_stock_tab.status_updated.connect(self.update_status_bar)
        self.tab_widget.addTab(self.mro_stock_tab, "MRO Stock")

        # ... add other tabs ...

    def update_status_bar(self, message):
        """Update status bar with message"""
        self.statusBar().showMessage(message, 5000)

    def closeEvent(self, event):
        """Clean up database connection on close"""
        if self.conn:
            self.conn.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CMMSMainWindow()
    window.show()
    sys.exit(app.exec_())
```

## Database Initialization

The MRO Stock tab automatically initializes its database tables when instantiated. However, if you want to verify or manually create them:

```python
# The tab calls this automatically in __init__
mro_stock_tab.init_database()
```

This creates:
- `mro_inventory` table
- `mro_stock_transactions` table
- `cm_parts_used` table
- All necessary indexes

## Advanced Integration

### 1. Custom Current User

If you have a login system:

```python
class CMMSMainWindow(QMainWindow):
    def __init__(self, logged_in_user):
        super().__init__()
        self.current_user = logged_in_user

        # Pass to MRO tab
        self.mro_stock_tab = MROStockTab(
            conn=self.conn,
            current_user=self.current_user,  # Used in transactions
            parent=self
        )
```

### 2. Linking with CM Module

If you have a CM (Corrective Maintenance) module, you can link parts usage:

```python
# In your CM completion dialog:
def record_parts_used(self, cm_number, parts_list):
    """Record parts used in a CM"""
    cursor = self.conn.cursor()

    for part in parts_list:
        # Insert into cm_parts_used
        cursor.execute('''
            INSERT INTO cm_parts_used
            (cm_number, part_number, quantity_used, total_cost, recorded_by, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            cm_number,
            part['part_number'],
            part['quantity'],
            part['cost'],
            self.current_user,
            part.get('notes', '')
        ))

        # Update inventory
        cursor.execute('''
            UPDATE mro_inventory
            SET quantity_in_stock = quantity_in_stock - %s,
                last_updated = %s
            WHERE part_number = %s
        ''', (
            part['quantity'],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            part['part_number']
        ))

    self.conn.commit()

    # Refresh MRO tab if visible
    if hasattr(self.main_window, 'mro_stock_tab'):
        self.main_window.mro_stock_tab.refresh_inventory()
```

### 3. Low Stock Notifications

You can check for low stock items at startup:

```python
class CMMSMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ... initialization ...

        # Check for low stock items
        self.check_low_stock_on_startup()

    def check_low_stock_on_startup(self):
        """Check for low stock items on startup"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) as count
                FROM mro_inventory
                WHERE quantity_in_stock < minimum_stock
                AND status = 'Active'
            ''')

            result = cursor.fetchone()
            low_stock_count = result['count']

            if low_stock_count > 0:
                from PyQt5.QtWidgets import QMessageBox
                reply = QMessageBox.question(
                    self,
                    "Low Stock Alert",
                    f"There are {low_stock_count} items with low stock.\n\n"
                    f"Would you like to view them now?",
                    QMessageBox.Yes | QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    # Switch to MRO tab and show alert
                    self.tab_widget.setCurrentWidget(self.mro_stock_tab)
                    self.mro_stock_tab.show_low_stock_alert()

        except Exception as e:
            print(f"Error checking low stock: {e}")
```

### 4. Scheduled Reports

Generate automatic stock reports:

```python
from PyQt5.QtCore import QTimer

class CMMSMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ... initialization ...

        # Generate monthly stock report
        self.setup_monthly_report()

    def setup_monthly_report(self):
        """Setup timer for monthly stock report"""
        # Check every day at midnight
        timer = QTimer(self)
        timer.timeout.connect(self.check_monthly_report)
        timer.start(24 * 60 * 60 * 1000)  # 24 hours

    def check_monthly_report(self):
        """Check if it's time for monthly report"""
        from datetime import datetime

        # Run on the 1st of each month
        if datetime.now().day == 1:
            self.generate_monthly_stock_report()

    def generate_monthly_stock_report(self):
        """Generate and save monthly stock report"""
        # This would call the MRO tab's report generation
        # and automatically save to a specific location
        pass
```

## Troubleshooting Integration

### Issue: Import Error

```
ModuleNotFoundError: No module named 'mro_stock_tab_pyqt5'
```

**Solution**: Ensure `mro_stock_tab_pyqt5.py` is in the same directory as your main application file, or add it to your Python path.

### Issue: Database Connection Error

```
psycopg2.OperationalError: could not connect to server
```

**Solution**:
1. Verify PostgreSQL is running
2. Check connection parameters (host, database, user, password)
3. Ensure firewall allows connection
4. Verify database exists

### Issue: Table Already Exists Error

```
psycopg2.errors.DuplicateTable: relation "mro_inventory" already exists
```

**Solution**: This is normal! The `CREATE TABLE IF NOT EXISTS` statement handles this gracefully. The error is logged but doesn't stop execution.

### Issue: RealDictCursor Error

```
TypeError: 'str' object is not subscriptable
```

**Solution**: Make sure you're using `RealDictCursor`:

```python
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    ...,
    cursor_factory=RealDictCursor  # Important!
)
```

## Testing the Integration

After integration, test these features:

1. **Basic Operations**
   - [ ] Add a new part
   - [ ] Edit the part
   - [ ] Delete the part
   - [ ] View part details

2. **Search & Filter**
   - [ ] Search by name
   - [ ] Filter by system
   - [ ] Filter by status
   - [ ] Filter by location

3. **Stock Transactions**
   - [ ] Add stock
   - [ ] Remove stock
   - [ ] View transaction history

4. **Import/Export**
   - [ ] Export to CSV
   - [ ] Import from CSV
   - [ ] Verify data accuracy

5. **Reports**
   - [ ] Generate stock report
   - [ ] View low stock alert
   - [ ] Export report to file

6. **Pictures**
   - [ ] Upload picture
   - [ ] View picture in details
   - [ ] Update picture
   - [ ] Clear picture

## Performance Considerations

For large inventories (>10,000 parts):

1. **Pagination**: Consider adding pagination to the table
2. **Lazy Loading**: Load images on-demand rather than all at once
3. **Indexes**: Ensure all database indexes are created (automatic)
4. **Connection Pooling**: Use a connection pool for better performance

```python
from psycopg2 import pool

# Create connection pool
connection_pool = pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=10,
    host="localhost",
    database="cmms_db",
    user="cmms_user",
    password="your_password"
)

# Get connection
conn = connection_pool.getconn()

# Pass to MRO tab
mro_tab = MROStockTab(conn=conn, ...)

# Return connection when done
connection_pool.putconn(conn)
```

## Next Steps

After successful integration:

1. Import your existing inventory data via CSV
2. Set minimum stock levels for critical parts
3. Train users on the interface
4. Set up regular stock audits
5. Integrate with CM module for parts tracking
6. Generate baseline reports

## Support

For integration help:
- Review `MRO_STOCK_TAB_README.md` for detailed documentation
- Check code comments in `mro_stock_tab_pyqt5.py`
- Test with small dataset first
- Verify database permissions

---

**Last Updated**: 2025-11-15
**Status**: Production Ready ✓

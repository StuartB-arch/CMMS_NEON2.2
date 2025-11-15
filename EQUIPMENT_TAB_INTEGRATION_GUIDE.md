# Equipment Tab PyQt5 Integration Guide

## Overview

This document provides comprehensive instructions for integrating the `equipment_tab_pyqt5.py` module into your PyQt5-based CMMS application.

## File Location

- **Module File**: `/home/user/CMMS_NEON2.2/equipment_tab_pyqt5.py`
- **This Guide**: `/home/user/CMMS_NEON2.2/EQUIPMENT_TAB_INTEGRATION_GUIDE.md`

## Features

The Equipment Management Tab provides a complete PyQt5 implementation with the following features:

### Core Functionality
- **Equipment List Display**: QTableWidget with sortable columns
- **Real-time Search**: Filter equipment as you type
- **Location Filtering**: Dropdown filter by equipment location
- **Multi-select Support**: Select multiple equipment for bulk operations
- **Statistics Dashboard**: Real-time counts of Total, Cannot Find, Run to Failure, and Active assets

### Equipment Operations
- **Add Equipment**: Dialog to add new equipment with all fields
- **Edit Equipment**: Full editing capabilities including:
  - Standard fields (SAP, BFM, Description, Location, etc.)
  - PM cycle configuration (Monthly, Six Month, Annual)
  - Status management (Active, Run to Failure, Cannot Find)
  - Technician tracking for Cannot Find assets
- **Bulk Edit PM Cycles**: Update PM cycles for multiple assets at once
- **CSV Import**: Import equipment with intelligent column mapping
- **CSV Export**: Export complete equipment list

### Database Integration
- Full PostgreSQL support
- Transaction management with rollback on errors
- Foreign key constraint handling
- Conflict resolution (ON CONFLICT DO UPDATE)

## Integration Instructions

### Step 1: Import the Module

In your main PyQt5 application file, import the EquipmentTab class:

```python
from equipment_tab_pyqt5 import EquipmentTab
```

### Step 2: Create the Tab

In your main window class, create the equipment tab and add it to your tab widget:

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Your existing initialization code...
        self.conn = self.get_database_connection()
        self.technicians = self.load_technicians()  # Load from your config/database

        # Create tab widget (if you don't have one already)
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create and add Equipment Management tab
        self.equipment_tab = EquipmentTab(self.conn, self.technicians, parent=self)
        self.tab_widget.addTab(self.equipment_tab, "Equipment Management")

        # Connect status updates to your status bar (optional)
        self.equipment_tab.status_updated.connect(self.update_status_bar)

    def update_status_bar(self, message):
        """Update the status bar with messages from equipment tab"""
        if hasattr(self, 'statusBar'):
            self.statusBar().showMessage(message, 5000)  # Show for 5 seconds
```

### Step 3: Required Dependencies

Ensure you have the required dependencies installed:

```bash
pip install PyQt5 pandas psycopg2-binary
```

### Step 4: Database Schema

Ensure your database has the required tables. The Equipment tab requires:

#### Primary Table: `equipment`
```sql
CREATE TABLE IF NOT EXISTS equipment (
    id SERIAL PRIMARY KEY,
    sap_material_no TEXT,
    bfm_equipment_no TEXT UNIQUE,
    description TEXT,
    tool_id_drawing_no TEXT,
    location TEXT,
    master_lin TEXT,
    monthly_pm BOOLEAN DEFAULT FALSE,
    six_month_pm BOOLEAN DEFAULT FALSE,
    annual_pm BOOLEAN DEFAULT FALSE,
    last_monthly_pm TEXT,
    last_six_month_pm TEXT,
    last_annual_pm TEXT,
    next_monthly_pm TEXT,
    next_six_month_pm TEXT,
    next_annual_pm TEXT,
    status TEXT DEFAULT 'Active',
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Supporting Tables

**Cannot Find Assets**:
```sql
CREATE TABLE IF NOT EXISTS cannot_find_assets (
    id SERIAL PRIMARY KEY,
    bfm_equipment_no TEXT UNIQUE,
    description TEXT,
    location TEXT,
    technician_name TEXT,
    reported_date TEXT,
    status TEXT,
    notes TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Run to Failure Assets**:
```sql
CREATE TABLE IF NOT EXISTS run_to_failure_assets (
    id SERIAL PRIMARY KEY,
    bfm_equipment_no TEXT UNIQUE,
    description TEXT,
    location TEXT,
    technician_name TEXT,
    completion_date TEXT,
    labor_hours REAL,
    notes TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Usage Guide

### For End Users

#### Searching Equipment
1. Use the **Search Equipment** field to filter by SAP, BFM, Description, Location, or LIN
2. Filtering happens in real-time as you type
3. Use **Filter by Location** dropdown to filter by specific location
4. Click **Clear Filters** to reset all filters

#### Adding Equipment
1. Click **Add Equipment** button
2. Fill in the required fields:
   - SAP Material No (optional)
   - BFM Equipment No (required, must be unique)
   - Description
   - Tool ID/Drawing No
   - Location
   - Master LIN
3. Select PM cycles (Monthly, Six Month, Annual)
4. Click **Save** to add the equipment

#### Editing Equipment
1. Select equipment from the table (single click)
2. Click **Edit Equipment** button
3. Modify fields as needed
4. For special statuses:
   - **Run to Failure**: Check the "Set as Run to Failure Equipment" box
   - **Cannot Find**: Check "Mark as Cannot Find" and select reporting technician
5. Click **Update Equipment** to save changes

#### Bulk Editing PM Cycles
1. Select multiple equipment (Ctrl+Click or Shift+Click)
2. Click **Bulk Edit PM Cycles** button
3. Select which PM cycles to enable/disable
4. Click **Apply to All Selected**
5. Confirm the operation

#### Importing Equipment from CSV
1. Click **Import Equipment CSV** button
2. Select your CSV file
3. Map CSV columns to database fields:
   - The system will auto-detect common column names
   - Manually map any columns that weren't auto-detected
   - Leave unmapped fields as "(Not in CSV)"
4. Review sample data to verify mappings
5. Click **Import with These Mappings**
6. Review import results

#### Exporting Equipment
1. Click **Export Equipment** button
2. Choose save location and filename
3. Equipment list will be exported to CSV with all fields

### For Developers

#### Connecting Status Updates

The EquipmentTab emits a `status_updated` signal for status bar updates:

```python
self.equipment_tab.status_updated.connect(your_status_handler)
```

#### Accessing the Equipment Data

```python
# Get current equipment data
equipment_data = self.equipment_tab.equipment_data

# Refresh equipment list programmatically
self.equipment_tab.refresh_equipment_list()

# Update statistics
self.equipment_tab.update_equipment_statistics()
```

#### Customizing the Tab

You can customize the tab by modifying the source code:

**Change column widths**:
```python
# In create_equipment_table() method
header.setSectionResizeMode(0, QHeaderView.Fixed)
header.resizeSection(0, 150)  # Set SAP column to 150 pixels
```

**Add new columns**:
1. Update `create_equipment_table()` to add column
2. Update `refresh_equipment_list()` to populate column
3. Update `filter_equipment_list()` to filter column
4. Update dialog classes to handle new field

**Custom styling**:
```python
# Apply custom style sheet
self.equipment_table.setStyleSheet("""
    QTableWidget {
        background-color: white;
        alternate-background-color: #f0f0f0;
    }
""")
```

## Troubleshooting

### Issue: Database connection errors

**Solution**: Ensure your database connection is active and passed correctly to the tab:
```python
# Test connection
try:
    cursor = self.conn.cursor()
    cursor.execute('SELECT 1')
    print("Database connection OK")
except Exception as e:
    print(f"Database connection error: {e}")
```

### Issue: Import fails with encoding errors

**Solution**: The CSV import uses `cp1252` encoding by default. For other encodings:
```python
# In CSVMappingDialog.__init__(), change:
df = pd.read_csv(file_path, encoding='utf-8', nrows=5)
```

### Issue: Statistics not updating

**Solution**: Manually refresh statistics:
```python
self.equipment_tab.update_equipment_statistics()
```

### Issue: Table not sortable

**Solution**: Ensure sorting is enabled:
```python
self.equipment_table.setSortingEnabled(True)
```

## API Reference

### EquipmentTab Class

**Constructor**:
```python
EquipmentTab(conn, technicians, parent=None)
```
- `conn`: Database connection object (psycopg2 connection)
- `technicians`: List of technician names
- `parent`: Parent widget (optional)

**Signals**:
- `status_updated(str)`: Emitted when status message should be displayed

**Public Methods**:
- `refresh_equipment_list()`: Reload and display equipment data
- `load_equipment_data()`: Load equipment from database
- `filter_equipment_list()`: Apply current filters
- `clear_equipment_filters()`: Clear all filters
- `update_equipment_statistics()`: Refresh statistics display
- `populate_location_filter()`: Update location dropdown

### Dialog Classes

**AddEquipmentDialog**:
```python
AddEquipmentDialog(conn, parent=None)
```
- Returns: QDialog.Accepted if equipment was added, QDialog.Rejected if cancelled

**EditEquipmentDialog**:
```python
EditEquipmentDialog(conn, bfm_no, technicians, parent=None)
```
- `bfm_no`: BFM Equipment Number to edit
- Returns: QDialog.Accepted if updated, QDialog.Rejected if cancelled

**BulkEditPMCyclesDialog**:
```python
BulkEditPMCyclesDialog(conn, selected_bfms, parent=None)
```
- `selected_bfms`: List of BFM Equipment Numbers to update
- Returns: QDialog.Accepted if updated, QDialog.Rejected if cancelled

**CSVMappingDialog**:
```python
CSVMappingDialog(conn, file_path, parent=None)
```
- `file_path`: Path to CSV file to import
- Returns: QDialog.Accepted if imported, QDialog.Rejected if cancelled

## Complete Example

Here's a complete minimal example:

```python
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
import psycopg2
from equipment_tab_pyqt5 import EquipmentTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMMS - Equipment Management")
        self.resize(1200, 800)

        # Database connection
        self.conn = psycopg2.connect(
            host="localhost",
            database="cmms",
            user="your_user",
            password="your_password"
        )

        # Technician list
        self.technicians = [
            "John Smith",
            "Jane Doe",
            "Bob Johnson"
        ]

        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create equipment tab
        self.equipment_tab = EquipmentTab(
            self.conn,
            self.technicians,
            parent=self
        )

        # Connect status updates
        self.equipment_tab.status_updated.connect(
            lambda msg: self.statusBar().showMessage(msg, 5000)
        )

        # Add tab
        self.tabs.addTab(self.equipment_tab, "Equipment Management")

    def closeEvent(self, event):
        """Clean up database connection on close"""
        if hasattr(self, 'conn'):
            self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
```

## Migration from Tkinter

If you're migrating from the Tkinter version, here are the key differences:

| Tkinter | PyQt5 | Notes |
|---------|-------|-------|
| `ttk.Treeview` | `QTableWidget` | More flexible and feature-rich |
| `tk.StringVar()` | Direct widget access | No intermediate variables needed |
| `messagebox` | `QMessageBox` | Similar API, slightly different methods |
| `filedialog` | `QFileDialog` | Static methods return tuples |
| `.pack()`, `.grid()` | Layouts | More structured layout management |
| `bind()` | `connect()` | Signal/slot mechanism |
| `Toplevel` | `QDialog` | Modal dialogs built-in |

## Performance Considerations

- **Large Datasets**: The table widget handles thousands of rows efficiently
- **Filtering**: Real-time filtering is optimized for responsive UI
- **Database**: Uses connection pooling when available
- **Sorting**: Built-in sorting is hardware-accelerated

## Security Considerations

- **SQL Injection**: All queries use parameterized statements
- **Input Validation**: Add validation in dialog `save` methods if needed
- **Permissions**: Implement user role checking if required

## Support and Contributions

For issues or enhancements:
1. Check this guide first
2. Review the source code comments
3. Test with sample data
4. Document any bugs with screenshots and steps to reproduce

## License

This module is part of the CMMS system and follows the same license as the main application.

## Version History

- **v1.0** (2025-01-15): Initial PyQt5 implementation
  - Complete Equipment Management functionality
  - All dialog types (Add, Edit, Bulk Edit, CSV Import)
  - Full statistics dashboard
  - Search and filtering capabilities
  - Multi-select support
  - Database transaction management

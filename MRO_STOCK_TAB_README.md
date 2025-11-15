# MRO Stock Management Tab - PyQt5 Implementation

## Overview

Complete PyQt5 implementation of the MRO (Maintenance, Repair, Operations) Stock Management module, converted from the Tkinter version in `mro_stock_module.py` (~2,130 lines). This module provides comprehensive inventory management with advanced features for tracking parts, stock levels, transactions, and integration with Corrective Maintenance (CM) records.

## File Information

- **File**: `/home/user/CMMS_NEON2.2/mro_stock_tab_pyqt5.py`
- **Lines of Code**: ~2,400+ lines
- **Original Source**: `mro_stock_module.py` (Tkinter)
- **Status**: Production-ready ✓

## Key Features

### 1. Inventory Management
- **Complete CRUD Operations**: Add, Edit, Delete, and View parts
- **Advanced Search & Filtering**: Multi-field search with real-time filtering
- **Sortable Columns**: Click column headers to sort
- **Multi-Select**: Select and manage multiple items
- **Picture Support**: Store up to 2 pictures per part in database (BYTEA)
- **Status Tracking**: Active/Inactive status for each part

### 2. Stock Transaction Tracking
- **Add Stock**: Increase inventory quantities
- **Remove Stock**: Decrease inventory quantities
- **Transaction History**: Complete audit trail of all stock movements
- **Work Order Integration**: Link transactions to work orders
- **Technician Tracking**: Record who performed each transaction
- **Notes**: Add detailed notes to each transaction

### 3. Location Management
- **Hierarchical Storage**: Location → Rack → Row → Bin
- **Location Filter**: Quick filter by storage location
- **Supplier Tracking**: Track supplier for each part
- **Equipment Association**: Link parts to specific equipment

### 4. CM Integration
- **Parts Usage Tracking**: Track parts used in Corrective Maintenance
- **CM History**: View all CMs where a part was used
- **Cost Tracking**: Calculate total cost of parts used
- **Usage Statistics**: 30-day usage, total quantity used, cost analysis
- **Cross-Reference**: Link between MRO inventory and CM records

### 5. Import/Export
- **CSV Import**: Import parts with column mapping dialog
- **Auto-Mapping**: Automatically detect and map CSV columns
- **CSV Export**: Export entire inventory to CSV
- **Duplicate Handling**: Skip duplicates during import
- **Error Reporting**: Detailed error messages for import issues

### 6. Reports & Analytics
- **Stock Report**: Comprehensive inventory report with statistics
- **Low Stock Alerts**: Real-time alerts for items below minimum
- **Usage Reports**: Parts consumption analysis
- **Value Calculations**: Total inventory value tracking
- **Monthly Breakdown**: CM parts usage by month
- **Top 10 Reports**: Most used parts in CMs

### 7. Statistics Dashboard
- **Total Parts**: Count of active parts
- **Total Value**: Sum of inventory value (quantity × price)
- **Low Stock Count**: Number of items below minimum
- **Real-time Updates**: Automatic refresh after changes

## User Interface Components

### Main Window Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Inventory Statistics                                       │
│  Total Parts: 150 | Total Value: $45,250.00 | Low Stock: 12│
├─────────────────────────────────────────────────────────────┤
│  MRO Stock Controls                                         │
│  [Add] [Edit] [Delete] [Details] [Transaction]            │
│  [Import] [Export] [Report] [Low Stock Alert]              │
├─────────────────────────────────────────────────────────────┤
│  Search & Filters                                           │
│  Search: [________] System: [All ▼] Status: [Active ▼]    │
│  Location: [All ▼] [Refresh]                               │
├─────────────────────────────────────────────────────────────┤
│  Part# │ Name │ Model │ Equipment │ System │ Qty │ ...    │
│  ──────┼──────┼───────┼───────────┼────────┼─────┼────    │
│  P001  │Bearing│ XX123 │ Pump A    │ Mech   │ 25  │ ...    │
│  P002  │Filter │ YY456 │ Comp B    │ Hydr   │ 5   │ ...    │
│  ...                                                        │
└─────────────────────────────────────────────────────────────┘
```

### Dialog Windows

#### 1. Add/Edit Part Dialog
- **Scrollable Form**: Handles all fields without overwhelming screen
- **Picture Upload**: Browse and preview images (up to 2 per part)
- **Organized Sections**:
  - Basic Information (Name, Part Number, Model, Equipment)
  - Stock Information (System, Unit, Quantity, Price, Minimum, Supplier)
  - Location Information (Location, Rack, Row, Bin)
  - Status (Active/Inactive)
  - Pictures (2 images with preview)
  - Notes (Text area)
- **Validation**: Required fields marked with asterisk (*)
- **Read-only Part Number**: Prevent changes to part number when editing

#### 2. Part Details Dialog (3 Tabs)

**Tab 1: Part Information**
- Complete part details display
- Picture thumbnails (200x200 pixels)
- Stock status indicator (color-coded):
  - ✓ Green: Stock OK
  - ⚡ Orange: Stock Getting Low
  - ⚠ Red: LOW STOCK - Reorder Recommended
- Total value calculation

**Tab 2: CM Usage History**
- List of all CMs where part was used
- Statistics:
  - Total CMs
  - Total quantity used
  - Total cost
  - Usage last 30 days
- Sortable table with:
  - CM Number
  - Description
  - Equipment
  - Quantity Used
  - Cost
  - Date
  - Technician
  - Status
  - Notes

**Tab 3: All Transactions**
- Complete transaction history
- Color-coded quantities:
  - Green: Additions (+)
  - Red: Removals (-)
- Transaction details:
  - Date/Time
  - Type (Add/Remove)
  - Quantity
  - Technician
  - Work Order
  - Notes

#### 3. Stock Transaction Dialog
- Current stock display
- Transaction type selection (Add/Remove)
- Quantity input with validation
- Work order reference
- Notes field
- Prevents negative stock

#### 4. CSV Import Dialog
- File browser
- Column mapping interface
- Auto-detection of columns
- Required field validation
- Progress reporting
- Error handling

#### 5. Low Stock Alert Dialog
- Table of all low-stock items
- Shows:
  - Part Number
  - Name
  - Current Quantity
  - Minimum Required
  - Deficit
  - Unit
  - Location
  - Supplier
- Sortable columns
- Count in title

#### 6. Stock Report Dialog
- Comprehensive text report
- Sections:
  - Summary statistics
  - Low stock alerts
  - Inventory by engineering system
  - CM parts usage (monthly)
  - Top 10 most used parts
- Export to text file

## Database Schema

### Table: `mro_inventory`

```sql
CREATE TABLE mro_inventory (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    part_number TEXT UNIQUE NOT NULL,
    model_number TEXT,
    equipment TEXT,
    engineering_system TEXT,
    unit_of_measure TEXT,
    quantity_in_stock REAL DEFAULT 0,
    unit_price REAL DEFAULT 0,
    minimum_stock REAL DEFAULT 0,
    supplier TEXT,
    location TEXT,
    rack TEXT,
    row TEXT,
    bin TEXT,
    picture_1_path TEXT,
    picture_2_path TEXT,
    picture_1_data BYTEA,        -- Binary image data
    picture_2_data BYTEA,        -- Binary image data
    notes TEXT,
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'Active'
);
```

### Table: `mro_stock_transactions`

```sql
CREATE TABLE mro_stock_transactions (
    id SERIAL PRIMARY KEY,
    part_number TEXT NOT NULL,
    transaction_type TEXT NOT NULL,  -- 'Add' or 'Remove'
    quantity REAL NOT NULL,
    transaction_date TEXT DEFAULT CURRENT_TIMESTAMP,
    technician_name TEXT,
    work_order TEXT,
    notes TEXT,
    FOREIGN KEY (part_number) REFERENCES mro_inventory (part_number)
);
```

### Table: `cm_parts_used`

```sql
CREATE TABLE cm_parts_used (
    id SERIAL PRIMARY KEY,
    cm_number TEXT NOT NULL,
    part_number TEXT NOT NULL,
    quantity_used REAL NOT NULL,
    total_cost REAL DEFAULT 0,
    recorded_date TEXT DEFAULT CURRENT_TIMESTAMP,
    recorded_by TEXT,
    notes TEXT,
    FOREIGN KEY (part_number) REFERENCES mro_inventory (part_number)
);
```

### Performance Indexes

```sql
-- Basic indexes
CREATE INDEX idx_mro_part_number ON mro_inventory(part_number);
CREATE INDEX idx_mro_name ON mro_inventory(name);

-- Functional indexes for case-insensitive searches
CREATE INDEX idx_mro_engineering_system_lower ON mro_inventory(LOWER(engineering_system));
CREATE INDEX idx_mro_status_lower ON mro_inventory(LOWER(status));
CREATE INDEX idx_mro_location_lower ON mro_inventory(LOWER(location));

-- Transaction indexes
CREATE INDEX idx_mro_transactions_part_number ON mro_stock_transactions(part_number);
CREATE INDEX idx_mro_transactions_date ON mro_stock_transactions(transaction_date);

-- CM parts indexes
CREATE INDEX idx_cm_parts_cm_number ON cm_parts_used(cm_number);
CREATE INDEX idx_cm_parts_part_number ON cm_parts_used(part_number);
```

## Classes and Methods

### Main Class: `MROStockTab`

```python
class MROStockTab(QWidget):
    """Main MRO Stock Management Tab Widget"""

    # Signal
    status_updated = pyqtSignal(str)

    # Initialization
    def __init__(self, conn, current_user='System', parent=None)
    def init_database(self)
    def init_ui(self)

    # UI Creation
    def create_statistics_group(self) -> QGroupBox
    def create_controls_group(self) -> QGroupBox
    def create_search_frame(self) -> QFrame
    def create_inventory_table(self)

    # Data Operations
    def refresh_inventory(self)
    def filter_inventory(self)
    def update_location_filter(self)
    def update_statistics(self)

    # Part Management
    def add_part(self)
    def edit_selected_part(self)
    def delete_selected_part(self)
    def view_part_details(self)

    # Stock Operations
    def stock_transaction(self)

    # Import/Export
    def import_from_csv(self)
    def export_to_csv(self)

    # Reports
    def generate_stock_report(self)
    def show_low_stock_alert(self)
```

### Dialog Classes

```python
class AddEditPartDialog(QDialog):
    """Add or Edit Part Dialog"""
    def __init__(self, conn, part_data=None, parent=None)
    def setup_ui(self)
    def populate_fields(self)
    def browse_picture(self, pic_num)
    def clear_picture(self, pic_num)
    def update_picture_preview(self, pic_num)
    def validate_fields(self) -> bool
    def save_part(self)

class PartDetailsDialog(QDialog):
    """View Part Details with Tabs"""
    def __init__(self, conn, part_number, parent=None)
    def setup_ui(self)
    def setup_info_tab(self)
    def setup_cm_history_tab(self)
    def setup_transactions_tab(self)
    def load_data(self)
    def load_part_info(self, part_data)
    def load_cm_history(self, part_data)
    def load_transactions(self)

class StockTransactionDialog(QDialog):
    """Stock Transaction Dialog"""
    def __init__(self, conn, part_number, current_user='System', parent=None)
    def setup_ui(self)
    def load_current_stock(self)
    def process_transaction(self)

class CSVImportDialog(QDialog):
    """CSV Import Dialog with Column Mapping"""
    def __init__(self, conn, parent=None)
    def setup_ui(self)
    def browse_file(self)
    def load_csv_headers(self)
    def auto_map_columns(self)
    def import_csv(self)
```

## Integration Instructions

### Option 1: Add to Existing PyQt5 Application

```python
from mro_stock_tab_pyqt5 import MROStockTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Add MRO Stock tab
        self.mro_tab = MROStockTab(
            conn=self.conn,
            current_user=self.current_user
        )

        # Connect signals
        self.mro_tab.status_updated.connect(self.update_status_bar)

        # Add to tab widget
        self.tab_widget.addTab(self.mro_tab, "MRO Stock")
```

### Option 2: Standalone Application

```python
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import psycopg2
from psycopg2.extras import RealDictCursor
from mro_stock_tab_pyqt5 import MROStockTab

app = QApplication(sys.argv)

# Database connection
conn = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_user",
    password="your_password",
    cursor_factory=RealDictCursor
)

window = QMainWindow()
window.setWindowTitle("MRO Stock Management")
window.setGeometry(100, 100, 1400, 800)

tab = MROStockTab(conn, current_user="Your Name")
window.setCentralWidget(tab)

window.show()
sys.exit(app.exec_())
```

## Usage Examples

### Adding a New Part

1. Click **"Add New Part"** button
2. Fill in required fields (marked with *)
3. Optionally add pictures (Browse → Select Image)
4. Add notes if needed
5. Click **"Save"**

### Editing a Part

1. Select part in table
2. Click **"Edit Selected Part"**
3. Modify fields as needed
4. Pictures: Keep existing, replace, or clear
5. Click **"Update Part"**

### Stock Transaction

1. Select part in table
2. Click **"Stock Transaction"**
3. Choose "Add Stock" or "Remove Stock"
4. Enter quantity
5. Optionally add work order and notes
6. Click **"Save"**

### Importing from CSV

1. Click **"Import from CSV"**
2. Click **"Browse..."** and select CSV file
3. Map columns (auto-detection helps)
4. Verify required fields are mapped
5. Click **"OK"** to import

### Viewing Low Stock

1. Click **"Low Stock Alert"**
2. Review items below minimum
3. Plan reorders based on deficit
4. Close when done

### Generating Reports

1. Click **"Stock Report"**
2. Review comprehensive report
3. Click **"Export Report"** to save
4. Choose location and save

## Search and Filter Features

### Search Bar
Searches across multiple fields:
- Part Name
- Part Number
- Model Number
- Equipment
- Location

**Example**: Type "bearing" to find all parts with "bearing" in any field

### System Filter
Filter by engineering system:
- All (default)
- Mechanical
- Electrical
- Pneumatic
- Hydraulic
- Other

### Status Filter
Filter by status:
- Active (default)
- All
- Inactive
- Low Stock (items below minimum)

### Location Filter
- Dynamically populated from database
- Shows only locations that contain parts
- Updates automatically when inventory changes

## Color Coding

### Stock Status in Table
- **White Background**: Normal stock level
- **Light Red Background**: Below minimum stock
- **Red Text**: Status shows "⚠ LOW"

### Transaction Quantities
- **Green Text**: Positive quantities (additions)
- **Red Text**: Negative quantities (removals)

## Best Practices

### 1. Part Number Convention
- Use consistent format (e.g., P-XXXX or PART-XXXX)
- Make unique and descriptive
- Don't change after creation

### 2. Minimum Stock Levels
- Set based on:
  - Lead time from supplier
  - Usage rate (check CM history)
  - Critical equipment needs
  - Storage capacity

### 3. Pictures
- Use clear, well-lit photos
- Show identifying features
- Include multiple angles if needed
- Keep file sizes reasonable (<5MB)

### 4. Location Organization
- Consistent naming scheme
- Location: Building/Room (e.g., "WAREHOUSE-A")
- Rack: Shelf unit (e.g., "RACK-01")
- Row: Vertical position (e.g., "ROW-3")
- Bin: Horizontal position (e.g., "BIN-B")

### 5. Transactions
- Always add notes for context
- Reference work orders when applicable
- Regular audits to verify accuracy

### 6. CSV Import
- Use template from export
- Validate data before import
- Test with small batch first
- Keep backup before bulk import

## Error Handling

The module includes comprehensive error handling:

- **Database Errors**: Rollback on failure, show error message
- **Validation Errors**: Prevent invalid data entry
- **File Errors**: Graceful handling of missing/corrupt images
- **Import Errors**: Skip problematic rows, continue processing
- **Transaction Errors**: Prevent negative stock

## Performance Optimizations

### Database
- Indexes on commonly searched fields
- Functional indexes for case-insensitive searches
- Efficient queries with specific column selection
- Connection pooling ready

### UI
- Sortable table without re-querying
- Lazy loading for large datasets
- Responsive filtering
- Minimal UI blocking

## Known Limitations

1. **Picture Size**: Large images stored in database can increase DB size
2. **Concurrent Edits**: No locking mechanism for simultaneous edits
3. **Bulk Operations**: No bulk edit/delete (single item at a time)
4. **Barcode Support**: No built-in barcode scanning

## Future Enhancements

Potential improvements:
- Barcode generation and scanning
- Purchase order integration
- Automatic reorder suggestions
- Email alerts for low stock
- Mobile companion app
- QR code labels
- Bulk edit capability
- Vendor management module
- Price history tracking
- Alternative supplier tracking

## Troubleshooting

### Common Issues

**Issue**: Pictures not loading
- **Solution**: Check BYTEA column exists, verify image data

**Issue**: Slow filtering
- **Solution**: Ensure indexes are created, check database connection

**Issue**: Import fails
- **Solution**: Verify CSV format, check column mapping, review error messages

**Issue**: Cannot delete part
- **Solution**: Check for foreign key constraints (transactions, CM usage)

## Testing

The module includes a test harness at the bottom of the file:

```python
if __name__ == '__main__':
    # Test standalone
    # Update connection parameters
    # Run: python mro_stock_tab_pyqt5.py
```

## Dependencies

Required packages:
```
PyQt5 >= 5.15.0
psycopg2 >= 2.8.0
```

## File Structure

```
mro_stock_tab_pyqt5.py (2,400+ lines)
├── Imports and Documentation (50 lines)
├── AddEditPartDialog (400 lines)
├── PartDetailsDialog (500 lines)
├── StockTransactionDialog (200 lines)
├── CSVImportDialog (300 lines)
├── MROStockTab (Main Class) (900 lines)
└── Test Harness (50 lines)
```

## Support

For issues or questions:
1. Check this README
2. Review code comments
3. Check database connection and permissions
4. Verify all required tables and indexes exist

## License

Part of the AIT CMMS NEON 2.2 System

---

**Last Updated**: 2025-11-15
**Version**: 1.0
**Status**: Production Ready ✓

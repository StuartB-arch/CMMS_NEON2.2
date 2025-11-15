# PM Scheduling Tab Integration Guide

## Quick Start

### Step 1: Import the Module

Add to your PyQt5 main application file:

```python
from pm_scheduling_tab_pyqt5 import PMSchedulingTab
```

### Step 2: Create the Tab

In your main window's `__init__` or tab creation method:

```python
# Create PM Scheduling tab
self.pm_scheduling_tab = PMSchedulingTab(
    conn=self.conn,  # Your PostgreSQL database connection
    technicians=self.technicians,  # List of technician names
    parent=self
)

# Connect status signal to your status bar
self.pm_scheduling_tab.status_updated.connect(self.update_status)

# Add to your tab widget
self.main_tabs.addTab(self.pm_scheduling_tab, "PM Scheduling")
```

### Step 3: Ensure PMSchedulingService is Available

The module needs PMSchedulingService. You have two options:

**Option A: Use the version from AIT_CMMS_REV3.py** (Recommended)
- This version includes full database operations
- No additional code needed if you're already using AIT_CMMS_REV3.py

**Option B: Use pm_scheduler.py**
- Standalone module with core scheduling logic
- Module will automatically adapt to this version

### Step 4: Database Setup

Ensure these tables exist in your PostgreSQL database:
- `weekly_pm_schedules`
- `equipment`
- `pm_templates` (optional, for custom forms)
- `pm_completions`

See PM_SCHEDULING_TAB_README.md for complete schema.

### Step 5: Configure Technicians

Set your technician list before creating the tab:

```python
self.technicians = [
    'John Smith',
    'Jane Doe',
    'Bob Johnson',
    'Alice Williams'
]
```

## Complete Example

```python
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget
from pm_scheduling_tab_pyqt5 import PMSchedulingTab
import psycopg2

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AIT CMMS System")
        self.setGeometry(100, 100, 1400, 900)

        # Database connection
        self.conn = psycopg2.connect(
            host="localhost",
            database="cmms_db",
            user="postgres",
            password="your_password"
        )

        # Technician list
        self.technicians = ['John Smith', 'Jane Doe', 'Bob Johnson']

        # Create central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Add PM Scheduling tab
        self.pm_scheduling_tab = PMSchedulingTab(
            conn=self.conn,
            technicians=self.technicians,
            parent=self
        )
        self.pm_scheduling_tab.status_updated.connect(self.update_status)
        self.tabs.addTab(self.pm_scheduling_tab, "PM Scheduling")

        # Status bar
        self.statusBar().showMessage("Ready")

    def update_status(self, message):
        """Update status bar with message"""
        self.statusBar().showMessage(message)

    def closeEvent(self, event):
        """Close database connection on exit"""
        if self.conn:
            self.conn.close()
        event.accept()

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
```

## Configuration Options

### Weekly PM Target

Change the target number of PMs per week:

```python
self.pm_scheduling_tab.weekly_pm_target = 150  # Default is 130
```

### Current Week Start

The module automatically calculates the current week (Monday):

```python
# This is set automatically, but you can override:
from datetime import datetime, timedelta
today = datetime.now()
self.pm_scheduling_tab.current_week_start = today - timedelta(days=today.weekday())
```

## File Structure

After integration, your project should have:

```
your_project/
├── pm_scheduling_tab_pyqt5.py      # Main module (provided)
├── PM_SCHEDULING_TAB_README.md     # Documentation (provided)
├── INTEGRATION_GUIDE.md            # This file (provided)
├── pm_scheduler.py                 # Scheduling algorithm (should exist)
├── img/
│   └── ait_logo.png               # Company logo for PDF forms
└── your_main_app.py               # Your main application
```

## Required Python Packages

Install these packages if not already available:

```bash
pip install PyQt5
pip install pandas
pip install openpyxl
pip install reportlab
pip install psycopg2-binary
```

Or use requirements.txt:

```txt
PyQt5>=5.15.0
pandas>=1.3.0
openpyxl>=3.0.0
reportlab>=3.6.0
psycopg2-binary>=2.9.0
```

## Testing the Integration

1. **Test Week Selector**:
   - Launch application
   - Click on PM Scheduling tab
   - Verify week selector shows available weeks

2. **Test Technician Tabs**:
   - Check that all technician tabs appear
   - Click through tabs to verify they load correctly

3. **Test Schedule Generation**:
   - Select a future week
   - Click "Generate Weekly Schedule"
   - Verify confirmation message appears
   - Check that assignments appear in technician tabs

4. **Test PDF Generation**:
   - Generate a schedule first
   - Click "Print PM Forms"
   - Verify PDF files are created in new folder
   - Open PDFs to check formatting

5. **Test Excel Export**:
   - Click "Export Schedule"
   - Save file
   - Open in Excel to verify data

6. **Test Technician Exclusion**:
   - Select one or more technicians in exclusion list
   - Generate schedule
   - Verify excluded technicians receive no assignments

## Troubleshooting

### "PMSchedulingService is not available"
- Ensure pm_scheduler.py is in the same directory
- Or ensure PMSchedulingService is defined in your main application
- Check import statement at top of pm_scheduling_tab_pyqt5.py

### "No weekly schedules found"
- This is normal if no schedules have been generated yet
- Click "Generate Weekly Schedule" to create first schedule

### "Error populating week selector"
- Check database connection
- Verify weekly_pm_schedules table exists
- Check PostgreSQL credentials

### PDF generation fails
- Ensure reportlab is installed: `pip install reportlab`
- Check that img/ait_logo.png exists (or remove logo loading code)
- Verify write permissions in current directory

### Excel export fails
- Ensure pandas and openpyxl are installed
- Check write permissions in target directory
- Verify data exists in database

### Schedule generation is slow
- Normal for large equipment lists (2000+ items)
- Progress messages appear in console
- UI remains responsive during processing

## Performance Tips

1. **Bulk Operations**: The module uses bulk loading for performance
2. **Database Indexes**: Create indexes on frequently queried columns:
   ```sql
   CREATE INDEX idx_weekly_schedules_week ON weekly_pm_schedules(week_start_date);
   CREATE INDEX idx_weekly_schedules_tech ON weekly_pm_schedules(assigned_technician);
   CREATE INDEX idx_equipment_bfm ON equipment(bfm_equipment_no);
   ```
3. **Connection Pooling**: Use database connection pooling for better performance
4. **Caching**: The scheduling service caches data during generation

## Next Steps

1. Review PM_SCHEDULING_TAB_README.md for detailed feature documentation
2. Test all features in your environment
3. Customize PDF forms with your logo and branding
4. Set up priority asset CSV files (PM_LIST_A220_1.csv, etc.)
5. Configure technician list in your main application
6. Set up regular database backups

## Support

For additional help:
1. Check console output for detailed error messages
2. Review PM_SCHEDULING_TAB_README.md for feature details
3. Verify database schema matches requirements
4. Ensure all required packages are installed

## Migration from Tkinter Version

If migrating from the Tkinter version:

1. **Same Database**: Uses same database schema - no changes needed
2. **Same Logic**: Uses same PMSchedulingService - behavior is identical
3. **Same Features**: All features from Tkinter version are included
4. **Enhanced UI**: PyQt5 provides better performance and appearance

Key differences:
- `QTableWidget` instead of `ttk.Treeview`
- `QComboBox` instead of `ttk.Combobox`
- `QListWidget` instead of `tk.Listbox`
- Signals instead of callbacks
- Better high-DPI support

The business logic and database operations are identical.

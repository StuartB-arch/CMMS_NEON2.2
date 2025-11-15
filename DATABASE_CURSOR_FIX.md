# PyQt5 Database Cursor Fix - CRITICAL

## Problem Description

When running the PyQt5 CMMS application, you may encounter errors like:
```
AttributeError: 'tuple' object has no attribute 'xxx'
TypeError: list indices must be integers or slices, not str
```

## Root Cause

The issue occurs because:

1. The main application passes a raw PostgreSQL connection to the tabs
2. When tabs create cursors with `conn.cursor()`, they don't specify the cursor factory
3. Without specifying `cursor_factory=extras.RealDictCursor`, cursors return tuples instead of dictionaries
4. Code that expects dictionary-like access (e.g., `row['column_name']`) fails

## Solution

All tabs must create cursors with the proper cursor factory. Change:

```python
# WRONG - Returns tuples
cursor = self.conn.cursor()
```

To:

```python
# CORRECT - Returns dictionaries
from psycopg2 import extras
cursor = self.conn.cursor(cursor_factory=extras.RealDictCursor)
```

## Files to Fix

The following tab files need to be updated:

1. **equipment_tab_pyqt5.py** - All cursor() calls
2. **pm_scheduling_tab_pyqt5.py** - All cursor() calls
3. **pm_completion_tab_pyqt5.py** - All cursor() calls
4. **cm_management_tab_pyqt5.py** - All cursor() calls
5. **mro_stock_tab_pyqt5.py** - All cursor() calls
6. **equipment_history_tab_pyqt5.py** - All cursor() calls
7. **kpi_trend_analyzer_tab_pyqt5.py** - All cursor() calls

## Quick Fix Script

Run this command to add the import and fix all cursor() calls:

```bash
#!/bin/bash

# Add import to each file if not already there
for file in equipment_tab_pyqt5.py pm_scheduling_tab_pyqt5.py pm_completion_tab_pyqt5.py \
            cm_management_tab_pyqt5.py mro_stock_tab_pyqt5.py equipment_history_tab_pyqt5.py \
            kpi_trend_analyzer_tab_pyqt5.py; do

    # Add import at the top if not already there
    if ! grep -q "from psycopg2 import extras" "$file"; then
        sed -i '1a from psycopg2 import extras' "$file"
    fi

    # Replace all cursor() calls with cursor(cursor_factory=extras.RealDictCursor)
    sed -i 's/cursor = self\.conn\.cursor()/cursor = self.conn.cursor(cursor_factory=extras.RealDictCursor)/g' "$file"
done

echo "All files have been fixed!"
```

## Manual Fix Instructions

For each tab file:

1. Add import at the top:
```python
from psycopg2 import extras
```

2. Find all instances of:
```python
cursor = self.conn.cursor()
```

3. Replace with:
```python
cursor = self.conn.cursor(cursor_factory=extras.RealDictCursor)
```

## Verification

After making the changes, test with:

```bash
python3 AIT_CMMS_REV3_PyQt5.py
```

The application should start without database attribute errors.

## Alternative Approach (If Above Doesn't Work)

If you still get errors, you can also modify how data is accessed:

Instead of expecting dictionaries:
```python
# DON'T DO THIS (expects dictionaries)
equipment_name = row['short_description']
```

Use tuple indexing:
```python
# DO THIS (works with tuples)
equipment_name = row[1]  # Use column index
```

But the RealDictCursor approach is preferred as it's more readable and maintainable.

## Database Connection Best Practice

For new code going forward, use the proper context manager:

```python
from database_utils import db_pool

# Good way to do database operations
with db_pool.get_cursor() as cursor:
    cursor.execute("SELECT * FROM equipment")
    data = cursor.fetchall()  # Returns RealDictCursor rows
```

This ensures proper connection management and cursor configuration.

## Support

If you continue to have issues after applying these fixes:

1. Check that all cursor() calls have been updated
2. Verify the imports are present at the top of each file
3. Check for any local cursor creation in dialogs (apply same fix)
4. Review error messages carefully - they'll indicate which attribute is missing


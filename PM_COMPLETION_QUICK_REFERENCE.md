# PM Completion Tab - Quick Reference Guide

## File Information
- **Main Module:** `/home/user/CMMS_NEON2.2/pm_completion_tab_pyqt5.py`
- **Documentation:** `/home/user/CMMS_NEON2.2/PM_COMPLETION_TAB_README.md`
- **Total Lines:** 897 lines
- **Size:** 36 KB

## Class Structure

### Class 1: `EquipmentPMHistoryDialog(QDialog)`
**Purpose:** Display PM history for a specific equipment

| Line | Method | Description |
|------|--------|-------------|
| 32 | `__init__(conn, bfm_no, parent)` | Initialize dialog with equipment number |
| 41 | `setup_ui()` | Create dialog layout with table |
| 68 | `load_history()` | Query and display last 20 PM completions |

**Key Features:**
- Shows last 20 completions for equipment
- Table with columns: Date, PM Type, Technician, Hours, Notes
- Sortable and resizable columns
- Modal dialog with close button

---

### Class 2: `PMCompletionTab(QWidget)` - Main Class
**Purpose:** Complete PM completion interface with form, validation, and history

#### Initialization & Setup (Lines 125-303)

| Line | Method | Description |
|------|--------|-------------|
| 125 | `__init__(conn, parent)` | Initialize tab, load data, setup UI |
| 141 | `setup_ui()` | Create main layout with form, stats, table |
| 158 | `create_completion_form()` | Build PM completion form with all fields |
| 247 | `create_statistics_display()` | Create statistics panel |
| 276 | `create_recent_completions_table()` | Create sortable completions table |

**Form Fields Created:**
- BFM Equipment Number (QComboBox with autocomplete)
- PM Type (QComboBox: Monthly/Six Month/Annual/etc.)
- Maintenance Technician (QComboBox from database)
- Labor Time (Hours: QSpinBox 0-24, Minutes: QSpinBox 0-59)
- PM Due Date (QLineEdit, YYYY-MM-DD)
- Special Equipment (QLineEdit)
- Notes (QTextEdit, multi-line)
- Next Annual PM Date (QLineEdit, auto-calculated)

**Buttons:**
- Submit PM Completion (green, calls `submit_pm_completion()`)
- Clear Form (calls `clear_form()`)
- Show Equipment PM History (calls `show_equipment_history()`)
- Refresh List (calls `load_recent_completions()`)

#### Data Loading (Lines 303-452)

| Line | Method | Description |
|------|--------|-------------|
| 303 | `load_technicians()` | Load technicians from users table |
| 336 | `load_equipment_list()` | Load equipment for autocomplete |
| 352 | `update_equipment_suggestions(text)` | Dynamic autocomplete as user types |
| 373 | `load_recent_completions()` | Load last 500 PM completions |
| 414 | `update_statistics()` | Update completion count statistics |
| 453 | `get_week_start(date)` | Get Monday of week for date |

**Technicians Loading:**
```sql
SELECT full_name FROM users
WHERE role = 'Technician'
ORDER BY full_name
```

**Equipment Autocomplete:**
```sql
SELECT bfm_equipment_no FROM equipment
WHERE LOWER(bfm_equipment_no) LIKE %s OR LOWER(description) LIKE %s
ORDER BY bfm_equipment_no LIMIT 20
```

**Recent Completions:**
```sql
SELECT completion_date, bfm_equipment_no, pm_type, technician_name,
    (labor_hours + labor_minutes/60.0) as total_hours
FROM pm_completions
ORDER BY completion_date DESC, id DESC LIMIT 500
```

#### Validation & Processing (Lines 460-663)

| Line | Method | Description |
|------|--------|-------------|
| 460 | `validate_pm_completion(...)` | Check for duplicates and validate data |
| 543 | `process_normal_pm_completion(...)` | Insert PM and update equipment dates |
| 634 | `verify_pm_completion_saved(...)` | Verify PM was saved to database |

**Validation Checks:**

1. **Duplicate Detection** (Line 471-497)
   - Monthly PM: Minimum 25 days between completions
   - Six Month PM: Minimum 150 days
   - Annual PM: Minimum 300 days
   - Shows: Previous completion date, technician, days since

2. **Technician Duplicate Check** (Line 500-517)
   - Same technician + same PM type + same equipment
   - Within last 7 days
   - Warns user

3. **Equipment Status Check** (Line 520-532)
   - Equipment exists in database
   - Status appropriate for PM type
   - Warns if Missing/Run to Failure equipment

**Process Normal PM Completion:**

1. **Insert Completion Record** (Line 553-570)
```sql
INSERT INTO pm_completions
(bfm_equipment_no, pm_type, technician_name, completion_date,
labor_hours, labor_minutes, pm_due_date, special_equipment,
notes, next_annual_pm_date)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
RETURNING id
```

2. **Update Equipment Dates** (Line 572-610)
   - Monthly: Updates `last_monthly_pm`, `next_monthly_pm` (+30 days)
   - Six Month: Updates `last_six_month_pm`, `next_six_month_pm` (+180 days)
   - Annual: Updates `last_annual_pm`, `next_annual_pm` (+365 days)

3. **Update Weekly Schedule** (Line 616-628)
```sql
UPDATE weekly_pm_schedules SET
status = 'Completed',
completion_date = %s,
labor_hours = %s,
notes = %s
WHERE id = (
    SELECT id FROM weekly_pm_schedules
    WHERE bfm_equipment_no = %s AND pm_type = %s AND assigned_technician = %s
    AND status = 'Scheduled'
    ORDER BY scheduled_date
    LIMIT 1
)
```

#### Submit & UI Actions (Lines 664-860)

| Line | Method | Description |
|------|--------|-------------|
| 664 | `submit_pm_completion()` | Main submit handler with full validation |
| 826 | `clear_form()` | Reset all form fields to default |
| 841 | `show_equipment_history()` | Open PM history dialog |

**Submit PM Completion Flow:**

1. **Validate Required Fields** (Line 666-689)
   - BFM Number → Warning if empty
   - PM Type → Warning if empty
   - Technician → Warning if empty

2. **Get Form Data** (Line 691-699)
   - Labor hours and minutes
   - PM due date (or today's date)
   - Special equipment
   - Notes
   - Next annual PM date

3. **Clean Transaction State** (Line 704-708)
   ```python
   try:
       self.conn.rollback()
   except:
       pass
   ```

4. **Run Validation** (Line 711-734)
   - Call `validate_pm_completion()`
   - Show warning dialog if issues found
   - User can proceed or cancel
   - Rollback if cancelled

5. **Auto-Calculate Next Annual PM** (Line 737-764)
   - Only for Annual PMs
   - Base: completion_date + 365 days
   - Offset: Equipment-specific ±30 days
   - Formula: `(hash(bfm_no) % 61) - 30`

6. **Process Completion** (Line 767-823)
   - Call `process_normal_pm_completion()`
   - Commit transaction on success
   - Verify with `verify_pm_completion_saved()`
   - Show success dialog
   - Clear form and refresh displays
   - Emit `pm_completed` signal
   - Rollback on any error

**Clear Form:**
- Resets all input fields to default values
- Sets focus back to BFM input
- Does not refresh data (use Refresh button for that)

**Show Equipment History:**
- Uses BFM number from form if entered
- Shows input dialog if BFM field is empty
- Opens `EquipmentPMHistoryDialog` with selected equipment

---

## Signals

### `pm_completed = pyqtSignal(str, str, str)`
**Emitted when:** PM is successfully saved and verified
**Arguments:**
1. `bfm_no` (str): Equipment BFM number
2. `pm_type` (str): PM type (Monthly/Annual/etc.)
3. `technician` (str): Technician name

**Example Usage:**
```python
pm_tab = PMCompletionTab(conn)
pm_tab.pm_completed.connect(lambda bfm, pm, tech:
    print(f"PM completed: {bfm} - {pm} by {tech}")
)
```

---

## Database Operations Summary

### Tables Modified

1. **pm_completions** (INSERT)
   - New record for each PM completion
   - Includes all form data

2. **equipment** (UPDATE)
   - Last PM dates
   - Next PM dates
   - Updated timestamp

3. **weekly_pm_schedules** (UPDATE)
   - Status → 'Completed'
   - Completion date
   - Labor hours
   - Notes

### Tables Queried

1. **users** (SELECT)
   - Load technician list
   - Filter by role='Technician'

2. **equipment** (SELECT)
   - Autocomplete suggestions
   - Validation checks
   - Status verification

3. **pm_completions** (SELECT)
   - Duplicate detection
   - Recent completions list
   - Equipment history
   - Statistics

4. **weekly_pm_schedules** (SELECT + UPDATE)
   - Find matching scheduled PM
   - Update status to completed

---

## Key Algorithms

### Next Annual PM Date Calculation
```python
def calculate_next_annual_pm(bfm_no, completion_date):
    """Calculate next annual PM with equipment-specific offset"""
    # Base calculation: +365 days
    completion_dt = datetime.strptime(completion_date, '%Y-%m-%d')
    next_annual_dt = completion_dt + timedelta(days=365)

    # Equipment-specific offset: ±30 days
    numeric_part = re.findall(r'\d+', bfm_no)
    if numeric_part:
        last_digits = int(numeric_part[-1]) % 61
        offset_days = last_digits - 30  # Range: -30 to +30
    else:
        offset_days = (hash(bfm_no) % 61) - 30

    next_annual_dt = next_annual_dt + timedelta(days=offset_days)
    return next_annual_dt.strftime('%Y-%m-%d')
```

**Purpose:** Spread annual PMs throughout the year to balance workload

### Week Start Calculation
```python
def get_week_start(date):
    """Get Monday of the week for a given date"""
    days_since_monday = date.weekday()  # Monday=0, Sunday=6
    week_start = date - timedelta(days=days_since_monday)
    return week_start.replace(hour=0, minute=0, second=0, microsecond=0)
```

**Purpose:** Calculate current week for statistics

---

## Error Handling Strategy

### Transaction Safety
```python
try:
    # Clean state
    self.conn.rollback()

    # Process PM
    success = self.process_normal_pm_completion(...)

    if success:
        # Commit transaction
        self.conn.commit()

        # Verify saved
        verification = self.verify_pm_completion_saved(...)

        if verified:
            # Success!
            show_success_message()
        else:
            # Saved but verification failed
            show_warning_message()
    else:
        # Failed to save
        self.conn.rollback()
        show_error_message()

except Exception as e:
    # Exception during process
    self.conn.rollback()
    show_error_message(e)
```

### User-Friendly Error Messages

| Error Type | User Message | Technical Details |
|------------|--------------|-------------------|
| Missing required field | "Please enter BFM Equipment Number" | Field name in message |
| Duplicate PM | "WARNING: Duplicate detected... Do you want to proceed?" | Days since last, threshold, technician |
| Database error | "Failed to submit PM completion: [error]" | Full exception message |
| Validation failure | "Found N potential issues: [list]" | All validation issues listed |
| Save failure | "Failed to process PM completion. Transaction rolled back." | Console shows stack trace |

---

## Performance Notes

### Database Query Optimization
- Equipment autocomplete: Limited to 20 results
- Recent completions: Limited to 500 records
- PM history: Limited to 20 records per equipment
- All queries use indexed columns (bfm_equipment_no, completion_date)

### UI Responsiveness
- Table sorting handled by Qt (fast)
- Column auto-sizing on data load
- No UI freezing during database operations
- Immediate feedback on button clicks

### Memory Management
- Database cursors properly closed after use
- Qt widgets auto-deleted when parent destroyed
- No memory leaks in signal/slot connections

---

## Testing Quick Checklist

### Smoke Test (5 minutes)
- [ ] Tab loads without errors
- [ ] Form displays all fields
- [ ] Equipment autocomplete works
- [ ] Technician dropdown populated
- [ ] Submit button saves PM
- [ ] Table shows recent completions

### Full Test (15 minutes)
- [ ] All form fields work correctly
- [ ] Validation catches missing required fields
- [ ] Duplicate detection triggers warning
- [ ] Statistics update after submission
- [ ] Equipment history dialog opens and shows data
- [ ] Clear button resets form
- [ ] Refresh button reloads table
- [ ] Database records saved correctly
- [ ] Weekly schedule updated
- [ ] Equipment dates updated

### Edge Cases
- [ ] Submit with empty notes → Works
- [ ] Submit with 0 labor time → Works
- [ ] Submit duplicate PM → Warning shown, can proceed
- [ ] Submit for non-existent equipment → Validation catches
- [ ] Submit with future date → Works
- [ ] Auto-calculate next annual PM → Correct offset applied

---

## Common Customizations

### Change PM Type Options
**File:** `pm_completion_tab_pyqt5.py`
**Line:** 163-165
```python
self.pm_type_combo.addItems(['', 'Monthly', 'Six Month', 'Annual',
                             'CANNOT FIND', 'Run to Failure'])
```

### Change Duplicate Thresholds
**File:** `pm_completion_tab_pyqt5.py`
**Line:** 484-488
```python
min_days = {
    'Monthly': 25,      # Change to 20, 30, etc.
    'Six Month': 150,   # Change to 120, 180, etc.
    'Annual': 300       # Change to 270, 330, etc.
}
```

### Change Recent Completions Limit
**File:** `pm_completion_tab_pyqt5.py`
**Line:** 379
```python
ORDER BY completion_date DESC, id DESC LIMIT 500  # Change to 100, 1000, etc.
```

### Change Equipment Autocomplete Limit
**File:** `pm_completion_tab_pyqt5.py`
**Line:** 361
```python
ORDER BY bfm_equipment_no LIMIT 20  # Change to 10, 50, etc.
```

### Add Custom Validation
**File:** `pm_completion_tab_pyqt5.py`
**Line:** 460 (in `validate_pm_completion()`)

Add after line 532:
```python
# Check 4: Custom validation
if some_condition:
    issues.append("Custom validation message")
```

---

## Integration Examples

### Example 1: Add to Tab Widget
```python
from pm_completion_tab_pyqt5 import PMCompletionTab

# In your main window
tabs = QTabWidget()
pm_tab = PMCompletionTab(self.db_connection)
tabs.addTab(pm_tab, "PM Completion")
```

### Example 2: Listen to Completions
```python
pm_tab = PMCompletionTab(conn)

def on_pm_done(bfm, pm_type, tech):
    print(f"PM completed: {bfm}")
    # Refresh dashboard, send email, etc.

pm_tab.pm_completed.connect(on_pm_done)
```

### Example 3: Pre-fill Form
```python
pm_tab = PMCompletionTab(conn)

# Pre-fill equipment number
pm_tab.bfm_input.setCurrentText("BFM-12345")

# Pre-select PM type
pm_tab.pm_type_combo.setCurrentText("Monthly")

# Pre-select technician
pm_tab.tech_combo.setCurrentText("John Doe")
```

### Example 4: Programmatic Submit
```python
pm_tab = PMCompletionTab(conn)

# Set all required fields
pm_tab.bfm_input.setCurrentText("BFM-12345")
pm_tab.pm_type_combo.setCurrentText("Monthly")
pm_tab.tech_combo.setCurrentText("John Doe")
pm_tab.labor_hours.setValue(2)
pm_tab.labor_minutes.setValue(30)
pm_tab.notes_input.setPlainText("Routine maintenance completed")

# Submit programmatically
pm_tab.submit_pm_completion()
```

---

## Debugging Tips

### Enable Verbose Logging
All methods already include print statements. Watch console output:
```
Loaded 9 technicians from database
Loaded 1234 equipment items
Loaded 500 recent PM completions
CHECK: PM completed and verified: BFM-12345 - Monthly by John Doe
```

### Database Query Debugging
Add before line 554 in `process_normal_pm_completion()`:
```python
print(f"SQL: INSERT INTO pm_completions VALUES {(bfm_no, pm_type, ...)}")
```

### Validation Debugging
Add at line 535 in `validate_pm_completion()`:
```python
print(f"Validation issues: {issues}")
```

### Signal Debugging
```python
pm_tab.pm_completed.connect(
    lambda bfm, pm, tech: print(f"SIGNAL: {bfm}, {pm}, {tech}")
)
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-15 | Initial PyQt5 port with full feature parity |

---

**Quick Start:**
```python
from pm_completion_tab_pyqt5 import PMCompletionTab
tab = PMCompletionTab(database_connection)
tab.show()
```

**That's it!** 🎉

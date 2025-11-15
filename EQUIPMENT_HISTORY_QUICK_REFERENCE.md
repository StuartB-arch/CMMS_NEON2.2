# Equipment History Tab - Quick Reference Card

## Quick Start (3 Lines)

```python
from equipment_history_tab_pyqt5 import EquipmentHistoryTab
history_tab = EquipmentHistoryTab(conn)
tabs.addTab(history_tab, "Equipment History")
```

## File Location
```
/home/user/CMMS_NEON2.2/equipment_history_tab_pyqt5.py
```

## Module Stats
- **Lines**: 1,350
- **Classes**: 4
- **Methods**: 33
- **Queries**: 7

## Main Classes

### EquipmentHistoryTab
```python
tab = EquipmentHistoryTab(conn, parent=None)
tab.status_updated.connect(status_bar.showMessage)
```

### TimelineWidget
```python
timeline = TimelineWidget()
timeline.set_events(event_list)
```

### EventDetailDialog
```python
dialog = EventDetailDialog(event_data, parent)
dialog.exec_()
```

## Key Methods

| Method | Purpose |
|--------|---------|
| `load_equipment_list()` | Load all equipment into dropdown |
| `load_equipment_history()` | Load PM/CM/Parts for equipment |
| `apply_filters()` | Filter events by date/type |
| `update_statistics()` | Calculate and display stats |
| `calculate_health_score()` | Compute 0-100 health score |
| `show_health_report()` | Display detailed health dialog |
| `export_to_csv()` | Export events to CSV file |

## Event Data Structure

```python
{
    'date': '2025-01-15',
    'event_type': 'PM',  # or 'CM', 'PART'
    'description': 'Monthly PM Completion',
    'technician': 'John Smith',
    'labor_hours': 2.5,
    'status': 'Completed',
    'color': '#4CAF50',
    'category': 'Preventive Maintenance',
    'title': 'Monthly PM',
    'details': 'Technician: John Smith, Hours: 2.5'
}
```

## Database Queries

### Get PM History
```python
events = self.get_pm_history('2024-01-01', '2025-01-01')
```

### Get CM History
```python
events = self.get_cm_history('2024-01-01', '2025-01-01')
```

### Get Parts History
```python
events = self.get_parts_history('2024-01-01', '2025-01-01')
```

## Health Score Formula

```
Base Score = 100

Deductions:
- PM Compliance: (100 - compliance%) × 0.3
- CM Frequency: min(20, (cms_per_month - 1) × 10) if > 1/month
- Status: 30 if not 'Active'

Final = max(0, Base - Total Deductions)
```

## Color Codes

| Event Type | Color | Hex |
|------------|-------|-----|
| PM Completed | Green | `#4CAF50` |
| CM Open | Orange | `#FF9800` |
| CM Closed | Green | `#4CAF50` |
| Parts Request | Blue | `#2196F3` |
| High Priority | Red | `#F44336` |

## Filter Presets

| Preset | Range |
|--------|-------|
| Last 30 Days | QDate.currentDate().addDays(-30) |
| Last 90 Days | QDate.currentDate().addDays(-90) |
| Last 6 Months | QDate.currentDate().addMonths(-6) |
| Last Year | QDate.currentDate().addYears(-1) |
| Last 2 Years | QDate.currentDate().addYears(-2) |
| All Time | QDate(2000, 1, 1) |

## Signal Example

```python
def on_status_update(message):
    print(f"Status: {message}")

history_tab.status_updated.connect(on_status_update)
```

## Export CSV

```python
# Automatic with dialog
history_tab.export_to_csv()

# Default filename format
f"equipment_history_{bfm_no}_{YYYYMMDD}.csv"
```

## Common Patterns

### Navigate to History from Other Tab
```python
def view_history(self, bfm_no):
    tabs = self.window().findChild(QTabWidget)
    for i in range(tabs.count()):
        if tabs.tabText(i) == "Equipment History":
            tabs.setCurrentIndex(i)
            history = tabs.widget(i)
            idx = history.equipment_combo.findData(bfm_no)
            if idx >= 0:
                history.equipment_combo.setCurrentIndex(idx)
            break
```

### Show Quick History Dialog
```python
from equipment_history_tab_pyqt5 import EventDetailDialog

event = {
    'date': '2025-01-15',
    'event_type': 'PM',
    'technician': 'John',
    'labor_hours': 2.0,
    'notes': 'Routine maintenance'
}

dialog = EventDetailDialog(event, self)
dialog.exec_()
```

## Performance Tips

1. **Add Indexes**
```sql
CREATE INDEX idx_pm_bfm ON pm_completions(bfm_equipment_no);
CREATE INDEX idx_cm_bfm ON corrective_maintenance(bfm_equipment_no);
```

2. **Use Connection Pool**
```python
from database_utils import DatabaseConnectionPool
pool = DatabaseConnectionPool()
conn = pool.get_connection()
```

3. **Limit Date Range** for large datasets

## Error Handling Pattern

```python
try:
    cursor = self.conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    self.conn.commit()
except Exception as e:
    QMessageBox.critical(self, "Error", str(e))
    try:
        self.conn.rollback()
    except:
        pass
```

## Testing Snippet

```python
import unittest
from equipment_history_tab_pyqt5 import EquipmentHistoryTab

class TestHistory(unittest.TestCase):
    def test_load(self):
        tab = EquipmentHistoryTab(conn)
        tab.load_equipment_list()
        self.assertGreater(tab.equipment_combo.count(), 0)
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No events showing | Check date range, verify equipment has history |
| Timeline blank | Ensure events have valid dates |
| Health score "--" | Equipment needs PM flags set |
| Export fails | Check file permissions |
| Slow loading | Add database indexes |

## Dependencies

```bash
pip install PyQt5>=5.15.0 psycopg2>=2.9.0
```

## Required Tables

- `equipment` (bfm_equipment_no, short_description, status, monthly_pm, annual_pm)
- `pm_completions` (bfm_equipment_no, completion_date, pm_type, technician_name, labor_hours, notes)
- `corrective_maintenance` (cm_number, bfm_equipment_no, reported_date, description, status)
- `cm_parts_requests` (cm_number, requested_date, part_number, model_number)

## Integration Checklist

- [ ] Import EquipmentHistoryTab
- [ ] Create instance with database connection
- [ ] Connect status_updated signal
- [ ] Add to QTabWidget
- [ ] Test equipment selection
- [ ] Test filtering
- [ ] Test export
- [ ] Verify health scoring

## Documentation Files

1. `EQUIPMENT_HISTORY_TAB_README.md` - Complete documentation
2. `EQUIPMENT_HISTORY_INTEGRATION_GUIDE.md` - Integration guide
3. `EQUIPMENT_HISTORY_IMPLEMENTATION_SUMMARY.md` - Implementation details
4. `EQUIPMENT_HISTORY_QUICK_REFERENCE.md` - This file

## Support

- Review README for detailed documentation
- Check Integration Guide for examples
- See Implementation Summary for architecture

---

**Quick Ref Version**: 1.0.0
**Last Updated**: 2025-11-15

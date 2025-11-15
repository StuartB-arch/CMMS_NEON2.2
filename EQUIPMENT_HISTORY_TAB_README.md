# Equipment History Tab - PyQt5 Implementation

## Overview

The Equipment History Tab (`equipment_history_tab_pyqt5.py`) provides comprehensive equipment maintenance history tracking and visualization for the CMMS NEON system. This module allows users to view, filter, and analyze the complete maintenance history of any equipment item, including PM completions, corrective maintenance, and parts usage.

## Features

### 1. Equipment Selection
- **Searchable Dropdown**: Select equipment from a searchable combo box
- **Real-time Search**: Filter equipment list by BFM number or description
- **Auto-refresh**: Reload equipment list with a single click

### 2. Timeline Visualization
- **Visual Timeline**: Graphical representation of all maintenance events over time
- **Color-coded Events**:
  - Green: PM completions and closed CMs
  - Orange: Open/In-Progress CMs
  - Blue: Parts requests
  - Red: High-priority open items
- **Interactive Tooltips**: Hover over timeline events to see details
- **Date-based Layout**: Events positioned chronologically on timeline

### 3. Event History Table
- **Comprehensive Columns**:
  - Date
  - Event Type (PM/CM/PART)
  - Description
  - Technician
  - Labor Hours
  - Priority/Type
  - Status
  - Details (double-click to view)
- **Sortable**: Click any column header to sort
- **Color-coded Rows**: Visual distinction between event types
- **Multi-select**: Select multiple events for batch operations

### 4. Filtering System
- **Date Range Filters**:
  - Custom start and end dates using calendar widgets
  - Quick presets: 30 days, 90 days, 6 months, 1 year, 2 years, all time
- **Event Type Filters**:
  - All Events
  - PM Only
  - CM Only
  - Parts Only
- **Real-time Application**: Filters apply immediately to table and timeline

### 5. Statistics Summary
Real-time statistics display:
- **Total PMs**: Count of preventive maintenance completions
- **Total CMs**: Count of corrective maintenance records
- **Total Hours**: Sum of all labor hours
- **Health Score**: Equipment health rating (0-100)
- **Last PM**: Date of most recent PM completion
- **Last CM**: Date of most recent CM record

### 6. Equipment Health Scoring
Intelligent health score calculation based on:
- **PM Compliance** (30% weight): Percentage of scheduled PMs completed
- **CM Frequency** (up to 20% penalty): Number of CMs per month
- **Equipment Status** (30% penalty): Active vs. inactive status

Score Interpretation:
- **80-100**: Excellent - Equipment performing well
- **60-79**: Good - Minor attention needed
- **0-59**: Needs Attention - Immediate review required

### 7. Health Report
Detailed health report dialog includes:
- Equipment identification
- Current status
- Overall health score
- PM compliance metrics
- CM frequency analysis
- Parts usage statistics
- Actionable recommendations

### 8. Export Capabilities
- **CSV Export**: Export all event data to CSV format
  - Includes all event details
  - Timestamped filename
  - UTF-8 encoding for international characters
- **PDF Export**: Placeholder for future implementation

### 9. Event Detail Dialog
Double-click any event to view complete details:
- Event date and type
- Technician information
- Labor hours
- Priority/status
- Complete notes
- Parts information (if applicable)
- Related CM numbers

## Database Queries

### PM Completions Query
```sql
SELECT completion_date, pm_type, technician_name, labor_hours,
       notes, special_equipment
FROM pm_completions
WHERE bfm_equipment_no = %s
AND completion_date >= %s
AND completion_date <= %s
ORDER BY completion_date DESC
```

### Corrective Maintenance Query
```sql
SELECT cm_number, reported_date, closed_date, description, priority,
       status, assigned_technician, labor_hours, notes, root_cause,
       corrective_action
FROM corrective_maintenance
WHERE bfm_equipment_no = %s
AND reported_date >= %s
AND reported_date <= %s
ORDER BY reported_date DESC
```

### Parts History Query
```sql
SELECT cpr.requested_date, cpr.part_number, cpr.model_number,
       cpr.requested_by, cpr.notes, cm.cm_number
FROM cm_parts_requests cpr
JOIN corrective_maintenance cm ON cpr.cm_number = cm.cm_number
WHERE cm.bfm_equipment_no = %s
AND cpr.requested_date >= %s
AND cpr.requested_date <= %s
ORDER BY cpr.requested_date DESC
```

### Health Metrics Queries
```sql
-- PM Compliance
SELECT COUNT(*), COALESCE(SUM(labor_hours), 0)
FROM pm_completions
WHERE bfm_equipment_no = %s
AND completion_date >= %s

-- CM Frequency
SELECT COUNT(*), COALESCE(SUM(labor_hours), 0)
FROM corrective_maintenance
WHERE bfm_equipment_no = %s
AND reported_date >= %s

-- Parts Count
SELECT COUNT(*)
FROM cm_parts_requests cpr
JOIN corrective_maintenance cm ON cpr.cm_number = cm.cm_number
WHERE cm.bfm_equipment_no = %s
AND cpr.requested_date >= %s
```

## Usage Guide

### Basic Workflow

1. **Select Equipment**
   ```
   - Use the dropdown to select an equipment item
   - Or type in the search field to filter the list
   - Click "Refresh Equipment" to reload the list
   ```

2. **View History**
   ```
   - Timeline shows visual representation of events
   - Table shows detailed event information
   - Statistics update automatically
   ```

3. **Apply Filters**
   ```
   - Use date range pickers for custom date ranges
   - Or select a quick preset (30 days, 90 days, etc.)
   - Filter by event type (PM, CM, Parts)
   - Click "Apply Filters" to update view
   ```

4. **View Event Details**
   ```
   - Double-click any row in the table
   - View complete event information in dialog
   - Close dialog to return to main view
   ```

5. **Export Data**
   ```
   - Click "Export to CSV" button
   - Choose save location
   - CSV file includes all filtered events
   ```

6. **View Health Report**
   ```
   - Click "View Health Report" button
   - Review comprehensive health metrics
   - Read recommendations for equipment maintenance
   ```

### Integration Example

```python
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from equipment_history_tab_pyqt5 import EquipmentHistoryTab
import psycopg2

# Create application
app = QApplication(sys.argv)
window = QMainWindow()

# Create database connection
conn = psycopg2.connect(
    dbname="cmms_db",
    user="user",
    password="password",
    host="localhost",
    port="5432"
)

# Create tab widget
tabs = QTabWidget()

# Create equipment history tab
history_tab = EquipmentHistoryTab(conn)

# Connect status updates
history_tab.status_updated.connect(lambda msg: window.statusBar().showMessage(msg))

# Add to tab widget
tabs.addTab(history_tab, "Equipment History")

# Show window
window.setCentralWidget(tabs)
window.show()

app.exec_()
```

## Classes and Methods

### EquipmentHistoryTab
Main widget class for equipment history tracking.

#### Constructor
```python
def __init__(self, conn, parent=None)
```
- **conn**: PostgreSQL database connection
- **parent**: Optional parent widget

#### Key Methods

##### load_equipment_list()
Loads all equipment from database into selection dropdown.

##### on_equipment_selected(text)
Handles equipment selection and loads history.

##### load_equipment_history()
Loads complete PM, CM, and parts history for selected equipment.

##### get_pm_history(start_date, end_date)
Retrieves PM completion records within date range.

##### get_cm_history(start_date, end_date)
Retrieves corrective maintenance records within date range.

##### get_parts_history(start_date, end_date)
Retrieves parts request records within date range.

##### apply_filters()
Applies current filter settings to event list.

##### update_statistics()
Calculates and updates statistics display.

##### calculate_health_score()
Calculates equipment health score based on metrics.

##### show_health_report()
Displays comprehensive health report dialog.

##### export_to_csv()
Exports event history to CSV file.

#### Signals
```python
status_updated = pyqtSignal(str)
```
Emitted when status message should be displayed.

### TimelineWidget
Custom graphics view for timeline visualization.

#### Constructor
```python
def __init__(self, parent=None)
```

#### Key Methods

##### set_events(events)
Sets the events to display on timeline.

##### draw_timeline()
Renders the visual timeline with events.

### EventDetailDialog
Dialog for displaying complete event information.

#### Constructor
```python
def __init__(self, event_data, parent=None)
```
- **event_data**: Dictionary containing event information

### TimelineGraphicsItem
Custom graphics item for timeline events with hover tooltips.

#### Constructor
```python
def __init__(self, event, x, y, width, height)
```

## Configuration

### Color Scheme
- **PM Events**: `#4CAF50` (Green)
- **CM Open/In Progress**: `#FF9800` (Orange)
- **CM Closed**: `#4CAF50` (Green)
- **Parts Requests**: `#2196F3` (Blue)
- **High Priority**: `#F44336` (Red)

### Default Settings
- **Default Date Range**: Last 1 year
- **Default Event Filter**: All Events
- **Minimum Timeline Height**: 200 pixels
- **Table Alternating Colors**: Enabled
- **Sort Enabled**: Yes

## Error Handling

All database operations include comprehensive error handling:

```python
try:
    # Database operation
    cursor.execute(query, params)
    result = cursor.fetchall()
    self.conn.commit()
except Exception as e:
    QMessageBox.critical(self, "Database Error",
                        f"Error: {str(e)}")
    try:
        self.conn.rollback()
    except:
        pass
```

## Performance Considerations

1. **Lazy Loading**: Events loaded only when equipment is selected
2. **Filter Optimization**: Filters applied to in-memory data
3. **Database Commits**: Explicit commits after read operations
4. **Connection Pooling**: Use database_utils.py connection pool in production

## Dependencies

### Required Packages
```
PyQt5 >= 5.15.0
psycopg2 >= 2.9.0
```

### Optional Packages
```
reportlab >= 3.6.0  # For future PDF export
```

### Database Requirements
- PostgreSQL 12+
- Tables: equipment, pm_completions, corrective_maintenance, cm_parts_requests

## Troubleshooting

### Issue: Timeline not displaying
**Solution**: Ensure events have valid dates in YYYY-MM-DD format

### Issue: Health score shows "--"
**Solution**: Verify equipment has monthly_pm or annual_pm flags set

### Issue: Export fails
**Solution**: Check file permissions and disk space

### Issue: Slow performance
**Solution**: Add indexes on bfm_equipment_no columns:
```sql
CREATE INDEX idx_pm_bfm ON pm_completions(bfm_equipment_no);
CREATE INDEX idx_cm_bfm ON corrective_maintenance(bfm_equipment_no);
```

## Future Enhancements

1. **PDF Export**: Full implementation with charts and graphs
2. **Advanced Analytics**: Trend analysis and predictions
3. **Batch Operations**: Multi-equipment comparison
4. **Custom Reports**: User-defined report templates
5. **Email Integration**: Automated health report distribution
6. **Mobile View**: Responsive design for tablets
7. **Real-time Updates**: WebSocket integration for live updates

## Contributing

When adding new features:

1. Follow PyQt5 coding standards
2. Add comprehensive docstrings
3. Include error handling
4. Update this README
5. Add unit tests
6. Test with production data

## License

Part of CMMS NEON 2.2 - Internal use only

## Support

For issues or questions:
- Check this README first
- Review error logs
- Contact CMMS development team

---

**Last Updated**: 2025-11-15
**Version**: 1.0.0
**Author**: Claude Code
**Module**: equipment_history_tab_pyqt5.py

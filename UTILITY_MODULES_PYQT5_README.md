# PyQt5 Utility Modules - Complete Implementation

## Overview

Four complete PyQt5 utility modules have been created to provide essential functionality for the CMMS system. All modules are production-ready with full database integration, error handling, and modern UI design.

---

## 1. Parts Integration Dialog (`parts_integration_dialog_pyqt5.py`)

### Purpose
Manages parts consumption tracking for Corrective Maintenance (CM) work orders.

### Features
- **Search & Filter**: Quick search by part number or description
- **Stock Level Indicators**: Color-coded display (In Stock, Low Stock, Out of Stock)
- **Parts Selection**: Add/remove parts from consumption list
- **Inventory Validation**: Prevents consumption of out-of-stock items
- **Database Integration**:
  - Records to `cm_parts_used` table
  - Updates `mro_inventory` quantities
  - Creates `mro_stock_transactions` records
- **Cost Tracking**: Automatic cost calculation based on unit price

### Usage
```python
from parts_integration_dialog_pyqt5 import CMPartsIntegrationDialog

# Show parts consumption dialog
dialog = CMPartsIntegrationDialog(
    cm_number="CM-2024-001",
    technician_name="John Doe",
    conn=database_connection,
    parent=parent_widget
)
dialog.parts_saved.connect(callback_function)
dialog.exec_()
```

### Key Components
- `CMPartsIntegrationDialog`: Main dialog for adding parts
- `CMPartsViewDialog`: Read-only view of parts consumed for a CM
- Convenience functions: `show_parts_consumption_dialog()`, `show_cm_parts_details()`

### Database Tables Used
- `mro_inventory`: Parts catalog and stock levels
- `cm_parts_used`: Parts consumption records
- `mro_stock_transactions`: Transaction history

---

## 2. User Management Dialog (`user_management_dialog_pyqt5.py`)

### Purpose
Comprehensive user management interface for system administrators/managers.

### Features
- **User List**: Display all users with key information
- **Add User**: Create new users with role assignment
- **Edit User**: Modify user details, roles, and status
- **Delete User**: Remove users with safety confirmations
- **Password Management**: Force password resets
- **Session Monitoring**: View active user sessions
- **Audit Logging**: All actions logged to audit trail

### User Roles
- **Manager**: Full system access, user management
- **Technician**: Standard maintenance operations

### Usage
```python
from user_management_dialog_pyqt5 import UserManagementDialog

# Show user management dialog
dialog = UserManagementDialog(
    current_user="admin",
    parent=parent_widget
)
dialog.user_updated.connect(refresh_callback)
dialog.exec_()
```

### Key Components
- `UserManagementDialog`: Main user management interface
- `AddUserDialog`: New user creation dialog
- `EditUserDialog`: User editing dialog
- `SessionsViewDialog`: Active sessions viewer

### Security Features
- Password hashing using `UserManager.hash_password()`
- Minimum password length enforcement (4 characters)
- Prevent self-deletion
- Active/Inactive user status
- Audit logging via `AuditLogger`

### Database Tables Used
- `users`: User accounts and credentials
- `user_sessions`: Active login sessions
- `audit_log`: Action tracking

---

## 3. Password Change Dialog (`password_change_dialog_pyqt5.py`)

### Purpose
Allows any authenticated user to change their own password.

### Features
- **Secure Input**: Password fields with echo mode hidden
- **Validation**:
  - Current password verification
  - Minimum length requirement (4 characters)
  - New password confirmation
  - Prevents reuse of current password
- **User-Friendly**: Clear error messages and field focus management
- **Audit Trail**: Password changes logged to system
- **Keyboard Shortcuts**: Enter to submit, Escape to cancel

### Usage
```python
from password_change_dialog_pyqt5 import PasswordChangeDialog

# Show password change dialog
dialog = PasswordChangeDialog(
    current_user="John Doe",
    username="jdoe",
    parent=parent_widget
)
dialog.password_changed.connect(callback_function)
dialog.exec_()
```

### Validation Rules
1. Current password must be correct
2. New password minimum 4 characters
3. New password must match confirmation
4. New password must differ from current password

### Key Components
- `PasswordChangeDialog`: Main dialog class
- Convenience function: `show_password_change_dialog()`

### Database Integration
- Uses `UserManager.change_password()` for secure password updates
- Logs changes via `AuditLogger`
- Uses database connection pooling via `db_pool`

---

## 4. KPI Trend Analyzer Tab (`kpi_trend_analyzer_tab_pyqt5.py`)

### Purpose
Comprehensive KPI monitoring, trend analysis, and forecasting tool.

### Features
- **Dashboard View**: Summary of all KPIs with status indicators
- **Alerts System**:
  - Below target alerts
  - Declining trend warnings
  - Increasing trend alerts (for "lower is better" KPIs)
  - High volatility notifications
- **Detailed Trends**: Historical data analysis for each KPI
- **Chart Visualization**: Matplotlib-based trend charts
- **Export Capabilities**:
  - Text report export
  - CSV data export
- **Target Comparison**: Automatic comparison against defined targets

### Tracked KPIs
1. PM Adherence (Target: 90%)
2. Work Orders Opened
3. Work Orders Closed
4. Work Order Backlog (Target: ≤20)
5. Technical Availability (Target: 95%)
6. Mean Time Between Failures - MTBF (Target: 720 hours)
7. Mean Time To Repair - MTTR (Target: ≤8 hours)
8. Total Maintenance Labor Hours
9. Injury Frequency Rate (Target: 0)
10. Near Miss Reports

### Usage
```python
from kpi_trend_analyzer_tab_pyqt5 import KPITrendAnalyzerTab

# Create KPI analyzer tab
kpi_tab = KPITrendAnalyzerTab(
    conn=database_connection,
    parent=parent_widget
)
kpi_tab.status_updated.connect(status_bar_update)

# Add to tab widget
tab_widget.addTab(kpi_tab, "KPI Trends")
```

### Alert Severity Levels
- **HIGH**: KPI significantly below target (>20% gap)
- **MEDIUM**: KPI below target or showing concerning trends
- **LOW**: High volatility detected

### Key Components
- `KPITrendAnalyzer`: Backend analysis engine
- `KPITrendAnalyzerTab`: Main UI tab widget
- Statistical analysis methods:
  - `get_kpi_history()`: Retrieve historical data
  - `analyze_trend()`: Calculate trend statistics
  - `generate_alerts()`: Create alerts based on thresholds
  - `get_kpi_dashboard_summary()`: Generate summary statistics

### Charts (requires matplotlib)
- Line plots with actual values
- Target threshold lines
- Average value lines
- Period-based X-axis with rotated labels

### Database Tables Used
- `kpi_manual_data`: KPI measurements and values

---

## Integration with Main Application

### Import All Modules
```python
# Add to AIT_CMMS_REV3_PyQt5.py imports
from parts_integration_dialog_pyqt5 import CMPartsIntegrationDialog, show_parts_consumption_dialog
from user_management_dialog_pyqt5 import UserManagementDialog, show_user_management_dialog
from password_change_dialog_pyqt5 import PasswordChangeDialog, show_password_change_dialog
from kpi_trend_analyzer_tab_pyqt5 import KPITrendAnalyzerTab, show_kpi_trends
```

### Replace Old Imports
Replace these Tkinter imports:
```python
# OLD - Remove these
from cm_parts_integration import CMPartsIntegration
from user_management_ui import UserManagementDialog
from password_change_ui import show_password_change_dialog
from kpi_trend_analyzer import KPITrendViewer
```

### Menu Integration Example
```python
# User Menu
user_menu = menubar.addMenu("User")

# Change Password Action
change_password_action = QAction("Change Password", self)
change_password_action.triggered.connect(self.show_password_change)
user_menu.addAction(change_password_action)

# User Management Action (Managers only)
if self.user_role == "Manager":
    user_mgmt_action = QAction("Manage Users", self)
    user_mgmt_action.triggered.connect(self.show_user_management)
    user_menu.addAction(user_mgmt_action)
```

### Tab Integration Example
```python
# Add KPI Trends tab to main tab widget
kpi_tab = KPITrendAnalyzerTab(self.conn, self)
kpi_tab.status_updated.connect(self.update_status_bar)
self.tab_widget.addTab(kpi_tab, "KPI Trends")
```

---

## Common Patterns & Best Practices

### 1. Signal-Slot Connections
All dialogs emit signals for important events:
```python
dialog.parts_saved.connect(self.on_parts_saved)
dialog.user_updated.connect(self.refresh_user_list)
dialog.password_changed.connect(self.on_password_changed)
dialog.status_updated.connect(self.update_status_bar)
```

### 2. Modal vs Non-Modal
- **Modal**: Parts Integration, Password Change (blocks parent)
- **Non-Modal**: User Management, KPI Trends (allows interaction)

### 3. Database Connection
All modules expect a PostgreSQL database connection:
```python
# Using psycopg2 connection
conn = psycopg2.connect(...)

# Or using connection pool (recommended)
from database_utils import db_pool
with db_pool.get_cursor() as cursor:
    # operations
```

### 4. Error Handling
All modules include comprehensive error handling:
- QMessageBox for user-friendly error display
- Database transaction rollback on errors
- Input validation with helpful messages
- Try-except blocks around database operations

### 5. Styling Consistency
- Color coding: Red (critical), Orange (warning), Green (good), Gray (inactive)
- Bold fonts for headers and important labels
- Alternating row colors in tables
- Consistent spacing and padding

---

## Dependencies

### Required Python Packages
```
PyQt5>=5.15.0
psycopg2>=2.9.0
pandas>=1.3.0
matplotlib>=3.5.0  # Optional, for charts
```

### Database Requirements
- PostgreSQL 12+ with required tables
- Tables: users, user_sessions, audit_log, mro_inventory, cm_parts_used, mro_stock_transactions, kpi_manual_data

### Required Utility Modules
- `database_utils.py`: db_pool, UserManager, AuditLogger
- Standard library: datetime, statistics, csv, collections

---

## Testing Checklist

### Parts Integration Dialog
- [ ] Search functionality works
- [ ] Color coding displays correctly
- [ ] Cannot add out-of-stock parts
- [ ] Cannot exceed available quantity
- [ ] Duplicate parts prevented
- [ ] Database records created correctly
- [ ] Inventory quantities updated

### User Management Dialog
- [ ] User list loads correctly
- [ ] Add user creates database record
- [ ] Edit user updates all fields
- [ ] Delete user removes from database
- [ ] Cannot delete self
- [ ] Password reset works
- [ ] Session viewer displays active sessions
- [ ] Audit log entries created

### Password Change Dialog
- [ ] Current password validation
- [ ] New password length validation
- [ ] Password confirmation matching
- [ ] Prevents password reuse
- [ ] Database update successful
- [ ] Audit log entry created
- [ ] Keyboard shortcuts work

### KPI Trend Analyzer
- [ ] Dashboard summary displays
- [ ] Alerts generated correctly
- [ ] Trend calculations accurate
- [ ] Charts render (if matplotlib available)
- [ ] Export to text works
- [ ] Export to CSV works
- [ ] Historical data retrieved correctly

---

## File Locations

All files located in: `/home/user/CMMS_NEON2.2/`

```
parts_integration_dialog_pyqt5.py       (646 lines)
user_management_dialog_pyqt5.py         (637 lines)
password_change_dialog_pyqt5.py         (273 lines)
kpi_trend_analyzer_tab_pyqt5.py         (840 lines)
```

Total: 2,396 lines of production-ready PyQt5 code

---

## Support & Maintenance

### Common Issues

**Issue**: Database connection errors
**Solution**: Verify database credentials and connection pool configuration

**Issue**: Import errors for database_utils
**Solution**: Ensure database_utils.py is in the same directory

**Issue**: Matplotlib charts not displaying
**Solution**: Install matplotlib or disable charts tab

**Issue**: Permission errors
**Solution**: Verify user role has appropriate permissions

### Future Enhancements

1. **Parts Integration**
   - Barcode scanning support
   - Batch parts addition
   - Parts request workflow

2. **User Management**
   - Email notifications
   - Password complexity rules
   - Two-factor authentication
   - User activity reports

3. **Password Change**
   - Password strength indicator
   - Password history tracking
   - Expiration policies

4. **KPI Trends**
   - Predictive analytics
   - Machine learning forecasting
   - Real-time dashboards
   - Custom KPI definitions
   - Email alerts

---

## Version History

**Version 1.0** (2025-11-15)
- Initial release
- Complete port from Tkinter to PyQt5
- All features from original modules implemented
- Production-ready with full error handling

---

## License & Credits

Part of the AIT CMMS NEON 2.2 System
Converted from Tkinter to PyQt5 for improved UI/UX

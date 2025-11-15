# Utility Modules Integration Guide

## Quick Start - Integration Steps

### Step 1: Update Imports in Main Application

Replace the old Tkinter imports in `AIT_CMMS_REV3_PyQt5.py`:

```python
# OLD - REMOVE THESE LINES
from cm_parts_integration import CMPartsIntegration
from user_management_ui import UserManagementDialog
from password_change_ui import show_password_change_dialog
# Remove any Tkinter KPI trend imports

# NEW - ADD THESE LINES
from parts_integration_dialog_pyqt5 import (
    CMPartsIntegrationDialog,
    CMPartsViewDialog,
    show_parts_consumption_dialog,
    show_cm_parts_details
)
from user_management_dialog_pyqt5 import (
    UserManagementDialog,
    show_user_management_dialog
)
from password_change_dialog_pyqt5 import (
    PasswordChangeDialog,
    show_password_change_dialog
)
from kpi_trend_analyzer_tab_pyqt5 import (
    KPITrendAnalyzerTab,
    show_kpi_trends
)
```

---

### Step 2: Add Menu Items

Add these menu items to your main window:

```python
def create_menus(self):
    """Create application menus"""
    menubar = self.menuBar()

    # ===== USER MENU =====
    user_menu = menubar.addMenu("&User")

    # Change Password
    change_pwd_action = QAction("Change Password", self)
    change_pwd_action.triggered.connect(self.show_password_change_dialog)
    user_menu.addAction(change_pwd_action)

    # User Management (Managers only)
    if hasattr(self, 'user_role') and self.user_role == "Manager":
        user_menu.addSeparator()

        manage_users_action = QAction("Manage Users", self)
        manage_users_action.triggered.connect(self.show_user_management_dialog)
        user_menu.addAction(manage_users_action)

    # ===== TOOLS MENU =====
    tools_menu = menubar.addMenu("&Tools")

    # KPI Trends
    kpi_trends_action = QAction("KPI Trends && Alerts", self)
    kpi_trends_action.triggered.connect(self.show_kpi_trends)
    tools_menu.addAction(kpi_trends_action)
```

---

### Step 3: Implement Menu Action Methods

Add these methods to your main window class:

```python
def show_password_change_dialog(self):
    """Show password change dialog"""
    try:
        dialog = PasswordChangeDialog(
            current_user=self.current_user_full_name,
            username=self.current_username,
            parent=self
        )
        dialog.password_changed.connect(self.on_password_changed)
        dialog.exec_()
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to open password change dialog: {str(e)}")

def on_password_changed(self, success):
    """Handle password change completion"""
    if success:
        self.statusBar().showMessage("Password changed successfully", 5000)

def show_user_management_dialog(self):
    """Show user management dialog (Managers only)"""
    if not hasattr(self, 'user_role') or self.user_role != "Manager":
        QMessageBox.warning(self, "Access Denied",
                          "Only managers can access user management")
        return

    try:
        dialog = UserManagementDialog(
            current_user=self.current_username,
            parent=self
        )
        dialog.user_updated.connect(self.on_users_updated)
        dialog.show()  # Non-modal
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to open user management: {str(e)}")

def on_users_updated(self):
    """Handle user list updates"""
    self.statusBar().showMessage("User list updated", 3000)

def show_kpi_trends(self):
    """Show KPI trends analyzer"""
    try:
        # Can be shown as dialog or added as tab
        dialog = QDialog(self)
        dialog.setWindowTitle("KPI Trends & Alerts")
        dialog.setMinimumSize(1200, 800)

        layout = QVBoxLayout()
        kpi_tab = KPITrendAnalyzerTab(self.conn, dialog)
        kpi_tab.status_updated.connect(lambda msg: self.statusBar().showMessage(msg, 3000))
        layout.addWidget(kpi_tab)

        dialog.setLayout(layout)
        dialog.show()
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to open KPI trends: {str(e)}")
```

---

### Step 4: Integrate Parts Dialog in CM Management

Replace parts integration calls in your CM Management tab:

```python
# In your CM Management tab class

def record_parts_consumed(self, cm_number, technician_name):
    """Show parts consumption dialog for a CM work order"""
    try:
        dialog = CMPartsIntegrationDialog(
            cm_number=cm_number,
            technician_name=technician_name,
            conn=self.conn,
            parent=self
        )
        dialog.parts_saved.connect(lambda success: self.on_parts_saved(cm_number, success))
        dialog.exec_()
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to open parts dialog: {str(e)}")

def on_parts_saved(self, cm_number, success):
    """Handle parts save completion"""
    if success:
        self.statusBar().showMessage(f"Parts recorded for CM {cm_number}", 5000)
        # Refresh CM list or details as needed
        self.refresh_cm_list()

def view_cm_parts(self, cm_number):
    """View parts consumed for a CM work order"""
    try:
        dialog = CMPartsViewDialog(
            cm_number=cm_number,
            conn=self.conn,
            parent=self
        )
        dialog.exec_()
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to view parts: {str(e)}")
```

---

### Step 5: Add KPI Tab to Main Tab Widget (Optional)

To add KPI Trends as a permanent tab instead of a dialog:

```python
def setup_tabs(self):
    """Setup all tabs in main window"""
    self.tab_widget = QTabWidget()

    # ... existing tabs ...

    # Add KPI Trends Tab
    try:
        self.kpi_tab = KPITrendAnalyzerTab(self.conn, self)
        self.kpi_tab.status_updated.connect(
            lambda msg: self.statusBar().showMessage(msg, 3000)
        )
        self.tab_widget.addTab(self.kpi_tab, "KPI Trends")
    except Exception as e:
        print(f"Warning: Could not add KPI Trends tab: {e}")

    self.setCentralWidget(self.tab_widget)
```

---

### Step 6: Add Context Menu Items (Optional)

Add right-click context menu in CM Management table:

```python
def create_cm_context_menu(self, position):
    """Create context menu for CM table"""
    menu = QMenu()

    selected_items = self.cm_table.selectedItems()
    if not selected_items:
        return

    row = selected_items[0].row()
    cm_number = self.cm_table.item(row, 0).text()  # Assuming column 0 has CM number

    # Add Parts action
    add_parts_action = QAction("Record Parts Consumed", self)
    add_parts_action.triggered.connect(
        lambda: self.record_parts_consumed(cm_number, self.current_user)
    )
    menu.addAction(add_parts_action)

    # View Parts action
    view_parts_action = QAction("View Parts Used", self)
    view_parts_action.triggered.connect(lambda: self.view_cm_parts(cm_number))
    menu.addAction(view_parts_action)

    menu.exec_(self.cm_table.viewport().mapToGlobal(position))

# Connect context menu to table
self.cm_table.setContextMenuPolicy(Qt.CustomContextMenu)
self.cm_table.customContextMenuRequested.connect(self.create_cm_context_menu)
```

---

## Complete Example - Main Window Class

Here's a complete example showing how to integrate all modules:

```python
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMenuBar, QAction, QMessageBox
from PyQt5.QtCore import Qt
from parts_integration_dialog_pyqt5 import CMPartsIntegrationDialog, CMPartsViewDialog
from user_management_dialog_pyqt5 import UserManagementDialog
from password_change_dialog_pyqt5 import PasswordChangeDialog
from kpi_trend_analyzer_tab_pyqt5 import KPITrendAnalyzerTab


class CMSMainWindow(QMainWindow):
    """Main CMMS Application Window"""

    def __init__(self, conn, current_user, user_role):
        super().__init__()
        self.conn = conn
        self.current_username = current_user
        self.current_user_full_name = current_user  # Get from database
        self.user_role = user_role

        self.setWindowTitle("AIT CMMS NEON 2.2")
        self.setMinimumSize(1400, 900)

        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        # Create menus
        self.create_menus()

        # Create tabs
        self.setup_tabs()

        # Create status bar
        self.statusBar().showMessage("Ready")

    def create_menus(self):
        """Create application menus"""
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("&File")

        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # User Menu
        user_menu = menubar.addMenu("&User")

        change_pwd_action = QAction("Change Password", self)
        change_pwd_action.triggered.connect(self.show_password_change_dialog)
        user_menu.addAction(change_pwd_action)

        if self.user_role == "Manager":
            user_menu.addSeparator()
            manage_users_action = QAction("Manage Users", self)
            manage_users_action.triggered.connect(self.show_user_management_dialog)
            user_menu.addAction(manage_users_action)

        # Tools Menu
        tools_menu = menubar.addMenu("&Tools")

        kpi_trends_action = QAction("KPI Trends && Alerts", self)
        kpi_trends_action.triggered.connect(self.show_kpi_trends)
        tools_menu.addAction(kpi_trends_action)

        # Help Menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_tabs(self):
        """Setup all tabs"""
        self.tab_widget = QTabWidget()

        # Add your existing tabs here...
        # self.equipment_tab = EquipmentTab(self.conn, self.technicians, self)
        # self.tab_widget.addTab(self.equipment_tab, "Equipment")

        # Add KPI Trends Tab
        try:
            self.kpi_tab = KPITrendAnalyzerTab(self.conn, self)
            self.kpi_tab.status_updated.connect(
                lambda msg: self.statusBar().showMessage(msg, 3000)
            )
            self.tab_widget.addTab(self.kpi_tab, "KPI Trends")
        except Exception as e:
            print(f"Warning: Could not add KPI Trends tab: {e}")

        self.setCentralWidget(self.tab_widget)

    # ===== DIALOG METHODS =====

    def show_password_change_dialog(self):
        """Show password change dialog"""
        try:
            dialog = PasswordChangeDialog(
                current_user=self.current_user_full_name,
                username=self.current_username,
                parent=self
            )
            dialog.password_changed.connect(self.on_password_changed)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error",
                               f"Failed to open password change dialog: {str(e)}")

    def on_password_changed(self, success):
        """Handle password change completion"""
        if success:
            self.statusBar().showMessage("Password changed successfully", 5000)

    def show_user_management_dialog(self):
        """Show user management dialog"""
        if self.user_role != "Manager":
            QMessageBox.warning(self, "Access Denied",
                              "Only managers can access user management")
            return

        try:
            dialog = UserManagementDialog(
                current_user=self.current_username,
                parent=self
            )
            dialog.user_updated.connect(self.on_users_updated)
            dialog.show()
        except Exception as e:
            QMessageBox.critical(self, "Error",
                               f"Failed to open user management: {str(e)}")

    def on_users_updated(self):
        """Handle user list updates"""
        self.statusBar().showMessage("User list updated", 3000)

    def show_kpi_trends(self):
        """Show KPI trends analyzer"""
        try:
            from PyQt5.QtWidgets import QDialog, QVBoxLayout

            dialog = QDialog(self)
            dialog.setWindowTitle("KPI Trends & Alerts")
            dialog.setMinimumSize(1200, 800)

            layout = QVBoxLayout()
            kpi_widget = KPITrendAnalyzerTab(self.conn, dialog)
            kpi_widget.status_updated.connect(
                lambda msg: self.statusBar().showMessage(msg, 3000)
            )
            layout.addWidget(kpi_widget)

            dialog.setLayout(layout)
            dialog.show()
        except Exception as e:
            QMessageBox.critical(self, "Error",
                               f"Failed to open KPI trends: {str(e)}")

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About CMMS",
                         "AIT CMMS NEON 2.2\n\n"
                         "Computerized Maintenance Management System\n"
                         "PyQt5 Version")
```

---

## Testing the Integration

### 1. Test Password Change
1. Run application and login
2. Click User > Change Password
3. Enter current password
4. Enter new password (min 4 chars)
5. Confirm new password
6. Verify success message
7. Logout and login with new password

### 2. Test User Management (Manager only)
1. Login as manager
2. Click User > Manage Users
3. Click "Add User" - create test user
4. Select user and click "Edit User" - modify details
5. Click "View Sessions" - check active sessions
6. Select user and click "Delete User" - remove test user

### 3. Test Parts Integration
1. Open CM Management tab
2. Select a CM work order
3. Click button to record parts (or right-click context menu)
4. Search for a part
5. Select part and enter quantity
6. Click "Add to Consumed List"
7. Click "Save and Complete"
8. Verify parts recorded in database

### 4. Test KPI Trends
1. Click Tools > KPI Trends & Alerts
2. View Alerts tab - check for any alerts
3. View Dashboard tab - see summary
4. View Detailed Trends tab - select KPI and view analysis
5. View Charts tab - see visualization
6. Click "Export Report" - save text report
7. Click "Export to CSV" - save CSV data

---

## Troubleshooting

### Common Integration Issues

**Problem**: Import errors
**Solution**: Ensure all files are in the same directory as main application

**Problem**: Database connection errors
**Solution**: Verify `self.conn` is a valid psycopg2 connection

**Problem**: Signal not connecting
**Solution**: Check signal name matches exactly (case-sensitive)

**Problem**: Dialog doesn't appear
**Solution**: Check for exceptions, use try-except blocks

**Problem**: Matplotlib charts not showing
**Solution**: Install matplotlib: `pip install matplotlib`

---

## Migration Checklist

- [ ] Update imports in main application file
- [ ] Remove old Tkinter dialog code
- [ ] Add menu items for new dialogs
- [ ] Implement menu action methods
- [ ] Update CM Management to use new parts dialog
- [ ] Add KPI tab to main tab widget (optional)
- [ ] Test password change functionality
- [ ] Test user management (as manager)
- [ ] Test parts integration in CM workflow
- [ ] Test KPI trends and alerts
- [ ] Update documentation
- [ ] Train users on new interfaces

---

## Performance Optimization

### Database Queries
- Use connection pooling (`db_pool`) for better performance
- Add indexes on frequently queried columns
- Limit historical data queries with date ranges

### UI Responsiveness
- Load large datasets asynchronously
- Use pagination for long lists
- Show loading indicators for slow operations

### Memory Management
- Close dialogs when done
- Disconnect signals when widgets destroyed
- Clear large data structures after use

---

## Next Steps

1. **Backup Current System**: Before integration, backup database and code
2. **Test in Development**: Test all modules in development environment
3. **User Acceptance Testing**: Have end users test new interfaces
4. **Deploy to Production**: Roll out gradually, monitor for issues
5. **Gather Feedback**: Collect user feedback for improvements
6. **Document Changes**: Update user manuals and training materials

---

## Support

For issues or questions:
1. Check error messages in console output
2. Review database logs for SQL errors
3. Verify all dependencies installed
4. Check file permissions
5. Consult UTILITY_MODULES_PYQT5_README.md for detailed documentation

---

Last Updated: 2025-11-15
Version: 1.0

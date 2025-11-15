#!/usr/bin/env python3
"""
Test script for Equipment Tab PyQt5 Implementation

This script creates a standalone window to test the Equipment Management tab
without requiring the full CMMS application.

Usage:
    python test_equipment_tab.py

Requirements:
    - PyQt5
    - pandas
    - psycopg2-binary
    - Access to CMMS database
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QMessageBox, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt
import psycopg2

# Add current directory to path to import equipment_tab_pyqt5
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from equipment_tab_pyqt5 import EquipmentTab


class TestMainWindow(QMainWindow):
    """Test main window for Equipment Tab"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equipment Management Tab - Test Window")
        self.resize(1400, 900)

        # Database configuration - MODIFY THESE VALUES
        self.DB_CONFIG = {
            'host': 'localhost',
            'database': 'cmms_database',
            'user': 'postgres',
            'password': 'your_password_here',
            'port': 5432
        }

        # Technicians list - MODIFY AS NEEDED
        self.technicians = [
            'John Smith',
            'Jane Doe',
            'Bob Johnson',
            'Alice Williams',
            'Charlie Brown'
        ]

        # Try to connect to database
        if not self.connect_to_database():
            QMessageBox.critical(
                self,
                "Database Connection Failed",
                "Could not connect to the database.\n\n"
                "Please check your database configuration in test_equipment_tab.py\n"
                "and ensure the database server is running."
            )
            sys.exit(1)

        self.init_ui()

    def connect_to_database(self):
        """Connect to the database"""
        try:
            self.conn = psycopg2.connect(
                host=self.DB_CONFIG['host'],
                database=self.DB_CONFIG['database'],
                user=self.DB_CONFIG['user'],
                password=self.DB_CONFIG['password'],
                port=self.DB_CONFIG['port']
            )

            # Test connection
            cursor = self.conn.cursor()
            cursor.execute('SELECT version()')
            version = cursor.fetchone()
            print(f"Connected to database: {version[0]}")

            # Check if equipment table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = 'equipment'
                )
            """)
            table_exists = cursor.fetchone()[0]

            if not table_exists:
                QMessageBox.warning(
                    self,
                    "Equipment Table Missing",
                    "The 'equipment' table does not exist in the database.\n\n"
                    "The tab will load but may not function correctly.\n"
                    "Please create the required database schema."
                )

            return True

        except psycopg2.Error as e:
            print(f"Database connection error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def init_ui(self):
        """Initialize the user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Create equipment tab
        try:
            self.equipment_tab = EquipmentTab(
                self.conn,
                self.technicians,
                parent=self
            )

            # Connect status updates to status bar
            self.equipment_tab.status_updated.connect(self.update_status)

            # Add tab
            self.tabs.addTab(self.equipment_tab, "Equipment Management")

            # Initial status
            self.update_status("Equipment Management Tab loaded successfully")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Loading Equipment Tab",
                f"Failed to load Equipment Tab:\n\n{str(e)}"
            )
            print(f"Error loading equipment tab: {e}")
            import traceback
            traceback.print_exc()

    def update_status(self, message):
        """Update status bar with message"""
        self.statusBar().showMessage(message, 5000)  # Show for 5 seconds
        print(f"Status: {message}")

    def closeEvent(self, event):
        """Handle window close event"""
        # Ask for confirmation
        reply = QMessageBox.question(
            self,
            'Exit',
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Close database connection
            if hasattr(self, 'conn') and self.conn:
                try:
                    self.conn.close()
                    print("Database connection closed")
                except:
                    pass
            event.accept()
        else:
            event.ignore()


def check_dependencies():
    """Check if all required dependencies are installed"""
    missing_deps = []

    try:
        import PyQt5
    except ImportError:
        missing_deps.append('PyQt5')

    try:
        import pandas
    except ImportError:
        missing_deps.append('pandas')

    try:
        import psycopg2
    except ImportError:
        missing_deps.append('psycopg2-binary')

    if missing_deps:
        print("ERROR: Missing dependencies!")
        print("\nPlease install the following packages:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nInstall with: pip install " + " ".join(missing_deps))
        return False

    return True


def main():
    """Main function"""
    print("=" * 60)
    print("Equipment Management Tab - Test Script")
    print("=" * 60)

    # Check dependencies
    print("\nChecking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("All dependencies found!")

    # Check if equipment_tab_pyqt5.py exists
    if not os.path.exists('equipment_tab_pyqt5.py'):
        print("\nERROR: equipment_tab_pyqt5.py not found!")
        print("Please ensure the file is in the same directory as this test script.")
        sys.exit(1)
    print("Equipment tab module found!")

    # Create application
    print("\nStarting application...")
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')  # Modern look

    # Create and show main window
    window = TestMainWindow()
    window.show()

    print("\nTest window opened successfully!")
    print("\nInstructions:")
    print("  1. The Equipment Management tab should be visible")
    print("  2. Try adding, editing, and filtering equipment")
    print("  3. Check the status bar for messages")
    print("  4. Close the window to exit")
    print("\n" + "=" * 60)

    # Run application
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

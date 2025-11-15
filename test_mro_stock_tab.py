"""
Test file for MRO Stock Tab
Verifies basic functionality and database setup
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import psycopg2
from psycopg2.extras import RealDictCursor
import traceback

# Import the MRO Stock Tab
try:
    from mro_stock_tab_pyqt5 import MROStockTab
    print("✓ Successfully imported MROStockTab")
except ImportError as e:
    print(f"✗ Failed to import MROStockTab: {e}")
    sys.exit(1)


def test_database_connection():
    """Test database connection"""
    print("\n=== Testing Database Connection ===")

    # Update these with your database credentials
    DB_CONFIG = {
        'host': 'localhost',
        'database': 'your_database',
        'user': 'your_user',
        'password': 'your_password'
    }

    try:
        conn = psycopg2.connect(
            **DB_CONFIG,
            cursor_factory=RealDictCursor
        )
        print("✓ Database connection successful")
        return conn
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return None


def test_table_creation(conn):
    """Test that all required tables are created"""
    print("\n=== Testing Table Creation ===")

    required_tables = [
        'mro_inventory',
        'mro_stock_transactions',
        'cm_parts_used'
    ]

    try:
        cursor = conn.cursor()

        for table_name in required_tables:
            cursor.execute('''
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = %s
                );
            ''', (table_name,))

            exists = cursor.fetchone()['exists']

            if exists:
                print(f"✓ Table '{table_name}' exists")
            else:
                print(f"✗ Table '{table_name}' does not exist")

        return True

    except Exception as e:
        print(f"✗ Error checking tables: {e}")
        return False


def test_insert_sample_data(conn):
    """Insert sample data for testing"""
    print("\n=== Inserting Sample Data ===")

    sample_parts = [
        {
            'name': 'Test Bearing',
            'part_number': 'TEST-001',
            'model_number': 'BRG-123',
            'equipment': 'Pump A',
            'engineering_system': 'Mechanical',
            'unit_of_measure': 'EA',
            'quantity_in_stock': 10.0,
            'unit_price': 25.50,
            'minimum_stock': 5.0,
            'supplier': 'Test Supplier Inc.',
            'location': 'WAREHOUSE-A',
            'rack': 'R-01',
            'row': 'ROW-2',
            'bin': 'BIN-C',
            'notes': 'Test part for verification'
        },
        {
            'name': 'Test Filter',
            'part_number': 'TEST-002',
            'model_number': 'FLT-456',
            'equipment': 'Compressor B',
            'engineering_system': 'Hydraulic',
            'unit_of_measure': 'EA',
            'quantity_in_stock': 3.0,
            'unit_price': 45.00,
            'minimum_stock': 8.0,  # Low stock for testing
            'supplier': 'Filter Co.',
            'location': 'WAREHOUSE-B',
            'rack': 'R-05',
            'row': 'ROW-1',
            'bin': 'BIN-A',
            'notes': 'Low stock test part'
        }
    ]

    try:
        cursor = conn.cursor()

        for part in sample_parts:
            try:
                cursor.execute('''
                    INSERT INTO mro_inventory (
                        name, part_number, model_number, equipment, engineering_system,
                        unit_of_measure, quantity_in_stock, unit_price, minimum_stock,
                        supplier, location, rack, row, bin, notes
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (part_number) DO NOTHING
                ''', (
                    part['name'], part['part_number'], part['model_number'],
                    part['equipment'], part['engineering_system'],
                    part['unit_of_measure'], part['quantity_in_stock'],
                    part['unit_price'], part['minimum_stock'], part['supplier'],
                    part['location'], part['rack'], part['row'], part['bin'],
                    part['notes']
                ))

                if cursor.rowcount > 0:
                    print(f"✓ Inserted part: {part['part_number']}")
                else:
                    print(f"⚠ Part already exists: {part['part_number']}")

            except Exception as e:
                print(f"✗ Error inserting {part['part_number']}: {e}")

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"✗ Error inserting sample data: {e}")
        return False


def test_ui_creation(conn):
    """Test UI creation"""
    print("\n=== Testing UI Creation ===")

    try:
        app = QApplication(sys.argv)

        # Create main window
        window = QMainWindow()
        window.setWindowTitle("MRO Stock Tab - Test")
        window.setGeometry(100, 100, 1400, 800)

        # Create MRO Stock tab
        mro_tab = MROStockTab(
            conn=conn,
            current_user="Test User"
        )

        window.setCentralWidget(mro_tab)

        print("✓ UI created successfully")
        print("✓ Opening test window...")

        # Show instructions
        QMessageBox.information(
            window,
            "Test Instructions",
            "Test Window Created!\n\n"
            "Please verify:\n"
            "1. Statistics show correct counts\n"
            "2. Table displays sample parts\n"
            "3. Filters work correctly\n"
            "4. Search functions properly\n"
            "5. Low stock item (TEST-002) is highlighted\n\n"
            "Close the window when done testing."
        )

        window.show()
        return app.exec_()

    except Exception as e:
        print(f"✗ Error creating UI: {e}")
        traceback.print_exc()
        return 1


def main():
    """Main test function"""
    print("=" * 60)
    print("MRO Stock Tab - Test Suite")
    print("=" * 60)

    # Test 1: Database Connection
    conn = test_database_connection()
    if not conn:
        print("\n❌ Database connection failed. Please update DB_CONFIG in this file.")
        print("Update the following in test_mro_stock_tab.py:")
        print("  - host")
        print("  - database")
        print("  - user")
        print("  - password")
        return 1

    # Test 2: Table Creation (automatic via MROStockTab init)
    print("\n=== Initializing MRO Stock Module ===")
    try:
        # This will create tables automatically
        from mro_stock_tab_pyqt5 import MROStockTab

        # Create a temporary instance to initialize database
        temp_conn = psycopg2.connect(
            host='localhost',
            database='your_database',
            user='your_user',
            password='your_password',
            cursor_factory=RealDictCursor
        )

        # Create instance (this calls init_database)
        temp_tab = MROStockTab(temp_conn, current_user="Init")
        print("✓ Database initialization complete")

    except Exception as e:
        print(f"✗ Error during initialization: {e}")
        traceback.print_exc()
        return 1

    # Test 3: Verify tables exist
    test_table_creation(conn)

    # Test 4: Insert sample data
    test_insert_sample_data(conn)

    # Test 5: Create UI and run
    print("\n=== Starting UI Test ===")
    result = test_ui_creation(conn)

    # Cleanup
    if conn:
        conn.close()
        print("\n✓ Database connection closed")

    print("\n" + "=" * 60)
    if result == 0:
        print("✓ All tests completed successfully!")
    else:
        print("⚠ Some tests may have issues. Review output above.")
    print("=" * 60)

    return result


if __name__ == '__main__':
    sys.exit(main())

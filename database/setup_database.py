"""
EPAM Practice Database Setup
Creates SQLite database with sample data for all exercises
"""

import sqlite3
from datetime import datetime, timedelta

def create_database():
    """Create database with all necessary tables"""
    
    # Connect to database
    conn = sqlite3.connect('epam_practice.db')
    cursor = conn.cursor()
    
    print("Creating tables...")
    
    # =========================================================================
    # EMPLOYEES TABLE
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        emp_id INTEGER PRIMARY KEY,
        emp_name TEXT NOT NULL,
        job_name TEXT,
        manager_id INTEGER,
        start_date DATE,
        salary REAL,
        commission REAL,
        dep_id INTEGER
    )
    ''')
    
    # Sample data for employees
    employees_data = [
        (68319, 'KAYLING', 'PRESIDENT', None, '1991-11-18', 6000.00, None, 1001),
        (66928, 'BLAZE', 'MANAGER', 68319, '1991-05-01', 2750.00, None, 3001),
        (67832, 'CLARE', 'MANAGER', 68319, '1991-06-09', 2550.00, None, 1001),
        (65646, 'JONAS', 'MANAGER', 68319, '1991-04-02', 2957.00, None, 2001),
        (67858, 'SCARLET', 'ANALYST', 65646, '1997-04-19', 3100.00, None, 2001),
        (69062, 'FRANK', 'ANALYST', 65646, '1991-12-03', 3100.00, None, 2001),
        (63679, 'SANDRINE', 'CLERK', 69062, '1990-12-18', 900.00, None, 2001),
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO employees VALUES (?,?,?,?,?,?,?,?)', employees_data)
    
    # =========================================================================
    # DEPARTMENTS TABLE
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY,
        department_name TEXT NOT NULL
    )
    ''')
    
    departments_data = [
        (1001, 'Executive'),
        (2001, 'Analytics'),
        (3001, 'Operations'),
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO departments VALUES (?,?)', departments_data)
    
    # =========================================================================
    # ORDERS TABLE (for window functions practice)
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        cid TEXT,
        order_id TEXT PRIMARY KEY,
        order_date DATE,
        order_value REAL
    )
    ''')
    
    orders_data = [
        ('A', 'qwerty', '2024-01-01', 10),
        ('A', 'asdfgh', '2024-01-03', 20),
        ('A', 'zxcvbn', '2024-01-10', 30),
        ('B', 'uiopyy', '2024-01-02', 40),
        ('B', 'lkjhgf', '2024-01-06', 50),
        ('B', 'mnbvcx', '2024-01-08', 60),
        ('B', 'rtyfgh', '2024-01-10', 70),
        ('C', 'fghcvb', '2024-02-01', 80),
        ('C', 'bnmghj', '2024-02-01', 90),
        ('C', 'wersdf', '2024-02-03', 100),
        ('C', 'asdzxc', '2024-02-04', 110),
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO orders VALUES (?,?,?,?)', orders_data)
    
    # =========================================================================
    # EMPLOYEE TABLE (for manager/bonus exercises)
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employee (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        managerId INTEGER
    )
    ''')
    
    employee_data = [
        (101, 'John', 'A', None),
        (102, 'Dan', 'A', 101),
        (103, 'James', 'A', 101),
        (104, 'Amy', 'A', 101),
        (105, 'Anne', 'A', 101),
        (106, 'Ron', 'B', 101),
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO employee VALUES (?,?,?,?)', employee_data)
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employee_salary (
        empId INTEGER PRIMARY KEY,
        name TEXT,
        supervisor INTEGER,
        salary REAL
    )
    ''')
    
    employee_salary_data = [
        (3, 'Brad', None, 4000),
        (1, 'John', 3, 1000),
        (2, 'Dan', 3, 2000),
        (4, 'Thomas', 3, 4000),
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO employee_salary VALUES (?,?,?,?)', employee_salary_data)
    
    # =========================================================================
    # BONUS TABLE
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bonus (
        empId INTEGER PRIMARY KEY,
        bonus REAL
    )
    ''')
    
    bonus_data = [
        (2, 500),
        (4, 2000),
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO bonus VALUES (?,?)', bonus_data)
    
    # =========================================================================
    # COURSES TABLE
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        student TEXT,
        class TEXT
    )
    ''')
    
    courses_data = [
        ('A', 'Math'),
        ('B', 'English'),
        ('C', 'Math'),
        ('D', 'Biology'),
        ('E', 'Math'),
        ('F', 'Computer'),
        ('G', 'Math'),
        ('H', 'Math'),
        ('I', 'Math'),
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO courses VALUES (?,?)', courses_data)
    
    # =========================================================================
    # SALES AND PRODUCTS TABLES
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY,
        product_id INTEGER,
        year INTEGER,
        quantity INTEGER,
        price REAL
    )
    ''')
    
    sales_data = [
        (1, 100, 2008, 10, 5000),
        (2, 100, 2009, 12, 5000),
        (7, 200, 2011, 15, 9000),
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO sales VALUES (?,?,?,?,?)', sales_data)
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT
    )
    ''')
    
    products_data = [
        (100, 'Nokia'),
        (200, 'Apple'),
        (300, 'Samsung'),
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO products VALUES (?,?)', products_data)
    
    # =========================================================================
    # STUDENTS TABLE
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER
    )
    ''')
    
    students_data = [
        (101, 'Ulysses', 13),
        (53, 'William', 10),
        (128, 'Henry', 6),
        (3, 'Henry', 11),
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO students VALUES (?,?,?)', students_data)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("✅ Database created successfully!")
    print(f"✅ Location: epam_practice.db")
    print("\nTables created:")
    print("  - employees (7 rows)")
    print("  - departments (3 rows)")
    print("  - orders (11 rows)")
    print("  - employee (6 rows)")
    print("  - employee_salary (4 rows)")
    print("  - bonus (2 rows)")
    print("  - courses (9 rows)")
    print("  - sales (3 rows)")
    print("  - products (3 rows)")
    print("  - students (4 rows)")
    print("\n🚀 Ready for SQL practice!")

def test_database():
    """Test database with a simple query"""
    conn = sqlite3.connect('epam_practice.db')
    cursor = conn.cursor()
    
    print("\n" + "="*70)
    print("Testing database...")
    print("="*70)
    
    # Test query
    cursor.execute("SELECT * FROM orders LIMIT 5")
    results = cursor.fetchall()
    
    print("\nSample from orders table:")
    print("cid | order_id | order_date | order_value")
    print("-" * 50)
    for row in results:
        print(f"{row[0]:3} | {row[1]:8} | {row[2]} | {row[3]}")
    
    conn.close()
    print("\n✅ Database test passed!")

if __name__ == "__main__":
    print("="*70)
    print("EPAM Practice Database Setup")
    print("="*70)
    print()
    
    create_database()
    test_database()
    
    print("\n" + "="*70)
    print("Setup complete! You can now:")
    print("  1. Open epam_practice.db in DBeaver or any SQL client")
    print("  2. Practice SQL queries from exercises")
    print("  3. Test EPAM interview problems")
    print("="*70)


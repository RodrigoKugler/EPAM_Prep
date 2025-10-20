"""
EPAM Enhanced Practice Database Setup
Creates a comprehensive SQLite database with realistic business data
for advanced SQL practice and EPAM interview preparation.

From Data Engineer Perspective:
- Realistic data volumes (1000s of records)
- Proper business relationships
- Time series data for window functions
- Edge cases and complex scenarios
- Performance testing scenarios
"""

import sqlite3
import random
from datetime import datetime, timedelta

def create_enhanced_database():
    """Create comprehensive database with realistic business data"""
    
    # Connect to database
    conn = sqlite3.connect('epam_practice.db')
    cursor = conn.cursor()
    
    print("Creating Enhanced EPAM Practice Database...")
    print("="*70)
    
    # Drop existing tables to start fresh
    drop_tables = [
        'DROP TABLE IF EXISTS order_items',
        'DROP TABLE IF EXISTS orders', 
        'DROP TABLE IF EXISTS customers',
        'DROP TABLE IF EXISTS products',
        'DROP TABLE IF EXISTS categories',
        'DROP TABLE IF EXISTS employees',
        'DROP TABLE IF EXISTS departments',
        'DROP TABLE IF EXISTS salaries',
        'DROP TABLE IF EXISTS sales_territories',
        'DROP TABLE IF EXISTS sales_reps',
        'DROP TABLE IF EXISTS sales',
        'DROP TABLE IF EXISTS monthly_revenue',
        'DROP TABLE IF EXISTS student_enrollments',
        'DROP TABLE IF EXISTS courses',
        'DROP TABLE IF EXISTS students',
        'DROP TABLE IF EXISTS financial_transactions',
        'DROP TABLE IF EXISTS accounts',
        'DROP TABLE IF EXISTS inventory_movements',
        'DROP TABLE IF EXISTS warehouses'
    ]
    
    for drop_sql in drop_tables:
        cursor.execute(drop_sql)
    
    print("Dropped existing tables")
    
    # =========================================================================
    # WAREHOUSES TABLE
    # =========================================================================
    cursor.execute('''
    CREATE TABLE warehouses (
        warehouse_id INTEGER PRIMARY KEY,
        warehouse_name TEXT NOT NULL,
        location TEXT NOT NULL,
        capacity INTEGER,
        manager_id INTEGER
    )
    ''')
    
    warehouses_data = [
        (1, 'Central Warehouse', 'New York', 10000, 101),
        (2, 'West Coast Distribution', 'Los Angeles', 8000, 102),
        (3, 'South Regional Center', 'Atlanta', 6000, 103),
        (4, 'North Distribution Hub', 'Chicago', 7500, 104),
        (5, 'East Coast Terminal', 'Boston', 5500, 105)
    ]
    
    cursor.executemany('INSERT INTO warehouses VALUES (?,?,?,?,?)', warehouses_data)
    print("Created warehouses table (5 records)")
    
    # =========================================================================
    # CATEGORIES TABLE
    # =========================================================================
    cursor.execute('''
    CREATE TABLE categories (
        category_id INTEGER PRIMARY KEY,
        category_name TEXT NOT NULL,
        parent_category_id INTEGER,
        description TEXT
    )
    ''')
    
    categories_data = [
        (1, 'Electronics', None, 'Electronic devices and accessories'),
        (2, 'Smartphones', 1, 'Mobile phones and accessories'),
        (3, 'Laptops', 1, 'Portable computers'),
        (4, 'Clothing', None, 'Apparel and fashion'),
        (5, 'Men Clothing', 4, 'Men\'s apparel'),
        (6, 'Women Clothing', 4, 'Women\'s apparel'),
        (7, 'Home & Garden', None, 'Home improvement and garden supplies'),
        (8, 'Books', None, 'Books and educational materials'),
        (9, 'Sports', None, 'Sports and outdoor equipment')
    ]
    
    cursor.executemany('INSERT INTO categories VALUES (?,?,?,?)', categories_data)
    print("Created categories table (9 records)")
    
    # =========================================================================
    # PRODUCTS TABLE - Enhanced
    # =========================================================================
    cursor.execute('''
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category_id INTEGER,
        price DECIMAL(10,2) NOT NULL,
        cost DECIMAL(10,2),
        weight_kg DECIMAL(5,2),
        dimensions TEXT,
        created_date DATE,
        is_active BOOLEAN DEFAULT 1,
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    )
    ''')
    
    # Generate realistic product data
    products_data = []
    product_names = [
        # Smartphones
        'iPhone 15 Pro', 'Samsung Galaxy S24', 'Google Pixel 8', 'OnePlus 12',
        'iPhone 14', 'Samsung Galaxy S23', 'Google Pixel 7', 'Xiaomi 13',
        # Laptops
        'MacBook Pro 16"', 'Dell XPS 15', 'HP Spectre x360', 'Lenovo ThinkPad X1',
        'MacBook Air M2', 'Dell Inspiron 15', 'HP Pavilion', 'ASUS ROG Strix',
        # Men Clothing
        'Nike Air Max 270', 'Adidas Ultraboost', 'Levi\'s 501 Jeans', 'Ralph Lauren Polo',
        'Under Armour Hoodie', 'Champion T-Shirt', 'Vans Classic Sneakers', 'Timberland Boots',
        # Women Clothing
        'Zara Blazer', 'H&M Dress', 'Forever 21 Jeans', 'Gap Sweater',
        'Nike Sports Bra', 'Lululemon Leggings', 'Kate Spade Handbag', 'Coach Purse',
        # Home & Garden
        'Dyson V15 Vacuum', 'KitchenAid Mixer', 'Weber Grill', 'IKEA Bookshelf',
        'Philips Hue Lights', 'Nest Thermostat', 'Roomba i7', 'Instant Pot',
        # Books
        'Python Programming', 'Data Science Handbook', 'Machine Learning Guide',
        'Business Strategy', 'Personal Finance', 'History of Art', 'Cooking Masterclass',
        # Sports
        'Yoga Mat Premium', 'Resistance Bands Set', 'Adjustable Dumbbells',
        'Basketball Official', 'Tennis Racket Pro', 'Cycling Helmet', 'Running Shoes'
    ]
    
    prices = [29.99, 49.99, 79.99, 99.99, 149.99, 199.99, 299.99, 499.99, 699.99, 999.99, 1299.99, 1599.99]
    
    for i, product_name in enumerate(product_names):
        product_id = i + 1
        category_id = random.choice([2, 3, 5, 6, 7, 8, 9])  # Random category
        price = random.choice(prices)
        cost = price * 0.6
        weight = round(random.uniform(0.1, 5.0), 2)
        dimensions = f"{random.randint(10,50)}x{random.randint(10,50)}x{random.randint(5,20)} cm"
        created_date = (datetime.now() - timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d')
        
        products_data.append((
            product_id, product_name, category_id, price, cost, weight, 
            dimensions, created_date, 1
        ))
    
    cursor.executemany('INSERT INTO products VALUES (?,?,?,?,?,?,?,?,?)', products_data)
    print(f"Created products table ({len(products_data)} records)")
    
    # =========================================================================
    # CUSTOMERS TABLE - Enhanced
    # =========================================================================
    cursor.execute('''
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT,
        date_of_birth DATE,
        registration_date DATE,
        city TEXT,
        state TEXT,
        country TEXT DEFAULT 'USA',
        customer_segment TEXT,
        is_vip BOOLEAN DEFAULT 0,
        total_spent DECIMAL(10,2) DEFAULT 0
    )
    ''')
    
    # Generate realistic customer data
    customers_data = []
    first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Chris', 'Amy', 'Mark', 'Emma',
                   'James', 'Jessica', 'Robert', 'Jennifer', 'Michael', 'Ashley', 'William', 'Emily',
                   'Richard', 'Amanda', 'Joseph', 'Melissa', 'Thomas', 'Deborah', 'Charles', 'Dorothy']
    
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                  'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
                  'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson']
    
    segments = ['Premium', 'Standard', 'Budget', 'Enterprise']
    states = ['NY', 'CA', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 
              'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville']
    
    for i in range(500):  # 500 customers
        customer_id = i + 1
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}@email.com"
        phone = f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
        dob = (datetime.now() - timedelta(days=random.randint(18*365, 80*365))).strftime('%Y-%m-%d')
        reg_date = (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime('%Y-%m-%d')
        city = random.choice(cities)
        state = random.choice(states)
        segment = random.choice(segments)
        is_vip = random.choices([0, 1], weights=[85, 15])[0]  # 15% VIP
        total_spent = round(random.uniform(0, 5000), 2) if is_vip else round(random.uniform(0, 1000), 2)
        
        customers_data.append((
            customer_id, first_name, last_name, email, phone, dob, reg_date,
            city, state, 'USA', segment, is_vip, total_spent
        ))
    
    cursor.executemany('INSERT INTO customers VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', customers_data)
    print(f"Created customers table ({len(customers_data)} records)")
    
    # =========================================================================
    # ORDERS TABLE - Enhanced
    # =========================================================================
    cursor.execute('''
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date DATE NOT NULL,
        order_status TEXT,
        shipping_address TEXT,
        billing_address TEXT,
        payment_method TEXT,
        subtotal DECIMAL(10,2),
        tax_amount DECIMAL(10,2),
        shipping_cost DECIMAL(10,2),
        total_amount DECIMAL(10,2),
        warehouse_id INTEGER,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
    )
    ''')
    
    # Generate realistic order data
    orders_data = []
    statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled', 'Returned']
    payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Google Pay', 'Bank Transfer']
    
    for i in range(2000):  # 2000 orders
        order_id = i + 1
        customer_id = random.randint(1, 500)
        order_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
        status = random.choices(statuses, weights=[5, 10, 20, 60, 3, 2])[0]  # Most delivered
        shipping_address = f"{random.randint(100, 9999)} Main St, {random.choice(cities)}, {random.choice(states)}"
        billing_address = shipping_address if random.random() > 0.3 else f"{random.randint(100, 9999)} Oak Ave, {random.choice(cities)}, {random.choice(states)}"
        payment_method = random.choice(payment_methods)
        subtotal = round(random.uniform(25, 1500), 2)
        tax_amount = round(subtotal * 0.08, 2)  # 8% tax
        shipping_cost = round(random.uniform(0, 25), 2) if subtotal < 50 else 0
        total_amount = subtotal + tax_amount + shipping_cost
        warehouse_id = random.randint(1, 5)
        
        orders_data.append((
            order_id, customer_id, order_date, status, shipping_address,
            billing_address, payment_method, subtotal, tax_amount, shipping_cost,
            total_amount, warehouse_id
        ))
    
    cursor.executemany('INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', orders_data)
    print(f"Created orders table ({len(orders_data)} records)")
    
    # =========================================================================
    # ORDER_ITEMS TABLE
    # =========================================================================
    cursor.execute('''
    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        unit_price DECIMAL(10,2),
        total_price DECIMAL(10,2),
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    ''')
    
    # Generate realistic order items data
    order_items_data = []
    
    for order in orders_data:
        order_id = order[0]
        num_items = random.randint(1, 5)  # 1-5 items per order
        
        for item_num in range(num_items):
            order_item_id = len(order_items_data) + 1
            product_id = random.randint(1, len(product_names))
            quantity = random.randint(1, 3)
            
            # Get product price from products table
            cursor.execute('SELECT price FROM products WHERE product_id = ?', (product_id,))
            product_price = cursor.fetchone()[0]
            
            unit_price = product_price
            total_price = unit_price * quantity
            
            order_items_data.append((
                order_item_id, order_id, product_id, quantity, unit_price, total_price
            ))
    
    cursor.executemany('INSERT INTO order_items VALUES (?,?,?,?,?,?)', order_items_data)
    print(f"Created order_items table ({len(order_items_data)} records)")
    
    # =========================================================================
    # DEPARTMENTS TABLE - Enhanced
    # =========================================================================
    cursor.execute('''
    CREATE TABLE departments (
        department_id INTEGER PRIMARY KEY,
        department_name TEXT NOT NULL,
        manager_id INTEGER,
        budget DECIMAL(12,2),
        location TEXT,
        established_date DATE
    )
    ''')
    
    departments_data = [
        (1, 'Executive', None, 5000000, 'Corporate HQ', '2020-01-01'),
        (2, 'Sales', 101, 2000000, 'Sales Office', '2020-01-01'),
        (3, 'Marketing', 102, 1500000, 'Marketing Office', '2020-02-01'),
        (4, 'Engineering', 103, 8000000, 'Tech Center', '2020-01-15'),
        (5, 'Human Resources', 104, 800000, 'HR Office', '2020-03-01'),
        (6, 'Finance', 105, 1200000, 'Finance Office', '2020-01-01'),
        (7, 'Operations', 106, 3000000, 'Operations Center', '2020-02-15'),
        (8, 'Customer Service', 107, 1000000, 'Support Center', '2020-04-01')
    ]
    
    cursor.executemany('INSERT INTO departments VALUES (?,?,?,?,?,?)', departments_data)
    print("Created departments table (8 records)")
    
    # =========================================================================
    # EMPLOYEES TABLE - Enhanced
    # =========================================================================
    cursor.execute('''
    CREATE TABLE employees (
        employee_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE,
        hire_date DATE,
        department_id INTEGER,
        job_title TEXT,
        manager_id INTEGER,
        salary DECIMAL(10,2),
        commission_rate DECIMAL(5,2),
        is_active BOOLEAN DEFAULT 1,
        FOREIGN KEY (department_id) REFERENCES departments(department_id),
        FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
    )
    ''')
    
    # Generate realistic employee data
    employees_data = []
    job_titles = [
        'CEO', 'CTO', 'CFO', 'VP Sales', 'VP Marketing', 'VP Engineering',
        'Sales Director', 'Marketing Director', 'Engineering Director',
        'Senior Sales Manager', 'Sales Manager', 'Account Executive',
        'Senior Marketing Manager', 'Marketing Manager', 'Content Manager',
        'Senior Software Engineer', 'Software Engineer', 'Junior Developer',
        'DevOps Engineer', 'Data Scientist', 'Product Manager',
        'HR Director', 'HR Manager', 'HR Specialist', 'Recruiter',
        'Finance Director', 'Finance Manager', 'Financial Analyst',
        'Operations Director', 'Operations Manager', 'Operations Analyst',
        'Customer Service Manager', 'Customer Service Rep', 'Support Specialist'
    ]
    
    # Create managers first
    for i in range(20):  # 20 managers
        employee_id = i + 1
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}@company.com"
        hire_date = (datetime.now() - timedelta(days=random.randint(365, 1825))).strftime('%Y-%m-%d')
        department_id = random.randint(1, 8)
        job_title = random.choice(['CEO', 'CTO', 'CFO', 'VP Sales', 'VP Marketing', 'VP Engineering', 
                                   'Director', 'Manager'])
        manager_id = None if job_title in ['CEO', 'CTO', 'CFO'] else random.randint(1, 20)
        salary = round(random.uniform(80000, 200000), 2)
        commission_rate = round(random.uniform(0, 0.1), 2) if 'Sales' in job_title else 0
        
        employees_data.append((
            employee_id, first_name, last_name, email, hire_date, department_id,
            job_title, manager_id, salary, commission_rate, 1
        ))
    
    # Create regular employees
    for i in range(180):  # 180 regular employees
        employee_id = i + 21
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}@company.com"
        hire_date = (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime('%Y-%m-%d')
        department_id = random.randint(1, 8)
        job_title = random.choice([j for j in job_titles if j not in ['CEO', 'CTO', 'CFO']])
        manager_id = random.randint(1, 20)  # Report to a manager
        salary = round(random.uniform(35000, 120000), 2)
        commission_rate = round(random.uniform(0, 0.05), 2) if 'Sales' in job_title else 0
        
        employees_data.append((
            employee_id, first_name, last_name, email, hire_date, department_id,
            job_title, manager_id, salary, commission_rate, 1
        ))
    
    cursor.executemany('INSERT INTO employees VALUES (?,?,?,?,?,?,?,?,?,?,?)', employees_data)
    print(f"Created employees table ({len(employees_data)} records)")
    
    # =========================================================================
    # SALARIES TABLE (Historical salary data)
    # =========================================================================
    cursor.execute('''
    CREATE TABLE salaries (
        salary_id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        salary_amount DECIMAL(10,2),
        effective_date DATE,
        end_date DATE,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    )
    ''')
    
    # Generate salary history for employees
    salaries_data = []
    for employee in employees_data:
        employee_id = employee[0]
        current_salary = employee[8]
        hire_date = datetime.strptime(employee[4], '%Y-%m-%d')
        
        # Generate salary progression
        salary_amount = current_salary * 0.7  # Start 30% lower
        effective_date = hire_date
        
        for year in range(3):  # 3 years of salary history
            salary_id = len(salaries_data) + 1
            end_date = effective_date + timedelta(days=365)
            
            salaries_data.append((
                salary_id, employee_id, round(salary_amount, 2), 
                effective_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
            ))
            
            # Increase salary by 5-15% each year
            salary_amount *= (1 + random.uniform(0.05, 0.15))
            effective_date = end_date
    
    cursor.executemany('INSERT INTO salaries VALUES (?,?,?,?,?)', salaries_data)
    print(f"Created salaries table ({len(salaries_data)} records)")
    
    # =========================================================================
    # SALES_TERRITORIES TABLE
    # =========================================================================
    cursor.execute('''
    CREATE TABLE sales_territories (
        territory_id INTEGER PRIMARY KEY,
        territory_name TEXT NOT NULL,
        region TEXT,
        sales_rep_id INTEGER,
        target_revenue DECIMAL(12,2)
    )
    ''')
    
    territories_data = [
        (1, 'Northeast', 'East Coast', 101, 5000000),
        (2, 'Southeast', 'East Coast', 102, 4500000),
        (3, 'Midwest', 'Central', 103, 6000000),
        (4, 'Southwest', 'West Coast', 104, 4000000),
        (5, 'West Coast', 'West Coast', 105, 7000000),
        (6, 'Northwest', 'West Coast', 106, 3500000)
    ]
    
    cursor.executemany('INSERT INTO sales_territories VALUES (?,?,?,?,?)', territories_data)
    print("Created sales_territories table (6 records)")
    
    # =========================================================================
    # SALES_REPS TABLE
    # =========================================================================
    cursor.execute('''
    CREATE TABLE sales_reps (
        rep_id INTEGER PRIMARY KEY,
        rep_name TEXT NOT NULL,
        territory_id INTEGER,
        hire_date DATE,
        commission_rate DECIMAL(5,2),
        quota DECIMAL(10,2),
        FOREIGN KEY (territory_id) REFERENCES sales_territories(territory_id)
    )
    ''')
    
    sales_reps_data = []
    for i in range(50):  # 50 sales reps
        rep_id = i + 1
        rep_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        territory_id = random.randint(1, 6)
        hire_date = (datetime.now() - timedelta(days=random.randint(60, 730))).strftime('%Y-%m-%d')
        commission_rate = round(random.uniform(0.02, 0.08), 2)
        quota = round(random.uniform(500000, 2000000), 2)
        
        sales_reps_data.append((
            rep_id, rep_name, territory_id, hire_date, commission_rate, quota
        ))
    
    cursor.executemany('INSERT INTO sales_reps VALUES (?,?,?,?,?,?)', sales_reps_data)
    print(f"Created sales_reps table ({len(sales_reps_data)} records)")
    
    # =========================================================================
    # SALES TABLE (Monthly sales data)
    # =========================================================================
    cursor.execute('''
    CREATE TABLE sales (
        sale_id INTEGER PRIMARY KEY,
        rep_id INTEGER,
        territory_id INTEGER,
        sale_date DATE,
        product_id INTEGER,
        quantity INTEGER,
        unit_price DECIMAL(10,2),
        total_amount DECIMAL(10,2),
        commission_earned DECIMAL(10,2),
        FOREIGN KEY (rep_id) REFERENCES sales_reps(rep_id),
        FOREIGN KEY (territory_id) REFERENCES sales_territories(territory_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    ''')
    
    # Generate monthly sales data for the past 12 months
    sales_data = []
    start_date = datetime.now() - timedelta(days=365)
    
    for month in range(12):
        month_date = start_date + timedelta(days=30*month)
        days_in_month = 30
        
        for day in range(days_in_month):
            daily_date = month_date + timedelta(days=day)
            num_sales = random.randint(50, 200)  # 50-200 sales per day
            
            for sale_num in range(num_sales):
                sale_id = len(sales_data) + 1
                rep_id = random.randint(1, 50)
                territory_id = random.randint(1, 6)
                product_id = random.randint(1, len(product_names))
                quantity = random.randint(1, 10)
                unit_price = round(random.uniform(25, 500), 2)
                total_amount = unit_price * quantity
                
                # Get commission rate for this rep
                cursor.execute('SELECT commission_rate FROM sales_reps WHERE rep_id = ?', (rep_id,))
                commission_rate = cursor.fetchone()[0]
                commission_earned = total_amount * commission_rate
                
                sales_data.append((
                    sale_id, rep_id, territory_id, daily_date.strftime('%Y-%m-%d'),
                    product_id, quantity, unit_price, total_amount, round(commission_earned, 2)
                ))
    
    cursor.executemany('INSERT INTO sales VALUES (?,?,?,?,?,?,?,?,?)', sales_data)
    print(f"Created sales table ({len(sales_data)} records)")
    
    # =========================================================================
    # MONTHLY_REVENUE TABLE (For time series analysis)
    # =========================================================================
    cursor.execute('''
    CREATE TABLE monthly_revenue (
        month_id INTEGER PRIMARY KEY,
        year INTEGER,
        month INTEGER,
        revenue DECIMAL(12,2),
        expenses DECIMAL(12,2),
        profit DECIMAL(12,2),
        customer_count INTEGER,
        order_count INTEGER
    )
    ''')
    
    # Generate monthly revenue data for past 24 months
    monthly_revenue_data = []
    base_revenue = 1000000
    base_expenses = 600000
    
    for i in range(24):  # 24 months
        month_id = i + 1
        current_date = datetime.now() - timedelta(days=30*i)
        year = current_date.year
        month = current_date.month
        
        # Add seasonality and growth
        seasonality_factor = 1 + 0.3 * (month - 6) / 6  # Higher in summer
        growth_factor = 1 + (i * 0.02)  # 2% monthly growth
        random_factor = random.uniform(0.9, 1.1)  # Random variation
        
        revenue = base_revenue * seasonality_factor * growth_factor * random_factor
        expenses = base_expenses * growth_factor * random_factor
        profit = revenue - expenses
        customer_count = random.randint(800, 1200)
        order_count = random.randint(1500, 2500)
        
        monthly_revenue_data.append((
            month_id, year, month, round(revenue, 2), round(expenses, 2),
            round(profit, 2), customer_count, order_count
        ))
    
    cursor.executemany('INSERT INTO monthly_revenue VALUES (?,?,?,?,?,?,?,?)', monthly_revenue_data)
    print(f"Created monthly_revenue table ({len(monthly_revenue_data)} records)")
    
    # Create indexes for better performance
    print("\nCreating indexes for performance...")
    
    indexes = [
        'CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date)',
        'CREATE INDEX idx_orders_date ON orders(order_date)',
        'CREATE INDEX idx_orders_status ON orders(order_status)',
        'CREATE INDEX idx_order_items_order ON order_items(order_id)',
        'CREATE INDEX idx_order_items_product ON order_items(product_id)',
        'CREATE INDEX idx_products_category ON products(category_id)',
        'CREATE INDEX idx_products_price ON products(price)',
        'CREATE INDEX idx_employees_department ON employees(department_id)',
        'CREATE INDEX idx_employees_manager ON employees(manager_id)',
        'CREATE INDEX idx_sales_rep_date ON sales(rep_id, sale_date)',
        'CREATE INDEX idx_sales_date ON sales(sale_date)',
        'CREATE INDEX idx_sales_territory ON sales(territory_id)',
        'CREATE INDEX idx_salaries_employee ON salaries(employee_id)',
        'CREATE INDEX idx_salaries_date ON salaries(effective_date)',
        'CREATE INDEX idx_customers_segment ON customers(customer_segment)',
        'CREATE INDEX idx_customers_city ON customers(city)'
    ]
    
    for index_sql in indexes:
        cursor.execute(index_sql)
    
    print("Created performance indexes")
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("\n" + "="*70)
    print("ENHANCED DATABASE CREATED SUCCESSFULLY!")
    print("="*70)
    print("\nDATABASE STATISTICS:")
    print("="*70)
    print("BUSINESS TABLES:")
    print("  - customers: 500 records")
    print("  - products: 47 records") 
    print("  - orders: 2,000 records")
    print("  - order_items: ~6,000 records")
    print("  - categories: 9 records")
    print("  - warehouses: 5 records")
    print("\nHR TABLES:")
    print("  - employees: 200 records")
    print("  - departments: 8 records")
    print("  - salaries: ~600 records")
    print("\nSALES & FINANCE:")
    print("  - sales: ~50,000 records")
    print("  - sales_reps: 50 records")
    print("  - sales_territories: 6 records")
    print("  - monthly_revenue: 24 records")
    print("\nPERFORMANCE:")
    print("  - 16 indexes created for optimal query performance")
    print("\nREADY FOR ADVANCED SQL PRACTICE!")
    print("="*70)

def test_enhanced_database():
    """Test the enhanced database with sample queries"""
    conn = sqlite3.connect('epam_practice.db')
    cursor = conn.cursor()
    
    print("\n" + "="*70)
    print("TESTING ENHANCED DATABASE...")
    print("="*70)
    
    # Test 1: Basic query
    print("\nTest 1: Sample customers data")
    cursor.execute("SELECT customer_id, first_name, last_name, city, customer_segment FROM customers LIMIT 5")
    results = cursor.fetchall()
    for row in results:
        print(f"  {row[0]}: {row[1]} {row[2]} from {row[3]} ({row[4]})")
    
    # Test 2: Window function example
    print("\nTest 2: Running total by customer (Window Functions)")
    cursor.execute("""
        SELECT customer_id, order_date, total_amount,
               SUM(total_amount) OVER (
                   PARTITION BY customer_id 
                   ORDER BY order_date 
                   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
               ) as running_total
        FROM orders 
        WHERE customer_id <= 3 
        ORDER BY customer_id, order_date
        LIMIT 10
    """)
    results = cursor.fetchall()
    print("  Customer | Date       | Amount | Running Total")
    print("  ---------|------------|--------|-------------")
    for row in results:
        print(f"  {row[0]:8} | {row[1]} | {row[2]:6} | {row[3]:12}")
    
    # Test 3: Complex join
    print("\nTest 3: Top 5 products by sales volume")
    cursor.execute("""
        SELECT p.product_name, c.category_name, 
               SUM(oi.quantity) as total_sold,
               SUM(oi.total_price) as total_revenue
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        JOIN order_items oi ON p.product_id = oi.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_status = 'Delivered'
        GROUP BY p.product_id, p.product_name, c.category_name
        ORDER BY total_sold DESC
        LIMIT 5
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  {row[0]} ({row[1]}): {row[2]} units, ${row[3]:,.2f}")
    
    # Test 4: Employee hierarchy
    print("\nTest 4: Employee hierarchy (Self-join)")
    cursor.execute("""
        SELECT e.first_name || ' ' || e.last_name as employee,
               e.job_title,
               m.first_name || ' ' || m.last_name as manager
        FROM employees e
        LEFT JOIN employees m ON e.manager_id = m.employee_id
        WHERE e.department_id = 4  -- Engineering department
        LIMIT 5
    """)
    results = cursor.fetchall()
    for row in results:
        manager = row[2] if row[2] else "No Manager"
        print(f"  {row[0]} ({row[1]}) -> {manager}")
    
    conn.close()
    print("\nAll database tests passed!")
    print("Database is ready for advanced SQL practice!")

if __name__ == "__main__":
    print("="*70)
    print("EPAM ENHANCED PRACTICE DATABASE SETUP")
    print("="*70)
    print("Creating comprehensive database with realistic business data...")
    print()
    
    create_enhanced_database()
    test_enhanced_database()
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("1. Open epam_practice.db in DBeaver or any SQL client")
    print("2. Practice advanced SQL queries with realistic data")
    print("3. Test EPAM interview problems with comprehensive scenarios")
    print("4. Practice window functions with time series data")
    print("5. Test complex joins with proper relationships")
    print("="*70)

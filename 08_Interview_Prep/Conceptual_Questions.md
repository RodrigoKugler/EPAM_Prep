# EPAM Interview - Conceptual Questions Bank

## 🎯 Purpose
This contains ALL possible conceptual questions a recruiter might ask.
Practice explaining these clearly and concisely!

---

## 📊 SQL & Database Concepts

### Q1: What is the difference between WHERE and HAVING?
**Answer**:
- **WHERE**: Filters rows BEFORE grouping
- **HAVING**: Filters groups AFTER aggregation
- WHERE cannot use aggregate functions; HAVING can

**Example**:
```sql
-- WHERE: Filter orders before grouping
SELECT customer_id, SUM(amount)
FROM orders
WHERE amount > 100  -- Filter individual rows
GROUP BY customer_id;

-- HAVING: Filter groups after aggregation
SELECT customer_id, SUM(amount) as total
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 1000;  -- Filter aggregated results
```

---

### Q2: Explain ACID properties
**Answer**:
- **Atomicity**: Transaction is all-or-nothing (either all succeed or all fail)
- **Consistency**: Data remains in valid state (follows all rules/constraints)
- **Isolation**: Concurrent transactions don't interfere with each other
- **Durability**: Committed data persists even after system failure

**Real Example**: Bank transfer
- Atomicity: Debit from Account A and credit to Account B both happen or neither
- Consistency: Total money in system stays the same
- Isolation**: Two concurrent transfers don't corrupt balances
- Durability: Once transfer commits, it's permanent

---

### Q3: What is the difference between OLTP and OLAP?
**Answer**:

| Aspect | OLTP | OLAP |
|--------|------|------|
| **Purpose** | Transaction processing | Analytical processing |
| **Operations** | INSERT, UPDATE, DELETE | SELECT (complex queries) |
| **Data** | Current, detailed | Historical, aggregated |
| **Users** | Many (thousands) | Few (analysts) |
| **Response Time** | Milliseconds | Seconds to minutes |
| **Database Design** | Normalized | Denormalized (star/snowflake) |
| **Example** | Order processing, banking | Sales reports, BI dashboards |

**OLTP Example**: E-commerce adding items to cart
**OLAP Example**: "Show me quarterly sales trends by region"

---

### Q4: What are window functions? How do they differ from GROUP BY?
**Answer**:
- **Window functions**: Perform calculations across rows while keeping all rows in result
- **GROUP BY**: Aggregates rows into groups, collapsing them

**Key Difference**: Window functions don't reduce rows

**Example**:
```sql
-- GROUP BY: 3 rows (one per department)
SELECT department, AVG(salary)
FROM employees
GROUP BY department;

-- Window Function: All employee rows preserved
SELECT 
    name, 
    salary, 
    department,
    AVG(salary) OVER (PARTITION BY department) as dept_avg
FROM employees;
```

---

### Q5: Explain the different types of JOINs
**Answer**:

1. **INNER JOIN**: Returns only matching rows from both tables
2. **LEFT JOIN**: All rows from left table + matching from right (NULL if no match)
3. **RIGHT JOIN**: All rows from right table + matching from left
4. **FULL OUTER JOIN**: All rows from both tables
5. **CROSS JOIN**: Cartesian product (every combination)
6. **SELF JOIN**: Table joined with itself

**Visual Example**:
```
Table A: [1, 2, 3]
Table B: [2, 3, 4]

INNER JOIN: [2, 3]
LEFT JOIN:  [1, 2, 3] (1 with NULL from B)
RIGHT JOIN: [2, 3, 4] (4 with NULL from A)
FULL OUTER: [1, 2, 3, 4] (1 and 4 with NULLs)
```

---

### Q6: What is a PRIMARY KEY vs FOREIGN KEY?
**Answer**:
- **PRIMARY KEY**: Uniquely identifies each row in a table (cannot be NULL)
- **FOREIGN KEY**: Links two tables together, references PRIMARY KEY in another table

**Example**:
```sql
-- Customers table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,  -- Primary Key
    name VARCHAR(100)
);

-- Orders table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,     -- Primary Key
    customer_id INT,              -- Foreign Key
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

**Purpose**: Maintain referential integrity (can't have order for non-existent customer)

---

### Q7: What is a subquery? Types of subqueries?
**Answer**:
A query nested inside another query

**Types**:
1. **Scalar Subquery**: Returns single value
   ```sql
   SELECT * FROM employees 
   WHERE salary > (SELECT AVG(salary) FROM employees);
   ```

2. **Row Subquery**: Returns single row
   ```sql
   WHERE (col1, col2) = (SELECT col1, col2 FROM...)
   ```

3. **Column Subquery**: Returns single column
   ```sql
   WHERE department_id IN (SELECT id FROM departments WHERE region = 'North')
   ```

4. **Table Subquery**: Returns multiple rows and columns
   ```sql
   FROM (SELECT * FROM large_table WHERE date > '2024-01-01') as filtered
   ```

---

### Q8: What is a CTE (Common Table Expression)?
**Answer**:
Temporary named result set that exists within a single query

**Benefits**:
- More readable than subqueries
- Can be referenced multiple times
- Supports recursion

**Example**:
```sql
WITH high_earners AS (
    SELECT * FROM employees WHERE salary > 80000
),
dept_summary AS (
    SELECT department, COUNT(*) as count
    FROM high_earners
    GROUP BY department
)
SELECT * FROM dept_summary WHERE count > 5;
```

**Better than**: Nested subqueries that are hard to read

---

### Q9: What is normalization? Denormalization?
**Answer**:

**Normalization**: Organizing data to reduce redundancy
- **1NF**: No repeating groups (atomic values)
- **2NF**: No partial dependencies
- **3NF**: No transitive dependencies

**Denormalization**: Intentionally adding redundancy for performance

**When to use**:
- **Normalize**: OLTP systems (data integrity)
- **Denormalize**: OLAP/Data warehouses (query speed)

**Example**:
```sql
-- Normalized (OLTP)
customers: customer_id, name
orders: order_id, customer_id, amount

-- Denormalized (OLAP)
orders_denorm: order_id, customer_id, customer_name, amount
-- Redundant customer_name for faster queries
```

---

### Q10: Explain indexes and their impact on performance
**Answer**:
Index is a data structure that improves query speed (like a book index)

**Types**:
- **Clustered**: Determines physical order of data (one per table)
- **Non-Clustered**: Separate structure with pointers to data (multiple allowed)

**Benefits**:
- Faster SELECT queries
- Faster WHERE, ORDER BY, JOIN operations

**Drawbacks**:
- Slower INSERT/UPDATE/DELETE (index must be updated)
- Uses additional disk space

**When to use**:
- Columns frequently used in WHERE
- Columns used in JOINs
- Columns frequently sorted

**When NOT to use**:
- Small tables
- Columns with low cardinality (few unique values)
- Tables with frequent INSERT/UPDATE

---

## 🏗️ Data Warehousing Concepts

### Q11: What is a Data Warehouse?
**Answer**:
Central repository of integrated data from multiple sources, optimized for analysis

**Characteristics**:
- **Subject-oriented**: Organized around subjects (sales, customers)
- **Integrated**: Data from multiple sources unified
- **Time-variant**: Tracks historical changes
- **Non-volatile**: Data doesn't change once loaded

**Difference from Database**:
| Database (OLTP) | Data Warehouse (OLAP) |
|-----------------|----------------------|
| Current data | Historical data |
| Normalized | Denormalized |
| Transaction processing | Analysis |
| Many small transactions | Few large queries |

---

### Q12: Explain Star Schema vs Snowflake Schema
**Answer**:

**Star Schema**:
- One fact table surrounded by dimension tables
- Dimensions are denormalized (no subdimensions)
- Simpler, faster queries
- More storage (redundancy)

```
        [Product Dim]
              |
[Date Dim] - [FACT] - [Customer Dim]
              |
        [Store Dim]
```

**Snowflake Schema**:
- Dimensions are normalized (broken into subdimensions)
- Less storage (no redundancy)
- More complex queries (more joins)

```
[Product Category]
        |
    [Product] --- [FACT] --- [Customer] --- [City]
        |                                      |
     [Brand]                              [State]
```

**When to use**:
- **Star**: Most data warehouses (simplicity + performance)
- **Snowflake**: When storage is critical

---

### Q13: What are Slowly Changing Dimensions (SCD)?
**Answer**:
Techniques for tracking dimension changes over time

**Type 1 (Overwrite)**:
- Update the record
- No history preserved
- Example: Fix a typo

```
Before: customer_name = "Jhon"
After:  customer_name = "John"
```

**Type 2 (Add New Row)**:
- Keep history
- Add new row with new values
- Track using effective dates or version numbers

```
id | name | city | effective_date | current_flag
1  | John | NYC  | 2020-01-01    | N
2  | John | LA   | 2023-01-01    | Y  ← Customer moved
```

**Type 3 (Add New Column)**:
- Limited history (usually previous value only)
- Example: current_address, previous_address

```
customer_id | name | current_city | previous_city
1           | John | LA           | NYC
```

**Most Common**: Type 2 (full history preservation)

---

### Q14: What is a Fact Table vs Dimension Table?
**Answer**:

**Fact Table**:
- Contains measurements/metrics (quantitative data)
- Foreign keys to dimension tables
- Large (millions/billions of rows)
- Examples: sales amount, quantity, profit

**Dimension Table**:
- Contains descriptive attributes (qualitative data)
- Primary key referenced by fact table
- Smaller (thousands/millions of rows)
- Examples: customer name, product description, date

**Example**:
```sql
-- Fact Table
sales_fact (
    sale_id,
    product_id,    -- FK to product dimension
    customer_id,   -- FK to customer dimension
    date_id,       -- FK to date dimension
    quantity,      -- Measure
    amount         -- Measure
)

-- Dimension Table
product_dim (
    product_id,    -- PK
    product_name,
    category,
    brand
)
```

---

### Q15: What is Data Vault modeling?
**Answer**:
Agile data modeling approach for enterprise data warehouses

**Components**:
1. **Hubs**: Business entities (Customer, Product)
2. **Links**: Relationships between hubs (Sale = Customer + Product)
3. **Satellites**: Descriptive attributes and history

**Benefits**:
- Handles changing requirements well
- Maintains full history
- Supports parallel loading

**When to use**: Large enterprises with frequent changes

---

## 🔄 ETL Concepts

### Q16: What is ETL? Explain each stage.
**Answer**:
**ETL = Extract, Transform, Load**

**Extract**:
- Pull data from source systems (databases, APIs, files)
- Incremental vs full extraction

**Transform**:
- Clean data (remove duplicates, fix formats)
- Validate data (check constraints, rules)
- Enrich data (calculate fields, join data)
- Aggregate data (summarize)

**Load**:
- Insert data into target (data warehouse)
- Full load vs incremental load

**Example**:
```python
# Extract
data = extract_from_api('https://api.example.com/sales')

# Transform
data = clean_data(data)          # Remove nulls, fix formats
data = enrich_data(data)         # Add calculated fields
data = validate_data(data)       # Check data quality

# Load
load_to_warehouse(data, 'sales_fact')
```

---

### Q17: ETL vs ELT - What's the difference?
**Answer**:

**ETL (Traditional)**:
- Transform happens BEFORE loading
- Done in ETL tool/server
- Better for complex transformations
- Used with traditional data warehouses

**ELT (Modern)**:
- Load data first, transform in target
- Leverages warehouse's processing power
- Faster initial load
- Used with cloud data warehouses (BigQuery, Snowflake, Redshift)

**When to use**:
- **ETL**: Legacy systems, limited warehouse resources
- **ELT**: Cloud warehouses with high compute power

---

### Q18: What is incremental loading?
**Answer**:
Loading only new/changed data since last load (not full reload)

**Methods**:
1. **Timestamp-based**: Load records WHERE modified_date > last_load_date
2. **Flag-based**: Load records WHERE is_processed = false
3. **CDC (Change Data Capture)**: Track changes at database level

**Benefits**:
- Faster loads
- Less resource usage
- Less impact on source system

**Example**:
```sql
-- Full Load (slow)
INSERT INTO warehouse.customers
SELECT * FROM source.customers;

-- Incremental Load (fast)
INSERT INTO warehouse.customers
SELECT * FROM source.customers
WHERE modified_date > (SELECT MAX(load_date) FROM warehouse.customers);
```

---

### Q19: What is data quality? How to ensure it?
**Answer**:
Ensuring data is accurate, complete, consistent, and reliable

**Data Quality Dimensions**:
1. **Accuracy**: Data is correct
2. **Completeness**: No missing values
3. **Consistency**: No contradictions
4. **Validity**: Follows business rules
5. **Timeliness**: Data is up-to-date
6. **Uniqueness**: No duplicates

**Techniques**:
- **Validation rules**: Check constraints (age > 0, email format)
- **Referential integrity**: FKs match PKs
- **Data profiling**: Analyze data patterns
- **Cleansing**: Fix/remove bad data
- **Monitoring**: Track quality metrics

**Example**:
```python
def validate_customer_data(data):
    # Completeness
    assert data['customer_id'].notna().all(), "Missing customer IDs"
    
    # Validity
    assert (data['age'] > 0).all(), "Invalid ages"
    assert data['email'].str.contains('@').all(), "Invalid emails"
    
    # Uniqueness
    assert not data['customer_id'].duplicated().any(), "Duplicate IDs"
    
    return True
```

---

## ☁️ Cloud & Big Data Concepts

### Q20: What is a Data Lake?
**Answer**:
Central repository storing all data (structured, semi-structured, unstructured) in native format

**Characteristics**:
- Schema-on-read (apply structure when reading)
- Stores raw data
- Cheaper storage than data warehouse
- Used for big data, ML, advanced analytics

**Data Lake vs Data Warehouse**:
| Data Lake | Data Warehouse |
|-----------|----------------|
| Raw, unprocessed data | Processed, clean data |
| All data types | Structured data |
| Schema-on-read | Schema-on-write |
| For data scientists | For business analysts |
| Cheaper | More expensive |

**Example**: AWS S3, Azure Data Lake, GCP Cloud Storage

---

### Q21: What is Apache Airflow?
**Answer**:
Workflow orchestration platform for scheduling and monitoring data pipelines

**Key Concepts**:
- **DAG**: Directed Acyclic Graph (workflow definition)
- **Operators**: Individual tasks (BashOperator, PythonOperator, SQLOperator)
- **Sensors**: Wait for conditions (FileSensor, TimeSensor)
- **Tasks**: Instances of operators

**Use Case**: Schedule daily ETL jobs

**Example DAG**:
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

dag = DAG(
    'etl_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily'
)

extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load_data,
    dag=dag
)

extract_task >> transform_task >> load_task  # Dependencies
```

---

### Q22: What is BigQuery?
**Answer**:
Google Cloud's serverless, fully-managed data warehouse

**Key Features**:
- **Serverless**: No infrastructure management
- **Scalable**: Handles petabytes of data
- **Fast**: Parallel processing
- **SQL-based**: Standard SQL interface
- **Separation of storage and compute**: Pay separately

**When to use**: Cloud-native data warehousing, large-scale analytics

---

### Q23: What is partitioning in BigQuery?
**Answer**:
Dividing large tables into smaller chunks for better performance and cost

**Types**:
1. **Date-based**: Partition by date column
2. **Integer-based**: Partition by range
3. **Ingestion-time**: Partition by load time

**Benefits**:
- Faster queries (scan less data)
- Lower cost (pay per data scanned)

**Example**:
```sql
-- Create partitioned table
CREATE TABLE sales (
    sale_id INT64,
    sale_date DATE,
    amount FLOAT64
)
PARTITION BY sale_date;

-- Query only specific partition (cheaper!)
SELECT * FROM sales
WHERE sale_date = '2024-01-01';  -- Scans only 1 day's data
```

---

### Q24: What is PySpark?
**Answer**:
Python API for Apache Spark (distributed computing framework)

**Key Concepts**:
- **RDD**: Resilient Distributed Dataset (low-level)
- **DataFrame**: Structured data (like pandas but distributed)
- **Lazy Evaluation**: Computations happen only when needed

**Use Case**: Process large datasets that don't fit in memory

**Example**:
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('etl').getOrCreate()

# Read data
df = spark.read.csv('large_file.csv', header=True)

# Transform (lazy)
df_filtered = df.filter(df.amount > 100)
df_grouped = df_filtered.groupBy('customer_id').sum('amount')

# Action (triggers execution)
df_grouped.show()
```

---

## 🐍 Python Concepts

### Q25: What is the difference between list and tuple?
**Answer**:

| List | Tuple |
|------|-------|
| Mutable (can change) | Immutable (cannot change) |
| `[1, 2, 3]` | `(1, 2, 3)` |
| Slower | Faster |
| More memory | Less memory |

**Use List**: When you need to modify data
**Use Tuple**: When data shouldn't change (like coordinates)

---

### Q26: What are Python comprehensions?
**Answer**:
Concise way to create lists, dicts, sets

**List Comprehension**:
```python
# Traditional
squares = []
for i in range(10):
    squares.append(i**2)

# Comprehension (better!)
squares = [i**2 for i in range(10)]

# With condition
even_squares = [i**2 for i in range(10) if i % 2 == 0]
```

**Dict Comprehension**:
```python
# Create dict from list
names = ['Alice', 'Bob', 'Charlie']
name_lengths = {name: len(name) for name in names}
# {'Alice': 5, 'Bob': 3, 'Charlie': 7}
```

---

### Q27: Explain Python's GIL
**Answer**:
**Global Interpreter Lock**: Mutex that allows only one thread to execute Python code at a time

**Impact**:
- Multi-threading doesn't help with CPU-bound tasks
- Multi-threading helps with I/O-bound tasks (waiting for network/disk)

**Solutions**:
- Use **multiprocessing** for CPU-bound tasks
- Use **async/await** for I/O-bound tasks

---

## 📝 BEST PRACTICES

### Q28: How do you handle errors in data pipelines?
**Answer**:

1. **Try-Except Blocks**: Catch and handle errors
   ```python
   try:
       load_data()
   except Exception as e:
       log_error(e)
       send_alert()
   ```

2. **Validation**: Check data before processing
3. **Logging**: Track all operations
4. **Retries**: Auto-retry failed operations
5. **Monitoring**: Alert on failures
6. **Dead Letter Queue**: Store failed records for later review

---

### Q29: What is CI/CD in context of data pipelines?
**Answer**:
**Continuous Integration / Continuous Deployment**

**CI**: Automatically test code changes
**CD**: Automatically deploy to production

**For Data Pipelines**:
- Version control (Git)
- Automated testing (unit tests, data quality tests)
- Automated deployment (Airflow DAGs, SQL scripts)

**Example Tools**: Jenkins, GitHub Actions, GitLab CI/CD

---

### Q30: How do you optimize SQL queries?
**Answer**:

1. **Use indexes** on WHERE/JOIN columns
2. **Avoid SELECT \***: Select only needed columns
3. **Use WHERE before JOIN**: Filter early
4. **Use proper JOINs**: INNER vs LEFT
5. **Avoid functions in WHERE**: `WHERE YEAR(date) = 2024` is slow
6. **Use LIMIT**: When you don't need all rows
7. **Analyze execution plan**: Find bottlenecks
8. **Partition large tables**
9. **Use appropriate data types**
10. **Avoid correlated subqueries**: Use JOINs instead

---

**Total: 30 Essential Questions!**
**Practice explaining each clearly and with examples!**

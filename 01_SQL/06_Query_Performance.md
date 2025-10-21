# SQL Query Performance - Data Engineering Optimization

## 🎯 Learning Objectives

By the end of this module, you will be able to:
- **Understand query execution plans** and identify bottlenecks
- **Optimize SQL queries** for large datasets
- **Choose the right indexes** for different scenarios
- **Write efficient JOINs** and avoid performance pitfalls
- **Profile and measure** query performance
- **Optimize window functions** and complex queries
- **Handle big data** performance challenges

---

## 🔥 Why Query Performance Matters for Data Engineering

Query performance is **critical for data engineering**:

1. **Large Datasets**: Data engineers work with millions/billions of records
2. **Real-time Processing**: ETL pipelines must run within time windows
3. **Cost Optimization**: Slow queries = expensive compute resources
4. **User Experience**: Analytics queries must return results quickly
5. **System Stability**: Poor queries can crash systems
6. **Scalability**: Queries must perform as data grows

**EPAM will test your ability to write efficient queries for large datasets. Master this = you're ready for production mistakes.**

---

## 📚 Query Execution Plans - Understanding the Engine

### What is a Query Execution Plan?

A query execution plan shows **how the database engine will execute your query**:
- Which indexes will be used
- How tables will be joined
- What operations will be performed
- Estimated costs and row counts

### How to Read Execution Plans

```sql
-- Enable execution plan (SQLite)
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 123;

-- Enable execution plan (PostgreSQL)
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 123;

-- Enable execution plan (SQL Server)
SET SHOWPLAN_ALL ON;
SELECT * FROM orders WHERE customer_id = 123;
```

### Common Execution Plan Operations

| Operation | Description | Performance Impact |
|-----------|-------------|-------------------|
| **Table Scan** | Reads entire table | ⚠️ Slow for large tables |
| **Index Seek** | Uses index to find specific rows | ✅ Fast |
| **Index Scan** | Reads entire index | ⚠️ Slower than seek |
| **Hash Join** | Uses hash table for joins | ✅ Good for large tables |
| **Nested Loop** | Nested iteration for joins | ⚠️ Slow for large tables |
| **Sort** | Sorts result set | ⚠️ Expensive operation |

---

## 🔧 Indexing Strategies - The Performance Foundation

### Types of Indexes

#### 1. Single Column Indexes
```sql
-- Create single column index
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_customers_email ON customers(email);
```

**When to Use**:
- Frequently queried columns
- JOIN columns
- WHERE clause columns
- ORDER BY columns

#### 2. Composite Indexes
```sql
-- Create composite index
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_orders_date_amount ON orders(order_date, order_amount);
```

**When to Use**:
- Multiple columns in WHERE clause
- Multi-column JOINs
- Complex filtering conditions

#### 3. Covering Indexes
```sql
-- Create covering index (includes all needed columns)
CREATE INDEX idx_orders_covering ON orders(customer_id, order_date, order_amount);
```

**When to Use**:
- Queries that only need indexed columns
- Avoids table lookups
- Maximum performance for specific queries

### Index Design Principles

#### 1. Choose the Right Columns
```sql
-- ✅ GOOD: Index on frequently queried columns
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- ❌ BAD: Index on rarely queried columns
CREATE INDEX idx_orders_order_id ON orders(order_id);  -- Primary key already indexed
```

#### 2. Consider Column Order in Composite Indexes
```sql
-- ✅ GOOD: Most selective column first
CREATE INDEX idx_orders_date_customer ON orders(order_date, customer_id);

-- ❌ BAD: Less selective column first
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
```

#### 3. Avoid Over-Indexing
```sql
-- ❌ BAD: Too many indexes
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_orders_customer_amount ON orders(customer_id, order_amount);
-- Better to use one composite index
```

---

## 🚀 Query Optimization Techniques

### 1. Optimize WHERE Clauses

#### ❌ INEFFICIENT: Functions in WHERE
```sql
-- Slow: Function applied to every row
SELECT * FROM orders WHERE YEAR(order_date) = 2024;
SELECT * FROM customers WHERE UPPER(customer_name) = 'ALICE';
```

#### ✅ EFFICIENT: Direct Comparisons
```sql
-- Fast: Direct column comparison
SELECT * FROM orders WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01';
SELECT * FROM customers WHERE customer_name = 'Alice';
```

### 2. Optimize JOINs

#### ❌ INEFFICIENT: Cartesian Products
```sql
-- Slow: Missing JOIN condition
SELECT c.customer_name, o.order_amount
FROM customers c, orders o;  -- Creates Cartesian product!
```

#### ✅ EFFICIENT: Proper JOINs
```sql
-- Fast: Explicit JOIN condition
SELECT c.customer_name, o.order_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

#### ❌ INEFFICIENT: Multiple Table Scans
```sql
-- Slow: Multiple subqueries
SELECT 
    customer_id,
    (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count,
    (SELECT SUM(order_amount) FROM orders WHERE customer_id = c.customer_id) as total_spent
FROM customers c;
```

#### ✅ EFFICIENT: Single JOIN with Aggregation
```sql
-- Fast: Single JOIN with GROUP BY
SELECT 
    c.customer_id,
    COUNT(o.order_id) as order_count,
    COALESCE(SUM(o.order_amount), 0) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;
```

### 3. Optimize Window Functions

#### ❌ INEFFICIENT: Unbounded Windows
```sql
-- Slow: Unbounded window on large dataset
SELECT 
    customer_id,
    order_date,
    SUM(order_amount) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
FROM orders;
```

#### ✅ EFFICIENT: Bounded Windows
```sql
-- Fast: Bounded window
SELECT 
    customer_id,
    order_date,
    SUM(order_amount) OVER (ORDER BY order_date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)
FROM orders;
```

### 4. Optimize Subqueries

#### ❌ INEFFICIENT: Correlated Subqueries
```sql
-- Slow: Correlated subquery
SELECT 
    customer_id,
    customer_name,
    (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count
FROM customers c;
```

#### ✅ EFFICIENT: JOINs or Window Functions
```sql
-- Fast: JOIN with GROUP BY
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;
```

---

## 🎯 Performance Monitoring and Profiling

### 1. Query Profiling

#### SQLite Profiling
```sql
-- Enable profiling
.timer on

-- Run query and see execution time
SELECT * FROM orders WHERE customer_id = 123;

-- Get detailed profiling info
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 123;
```

#### PostgreSQL Profiling
```sql
-- Enable timing
\timing on

-- Run query with detailed plan
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 123;

-- Get buffer usage
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE customer_id = 123;
```

### 2. Performance Metrics

#### Key Metrics to Monitor
- **Execution Time**: How long the query takes
- **Rows Examined**: How many rows were processed
- **Rows Returned**: How many rows were returned
- **Index Usage**: Whether indexes were used effectively
- **Memory Usage**: How much memory was consumed
- **I/O Operations**: Disk read/write operations

#### Performance Benchmarks
```sql
-- Benchmark query performance
SELECT 
    'Query 1' as query_name,
    COUNT(*) as row_count,
    MIN(order_date) as min_date,
    MAX(order_date) as max_date
FROM orders
WHERE order_date >= '2024-01-01';

-- Compare with different approaches
SELECT 
    'Query 2' as query_name,
    COUNT(*) as row_count,
    MIN(order_date) as min_date,
    MAX(order_date) as max_date
FROM orders
WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';
```

---

## 🔥 Real-World Performance Scenarios

### Scenario 1: Large Dataset Analysis

#### Problem: Analyze 10 million orders
```sql
-- ❌ INEFFICIENT: Full table scan
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(order_amount) as total_spent
FROM orders
GROUP BY customer_id;
```

#### Solution: Optimized with Indexes
```sql
-- ✅ EFFICIENT: Use covering index
CREATE INDEX idx_orders_covering ON orders(customer_id, order_amount);

SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(order_amount) as total_spent
FROM orders
GROUP BY customer_id;
```

### Scenario 2: Complex JOINs

#### Problem: Join multiple large tables
```sql
-- ❌ INEFFICIENT: Multiple table scans
SELECT 
    c.customer_name,
    p.product_name,
    o.order_date,
    oi.quantity,
    oi.unit_price
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2024-01-01';
```

#### Solution: Optimized with Proper Indexes
```sql
-- ✅ EFFICIENT: Create indexes for JOIN columns
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Use covering index for orders
CREATE INDEX idx_orders_covering ON orders(customer_id, order_date, order_id);

SELECT 
    c.customer_name,
    p.product_name,
    o.order_date,
    oi.quantity,
    oi.unit_price
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2024-01-01';
```

### Scenario 3: Window Function Optimization

#### Problem: Running totals on large dataset
```sql
-- ❌ INEFFICIENT: Unbounded window
SELECT 
    customer_id,
    order_date,
    order_amount,
    SUM(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM orders
ORDER BY customer_id, order_date;
```

#### Solution: Optimized with Bounded Windows
```sql
-- ✅ EFFICIENT: Bounded window for recent data
SELECT 
    customer_id,
    order_date,
    order_amount,
    SUM(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as running_total_30_days
FROM orders
WHERE order_date >= '2024-01-01'
ORDER BY customer_id, order_date;
```

---

## 🎯 Big Data Performance Patterns

### 1. Partitioning Strategies

#### Date Partitioning
```sql
-- Partition large tables by date
CREATE TABLE orders_2024_01 (
    LIKE orders
) PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE orders_2024_02 (
    LIKE orders
) PARTITION OF orders
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

#### Hash Partitioning
```sql
-- Partition by customer ID hash
CREATE TABLE orders_partition_0 (
    LIKE orders
) PARTITION OF orders
FOR VALUES WITH (modulus 4, remainder 0);
```

### 2. Data Archiving

#### Archive Old Data
```sql
-- Move old data to archive table
INSERT INTO orders_archive
SELECT * FROM orders
WHERE order_date < '2023-01-01';

-- Delete archived data
DELETE FROM orders
WHERE order_date < '2023-01-01';
```

### 3. Materialized Views

#### Create Materialized Views for Complex Queries
```sql
-- Create materialized view for complex aggregations
CREATE MATERIALIZED VIEW customer_summary AS
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(order_amount) as total_spent,
    AVG(order_amount) as avg_order_value,
    MAX(order_date) as last_order_date
FROM orders
GROUP BY customer_id;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW customer_summary;
```

---

## 🔧 Performance Troubleshooting

### 1. Identify Slow Queries

#### Query Performance Analysis
```sql
-- Find slow queries (PostgreSQL)
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

#### Identify Missing Indexes
```sql
-- Find queries that could benefit from indexes
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats
WHERE schemaname = 'public'
ORDER BY n_distinct DESC;
```

### 2. Common Performance Issues

#### Issue 1: Missing Indexes
```sql
-- ❌ PROBLEM: Full table scan
SELECT * FROM orders WHERE customer_id = 123;

-- ✅ SOLUTION: Create index
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

#### Issue 2: Inefficient JOINs
```sql
-- ❌ PROBLEM: Nested loop join on large tables
SELECT c.customer_name, o.order_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- ✅ SOLUTION: Use hash join with proper indexes
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

#### Issue 3: Unbounded Windows
```sql
-- ❌ PROBLEM: Unbounded window function
SELECT 
    customer_id,
    SUM(order_amount) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
FROM orders;

-- ✅ SOLUTION: Use bounded window
SELECT 
    customer_id,
    SUM(order_amount) OVER (ORDER BY order_date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)
FROM orders;
```

---

## 💡 Performance Best Practices

### 1. Query Design Principles

#### Start with the Right Table
```sql
-- ✅ GOOD: Start with filtered table
SELECT c.customer_name, o.order_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01';

-- ❌ BAD: Start with large unfiltered table
SELECT c.customer_name, o.order_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2024-01-01';
```

#### Use Appropriate Data Types
```sql
-- ✅ GOOD: Use appropriate data types
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    order_amount DECIMAL(10,2)
);

-- ❌ BAD: Use oversized data types
CREATE TABLE orders (
    order_id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255),
    order_date VARCHAR(255),
    order_amount VARCHAR(255)
);
```

### 2. Index Management

#### Regular Index Maintenance
```sql
-- Rebuild indexes regularly
REINDEX TABLE orders;

-- Update statistics
ANALYZE orders;

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

#### Monitor Index Bloat
```sql
-- Check for index bloat
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;
```

### 3. Query Optimization Checklist

#### Before Writing a Query
- [ ] Understand the data volume
- [ ] Identify the most selective filters
- [ ] Plan the JOIN order
- [ ] Consider index availability

#### After Writing a Query
- [ ] Check the execution plan
- [ ] Measure execution time
- [ ] Verify index usage
- [ ] Test with sample data
- [ ] Monitor resource usage

---

## 🎯 EPAM Interview Scenarios

### Scenario 1: Optimize Slow Query
**Problem**: A query is taking 30 seconds to run. How would you optimize it?

```sql
-- Given slow query
SELECT 
    c.customer_name,
    p.product_name,
    COUNT(*) as order_count,
    SUM(oi.quantity * oi.unit_price) as total_revenue
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2023-01-01'
GROUP BY c.customer_name, p.product_name
ORDER BY total_revenue DESC;
```

**Solution**:
```sql
-- Step 1: Create indexes
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Step 2: Use covering index
CREATE INDEX idx_orders_covering ON orders(customer_id, order_date, order_id);

-- Step 3: Optimize query
SELECT 
    c.customer_name,
    p.product_name,
    COUNT(*) as order_count,
    SUM(oi.quantity * oi.unit_price) as total_revenue
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2023-01-01'
GROUP BY c.customer_name, p.product_name
ORDER BY total_revenue DESC;
```

### Scenario 2: Handle Large Dataset
**Problem**: How would you handle a query on a table with 100 million rows?

**Solution**:
```sql
-- Step 1: Use partitioning
CREATE TABLE orders_2024 PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- Step 2: Create appropriate indexes
CREATE INDEX idx_orders_2024_customer_id ON orders_2024(customer_id);

-- Step 3: Use efficient query patterns
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(order_amount) as total_spent
FROM orders_2024
WHERE order_date >= '2024-01-01'
GROUP BY customer_id;

-- Step 4: Consider materialized views for complex aggregations
CREATE MATERIALIZED VIEW customer_summary_2024 AS
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(order_amount) as total_spent
FROM orders_2024
GROUP BY customer_id;
```

---

## 🚀 Practice Exercises

**See**: `01_SQL/exercises/06_Query_Performance_Exercises.md`

**Master these patterns**:
1. ✅ Analyze execution plans
2. ✅ Design effective indexes
3. ✅ Optimize JOIN performance
4. ✅ Handle large datasets
5. ✅ Optimize window functions
6. ✅ Troubleshoot slow queries
7. ✅ Implement partitioning strategies
8. ✅ Monitor query performance

**Target Time**: Optimize any query in under 10 minutes

---

## 📚 Quick Reference Cheat Sheet

### Performance Optimization Checklist
- [ ] Use appropriate indexes
- [ ] Optimize WHERE clauses
- [ ] Choose efficient JOINs
- [ ] Avoid functions in WHERE
- [ ] Use bounded windows
- [ ] Consider partitioning
- [ ] Monitor execution plans
- [ ] Test with realistic data

### Index Design Principles
- Index frequently queried columns
- Use composite indexes for multi-column queries
- Consider column order in composite indexes
- Avoid over-indexing
- Monitor index usage

### Query Optimization Techniques
- Start with filtered tables
- Use appropriate data types
- Avoid correlated subqueries
- Use JOINs instead of subqueries when possible
- Consider materialized views for complex queries

---

## 🎯 Next Steps

1. **Practice query optimization** until you can optimize any query in < 10 minutes
2. **Complete all exercises** in `01_SQL/exercises/06_Query_Performance_Exercises.md`
3. **Review solutions** only after attempting
4. **Move to**: Data Types and Functions

**You're now ready to optimize queries for production systems!** 🚀

---

**Key Takeaway**: Query performance is about **understanding how the database engine works** and designing your queries accordingly. Master indexing, execution plans, and optimization techniques, and you'll be ready for any performance challenge.

**Next Module**: `01_SQL/05_Data_Types_Functions.md`



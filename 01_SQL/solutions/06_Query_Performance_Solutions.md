# SQL Query Performance - Exercise Solutions

## 🎯 Solution Guidelines

- **Approach**: Focus on performance optimization techniques
- **Analysis**: Always analyze execution plans first
- **Optimization**: Apply multiple optimization strategies
- **Testing**: Measure performance improvements

---

## 📚 Exercise 1: Execution Plan Analysis

### Solution 1.1: Analyze Query Execution Plan
```sql
-- Given query
SELECT 
    c.customer_name,
    COUNT(o.order_id) as order_count,
    SUM(o.order_amount) as total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE c.customer_segment = 'Premium'
GROUP BY c.customer_name
ORDER BY total_spent DESC;

-- Analysis using EXPLAIN QUERY PLAN
EXPLAIN QUERY PLAN SELECT 
    c.customer_name,
    COUNT(o.order_id) as order_count,
    SUM(o.order_amount) as total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE c.customer_segment = 'Premium'
GROUP BY c.customer_name
ORDER BY total_spent DESC;
```

**Execution Plan Analysis**:
- **Issue 1**: Full table scan on customers table (no index on customer_segment)
- **Issue 2**: Full table scan on orders table (no index on customer_id)
- **Issue 3**: No covering index for the query

**Optimization Recommendations**:
```sql
-- Create indexes for optimization
CREATE INDEX idx_customers_segment ON customers(customer_segment);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_customer_amount ON orders(customer_id, order_amount);

-- Optimized query
SELECT 
    c.customer_name,
    COUNT(o.order_id) as order_count,
    SUM(o.order_amount) as total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE c.customer_segment = 'Premium'
GROUP BY c.customer_name
ORDER BY total_spent DESC;
```

**Performance Improvements**:
- Index seek on customers table instead of table scan
- Index seek on orders table instead of table scan
- Reduced I/O operations
- Faster query execution

---

### Solution 1.2: Compare Execution Plans
```sql
-- Query 1: JOIN with aggregation
EXPLAIN QUERY PLAN SELECT 
    o.order_id,
    o.order_date,
    SUM(oi.quantity * oi.unit_price) as total_amount
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_date >= '2024-01-01'
GROUP BY o.order_id, o.order_date
ORDER BY total_amount DESC;

-- Query 2: Direct column access
EXPLAIN QUERY PLAN SELECT 
    o.order_id,
    o.order_date,
    o.total_amount
FROM orders o
WHERE o.order_date >= '2024-01-01'
ORDER BY o.total_amount DESC;
```

**Execution Plan Comparison**:

**Query 1 Analysis**:
- Table scan on orders table
- Table scan on order_items table
- Hash join operation
- Group by operation
- Sort operation

**Query 2 Analysis**:
- Index seek on orders table (if indexed on order_date)
- Simple sort operation

**Recommendation**: Query 2 is more efficient because:
- Single table access instead of JOIN
- No aggregation required
- Simpler execution plan
- Better performance for large datasets

**Optimization**:
```sql
-- Create index for Query 2
CREATE INDEX idx_orders_date_amount ON orders(order_date, total_amount);

-- Use Query 2 for better performance
SELECT 
    o.order_id,
    o.order_date,
    o.total_amount
FROM orders o
WHERE o.order_date >= '2024-01-01'
ORDER BY o.total_amount DESC;
```

---

## 🔥 Exercise 2: Index Design and Optimization

### Solution 2.1: Design Indexes for Query Optimization
```sql
-- Query Pattern 1: Find orders by customer
-- Index: customer_id
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- Query Pattern 2: Find orders by date range
-- Index: order_date
CREATE INDEX idx_orders_order_date ON orders(order_date);

-- Query Pattern 3: Find orders by customer and date
-- Composite index: customer_id, order_date
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Query Pattern 4: Find orders by amount range
-- Index: order_amount
CREATE INDEX idx_orders_amount ON orders(order_amount);

-- Query Pattern 5: Find orders by customer, date, and amount
-- Covering index: customer_id, order_date, order_amount
CREATE INDEX idx_orders_covering ON orders(customer_id, order_date, order_amount);
```

**Index Design Principles Applied**:
- Single-column indexes for simple queries
- Composite indexes for multi-column queries
- Covering indexes for queries that only need indexed columns
- Proper column order in composite indexes (most selective first)

**Performance Impact**:
- Index seeks instead of table scans
- Reduced I/O operations
- Faster query execution
- Better scalability

---

### Solution 2.2: Index Usage Analysis
```sql
-- Given indexes
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_amount ON orders(order_amount);
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_customers_segment ON customers(customer_segment);

-- Query 1: Uses idx_orders_customer_id
SELECT * FROM orders WHERE customer_id = 123;

-- Query 2: Uses idx_orders_order_date
SELECT * FROM orders WHERE order_date >= '2024-01-01';

-- Query 3: Uses idx_orders_customer_date (composite index)
SELECT * FROM orders WHERE customer_id = 123 AND order_date >= '2024-01-01';

-- Query 4: Uses idx_orders_amount
SELECT * FROM orders WHERE order_amount > 1000;

-- Query 5: Uses idx_orders_order_date (partial index usage)
SELECT * FROM orders WHERE order_date >= '2024-01-01' AND order_amount > 1000;
```

**Index Usage Analysis**:

**Query 1**: ✅ Uses `idx_orders_customer_id`
- Efficient index seek
- Good performance

**Query 2**: ✅ Uses `idx_orders_order_date`
- Efficient index seek
- Good performance

**Query 3**: ✅ Uses `idx_orders_customer_date`
- Efficient composite index usage
- Excellent performance

**Query 4**: ✅ Uses `idx_orders_amount`
- Efficient index seek
- Good performance

**Query 5**: ⚠️ Partial index usage
- Uses `idx_orders_order_date` for date filter
- Table scan for amount filter
- Could be optimized with composite index

**Optimization Recommendations**:
```sql
-- Create composite index for Query 5
CREATE INDEX idx_orders_date_amount ON orders(order_date, order_amount);

-- Remove unused index if not needed
-- DROP INDEX idx_orders_amount;  -- Only if not used elsewhere
```

---

## 🎯 Exercise 3: JOIN Optimization

### Solution 3.1: Optimize Complex JOINs
```sql
-- Given query
SELECT 
    c.customer_name,
    c.customer_segment,
    p.product_name,
    p.product_category,
    COUNT(oi.order_id) as order_count,
    SUM(oi.quantity * oi.unit_price) as total_revenue
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.customer_name, c.customer_segment, p.product_name, p.product_category
ORDER BY total_revenue DESC;
```

**Optimization Strategy**:

**Step 1: Create Indexes**
```sql
-- Indexes for JOIN columns
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Covering index for orders
CREATE INDEX idx_orders_covering ON orders(customer_id, order_date, order_id);

-- Covering index for order_items
CREATE INDEX idx_order_items_covering ON order_items(order_id, product_id, quantity, unit_price);
```

**Step 2: Optimize Query**
```sql
-- Optimized query with better JOIN order
SELECT 
    c.customer_name,
    c.customer_segment,
    p.product_name,
    p.product_category,
    COUNT(oi.order_id) as order_count,
    SUM(oi.quantity * oi.unit_price) as total_revenue
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.customer_name, c.customer_segment, p.product_name, p.product_category
ORDER BY total_revenue DESC;
```

**Performance Improvements**:
- Start with filtered orders table (smaller dataset)
- Use covering indexes to avoid table lookups
- Efficient JOIN operations
- Reduced I/O operations

---

### Solution 3.2: Choose Optimal JOIN Strategy
```sql
-- Approach 1: LEFT JOIN
EXPLAIN QUERY PLAN SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) as order_count,
    COALESCE(SUM(o.order_amount), 0) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;

-- Approach 2: Subquery
EXPLAIN QUERY PLAN SELECT 
    c.customer_id,
    c.customer_name,
    (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count,
    (SELECT COALESCE(SUM(order_amount), 0) FROM orders WHERE customer_id = c.customer_id) as total_spent
FROM customers c;

-- Approach 3: Window Function
EXPLAIN QUERY PLAN SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) OVER (PARTITION BY c.customer_id) as order_count,
    COALESCE(SUM(o.order_amount) OVER (PARTITION BY c.customer_id), 0) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

**Performance Comparison**:

**Approach 1 (LEFT JOIN)**: ✅ **RECOMMENDED**
- Single table scan on customers
- Single table scan on orders
- Efficient hash join
- Good performance for large datasets

**Approach 2 (Subquery)**: ❌ **NOT RECOMMENDED**
- Multiple table scans on orders table
- Correlated subqueries are slow
- Poor performance for large datasets

**Approach 3 (Window Function)**: ⚠️ **CONDITIONAL**
- Single table scan on customers
- Single table scan on orders
- Window function overhead
- Good for complex calculations

**Recommendation**: Use Approach 1 (LEFT JOIN) because:
- Best performance for large datasets
- Simple and readable
- Efficient execution plan
- Scales well with data growth

---

## 🔧 Exercise 4: Window Function Optimization

### Solution 4.1: Optimize Window Functions
```sql
-- Given query
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

**Optimization Strategies**:

**Strategy 1: Use Bounded Windows**
```sql
-- Optimized with bounded window
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

**Strategy 2: Use Indexes**
```sql
-- Create index for window function
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date, order_amount);

-- Optimized query with index
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

**Strategy 3: Alternative Approach**
```sql
-- Use CTE for better performance
WITH customer_orders AS (
    SELECT 
        customer_id,
        order_date,
        order_amount
    FROM orders
    WHERE order_date >= '2024-01-01'
    ORDER BY customer_id, order_date
)
SELECT 
    customer_id,
    order_date,
    order_amount,
    SUM(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM customer_orders;
```

**Performance Improvements**:
- Bounded windows reduce computation
- Proper indexes improve sorting
- CTEs can improve readability and performance
- Filter early to reduce data volume

---

### Solution 4.2: Compare Window Function Approaches
```sql
-- Approach 1: Unbounded Window
EXPLAIN QUERY PLAN SELECT 
    customer_id,
    order_date,
    order_amount,
    SUM(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM orders;

-- Approach 2: Bounded Window
EXPLAIN QUERY PLAN SELECT 
    customer_id,
    order_date,
    order_amount,
    SUM(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as running_total_30_days
FROM orders;

-- Approach 3: Self JOIN
EXPLAIN QUERY PLAN SELECT 
    o1.customer_id,
    o1.order_date,
    o1.order_amount,
    SUM(o2.order_amount) as running_total
FROM orders o1
INNER JOIN orders o2 ON o1.customer_id = o2.customer_id 
                    AND o2.order_date <= o1.order_date
GROUP BY o1.customer_id, o1.order_date, o1.order_amount
ORDER BY o1.customer_id, o1.order_date;
```

**Performance Comparison**:

**Approach 1 (Unbounded Window)**: ⚠️ **SLOW**
- Computes running total for all previous rows
- Memory intensive for large datasets
- Poor performance for long customer histories

**Approach 2 (Bounded Window)**: ✅ **RECOMMENDED**
- Computes running total for last 30 days only
- Memory efficient
- Good performance for large datasets
- Practical for most business use cases

**Approach 3 (Self JOIN)**: ❌ **NOT RECOMMENDED**
- Cartesian product for each customer
- Very slow for large datasets
- High memory usage
- Poor scalability

**Recommendation**: Use Approach 2 (Bounded Window) because:
- Best performance for large datasets
- Memory efficient
- Practical business value
- Scales well with data growth

---

## 🚀 Exercise 5: Large Dataset Handling

### Solution 5.1: Optimize Large Dataset Query
```sql
-- Given query
SELECT 
    c.customer_segment,
    COUNT(*) as order_count,
    SUM(o.order_amount) as total_revenue,
    AVG(o.order_amount) as avg_order_value
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.customer_segment
ORDER BY total_revenue DESC;
```

**Optimization Strategies**:

**Strategy 1: Create Indexes**
```sql
-- Indexes for optimization
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_customers_segment ON customers(customer_segment);
```

**Strategy 2: Use Partitioning**
```sql
-- Partition orders table by date
CREATE TABLE orders_2024 PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- Query partitioned table
SELECT 
    c.customer_segment,
    COUNT(*) as order_count,
    SUM(o.order_amount) as total_revenue,
    AVG(o.order_amount) as avg_order_value
FROM customers c
INNER JOIN orders_2024 o ON c.customer_id = o.customer_id
GROUP BY c.customer_segment
ORDER BY total_revenue DESC;
```

**Strategy 3: Use Materialized View**
```sql
-- Create materialized view for pre-computed results
CREATE MATERIALIZED VIEW customer_segment_summary AS
SELECT 
    c.customer_segment,
    COUNT(*) as order_count,
    SUM(o.order_amount) as total_revenue,
    AVG(o.order_amount) as avg_order_value
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.customer_segment;

-- Query materialized view
SELECT * FROM customer_segment_summary
ORDER BY total_revenue DESC;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW customer_segment_summary;
```

**Performance Improvements**:
- Indexes reduce table scans
- Partitioning improves query performance
- Materialized views provide instant results
- Reduced I/O operations

---

### Solution 5.2: Implement Partitioning Strategy
```sql
-- Partitioning design for orders table
-- Partition by date (monthly partitions)

-- Create partitioned table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    order_amount DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

-- Create monthly partitions
CREATE TABLE orders_2024_01 PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE orders_2024_02 PARTITION OF orders
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

CREATE TABLE orders_2024_03 PARTITION OF orders
FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');

-- Create indexes on partitions
CREATE INDEX idx_orders_2024_01_customer_id ON orders_2024_01(customer_id);
CREATE INDEX idx_orders_2024_02_customer_id ON orders_2024_02(customer_id);
CREATE INDEX idx_orders_2024_03_customer_id ON orders_2024_03(customer_id);
```

**Query Optimization for Partitioned Tables**:
```sql
-- Optimized query for partitioned table
SELECT 
    c.customer_segment,
    COUNT(*) as order_count,
    SUM(o.order_amount) as total_revenue
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01'
  AND o.order_date < '2024-04-01'
GROUP BY c.customer_segment
ORDER BY total_revenue DESC;
```

**Maintenance Procedures**:
```sql
-- Add new partition
CREATE TABLE orders_2024_04 PARTITION OF orders
FOR VALUES FROM ('2024-04-01') TO ('2024-05-01');

-- Drop old partition
DROP TABLE orders_2023_12;

-- Analyze partitions
ANALYZE orders_2024_01;
ANALYZE orders_2024_02;
ANALYZE orders_2024_03;
```

**Benefits**:
- Improved query performance
- Easier maintenance
- Better data management
- Scalable architecture

---

## 🎯 Exercise 6: Performance Troubleshooting

### Solution 6.1: Identify Performance Bottlenecks
```sql
-- Given query
SELECT 
    c.customer_name,
    p.product_name,
    COUNT(*) as order_count,
    SUM(oi.quantity * oi.unit_price) as total_revenue,
    AVG(oi.quantity * oi.unit_price) as avg_order_value
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE c.customer_segment = 'Premium'
  AND o.order_date >= '2024-01-01'
  AND p.product_category = 'Electronics'
GROUP BY c.customer_name, p.product_name
HAVING COUNT(*) > 5
ORDER BY total_revenue DESC;
```

**Performance Bottleneck Analysis**:

**Bottleneck 1**: Missing indexes on JOIN columns
**Bottleneck 2**: No index on WHERE clause columns
**Bottleneck 3**: Complex JOIN chain
**Bottleneck 4**: HAVING clause without index support

**Optimization Recommendations**:
```sql
-- Create indexes for optimization
CREATE INDEX idx_customers_segment ON customers(customer_segment);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_products_category ON products(product_category);

-- Covering indexes
CREATE INDEX idx_orders_covering ON orders(customer_id, order_date, order_id);
CREATE INDEX idx_order_items_covering ON order_items(order_id, product_id, quantity, unit_price);
```

**Improved Query**:
```sql
-- Optimized query with better structure
SELECT 
    c.customer_name,
    p.product_name,
    COUNT(*) as order_count,
    SUM(oi.quantity * oi.unit_price) as total_revenue,
    AVG(oi.quantity * oi.unit_price) as avg_order_value
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE c.customer_segment = 'Premium'
  AND o.order_date >= '2024-01-01'
  AND p.product_category = 'Electronics'
GROUP BY c.customer_name, p.product_name
HAVING COUNT(*) > 5
ORDER BY total_revenue DESC;
```

**Performance Improvements**:
- Start with filtered orders table
- Use covering indexes to avoid table lookups
- Efficient JOIN operations
- Reduced I/O operations

---

### Solution 6.2: Optimize Slow Query
```sql
-- Given slow query
SELECT 
    c.customer_id,
    c.customer_name,
    (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count,
    (SELECT SUM(order_amount) FROM orders WHERE customer_id = c.customer_id) as total_spent,
    (SELECT AVG(order_amount) FROM orders WHERE customer_id = c.customer_id) as avg_order_value,
    (SELECT MAX(order_date) FROM orders WHERE customer_id = c.customer_id) as last_order_date
FROM customers c
WHERE c.customer_segment = 'Premium';
```

**Performance Analysis**:
- **Issue 1**: Correlated subqueries are slow
- **Issue 2**: Multiple table scans on orders table
- **Issue 3**: No indexes on customer_id
- **Issue 4**: Inefficient query structure

**Optimized Query**:
```sql
-- Optimized query using JOINs
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) as order_count,
    COALESCE(SUM(o.order_amount), 0) as total_spent,
    COALESCE(AVG(o.order_amount), 0) as avg_order_value,
    MAX(o.order_date) as last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.customer_segment = 'Premium'
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spent DESC;
```

**Index Recommendations**:
```sql
-- Create indexes for optimization
CREATE INDEX idx_customers_segment ON customers(customer_segment);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_customer_amount ON orders(customer_id, order_amount);
```

**Performance Improvements**:
- Single table scan on customers
- Single table scan on orders
- Efficient hash join
- Reduced execution time from 30 seconds to < 1 second

---

## 🔥 Exercise 7: Real-World Performance Scenarios

### Solution 7.1: ETL Pipeline Optimization
```sql
-- Given ETL query
SELECT 
    ro.customer_id,
    c.customer_name,
    c.customer_segment,
    p.product_name,
    p.product_category,
    ro.order_date,
    ro.order_amount,
    ro.quantity,
    ro.unit_price,
    ro.quantity * ro.unit_price as total_amount
FROM raw_orders ro
LEFT JOIN customers c ON ro.customer_id = c.customer_id
LEFT JOIN products p ON ro.product_id = p.product_id
WHERE ro.order_date >= '2024-01-01'
ORDER BY ro.order_date, ro.customer_id;
```

**ETL Optimization Strategies**:

**Strategy 1: Batch Processing**
```sql
-- Process data in batches
SELECT 
    ro.customer_id,
    c.customer_name,
    c.customer_segment,
    p.product_name,
    p.product_category,
    ro.order_date,
    ro.order_amount,
    ro.quantity,
    ro.unit_price,
    ro.quantity * ro.unit_price as total_amount
FROM raw_orders ro
LEFT JOIN customers c ON ro.customer_id = c.customer_id
LEFT JOIN products p ON ro.product_id = p.product_id
WHERE ro.order_date >= '2024-01-01'
  AND ro.order_date < '2024-02-01'
ORDER BY ro.order_date, ro.customer_id;
```

**Strategy 2: Create Indexes**
```sql
-- Indexes for ETL optimization
CREATE INDEX idx_raw_orders_date ON raw_orders(order_date);
CREATE INDEX idx_raw_orders_customer_id ON raw_orders(customer_id);
CREATE INDEX idx_raw_orders_product_id ON raw_orders(product_id);
```

**Strategy 3: Use CTEs for Readability**
```sql
-- ETL with CTEs for better readability
WITH filtered_orders AS (
    SELECT *
    FROM raw_orders
    WHERE order_date >= '2024-01-01'
),
enriched_orders AS (
    SELECT 
        ro.customer_id,
        c.customer_name,
        c.customer_segment,
        p.product_name,
        p.product_category,
        ro.order_date,
        ro.order_amount,
        ro.quantity,
        ro.unit_price,
        ro.quantity * ro.unit_price as total_amount
    FROM filtered_orders ro
    LEFT JOIN customers c ON ro.customer_id = c.customer_id
    LEFT JOIN products p ON ro.product_id = p.product_id
)
SELECT * FROM enriched_orders
ORDER BY order_date, customer_id;
```

**Performance Improvements**:
- Batch processing reduces memory usage
- Indexes improve JOIN performance
- CTEs improve readability and maintainability
- Better error handling and debugging

---

### Solution 7.2: Analytics Dashboard Optimization
```sql
-- Dashboard Query 1: Total revenue by month
CREATE MATERIALIZED VIEW monthly_revenue AS
SELECT 
    DATE_TRUNC('month', order_date) as month,
    SUM(order_amount) as total_revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;

-- Dashboard Query 2: Top customers by revenue
CREATE MATERIALIZED VIEW top_customers AS
SELECT 
    c.customer_name,
    SUM(o.order_amount) as total_revenue
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_name
ORDER BY total_revenue DESC
LIMIT 100;

-- Dashboard Query 3: Product performance metrics
CREATE MATERIALIZED VIEW product_performance AS
SELECT 
    p.product_name,
    COUNT(oi.order_id) as order_count,
    SUM(oi.quantity) as total_quantity,
    SUM(oi.quantity * oi.unit_price) as total_revenue
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_name
ORDER BY total_revenue DESC;

-- Dashboard Query 4: Customer segment analysis
CREATE MATERIALIZED VIEW customer_segment_analysis AS
SELECT 
    c.customer_segment,
    COUNT(DISTINCT c.customer_id) as customer_count,
    SUM(o.order_amount) as total_revenue,
    AVG(o.order_amount) as avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_segment
ORDER BY total_revenue DESC;

-- Dashboard Query 5: Sales trends
CREATE MATERIALIZED VIEW sales_trends AS
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as order_count,
    SUM(order_amount) as total_revenue,
    AVG(order_amount) as avg_order_value
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

**Caching Strategies**:
```sql
-- Refresh materialized views
REFRESH MATERIALIZED VIEW monthly_revenue;
REFRESH MATERIALIZED VIEW top_customers;
REFRESH MATERIALIZED VIEW product_performance;
REFRESH MATERIALIZED VIEW customer_segment_analysis;
REFRESH MATERIALIZED VIEW sales_trends;

-- Schedule regular refreshes
-- CREATE OR REPLACE FUNCTION refresh_dashboard_views()
-- RETURNS void AS $$
-- BEGIN
--     REFRESH MATERIALIZED VIEW monthly_revenue;
--     REFRESH MATERIALIZED VIEW top_customers;
--     REFRESH MATERIALIZED VIEW product_performance;
--     REFRESH MATERIALIZED VIEW customer_segment_analysis;
--     REFRESH MATERIALIZED VIEW sales_trends;
-- END;
-- $$ LANGUAGE plpgsql;
```

**Performance Improvements**:
- Materialized views provide instant results
- Pre-computed aggregations
- Reduced query execution time
- Better user experience

---

## 💡 Exercise 8: Advanced Performance Patterns

### Solution 8.1: Query Plan Optimization
```sql
-- Given query
SELECT 
    c.customer_segment,
    COUNT(*) as customer_count,
    AVG(o.order_amount) as avg_order_value,
    SUM(o.order_amount) as total_revenue
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.customer_segment
HAVING COUNT(*) > 100
ORDER BY total_revenue DESC;
```

**Execution Plan Analysis**:
- Table scan on customers table
- Table scan on orders table
- Hash join operation
- Group by operation
- Having filter
- Sort operation

**Optimization Strategies**:

**Strategy 1: Create Indexes**
```sql
-- Indexes for optimization
CREATE INDEX idx_customers_segment ON customers(customer_segment);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
```

**Strategy 2: Optimize Query Structure**
```sql
-- Optimized query
SELECT 
    c.customer_segment,
    COUNT(*) as customer_count,
    AVG(o.order_amount) as avg_order_value,
    SUM(o.order_amount) as total_revenue
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.customer_segment
HAVING COUNT(*) > 100
ORDER BY total_revenue DESC;
```

**Strategy 3: Use Materialized View**
```sql
-- Create materialized view for complex aggregation
CREATE MATERIALIZED VIEW customer_segment_summary AS
SELECT 
    c.customer_segment,
    COUNT(*) as customer_count,
    AVG(o.order_amount) as avg_order_value,
    SUM(o.order_amount) as total_revenue
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.customer_segment
HAVING COUNT(*) > 100
ORDER BY total_revenue DESC;

-- Query materialized view
SELECT * FROM customer_segment_summary;
```

**Performance Improvements**:
- Indexes reduce table scans
- Better query structure improves execution plan
- Materialized views provide instant results
- Reduced I/O operations

---

### Solution 8.2: Memory and I/O Optimization
```sql
-- Given query
SELECT 
    o.order_id,
    o.order_date,
    o.customer_id,
    SUM(oi.quantity * oi.unit_price) as total_amount,
    COUNT(oi.order_item_id) as item_count
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_date >= '2024-01-01'
GROUP BY o.order_id, o.order_date, o.customer_id
ORDER BY total_amount DESC;
```

**Memory Optimization Strategies**:

**Strategy 1: Use Appropriate Data Types**
```sql
-- Optimize data types
CREATE TABLE orders_optimized (
    order_id INTEGER PRIMARY KEY,
    order_date DATE,
    customer_id INTEGER,
    order_amount DECIMAL(10,2)
);

CREATE TABLE order_items_optimized (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10,2)
);
```

**Strategy 2: Create Covering Indexes**
```sql
-- Covering indexes for I/O optimization
CREATE INDEX idx_orders_covering ON orders(order_id, order_date, customer_id);
CREATE INDEX idx_order_items_covering ON order_items(order_id, product_id, quantity, unit_price);
```

**Strategy 3: Optimize Query Structure**
```sql
-- Optimized query with better structure
SELECT 
    o.order_id,
    o.order_date,
    o.customer_id,
    SUM(oi.quantity * oi.unit_price) as total_amount,
    COUNT(oi.order_item_id) as item_count
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_date >= '2024-01-01'
GROUP BY o.order_id, o.order_date, o.customer_id
ORDER BY total_amount DESC;
```

**I/O Optimization Strategies**:

**Strategy 1: Use Partitioning**
```sql
-- Partition orders table by date
CREATE TABLE orders_2024 PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- Query partitioned table
SELECT 
    o.order_id,
    o.order_date,
    o.customer_id,
    SUM(oi.quantity * oi.unit_price) as total_amount,
    COUNT(oi.order_item_id) as item_count
FROM orders_2024 o
INNER JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_date, o.customer_id
ORDER BY total_amount DESC;
```

**Strategy 2: Use Materialized Views**
```sql
-- Create materialized view for complex aggregations
CREATE MATERIALIZED VIEW order_summary AS
SELECT 
    o.order_id,
    o.order_date,
    o.customer_id,
    SUM(oi.quantity * oi.unit_price) as total_amount,
    COUNT(oi.order_item_id) as item_count
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_date >= '2024-01-01'
GROUP BY o.order_id, o.order_date, o.customer_id
ORDER BY total_amount DESC;

-- Query materialized view
SELECT * FROM order_summary;
```

**Resource Usage Analysis**:
- Memory usage reduced with appropriate data types
- I/O operations reduced with covering indexes
- Query performance improved with partitioning
- Instant results with materialized views

---

## 🎯 Key Takeaways

### Performance Optimization Principles:
1. **Analyze execution plans** before optimizing
2. **Create appropriate indexes** for query patterns
3. **Optimize JOIN strategies** for large datasets
4. **Use bounded windows** for window functions
5. **Consider partitioning** for very large tables
6. **Use materialized views** for complex aggregations
7. **Monitor performance** continuously
8. **Test with realistic data** volumes

### Index Design Best Practices:
1. Index frequently queried columns
2. Use composite indexes for multi-column queries
3. Consider covering indexes for specific queries
4. Monitor index usage and remove unused indexes
5. Maintain indexes regularly

### Query Optimization Techniques:
1. Start with filtered tables
2. Use appropriate JOIN types
3. Avoid correlated subqueries
4. Use CTEs for complex logic
5. Consider alternative approaches

### Performance Monitoring:
1. Use execution plans to identify bottlenecks
2. Measure query execution times
3. Monitor resource usage
4. Set up performance alerts
5. Regular performance reviews

**Master these patterns and you'll be ready for any performance challenge!** 🚀

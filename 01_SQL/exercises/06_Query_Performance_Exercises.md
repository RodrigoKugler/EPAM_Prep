# SQL Query Performance - Practice Exercises

## 🎯 Exercise Guidelines

- **Time Target**: 10-15 minutes per exercise
- **Approach**: Focus on performance optimization techniques
- **Tools**: Use EXPLAIN QUERY PLAN to analyze execution plans
- **Practice**: Test with realistic data volumes

---

## 📚 Exercise 1: Execution Plan Analysis

### Problem 1.1: Analyze Query Execution Plan
**Tables**: `customers` (100K records), `orders` (1M records)

**Task**: Analyze the execution plan for the following query and identify performance issues.

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
```

**Expected Output**: 
- Execution plan analysis
- Performance bottlenecks identified
- Optimization recommendations

**Hint**: Use `EXPLAIN QUERY PLAN` to analyze the execution plan

---

### Problem 1.2: Compare Execution Plans
**Tables**: `orders` (1M records), `order_items` (5M records)

**Task**: Compare execution plans for two different query approaches and recommend the better one.

**Query 1**:
```sql
SELECT 
    o.order_id,
    o.order_date,
    SUM(oi.quantity * oi.unit_price) as total_amount
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_date >= '2024-01-01'
GROUP BY o.order_id, o.order_date
ORDER BY total_amount DESC;
```

**Query 2**:
```sql
SELECT 
    o.order_id,
    o.order_date,
    o.total_amount
FROM orders o
WHERE o.order_date >= '2024-01-01'
ORDER BY o.total_amount DESC;
```

**Expected Output**: 
- Execution plan comparison
- Performance analysis
- Recommendation with reasoning

---

## 🔥 Exercise 2: Index Design and Optimization

### Problem 2.1: Design Indexes for Query Optimization
**Tables**: `customers`, `orders`, `order_items`, `products`

**Task**: Design the optimal indexes for the following query patterns.

**Query Patterns**:
1. Find orders by customer
2. Find orders by date range
3. Find orders by customer and date
4. Find orders by amount range
5. Find orders by customer, date, and amount

**Expected Output**:
- Index design recommendations
- Index creation statements
- Performance impact analysis

**Hint**: Consider single-column, composite, and covering indexes

---

### Problem 2.2: Index Usage Analysis
**Tables**: `orders` (1M records), `customers` (100K records)

**Task**: Analyze which indexes are being used and which are not.

**Given Indexes**:
```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_amount ON orders(order_amount);
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_customers_segment ON customers(customer_segment);
```

**Queries to Analyze**:
```sql
-- Query 1
SELECT * FROM orders WHERE customer_id = 123;

-- Query 2
SELECT * FROM orders WHERE order_date >= '2024-01-01';

-- Query 3
SELECT * FROM orders WHERE customer_id = 123 AND order_date >= '2024-01-01';

-- Query 4
SELECT * FROM orders WHERE order_amount > 1000;

-- Query 5
SELECT * FROM orders WHERE order_date >= '2024-01-01' AND order_amount > 1000;
```

**Expected Output**:
- Index usage analysis for each query
- Recommendations for unused indexes
- Suggestions for new indexes

---

## 🎯 Exercise 3: JOIN Optimization

### Problem 3.1: Optimize Complex JOINs
**Tables**: `customers` (100K), `orders` (1M), `order_items` (5M), `products` (10K)

**Task**: Optimize the following complex JOIN query for better performance.

**Given Query**:
```sql
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

**Expected Output**:
- Optimized query
- Index recommendations
- Performance improvements

**Hint**: Consider JOIN order, indexes, and query structure

---

### Problem 3.2: Choose Optimal JOIN Strategy
**Tables**: `customers` (100K), `orders` (1M)

**Task**: Compare different JOIN strategies and choose the most efficient one.

**Scenario**: Find all customers and their order information, including customers with no orders.

**Approach 1 - LEFT JOIN**:
```sql
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) as order_count,
    COALESCE(SUM(o.order_amount), 0) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;
```

**Approach 2 - Subquery**:
```sql
SELECT 
    c.customer_id,
    c.customer_name,
    (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count,
    (SELECT COALESCE(SUM(order_amount), 0) FROM orders WHERE customer_id = c.customer_id) as total_spent
FROM customers c;
```

**Approach 3 - Window Function**:
```sql
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) OVER (PARTITION BY c.customer_id) as order_count,
    COALESCE(SUM(o.order_amount) OVER (PARTITION BY c.customer_id), 0) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

**Expected Output**:
- Performance comparison
- Execution plan analysis
- Recommendation with reasoning

---

## 🔧 Exercise 4: Window Function Optimization

### Problem 4.1: Optimize Window Functions
**Tables**: `orders` (1M records)

**Task**: Optimize window function queries for better performance.

**Given Query**:
```sql
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

**Expected Output**:
- Optimized query
- Performance improvements
- Alternative approaches

**Hint**: Consider bounded windows and partitioning strategies

---

### Problem 4.2: Compare Window Function Approaches
**Tables**: `orders` (1M records)

**Task**: Compare different approaches to calculating running totals.

**Approach 1 - Unbounded Window**:
```sql
SELECT 
    customer_id,
    order_date,
    order_amount,
    SUM(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM orders;
```

**Approach 2 - Bounded Window**:
```sql
SELECT 
    customer_id,
    order_date,
    order_amount,
    SUM(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as running_total_30_days
FROM orders;
```

**Approach 3 - Self JOIN**:
```sql
SELECT 
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

**Expected Output**:
- Performance comparison
- Use case recommendations
- Optimization suggestions

---

## 🚀 Exercise 5: Large Dataset Handling

### Problem 5.1: Optimize Large Dataset Query
**Tables**: `orders` (100M records), `customers` (10M records)

**Task**: Optimize a query on a very large dataset.

**Given Query**:
```sql
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

**Expected Output**:
- Optimization strategies
- Index recommendations
- Partitioning suggestions
- Performance improvements

**Hint**: Consider partitioning, materialized views, and query optimization

---

### Problem 5.2: Implement Partitioning Strategy
**Tables**: `orders` (100M records)

**Task**: Design a partitioning strategy for the orders table.

**Requirements**:
- Partition by date (monthly partitions)
- Support efficient date range queries
- Minimize maintenance overhead
- Handle data growth

**Expected Output**:
- Partitioning design
- Partition creation statements
- Query optimization for partitioned tables
- Maintenance procedures

---

## 🎯 Exercise 6: Performance Troubleshooting

### Problem 6.1: Identify Performance Bottlenecks
**Tables**: `customers`, `orders`, `order_items`, `products`

**Task**: Identify and fix performance bottlenecks in the following query.

**Given Query**:
```sql
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

**Expected Output**:
- Performance bottleneck analysis
- Optimization recommendations
- Improved query
- Index suggestions

---

### Problem 6.2: Optimize Slow Query
**Tables**: `orders` (1M records), `customers` (100K records)

**Task**: Optimize a query that's taking 30 seconds to execute.

**Given Slow Query**:
```sql
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

**Expected Output**:
- Performance analysis
- Optimized query
- Performance improvements
- Execution time comparison

---

## 🔥 Exercise 7: Real-World Performance Scenarios

### Problem 7.1: ETL Pipeline Optimization
**Tables**: `raw_orders` (50M records), `customers`, `products`

**Task**: Optimize an ETL pipeline query for data transformation.

**Given ETL Query**:
```sql
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

**Expected Output**:
- ETL optimization strategies
- Performance improvements
- Index recommendations
- Batch processing suggestions

---

### Problem 7.2: Analytics Dashboard Optimization
**Tables**: `orders` (1M records), `customers`, `products`

**Task**: Optimize queries for a real-time analytics dashboard.

**Dashboard Queries**:
1. Total revenue by month
2. Top customers by revenue
3. Product performance metrics
4. Customer segment analysis
5. Sales trends

**Expected Output**:
- Optimized dashboard queries
- Materialized view recommendations
- Caching strategies
- Performance improvements

---

## 💡 Exercise 8: Advanced Performance Patterns

### Problem 8.1: Query Plan Optimization
**Tables**: `orders` (1M records), `customers` (100K records)

**Task**: Analyze and optimize query execution plans.

**Given Query**:
```sql
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

**Expected Output**:
- Execution plan analysis
- Optimization strategies
- Performance improvements
- Alternative approaches

---

### Problem 8.2: Memory and I/O Optimization
**Tables**: `orders` (1M records), `order_items` (5M records)

**Task**: Optimize queries for memory and I/O efficiency.

**Given Query**:
```sql
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

**Expected Output**:
- Memory optimization strategies
- I/O optimization techniques
- Query improvements
- Resource usage analysis

---

## 🎯 Challenge Exercises

### Challenge 1: Complete Performance Audit
**Task**: Perform a complete performance audit on a complex query system.

**Requirements**:
- Analyze all queries in the system
- Identify performance bottlenecks
- Recommend optimizations
- Create performance monitoring plan
- Implement performance improvements

### Challenge 2: Scalability Design
**Task**: Design a scalable query system for handling 1 billion records.

**Requirements**:
- Partitioning strategy
- Index design
- Query optimization
- Performance monitoring
- Maintenance procedures

### Challenge 3: Real-Time Performance Optimization
**Task**: Optimize queries for a real-time analytics system.

**Requirements**:
- Sub-second query response times
- Efficient data processing
- Resource optimization
- Monitoring and alerting
- Performance tuning

---

## 📚 Exercise Solutions

**Solutions are available in**: `01_SQL/solutions/06_Query_Performance_Solutions.md`

**Remember**: 
- Attempt each exercise before checking solutions
- Focus on understanding performance concepts
- Practice with realistic data volumes
- Time yourself to improve speed

---

## 🎯 Success Criteria

**By completing these exercises, you should be able to**:
- ✅ Analyze query execution plans
- ✅ Design effective indexes
- ✅ Optimize JOIN performance
- ✅ Handle large datasets efficiently
- ✅ Optimize window functions
- ✅ Troubleshoot performance issues
- ✅ Implement partitioning strategies
- ✅ Monitor query performance

**Target**: Optimize any query in under 10 minutes! 🚀

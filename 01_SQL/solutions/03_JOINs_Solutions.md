# SQL Advanced JOINs - Exercise Solutions

## 🎯 Solution Guidelines

- **Approach**: Start with the business requirement, then choose the right JOIN type
- **Performance**: Consider efficiency and readability
- **Validation**: Always verify results with sample data
- **Best Practices**: Follow professional SQL standards

---

## 📚 Exercise 1: Basic JOIN Types

### Solution 1.1: Customer Order Analysis
```sql
-- Problem: Show all customers and their order information, including customers with no orders
-- Approach: Use LEFT JOIN to preserve all customers

SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) as order_count,
    COALESCE(SUM(o.order_amount), 0) as total_spent,
    CASE 
        WHEN COUNT(o.order_id) = 0 THEN 'No Orders'
        WHEN COUNT(o.order_id) = 1 THEN 'Single Order'
        ELSE 'Active Customer'
    END as customer_status
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spent DESC;
```

**Key Points**:
- `LEFT JOIN` preserves all customers
- `COALESCE` handles NULL values from customers with no orders
- `GROUP BY` aggregates order data per customer
- `CASE` statement provides business logic

---

### Solution 1.2: Product Sales Analysis
```sql
-- Problem: Find all products and their sales performance, including products with no sales
-- Approach: Use LEFT JOIN to preserve all products

SELECT 
    p.product_id,
    p.product_name,
    COALESCE(SUM(oi.quantity), 0) as total_quantity_sold,
    COALESCE(SUM(oi.quantity * oi.unit_price), 0) as total_revenue,
    CASE 
        WHEN COALESCE(SUM(oi.quantity), 0) = 0 THEN 'No Sales'
        WHEN COALESCE(SUM(oi.quantity), 0) < 10 THEN 'Low Sales'
        WHEN COALESCE(SUM(oi.quantity), 0) < 50 THEN 'Moderate Sales'
        ELSE 'High Sales'
    END as sales_status
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_revenue DESC;
```

---

## 🔥 Exercise 2: Data Reconciliation

### Solution 2.1: System Data Comparison
```sql
-- Problem: Compare customer data between two systems and identify discrepancies
-- Approach: Use FULL OUTER JOIN for complete comparison

SELECT 
    COALESCE(a.customer_id, b.customer_id) as customer_id,
    a.customer_name as system_a_name,
    b.customer_name as system_b_name,
    a.email as system_a_email,
    b.email as system_b_email,
    CASE 
        WHEN a.customer_id IS NULL THEN 'Missing in System A'
        WHEN b.customer_id IS NULL THEN 'Missing in System B'
        WHEN a.customer_name != b.customer_name THEN 'Name Mismatch'
        WHEN a.email != b.email THEN 'Email Mismatch'
        ELSE 'Perfect Match'
    END as issue_type
FROM system_a_customers a
FULL OUTER JOIN system_b_customers b ON a.customer_id = b.customer_id
ORDER BY issue_type, customer_id;
```

**Key Points**:
- `FULL OUTER JOIN` captures all records from both systems
- `COALESCE` handles NULL values from either side
- `CASE` statement categorizes different types of discrepancies

---

### Solution 2.2: Order Reconciliation
```sql
-- Problem: Find orders that exist in one system but not the other, and identify potential duplicates
-- Approach: Use FULL OUTER JOIN for complete comparison

SELECT 
    COALESCE(w.order_id, m.order_id) as order_id,
    w.order_amount as web_amount,
    m.order_amount as mobile_amount,
    w.order_date as web_date,
    m.order_date as mobile_date,
    CASE 
        WHEN w.order_id IS NULL THEN 'Only in Mobile'
        WHEN m.order_id IS NULL THEN 'Only in Web'
        WHEN w.order_amount != m.order_amount THEN 'Amount Mismatch'
        WHEN w.order_date != m.order_date THEN 'Date Mismatch'
        ELSE 'Perfect Match'
    END as reconciliation_status
FROM web_orders w
FULL OUTER JOIN mobile_orders m ON w.order_id = m.order_id
ORDER BY reconciliation_status, order_id;
```

---

## 🎯 Exercise 3: Star Schema Queries

### Solution 3.1: Sales Performance Report
```sql
-- Problem: Create a comprehensive sales report by customer segment, product category, and time period
-- Approach: Use INNER JOINs for star schema query

SELECT 
    c.customer_segment,
    p.product_category,
    d.year,
    d.quarter,
    COUNT(f.order_id) as total_orders,
    SUM(f.total_amount) as total_revenue,
    AVG(f.total_amount) as avg_order_value
FROM fact_sales f
INNER JOIN dim_customers c ON f.customer_id = c.customer_id
INNER JOIN dim_products p ON f.product_id = p.product_id
INNER JOIN dim_dates d ON f.order_date_id = d.date_id
WHERE d.year = 2024
GROUP BY c.customer_segment, p.product_category, d.year, d.quarter
ORDER BY total_revenue DESC;
```

**Key Points**:
- Star schema uses INNER JOINs to connect fact table with dimension tables
- `GROUP BY` aggregates metrics by dimension combinations
- `WHERE` clause filters for specific time period

---

### Solution 3.2: Customer Journey Analysis
```sql
-- Problem: Analyze customer behavior over time, including first purchase and customer lifetime value
-- Approach: Use window functions with JOINs for comprehensive analysis

SELECT 
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    MIN(f.order_date) as first_order_date,
    COUNT(f.order_id) as total_orders,
    SUM(f.total_amount) as total_spent,
    AVG(f.total_amount) as avg_order_value,
    JULIANDAY(MAX(f.order_date)) - JULIANDAY(MIN(f.order_date)) as customer_lifetime_days
FROM dim_customers c
INNER JOIN fact_orders f ON c.customer_id = f.customer_id
GROUP BY c.customer_id, c.customer_name, c.customer_segment
ORDER BY total_spent DESC;
```

---

## 🔧 Exercise 4: Self JOINs

### Solution 4.1: Employee Hierarchy
```sql
-- Problem: Create an employee hierarchy report showing each employee and their manager
-- Approach: Use SELF JOIN with LEFT JOIN to include top-level employees

SELECT 
    e1.employee_id,
    e1.employee_name,
    e1.manager_id,
    e2.employee_name as manager_name,
    CASE 
        WHEN e1.manager_id IS NULL THEN 1
        WHEN e2.manager_id IS NULL THEN 2
        WHEN e3.manager_id IS NULL THEN 3
        ELSE 4
    END as hierarchy_level
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.employee_id
LEFT JOIN employees e3 ON e2.manager_id = e3.employee_id
ORDER BY hierarchy_level, e1.employee_name;
```

**Key Points**:
- Multiple SELF JOINs to build hierarchy levels
- `LEFT JOIN` preserves employees without managers
- `CASE` statement determines hierarchy level

---

### Solution 4.2: Duplicate Customer Detection
```sql
-- Problem: Find potential duplicate customers based on similar names or email addresses
-- Approach: Use SELF JOIN with inequality condition to avoid comparing same record

SELECT 
    c1.customer_id as customer_1_id,
    c1.customer_name as customer_1_name,
    c1.email as customer_1_email,
    c2.customer_id as customer_2_id,
    c2.customer_name as customer_2_name,
    c2.email as customer_2_email,
    CASE 
        WHEN c1.email = c2.email THEN 'Same Email'
        WHEN LOWER(c1.customer_name) = LOWER(c2.customer_name) THEN 'Same Name'
        WHEN LOWER(c1.customer_name) LIKE '%' || LOWER(c2.customer_name) || '%' 
          OR LOWER(c2.customer_name) LIKE '%' || LOWER(c1.customer_name) || '%' 
        THEN 'Similar Name'
        ELSE 'Potential Duplicate'
    END as duplicate_reason
FROM customers c1
INNER JOIN customers c2 ON c1.customer_id < c2.customer_id
WHERE c1.email = c2.email 
   OR LOWER(c1.customer_name) = LOWER(c2.customer_name)
   OR LOWER(c1.customer_name) LIKE '%' || LOWER(c2.customer_name) || '%'
   OR LOWER(c2.customer_name) LIKE '%' || LOWER(c1.customer_name) || '%'
ORDER BY duplicate_reason, customer_1_id;
```

**Key Points**:
- `c1.customer_id < c2.customer_id` prevents comparing same record twice
- Multiple conditions in WHERE clause to catch different types of duplicates
- `LIKE` with wildcards for fuzzy name matching

---

## 🚀 Exercise 5: Complex Multi-Table JOINs

### Solution 5.1: ETL Data Enrichment
```sql
-- Problem: Enrich raw transaction data with customer, product, and regional information
-- Approach: Use LEFT JOINs to preserve all transactions, handle missing data gracefully

SELECT 
    rt.transaction_id,
    rt.transaction_date,
    COALESCE(c.customer_name, 'Unknown') as customer_name,
    COALESCE(c.customer_segment, 'Unknown') as customer_segment,
    COALESCE(p.product_name, 'Unknown') as product_name,
    COALESCE(p.product_category, 'Unknown') as product_category,
    COALESCE(r.region_name, 'Unknown') as region_name,
    rt.amount,
    CASE 
        WHEN c.customer_id IS NULL AND p.product_id IS NULL THEN 'Missing Data'
        WHEN c.customer_id IS NULL OR p.product_id IS NULL THEN 'Partially Enriched'
        ELSE 'Fully Enriched'
    END as enriched_status
FROM raw_transactions rt
LEFT JOIN customers c ON rt.customer_id = c.customer_id
LEFT JOIN products p ON rt.product_id = p.product_id
LEFT JOIN regions r ON rt.region_id = r.region_id
ORDER BY enriched_status, rt.transaction_date;
```

---

### Solution 5.2: Comprehensive Data Quality Check
```sql
-- Problem: Create a data quality dashboard showing various data quality metrics
-- Approach: Use multiple JOINs and conditional aggregation

SELECT 
    'Orders with Valid Customers' as quality_check,
    COUNT(*) as total_records,
    COUNT(CASE WHEN c.customer_id IS NOT NULL THEN 1 END) as valid_records,
    COUNT(CASE WHEN c.customer_id IS NULL THEN 1 END) as invalid_records,
    ROUND(COUNT(CASE WHEN c.customer_id IS NULL THEN 1 END) * 100.0 / COUNT(*), 2) as error_rate_pct
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id

UNION ALL

SELECT 
    'Orders with Valid Products' as quality_check,
    COUNT(*) as total_records,
    COUNT(CASE WHEN p.product_id IS NOT NULL THEN 1 END) as valid_records,
    COUNT(CASE WHEN p.product_id IS NULL THEN 1 END) as invalid_records,
    ROUND(COUNT(CASE WHEN p.product_id IS NULL THEN 1 END) * 100.0 / COUNT(*), 2) as error_rate_pct
FROM orders o
LEFT JOIN products p ON o.product_id = p.product_id

UNION ALL

SELECT 
    'Orders with Positive Amounts' as quality_check,
    COUNT(*) as total_records,
    COUNT(CASE WHEN o.order_amount > 0 THEN 1 END) as valid_records,
    COUNT(CASE WHEN o.order_amount <= 0 THEN 1 END) as invalid_records,
    ROUND(COUNT(CASE WHEN o.order_amount <= 0 THEN 1 END) * 100.0 / COUNT(*), 2) as error_rate_pct
FROM orders o

UNION ALL

SELECT 
    'Complete Orders' as quality_check,
    COUNT(*) as total_records,
    COUNT(CASE WHEN c.customer_id IS NOT NULL 
                AND p.product_id IS NOT NULL 
                AND o.order_amount > 0 
                AND o.order_date IS NOT NULL 
           THEN 1 END) as valid_records,
    COUNT(CASE WHEN c.customer_id IS NULL 
                OR p.product_id IS NULL 
                OR o.order_amount <= 0 
                OR o.order_date IS NULL 
           THEN 1 END) as invalid_records,
    ROUND(COUNT(CASE WHEN c.customer_id IS NULL 
                      OR p.product_id IS NULL 
                      OR o.order_amount <= 0 
                      OR o.order_date IS NULL 
                 THEN 1 END) * 100.0 / COUNT(*), 2) as error_rate_pct
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN products p ON o.product_id = p.product_id

ORDER BY quality_check;
```

---

## 🎯 Exercise 6: Performance Optimization

### Solution 6.1: Efficient Customer Analysis
```sql
-- Problem: Find top 100 customers by total spending efficiently
-- Approach: Start with filtered data, use appropriate indexes

-- Step 1: Create indexes for performance
-- CREATE INDEX idx_orders_customer_id ON orders(customer_id);
-- CREATE INDEX idx_orders_order_amount ON orders(order_amount);
-- CREATE INDEX idx_customers_customer_id ON customers(customer_id);

-- Step 2: Optimized query
SELECT 
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    SUM(o.order_amount) as total_spent,
    COUNT(o.order_id) as order_count,
    AVG(o.order_amount) as avg_order_value
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2023-01-01'  -- Filter early for performance
GROUP BY c.customer_id, c.customer_name, c.customer_segment
ORDER BY total_spent DESC
LIMIT 100;
```

**Performance Tips**:
- Start with the table that will be filtered most
- Use appropriate indexes on JOIN columns
- Filter early in the query
- Use `INNER JOIN` when you don't need NULLs

---

### Solution 6.2: Optimized Data Reconciliation
```sql
-- Problem: Efficiently find all discrepancies between two large datasets
-- Approach: Use summary statistics first, then drill down if needed

-- Step 1: Get summary statistics
SELECT 
    'Perfect Matches' as discrepancy_type,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM system_a_data), 2) as percentage
FROM system_a_data a
INNER JOIN system_b_data b ON a.customer_id = b.customer_id
WHERE a.customer_name = b.customer_name 
  AND a.email = b.email

UNION ALL

SELECT 
    'Missing in System A' as discrepancy_type,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM system_a_data), 2) as percentage
FROM system_b_data b
LEFT JOIN system_a_data a ON b.customer_id = a.customer_id
WHERE a.customer_id IS NULL

UNION ALL

SELECT 
    'Missing in System B' as discrepancy_type,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM system_a_data), 2) as percentage
FROM system_a_data a
LEFT JOIN system_b_data b ON a.customer_id = b.customer_id
WHERE b.customer_id IS NULL

UNION ALL

SELECT 
    'Data Mismatches' as discrepancy_type,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM system_a_data), 2) as percentage
FROM system_a_data a
INNER JOIN system_b_data b ON a.customer_id = b.customer_id
WHERE a.customer_name != b.customer_name 
   OR a.email != b.email

ORDER BY count DESC;
```

---

## 🔥 Exercise 7: Real-World Scenarios

### Solution 7.1: E-commerce Analytics
```sql
-- Problem: Create a comprehensive e-commerce analytics report
-- Approach: Use multiple JOINs with time-based grouping

SELECT 
    c.customer_segment,
    cat.category_name,
    DATE_TRUNC('month', o.order_date) as month,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(oi.quantity * oi.unit_price) as total_revenue,
    AVG(oi.quantity * oi.unit_price) as avg_order_value,
    COUNT(DISTINCT o.customer_id) as unique_customers
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
INNER JOIN categories cat ON p.category_id = cat.category_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.customer_segment, cat.category_name, DATE_TRUNC('month', o.order_date)
ORDER BY total_revenue DESC;
```

---

### Solution 7.2: Data Migration Validation
```sql
-- Problem: Validate data migration from old system to new system
-- Approach: Use aggregate queries to compare totals

SELECT 
    'Total Orders' as validation_check,
    (SELECT COUNT(*) FROM old_system_orders) as old_system_count,
    (SELECT COUNT(*) FROM new_system_orders) as new_system_count,
    (SELECT COUNT(*) FROM new_system_orders) - (SELECT COUNT(*) FROM old_system_orders) as difference,
    CASE 
        WHEN (SELECT COUNT(*) FROM old_system_orders) = (SELECT COUNT(*) FROM new_system_orders) 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as status

UNION ALL

SELECT 
    'Orders by Premium Customers' as validation_check,
    (SELECT COUNT(*) FROM old_system_orders o 
     INNER JOIN customers c ON o.customer_id = c.customer_id 
     WHERE c.customer_segment = 'Premium') as old_system_count,
    (SELECT COUNT(*) FROM new_system_orders o 
     INNER JOIN customers c ON o.customer_id = c.customer_id 
     WHERE c.customer_segment = 'Premium') as new_system_count,
    (SELECT COUNT(*) FROM new_system_orders o 
     INNER JOIN customers c ON o.customer_id = c.customer_id 
     WHERE c.customer_segment = 'Premium') - 
    (SELECT COUNT(*) FROM old_system_orders o 
     INNER JOIN customers c ON o.customer_id = c.customer_id 
     WHERE c.customer_segment = 'Premium') as difference,
    CASE 
        WHEN (SELECT COUNT(*) FROM old_system_orders o 
              INNER JOIN customers c ON o.customer_id = c.customer_id 
              WHERE c.customer_segment = 'Premium') = 
             (SELECT COUNT(*) FROM new_system_orders o 
              INNER JOIN customers c ON o.customer_id = c.customer_id 
              WHERE c.customer_segment = 'Premium')
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as status

ORDER BY validation_check;
```

---

## 💡 Exercise 8: Advanced Patterns

### Solution 8.1: Time-Series Data Analysis
```sql
-- Problem: Analyze sales trends with moving averages and period comparisons
-- Approach: Use window functions with JOINs for comprehensive analysis

SELECT 
    ds.date,
    r.region_name,
    p.product_category,
    ds.daily_sales,
    AVG(ds.daily_sales) OVER (
        PARTITION BY r.region_name, p.product_category 
        ORDER BY ds.date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as seven_day_avg,
    AVG(ds.daily_sales) OVER (
        PARTITION BY r.region_name, p.product_category 
        ORDER BY ds.date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as thirty_day_avg,
    ROUND(
        (ds.daily_sales - LAG(ds.daily_sales, 1) OVER (
            PARTITION BY r.region_name, p.product_category 
            ORDER BY ds.date
        )) * 100.0 / LAG(ds.daily_sales, 1) OVER (
            PARTITION BY r.region_name, p.product_category 
            ORDER BY ds.date
        ), 2
    ) as vs_previous_day_pct
FROM daily_sales ds
INNER JOIN regions r ON ds.region_id = r.region_id
INNER JOIN products p ON ds.product_id = p.product_id
ORDER BY ds.date DESC, r.region_name, p.product_category;
```

---

### Solution 8.2: Customer Cohort Analysis
```sql
-- Problem: Analyze customer retention and cohort performance
-- Approach: Use window functions and self-joins for cohort analysis

WITH customer_cohorts AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) as cohort_month,
        DATE_TRUNC('month', order_date) as order_month
    FROM orders
    GROUP BY customer_id, DATE_TRUNC('month', order_date)
),
cohort_analysis AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) as customer_count,
        COUNT(DISTINCT CASE WHEN order_month = cohort_month THEN customer_id END) as month_0_customers,
        COUNT(DISTINCT CASE WHEN order_month = DATE_ADD(cohort_month, INTERVAL 1 MONTH) THEN customer_id END) as month_1_customers,
        COUNT(DISTINCT CASE WHEN order_month = DATE_ADD(cohort_month, INTERVAL 2 MONTH) THEN customer_id END) as month_2_customers,
        COUNT(DISTINCT CASE WHEN order_month = DATE_ADD(cohort_month, INTERVAL 3 MONTH) THEN customer_id END) as month_3_customers
    FROM customer_cohorts
    GROUP BY cohort_month
)
SELECT 
    cohort_month,
    customer_count,
    ROUND(month_1_customers * 100.0 / month_0_customers, 2) as month_1_retention,
    ROUND(month_2_customers * 100.0 / month_0_customers, 2) as month_2_retention,
    ROUND(month_3_customers * 100.0 / month_0_customers, 2) as month_3_retention
FROM cohort_analysis
ORDER BY cohort_month;
```

---

## 🎯 Key Takeaways

### JOIN Selection Guide:
- **INNER JOIN**: When you need exact matches from both tables
- **LEFT JOIN**: When you want to preserve all records from the main table
- **RIGHT JOIN**: When you want to preserve all records from the secondary table
- **FULL OUTER JOIN**: When you need complete data reconciliation
- **CROSS JOIN**: When you need all possible combinations (use carefully!)
- **SELF JOIN**: When you need to compare records within the same table

### Performance Best Practices:
1. Start with the smallest/filtered table
2. Use appropriate indexes on JOIN columns
3. Filter early in the query
4. Use INNER JOIN when you don't need NULLs
5. Consider query execution plans for large datasets

### Data Quality Patterns:
1. Use FULL OUTER JOIN for complete reconciliation
2. Use LEFT JOIN to find missing relationships
3. Use SELF JOIN to find duplicates
4. Always validate results with counts
5. Handle NULL values appropriately with COALESCE

**Master these patterns and you'll be ready for any JOIN challenge!** 🚀


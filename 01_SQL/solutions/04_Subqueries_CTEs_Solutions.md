# SQL Subqueries & CTEs - Exercise Solutions

## 🎯 Solution Guidelines

- **Approach**: Start with the business requirement, then choose the right subquery/CTE type
- **Readability**: Use CTEs to break complex logic into manageable steps
- **Performance**: Consider when to use JOINs instead of subqueries
- **Best Practices**: Follow professional SQL standards

---

## 📚 Exercise 1: Basic Subqueries

### Solution 1.1: Customer Analysis with Scalar Subqueries
```sql
-- Problem: Create a customer analysis report using scalar subqueries
-- Approach: Use scalar subqueries in SELECT clause for simple calculations

SELECT 
    c.customer_id,
    c.customer_name,
    (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) as order_count,
    (SELECT COALESCE(SUM(order_amount), 0) FROM orders o WHERE o.customer_id = c.customer_id) as total_spent,
    (SELECT COALESCE(AVG(order_amount), 0) FROM orders o WHERE o.customer_id = c.customer_id) as avg_order_value,
    (SELECT MAX(order_date) FROM orders o WHERE o.customer_id = c.customer_id) as last_order_date
FROM customers c
ORDER BY total_spent DESC;
```

**Key Points**:
- Scalar subqueries return exactly one value
- Use `COALESCE` to handle NULL values
- Each subquery is executed for every row in the main query

---

### Solution 1.2: Product Performance Analysis
```sql
-- Problem: Analyze product performance using subqueries to find products with above-average sales
-- Approach: Use subqueries to calculate averages and compare

SELECT 
    p.product_id,
    p.product_name,
    (SELECT COALESCE(SUM(oi.quantity), 0) FROM order_items oi WHERE oi.product_id = p.product_id) as total_quantity,
    (SELECT COALESCE(SUM(oi.quantity * oi.unit_price), 0) FROM order_items oi WHERE oi.product_id = p.product_id) as total_revenue,
    (SELECT COALESCE(AVG(oi.quantity * oi.unit_price), 0) FROM order_items oi WHERE oi.product_id = p.product_id) as avg_order_value,
    CASE 
        WHEN (SELECT COALESCE(SUM(oi.quantity * oi.unit_price), 0) FROM order_items oi WHERE oi.product_id = p.product_id) > 
             (SELECT AVG(total_revenue) FROM (
                 SELECT SUM(oi.quantity * oi.unit_price) as total_revenue 
                 FROM order_items oi 
                 GROUP BY oi.product_id
             ) as product_revenues)
        THEN 'Above Average'
        ELSE 'Below Average'
    END as performance_status
FROM products p
ORDER BY total_revenue DESC;
```

---

## 🔥 Exercise 2: Column and Row Subqueries

### Solution 2.1: Customer Product History
```sql
-- Problem: Find customers and their product purchase history using column subqueries
-- Approach: Use column subqueries with GROUP_CONCAT for multiple values

SELECT 
    c.customer_id,
    c.customer_name,
    (SELECT GROUP_CONCAT(DISTINCT p.product_name ORDER BY p.product_name) 
     FROM orders o
     INNER JOIN order_items oi ON o.order_id = oi.order_id
     INNER JOIN products p ON oi.product_id = p.product_id
     WHERE o.customer_id = c.customer_id
    ) as products_purchased,
    (SELECT COUNT(DISTINCT p.product_id) 
     FROM orders o
     INNER JOIN order_items oi ON o.order_id = oi.order_id
     INNER JOIN products p ON oi.product_id = p.product_id
     WHERE o.customer_id = c.customer_id
    ) as total_products
FROM customers c
ORDER BY total_products DESC;
```

**Key Points**:
- Column subqueries return multiple values in a single column
- Use `GROUP_CONCAT` to combine multiple values into a string
- Use `DISTINCT` to avoid duplicates

---

### Solution 2.2: Order Details Analysis
```sql
-- Problem: Analyze order details using row subqueries to get first and last order information
-- Approach: Use row subqueries to get multiple columns from a single row

SELECT 
    c.customer_id,
    c.customer_name,
    (SELECT order_date FROM orders 
     WHERE customer_id = c.customer_id 
     ORDER BY order_date ASC LIMIT 1
    ) as first_order_date,
    (SELECT order_amount FROM orders 
     WHERE customer_id = c.customer_id 
     ORDER BY order_date ASC LIMIT 1
    ) as first_order_amount,
    (SELECT order_date FROM orders 
     WHERE customer_id = c.customer_id 
     ORDER BY order_date DESC LIMIT 1
    ) as last_order_date,
    (SELECT order_amount FROM orders 
     WHERE customer_id = c.customer_id 
     ORDER BY order_date DESC LIMIT 1
    ) as last_order_amount
FROM customers c
WHERE (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) > 0
ORDER BY c.customer_id;
```

---

## 🎯 Exercise 3: Table Subqueries

### Solution 3.1: Customer Segmentation Analysis
```sql
-- Problem: Create a customer segmentation analysis using table subqueries
-- Approach: Use table subqueries to create intermediate results

SELECT 
    customer_segment,
    COUNT(*) as customer_count,
    ROUND(AVG(total_spent), 2) as avg_total_spent,
    ROUND(AVG(order_count), 1) as avg_order_count,
    SUM(total_spent) as total_revenue
FROM (
    SELECT 
        c.customer_id,
        c.customer_segment,
        COUNT(o.order_id) as order_count,
        COALESCE(SUM(o.order_amount), 0) as total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_segment
) as customer_summary
GROUP BY customer_segment
ORDER BY total_revenue DESC;
```

**Key Points**:
- Table subqueries return complete table result sets
- Use table subqueries to create intermediate results
- Group by the calculated segments

---

### Solution 3.2: Product Category Performance
```sql
-- Problem: Analyze product category performance using table subqueries
-- Approach: Use table subqueries to aggregate data by category

SELECT 
    cat.category_name,
    COUNT(DISTINCT p.product_id) as total_products,
    SUM(oi.quantity) as total_quantity_sold,
    SUM(oi.quantity * oi.unit_price) as total_revenue,
    AVG(p.unit_price) as avg_product_price
FROM (
    SELECT 
        p.product_id,
        p.product_name,
        p.category_id,
        p.unit_price,
        SUM(oi.quantity) as total_quantity,
        SUM(oi.quantity * oi.unit_price) as total_revenue
    FROM products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.product_name, p.category_id, p.unit_price
) as product_summary p
INNER JOIN categories cat ON p.category_id = cat.category_id
GROUP BY cat.category_name
ORDER BY total_revenue DESC;
```

---

## 🔧 Exercise 4: Basic CTEs

### Solution 4.1: Customer Lifetime Value Analysis
```sql
-- Problem: Calculate customer lifetime value using CTEs for readable, step-by-step analysis
-- Approach: Use multiple CTEs to break down the calculation

WITH customer_orders AS (
    SELECT 
        customer_id,
        COUNT(*) as total_orders,
        SUM(order_amount) as total_spent,
        AVG(order_amount) as avg_order_value,
        MIN(order_date) as first_order_date,
        MAX(order_date) as last_order_date
    FROM orders
    GROUP BY customer_id
),
customer_lifetime AS (
    SELECT 
        co.*,
        JULIANDAY(co.last_order_date) - JULIANDAY(co.first_order_date) as customer_lifetime_days
    FROM customer_orders co
)
SELECT 
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    cl.total_orders,
    cl.total_spent,
    cl.avg_order_value,
    cl.customer_lifetime_days
FROM customers c
LEFT JOIN customer_lifetime cl ON c.customer_id = cl.customer_id
ORDER BY cl.total_spent DESC;
```

**Key Points**:
- CTEs make complex queries readable
- Break down calculations into logical steps
- Use meaningful names for CTEs

---

### Solution 4.2: Data Quality Assessment
```sql
-- Problem: Create a data quality assessment using CTEs to identify data issues
-- Approach: Use CTEs to build data quality checks step by step

WITH customer_data_checks AS (
    SELECT 
        'Customers with Valid Emails' as quality_check,
        COUNT(*) as total_records,
        COUNT(CASE WHEN email IS NOT NULL AND email LIKE '%@%' THEN 1 END) as valid_records,
        COUNT(CASE WHEN email IS NULL OR email NOT LIKE '%@%' THEN 1 END) as invalid_records
    FROM customers
    
    UNION ALL
    
    SELECT 
        'Customers with Valid Names' as quality_check,
        COUNT(*) as total_records,
        COUNT(CASE WHEN customer_name IS NOT NULL AND customer_name != '' THEN 1 END) as valid_records,
        COUNT(CASE WHEN customer_name IS NULL OR customer_name = '' THEN 1 END) as invalid_records
    FROM customers
    
    UNION ALL
    
    SELECT 
        'Customers with Orders' as quality_check,
        COUNT(*) as total_records,
        COUNT(CASE WHEN customer_id IN (SELECT DISTINCT customer_id FROM orders) THEN 1 END) as valid_records,
        COUNT(CASE WHEN customer_id NOT IN (SELECT DISTINCT customer_id FROM orders) THEN 1 END) as invalid_records
    FROM customers
),
quality_metrics AS (
    SELECT 
        quality_check,
        total_records,
        valid_records,
        invalid_records,
        ROUND(invalid_records * 100.0 / total_records, 2) as error_rate_pct
    FROM customer_data_checks
)
SELECT 
    quality_check,
    total_records,
    valid_records,
    invalid_records,
    error_rate_pct
FROM quality_metrics
ORDER BY error_rate_pct DESC;
```

---

## 🚀 Exercise 5: Advanced CTEs

### Solution 5.1: ETL Data Pipeline
```sql
-- Problem: Build an ETL pipeline using CTEs to transform raw customer data
-- Approach: Use multiple CTEs for each step of the ETL process

WITH raw_data AS (
    -- Step 1: Extract raw data
    SELECT 
        customer_id,
        customer_name,
        email,
        phone,
        registration_date
    FROM raw_customer_data
    WHERE registration_date >= '2023-01-01'
),
data_cleansing AS (
    -- Step 2: Clean and standardize data
    SELECT 
        customer_id,
        TRIM(UPPER(customer_name)) as customer_name,
        LOWER(TRIM(email)) as email,
        REPLACE(REPLACE(REPLACE(phone, '(', ''), ')', ''), '-', '') as phone,
        registration_date,
        CASE 
            WHEN email LIKE '%@%' AND email LIKE '%.%' THEN 'Valid'
            ELSE 'Invalid'
        END as email_status
    FROM raw_data
),
data_enrichment AS (
    -- Step 3: Enrich with additional data
    SELECT 
        dc.*,
        COALESCE(cs.customer_segment, 'Unknown') as customer_segment,
        COALESCE(r.region_name, 'Unknown') as region_name
    FROM data_cleansing dc
    LEFT JOIN customer_segments cs ON dc.customer_id = cs.customer_id
    LEFT JOIN regions r ON dc.customer_id = r.customer_id
),
data_quality AS (
    -- Step 4: Calculate data quality scores
    SELECT 
        *,
        CASE 
            WHEN email_status = 'Valid' AND LENGTH(phone) = 10 THEN 'High Quality'
            WHEN email_status = 'Valid' OR LENGTH(phone) = 10 THEN 'Medium Quality'
            ELSE 'Low Quality'
        END as data_quality_score
    FROM data_enrichment
)
-- Step 5: Final output
SELECT 
    customer_id,
    customer_name,
    email,
    phone,
    customer_segment,
    region_name,
    data_quality_score
FROM data_quality
WHERE data_quality_score IN ('High Quality', 'Medium Quality')
ORDER BY data_quality_score DESC, registration_date DESC;
```

---

### Solution 5.2: Complex Business Analytics
```sql
-- Problem: Create a comprehensive business analytics report using advanced CTEs
-- Approach: Use multiple CTEs to build complex analytics step by step

WITH customer_metrics AS (
    SELECT 
        c.customer_id,
        c.customer_segment,
        COUNT(o.order_id) as total_orders,
        SUM(o.order_amount) as total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_segment
),
category_metrics AS (
    SELECT 
        cat.category_name,
        COUNT(DISTINCT p.product_id) as total_products,
        SUM(oi.quantity) as total_quantity_sold
    FROM categories cat
    LEFT JOIN products p ON cat.category_id = p.category_id
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY cat.category_name
),
customer_category_analysis AS (
    SELECT 
        c.customer_segment,
        cat.category_name,
        COUNT(DISTINCT c.customer_id) as total_customers,
        COUNT(o.order_id) as total_orders,
        SUM(oi.quantity * oi.unit_price) as total_revenue,
        AVG(oi.quantity * oi.unit_price) as avg_order_value
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    LEFT JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN categories cat ON p.category_id = cat.category_id
    GROUP BY c.customer_segment, cat.category_name
)
SELECT 
    customer_segment,
    category_name,
    total_customers,
    total_orders,
    total_revenue,
    avg_order_value
FROM customer_category_analysis
ORDER BY total_revenue DESC;
```

---

## 🎯 Exercise 6: Recursive CTEs

### Solution 6.1: Employee Hierarchy
```sql
-- Problem: Build a complete employee hierarchy using recursive CTEs
-- Approach: Use recursive CTEs to build hierarchical data

WITH RECURSIVE employee_hierarchy AS (
    -- Base case: top-level employees (no manager)
    SELECT 
        employee_id,
        employee_name,
        manager_id,
        employee_name as hierarchy_path,
        1 as hierarchy_level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case: subordinates
    SELECT 
        e.employee_id,
        e.employee_name,
        e.manager_id,
        eh.hierarchy_path || ' -> ' || e.employee_name as hierarchy_path,
        eh.hierarchy_level + 1 as hierarchy_level
    FROM employees e
    INNER JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
)
SELECT 
    employee_id,
    employee_name,
    manager_id,
    (SELECT employee_name FROM employees WHERE employee_id = eh.manager_id) as manager_name,
    hierarchy_level,
    hierarchy_path
FROM employee_hierarchy eh
ORDER BY hierarchy_level, employee_name;
```

**Key Points**:
- Recursive CTEs use `WITH RECURSIVE`
- Base case defines the starting point
- Recursive case builds the hierarchy
- Use `UNION ALL` to combine results

---

### Solution 6.2: Product Category Hierarchy
```sql
-- Problem: Build a product category hierarchy using recursive CTEs
-- Approach: Use recursive CTEs to build category hierarchies

WITH RECURSIVE category_hierarchy AS (
    -- Base case: root categories
    SELECT 
        category_id,
        category_name,
        parent_category_id,
        category_name as full_path,
        1 as hierarchy_level
    FROM product_categories
    WHERE parent_category_id IS NULL
    
    UNION ALL
    
    -- Recursive case: subcategories
    SELECT 
        pc.category_id,
        pc.category_name,
        pc.parent_category_id,
        ch.full_path || ' > ' || pc.category_name as full_path,
        ch.hierarchy_level + 1 as hierarchy_level
    FROM product_categories pc
    INNER JOIN category_hierarchy ch ON pc.parent_category_id = ch.category_id
)
SELECT 
    category_id,
    category_name,
    parent_category_id,
    hierarchy_level,
    full_path
FROM category_hierarchy
ORDER BY hierarchy_level, category_name;
```

---

## 🔥 Exercise 7: Performance Optimization

### Solution 7.1: Optimize Correlated Subqueries
```sql
-- Problem: Rewrite correlated subqueries using JOINs for better performance
-- Approach: Convert to JOINs with GROUP BY

-- Original (inefficient):
-- SELECT 
--     customer_id,
--     customer_name,
--     (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count,
--     (SELECT SUM(order_amount) FROM orders WHERE customer_id = c.customer_id) as total_spent
-- FROM customers c;

-- Optimized solution:
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) as order_count,
    COALESCE(SUM(o.order_amount), 0) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spent DESC;
```

**Performance Benefits**:
- Single table scan instead of multiple subqueries
- Better query execution plan
- Reduced I/O operations

---

### Solution 7.2: Optimize Multiple Subqueries
```sql
-- Problem: Optimize multiple subqueries using CTEs or JOINs
-- Approach: Use CTEs to combine the logic

-- Original (inefficient):
-- SELECT 
--     customer_id,
--     (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count,
--     (SELECT SUM(order_amount) FROM orders WHERE customer_id = c.customer_id) as total_spent,
--     (SELECT COUNT(DISTINCT product_id) FROM order_items oi 
--      INNER JOIN orders o ON oi.order_id = o.order_id 
--      WHERE o.customer_id = c.customer_id) as unique_products
-- FROM customers c;

-- Optimized solution:
WITH customer_metrics AS (
    SELECT 
        c.customer_id,
        COUNT(o.order_id) as order_count,
        COALESCE(SUM(o.order_amount), 0) as total_spent,
        COUNT(DISTINCT oi.product_id) as unique_products
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_id
)
SELECT 
    customer_id,
    order_count,
    total_spent,
    unique_products
FROM customer_metrics
ORDER BY total_spent DESC;
```

---

## 🎯 Exercise 8: Real-World Scenarios

### Solution 8.1: Customer Churn Analysis
```sql
-- Problem: Analyze customer churn using CTEs to identify at-risk customers
-- Approach: Use CTEs to calculate time-based metrics

WITH customer_orders AS (
    SELECT 
        customer_id,
        MAX(order_date) as last_order_date,
        COUNT(*) as total_orders
    FROM orders
    GROUP BY customer_id
),
churn_analysis AS (
    SELECT 
        co.customer_id,
        c.customer_name,
        co.last_order_date,
        co.total_orders,
        JULIANDAY(CURRENT_DATE) - JULIANDAY(co.last_order_date) as days_since_last_order,
        CASE 
            WHEN JULIANDAY(CURRENT_DATE) - JULIANDAY(co.last_order_date) > 90 THEN 'Critical'
            WHEN JULIANDAY(CURRENT_DATE) - JULIANDAY(co.last_order_date) > 60 THEN 'High'
            WHEN JULIANDAY(CURRENT_DATE) - JULIANDAY(co.last_order_date) > 30 THEN 'Medium'
            ELSE 'Low'
        END as churn_risk
    FROM customer_orders co
    INNER JOIN customers c ON co.customer_id = c.customer_id
)
SELECT 
    customer_id,
    customer_name,
    last_order_date,
    days_since_last_order,
    churn_risk
FROM churn_analysis
ORDER BY days_since_last_order DESC;
```

---

### Solution 8.2: Product Recommendation Engine
```sql
-- Problem: Build a product recommendation engine using CTEs
-- Approach: Use CTEs to analyze customer behavior and product popularity

WITH customer_products AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        GROUP_CONCAT(DISTINCT p.product_name) as products_ordered
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    LEFT JOIN products p ON oi.product_id = p.product_id
    GROUP BY c.customer_id, c.customer_name
),
product_popularity AS (
    SELECT 
        p.product_name,
        COUNT(DISTINCT o.customer_id) as customer_count,
        SUM(oi.quantity) as total_quantity
    FROM products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    LEFT JOIN orders o ON oi.order_id = o.order_id
    GROUP BY p.product_name
),
recommendations AS (
    SELECT 
        cp.customer_id,
        cp.customer_name,
        pp.product_name,
        pp.customer_count,
        CASE 
            WHEN cp.products_ordered IS NULL THEN 'Popular Products'
            WHEN cp.products_ordered NOT LIKE '%' || pp.product_name || '%' THEN 'Similar Products'
            ELSE 'Already Ordered'
        END as recommendation_reason
    FROM customer_products cp
    CROSS JOIN product_popularity pp
    WHERE cp.products_ordered NOT LIKE '%' || pp.product_name || '%'
       OR cp.products_ordered IS NULL
)
SELECT 
    customer_id,
    customer_name,
    GROUP_CONCAT(product_name) as recommended_products,
    recommendation_reason
FROM recommendations
WHERE recommendation_reason != 'Already Ordered'
GROUP BY customer_id, customer_name, recommendation_reason
ORDER BY customer_id;
```

---

## 💡 Exercise 9: Advanced Patterns

### Solution 9.1: Time-Series Analysis with CTEs
```sql
-- Problem: Analyze sales trends using CTEs for time-series analysis
-- Approach: Use CTEs to calculate moving averages and trends

WITH daily_sales_data AS (
    SELECT 
        ds.date,
        r.region_name,
        p.product_category,
        ds.daily_sales
    FROM daily_sales ds
    INNER JOIN regions r ON ds.region_id = r.region_id
    INNER JOIN products p ON ds.product_id = p.product_id
),
sales_with_metrics AS (
    SELECT 
        *,
        AVG(daily_sales) OVER (
            PARTITION BY region_name, product_category 
            ORDER BY date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as seven_day_avg,
        AVG(daily_sales) OVER (
            PARTITION BY region_name, product_category 
            ORDER BY date 
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) as thirty_day_avg,
        LAG(daily_sales, 1) OVER (
            PARTITION BY region_name, product_category 
            ORDER BY date
        ) as previous_day_sales
    FROM daily_sales_data
)
SELECT 
    date,
    region_name,
    product_category,
    daily_sales,
    ROUND(seven_day_avg, 2) as seven_day_avg,
    ROUND(thirty_day_avg, 2) as thirty_day_avg,
    CASE 
        WHEN daily_sales > previous_day_sales THEN 'Up'
        WHEN daily_sales < previous_day_sales THEN 'Down'
        ELSE 'Same'
    END as trend
FROM sales_with_metrics
ORDER BY date DESC, region_name, product_category;
```

---

### Solution 9.2: Cohort Analysis
```sql
-- Problem: Perform cohort analysis using CTEs to analyze customer retention
-- Approach: Use CTEs to build cohort analysis step by step

WITH customer_cohorts AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) as cohort_month,
        DATE_TRUNC('month', order_date) as order_month
    FROM orders
    GROUP BY customer_id, DATE_TRUNC('month', order_date)
),
cohort_retention AS (
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
FROM cohort_retention
ORDER BY cohort_month;
```

---

## 🎯 Key Takeaways

### Subquery Selection Guide:
- **Scalar Subqueries**: When you need one value per main query row
- **Column Subqueries**: When you need multiple values in a single column
- **Row Subqueries**: When you need multiple columns from a single row
- **Table Subqueries**: When you need complete table result sets

### CTE Best Practices:
1. Use CTEs for readability and maintainability
2. Break complex logic into logical steps
3. Use meaningful names for CTEs
4. Test each CTE step by step
5. Consider performance implications

### Performance Optimization:
1. Use JOINs instead of correlated subqueries when possible
2. Use CTEs to combine multiple subqueries
3. Consider window functions for complex calculations
4. Test with sample data first
5. Monitor query execution plans

### Recursive CTEs:
1. Use `WITH RECURSIVE` for hierarchical data
2. Define base case and recursive case clearly
3. Use `UNION ALL` to combine results
4. Be careful with infinite recursion
5. Test with small datasets first

**Master these patterns and you'll be ready for any subquery/CTE challenge!** 🚀

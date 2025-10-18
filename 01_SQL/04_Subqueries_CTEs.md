# SQL Subqueries & CTEs - Complex Data Transformations

## 🎯 Learning Objectives

By the end of this module, you will be able to:
- **Master all subquery types** (scalar, column, row, table)
- **Use CTEs effectively** for readable complex queries
- **Implement recursive CTEs** for hierarchical data
- **Solve complex data transformation** problems
- **Optimize subquery performance** vs JOINs
- **Build multi-step data pipelines** with CTEs
- **Handle complex business logic** in SQL

---

## 🔥 Why Subqueries & CTEs Matter for Data Engineering

Subqueries and CTEs are **essential for complex data transformations**:

1. **Data Pipeline Logic**: Multi-step transformations
2. **Complex Business Rules**: Nested calculations and conditions
3. **Data Quality**: Validation and cleansing workflows
4. **Analytics**: Advanced calculations and aggregations
5. **ETL Processes**: Transform data in logical steps
6. **Readability**: Break complex queries into manageable pieces

**EPAM will test your ability to solve complex problems with nested logic. Master this = you're ready for senior data engineering challenges.**

---

## 📚 Subquery Types - Complete Reference

### Visual Subquery Types Overview

```
Scalar Subquery:    Returns single value (1 row, 1 column)
Column Subquery:    Returns single column (multiple rows, 1 column)
Row Subquery:       Returns single row (1 row, multiple columns)
Table Subquery:     Returns table (multiple rows, multiple columns)
```

---

## 🔥 Core Subquery Types - Deep Dive

### 1. Scalar Subqueries - Single Value Returns

**Purpose**: Returns exactly one value (1 row, 1 column)

```sql
-- Basic scalar subquery
SELECT 
    customer_id,
    customer_name,
    (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count
FROM customers c;
```

**Real-World Example**: Customer Analysis with Subqueries
```sql
-- Customer analysis with multiple scalar subqueries
SELECT 
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    
    -- Total orders
    (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) as total_orders,
    
    -- Total spent
    (SELECT COALESCE(SUM(order_amount), 0) FROM orders o WHERE o.customer_id = c.customer_id) as total_spent,
    
    -- Average order value
    (SELECT COALESCE(AVG(order_amount), 0) FROM orders o WHERE o.customer_id = c.customer_id) as avg_order_value,
    
    -- Last order date
    (SELECT MAX(order_date) FROM orders o WHERE o.customer_id = c.customer_id) as last_order_date,
    
    -- Customer status
    CASE 
        WHEN (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) = 0 THEN 'No Orders'
        WHEN (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) = 1 THEN 'Single Order'
        WHEN (SELECT COALESCE(SUM(order_amount), 0) FROM orders o WHERE o.customer_id = c.customer_id) > 1000 THEN 'High Value'
        ELSE 'Standard Customer'
    END as customer_status
FROM customers c
ORDER BY total_spent DESC;
```

**When to Use Scalar Subqueries**:
- Simple calculations per row
- When you need one value per main query row
- When the subquery is not too complex
- For readability in simple cases

---

### 2. Column Subqueries - Multiple Values in SELECT

**Purpose**: Returns multiple values in a single column

```sql
-- Basic column subquery
SELECT 
    customer_id,
    customer_name,
    (SELECT product_name FROM products WHERE product_id IN (
        SELECT product_id FROM order_items WHERE order_id IN (
            SELECT order_id FROM orders WHERE customer_id = c.customer_id
        )
    )) as products_ordered
FROM customers c;
```

**Real-World Example**: Product Recommendations
```sql
-- Find customers who bought products similar to a specific product
SELECT 
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    -- Products this customer has ordered
    (SELECT GROUP_CONCAT(p.product_name) 
     FROM orders o
     INNER JOIN order_items oi ON o.order_id = oi.order_id
     INNER JOIN products p ON oi.product_id = p.product_id
     WHERE o.customer_id = c.customer_id
    ) as products_ordered,
    -- Similar customers (customers who bought the same products)
    (SELECT COUNT(DISTINCT o2.customer_id)
     FROM orders o1
     INNER JOIN order_items oi1 ON o1.order_id = oi1.order_id
     INNER JOIN order_items oi2 ON oi1.product_id = oi2.product_id
     INNER JOIN orders o2 ON oi2.order_id = o2.order_id
     WHERE o1.customer_id = c.customer_id
       AND o2.customer_id != c.customer_id
    ) as similar_customers_count
FROM customers c
WHERE (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) > 0
ORDER BY similar_customers_count DESC;
```

---

### 3. Row Subqueries - Multiple Columns, Single Row

**Purpose**: Returns multiple columns from a single row

```sql
-- Basic row subquery
SELECT 
    customer_id,
    customer_name,
    (SELECT order_date, order_amount 
     FROM orders 
     WHERE customer_id = c.customer_id 
     ORDER BY order_date DESC 
     LIMIT 1
    ) as last_order_info
FROM customers c;
```

**Real-World Example**: Customer Lifetime Analysis
```sql
-- Analyze customer lifetime with first and last order details
SELECT 
    c.customer_id,
    c.customer_name,
    c.registration_date,
    
    -- First order details
    (SELECT order_date FROM orders 
     WHERE customer_id = c.customer_id 
     ORDER BY order_date ASC LIMIT 1
    ) as first_order_date,
    
    (SELECT order_amount FROM orders 
     WHERE customer_id = c.customer_id 
     ORDER BY order_date ASC LIMIT 1
    ) as first_order_amount,
    
    -- Last order details
    (SELECT order_date FROM orders 
     WHERE customer_id = c.customer_id 
     ORDER BY order_date DESC LIMIT 1
    ) as last_order_date,
    
    (SELECT order_amount FROM orders 
     WHERE customer_id = c.customer_id 
     ORDER BY order_date DESC LIMIT 1
    ) as last_order_amount,
    
    -- Customer lifetime metrics
    JULIANDAY((SELECT MAX(order_date) FROM orders WHERE customer_id = c.customer_id)) - 
    JULIANDAY((SELECT MIN(order_date) FROM orders WHERE customer_id = c.customer_id)) as customer_lifetime_days
FROM customers c
WHERE (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) > 0
ORDER BY customer_lifetime_days DESC;
```

---

### 4. Table Subqueries - Multiple Rows and Columns

**Purpose**: Returns a complete table result set

```sql
-- Basic table subquery
SELECT 
    customer_id,
    customer_name,
    total_orders,
    total_spent
FROM (
    SELECT 
        c.customer_id,
        c.customer_name,
        COUNT(o.order_id) as total_orders,
        SUM(o.order_amount) as total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
) as customer_summary
WHERE total_spent > 1000
ORDER BY total_spent DESC;
```

**Real-World Example**: Complex Data Analysis
```sql
-- Multi-step customer analysis using table subqueries
SELECT 
    customer_segment,
    COUNT(*) as customer_count,
    AVG(total_spent) as avg_spent,
    AVG(total_orders) as avg_orders,
    AVG(customer_lifetime_days) as avg_lifetime_days
FROM (
    SELECT 
        c.customer_segment,
        c.customer_id,
        COUNT(o.order_id) as total_orders,
        COALESCE(SUM(o.order_amount), 0) as total_spent,
        JULIANDAY(COALESCE(MAX(o.order_date), c.registration_date)) - 
        JULIANDAY(c.registration_date) as customer_lifetime_days
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_segment, c.customer_id
) as customer_metrics
GROUP BY customer_segment
ORDER BY avg_spent DESC;
```

---

## 🎯 Common Table Expressions (CTEs) - The Game Changer

**CTEs make complex queries readable and maintainable by breaking them into logical steps.**

### Basic CTE Syntax
```sql
WITH cte_name AS (
    SELECT ...
),
another_cte AS (
    SELECT ...
)
SELECT ...
FROM cte_name
JOIN another_cte ON ...
```

### Real-World Example: ETL Data Pipeline
```sql
-- ETL pipeline using CTEs for data transformation
WITH raw_data AS (
    -- Step 1: Extract and clean raw data
    SELECT 
        customer_id,
        TRIM(UPPER(customer_name)) as customer_name,
        LOWER(TRIM(email)) as email,
        CASE 
            WHEN phone LIKE '%(%' THEN REPLACE(REPLACE(REPLACE(phone, '(', ''), ')', ''), '-', '')
            ELSE phone
        END as clean_phone,
        registration_date,
        'RAW' as data_source
    FROM raw_customer_data
    WHERE registration_date >= '2023-01-01'
),

validated_data AS (
    -- Step 2: Validate and enrich data
    SELECT 
        customer_id,
        customer_name,
        email,
        clean_phone,
        registration_date,
        CASE 
            WHEN email LIKE '%@%' AND email LIKE '%.%' THEN 'Valid Email'
            ELSE 'Invalid Email'
        END as email_status,
        CASE 
            WHEN LENGTH(clean_phone) = 10 THEN 'Valid Phone'
            ELSE 'Invalid Phone'
        END as phone_status,
        data_source
    FROM raw_data
),

enriched_data AS (
    -- Step 3: Enrich with additional data
    SELECT 
        vd.*,
        COALESCE(cs.customer_segment, 'Unknown') as customer_segment,
        COALESCE(r.region_name, 'Unknown') as region_name,
        CASE 
            WHEN vd.email_status = 'Valid Email' AND vd.phone_status = 'Valid Phone' THEN 'High Quality'
            WHEN vd.email_status = 'Valid Email' OR vd.phone_status = 'Valid Phone' THEN 'Medium Quality'
            ELSE 'Low Quality'
        END as data_quality_score
    FROM validated_data vd
    LEFT JOIN customer_segments cs ON vd.customer_id = cs.customer_id
    LEFT JOIN regions r ON vd.customer_id = r.customer_id
)

-- Step 4: Final output
SELECT 
    customer_id,
    customer_name,
    email,
    clean_phone,
    customer_segment,
    region_name,
    data_quality_score,
    registration_date
FROM enriched_data
WHERE data_quality_score IN ('High Quality', 'Medium Quality')
ORDER BY data_quality_score DESC, registration_date DESC;
```

---

## 🔧 Advanced CTE Patterns

### 1. Multiple CTEs for Complex Logic
```sql
-- Complex business analysis using multiple CTEs
WITH customer_orders AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(order_amount) as total_spent,
        AVG(order_amount) as avg_order_value,
        MIN(order_date) as first_order_date,
        MAX(order_date) as last_order_date
    FROM orders
    GROUP BY customer_id
),

customer_segments AS (
    SELECT 
        customer_id,
        CASE 
            WHEN total_spent > 5000 THEN 'VIP'
            WHEN total_spent > 2000 THEN 'Premium'
            WHEN total_spent > 500 THEN 'Standard'
            ELSE 'Basic'
        END as calculated_segment,
        total_spent,
        order_count
    FROM customer_orders
),

segment_analysis AS (
    SELECT 
        calculated_segment,
        COUNT(*) as customer_count,
        AVG(total_spent) as avg_spent,
        AVG(order_count) as avg_orders,
        SUM(total_spent) as total_revenue
    FROM customer_segments
    GROUP BY calculated_segment
)

SELECT 
    calculated_segment,
    customer_count,
    ROUND(avg_spent, 2) as avg_spent,
    ROUND(avg_orders, 1) as avg_orders,
    total_revenue,
    ROUND(total_revenue * 100.0 / SUM(total_revenue) OVER (), 2) as revenue_percentage
FROM segment_analysis
ORDER BY total_revenue DESC;
```

### 2. CTEs for Data Quality Analysis
```sql
-- Comprehensive data quality analysis
WITH data_quality_checks AS (
    SELECT 
        'customers' as table_name,
        COUNT(*) as total_records,
        COUNT(CASE WHEN customer_id IS NULL THEN 1 END) as null_ids,
        COUNT(CASE WHEN customer_name IS NULL OR customer_name = '' THEN 1 END) as null_names,
        COUNT(CASE WHEN email IS NULL OR email = '' THEN 1 END) as null_emails,
        COUNT(CASE WHEN email NOT LIKE '%@%' THEN 1 END) as invalid_emails,
        COUNT(DISTINCT customer_id) as unique_ids
    FROM customers
    
    UNION ALL
    
    SELECT 
        'orders' as table_name,
        COUNT(*) as total_records,
        COUNT(CASE WHEN order_id IS NULL THEN 1 END) as null_ids,
        COUNT(CASE WHEN customer_id IS NULL THEN 1 END) as null_customers,
        COUNT(CASE WHEN order_amount IS NULL THEN 1 END) as null_amounts,
        COUNT(CASE WHEN order_amount <= 0 THEN 1 END) as invalid_amounts,
        COUNT(DISTINCT order_id) as unique_ids
    FROM orders
),

quality_metrics AS (
    SELECT 
        table_name,
        total_records,
        null_ids,
        null_names,
        null_emails,
        invalid_emails,
        unique_ids,
        total_records - unique_ids as duplicate_records,
        ROUND((null_ids + null_names + null_emails + invalid_emails) * 100.0 / total_records, 2) as error_rate
    FROM data_quality_checks
)

SELECT 
    table_name,
    total_records,
    error_rate,
    CASE 
        WHEN error_rate > 10 THEN 'CRITICAL'
        WHEN error_rate > 5 THEN 'HIGH'
        WHEN error_rate > 1 THEN 'MEDIUM'
        ELSE 'LOW'
    END as quality_status
FROM quality_metrics
ORDER BY error_rate DESC;
```

---

## 🚀 Recursive CTEs - Hierarchical Data

**Recursive CTEs are powerful for handling hierarchical data structures.**

### Basic Recursive CTE Syntax
```sql
WITH RECURSIVE cte_name AS (
    -- Base case
    SELECT ...
    FROM table
    WHERE condition
    
    UNION ALL
    
    -- Recursive case
    SELECT ...
    FROM table
    INNER JOIN cte_name ON ...
    WHERE condition
)
SELECT * FROM cte_name;
```

### Real-World Example: Employee Hierarchy
```sql
-- Build complete employee hierarchy using recursive CTE
WITH RECURSIVE employee_hierarchy AS (
    -- Base case: top-level employees (no manager)
    SELECT 
        employee_id,
        employee_name,
        manager_id,
        employee_name as hierarchy_path,
        0 as level,
        employee_name as manager_chain
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case: subordinates
    SELECT 
        e.employee_id,
        e.employee_name,
        e.manager_id,
        eh.hierarchy_path || ' -> ' || e.employee_name as hierarchy_path,
        eh.level + 1 as level,
        eh.manager_chain || ' -> ' || e.employee_name as manager_chain
    FROM employees e
    INNER JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
)

SELECT 
    employee_id,
    employee_name,
    level,
    hierarchy_path,
    manager_chain
FROM employee_hierarchy
ORDER BY level, employee_name;
```

### Real-World Example: Product Categories
```sql
-- Build product category hierarchy
WITH RECURSIVE category_hierarchy AS (
    -- Base case: root categories
    SELECT 
        category_id,
        category_name,
        parent_category_id,
        category_name as full_path,
        0 as level
    FROM product_categories
    WHERE parent_category_id IS NULL
    
    UNION ALL
    
    -- Recursive case: subcategories
    SELECT 
        pc.category_id,
        pc.category_name,
        pc.parent_category_id,
        ch.full_path || ' > ' || pc.category_name as full_path,
        ch.level + 1 as level
    FROM product_categories pc
    INNER JOIN category_hierarchy ch ON pc.parent_category_id = ch.category_id
)

SELECT 
    category_id,
    category_name,
    level,
    full_path
FROM category_hierarchy
ORDER BY level, category_name;
```

---

## 🎯 Subqueries vs JOINs - Performance Guide

### When to Use Subqueries vs JOINs

#### Use Subqueries When:
- Simple calculations per row
- When you need one value per main query row
- For readability in simple cases
- When the subquery is not too complex

#### Use JOINs When:
- Complex relationships
- Large datasets
- Performance is critical
- Multiple columns from related tables

### Performance Comparison Examples

#### ❌ INEFFICIENT: Correlated Subquery
```sql
-- Slow: Correlated subquery
SELECT 
    c.customer_id,
    c.customer_name,
    (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) as order_count,
    (SELECT SUM(order_amount) FROM orders o WHERE o.customer_id = c.customer_id) as total_spent
FROM customers c;
```

#### ✅ EFFICIENT: JOIN with Aggregation
```sql
-- Fast: JOIN with aggregation
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) as order_count,
    COALESCE(SUM(o.order_amount), 0) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;
```

#### ❌ INEFFICIENT: Multiple Subqueries
```sql
-- Slow: Multiple subqueries
SELECT 
    customer_id,
    (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count,
    (SELECT AVG(order_amount) FROM orders WHERE customer_id = c.customer_id) as avg_order,
    (SELECT MAX(order_date) FROM orders WHERE customer_id = c.customer_id) as last_order
FROM customers c;
```

#### ✅ EFFICIENT: Single JOIN with Window Functions
```sql
-- Fast: Single JOIN with window functions
SELECT 
    c.customer_id,
    COUNT(o.order_id) as order_count,
    AVG(o.order_amount) as avg_order,
    MAX(o.order_date) as last_order
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;
```

---

## 🔥 Real-World Data Engineering Scenarios

### Scenario 1: Complex ETL Pipeline
```sql
-- Multi-step ETL pipeline for customer data processing
WITH raw_customer_data AS (
    -- Step 1: Extract raw data
    SELECT 
        customer_id,
        customer_name,
        email,
        phone,
        address,
        registration_date,
        source_system
    FROM raw_customer_table
    WHERE registration_date >= '2023-01-01'
),

data_cleansing AS (
    -- Step 2: Clean and standardize data
    SELECT 
        customer_id,
        TRIM(UPPER(customer_name)) as customer_name,
        LOWER(TRIM(email)) as email,
        REPLACE(REPLACE(REPLACE(phone, '(', ''), ')', ''), '-', '') as clean_phone,
        TRIM(UPPER(address)) as address,
        registration_date,
        source_system,
        CASE 
            WHEN email LIKE '%@%' AND email LIKE '%.%' THEN 'Valid'
            ELSE 'Invalid'
        END as email_status
    FROM raw_customer_data
),

data_enrichment AS (
    -- Step 3: Enrich with additional data
    SELECT 
        dc.*,
        COALESCE(seg.customer_segment, 'Unknown') as customer_segment,
        COALESCE(reg.region_name, 'Unknown') as region_name,
        CASE 
            WHEN dc.email_status = 'Valid' AND LENGTH(dc.clean_phone) = 10 THEN 'High Quality'
            WHEN dc.email_status = 'Valid' OR LENGTH(dc.clean_phone) = 10 THEN 'Medium Quality'
            ELSE 'Low Quality'
        END as data_quality_score
    FROM data_cleansing dc
    LEFT JOIN customer_segments seg ON dc.customer_id = seg.customer_id
    LEFT JOIN regions reg ON dc.customer_id = reg.customer_id
),

data_validation AS (
    -- Step 4: Validate and flag issues
    SELECT 
        *,
        CASE 
            WHEN customer_segment = 'Unknown' THEN 'Missing Segment'
            WHEN region_name = 'Unknown' THEN 'Missing Region'
            WHEN data_quality_score = 'Low Quality' THEN 'Poor Data Quality'
            ELSE 'Valid'
        END as validation_status
    FROM data_enrichment
)

-- Step 5: Final output with quality metrics
SELECT 
    customer_id,
    customer_name,
    email,
    clean_phone,
    customer_segment,
    region_name,
    data_quality_score,
    validation_status,
    registration_date,
    source_system
FROM data_validation
WHERE validation_status = 'Valid'
ORDER BY data_quality_score DESC, registration_date DESC;
```

### Scenario 2: Advanced Analytics with CTEs
```sql
-- Complex customer analytics using multiple CTEs
WITH customer_metrics AS (
    SELECT 
        customer_id,
        COUNT(*) as total_orders,
        SUM(order_amount) as total_spent,
        AVG(order_amount) as avg_order_value,
        MIN(order_date) as first_order_date,
        MAX(order_date) as last_order_date,
        COUNT(DISTINCT product_id) as unique_products
    FROM orders o
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY customer_id
),

customer_segmentation AS (
    SELECT 
        customer_id,
        total_orders,
        total_spent,
        avg_order_value,
        unique_products,
        JULIANDAY(last_order_date) - JULIANDAY(first_order_date) as customer_lifetime_days,
        CASE 
            WHEN total_spent > 5000 AND total_orders > 10 THEN 'VIP'
            WHEN total_spent > 2000 AND total_orders > 5 THEN 'Premium'
            WHEN total_spent > 500 THEN 'Standard'
            ELSE 'Basic'
        END as customer_segment
    FROM customer_metrics
),

segment_analysis AS (
    SELECT 
        customer_segment,
        COUNT(*) as customer_count,
        AVG(total_spent) as avg_spent,
        AVG(total_orders) as avg_orders,
        AVG(avg_order_value) as avg_order_value,
        AVG(customer_lifetime_days) as avg_lifetime_days,
        SUM(total_spent) as total_revenue
    FROM customer_segmentation
    GROUP BY customer_segment
),

customer_rankings AS (
    SELECT 
        cs.*,
        RANK() OVER (ORDER BY total_spent DESC) as spending_rank,
        RANK() OVER (ORDER BY total_orders DESC) as order_rank,
        RANK() OVER (ORDER BY customer_lifetime_days DESC) as lifetime_rank
    FROM customer_segmentation cs
)

SELECT 
    customer_segment,
    customer_count,
    ROUND(avg_spent, 2) as avg_spent,
    ROUND(avg_orders, 1) as avg_orders,
    ROUND(avg_order_value, 2) as avg_order_value,
    ROUND(avg_lifetime_days, 0) as avg_lifetime_days,
    total_revenue,
    ROUND(total_revenue * 100.0 / SUM(total_revenue) OVER (), 2) as revenue_percentage
FROM segment_analysis
ORDER BY total_revenue DESC;
```

---

## ⚠️ Common Mistakes and Solutions

### 1. Correlated Subquery Performance Issues
```sql
-- ❌ WRONG: Correlated subquery (slow)
SELECT 
    customer_id,
    customer_name,
    (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count
FROM customers c;

-- ✅ CORRECT: Use JOIN or window function
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;
```

### 2. Multiple Subqueries When One Would Do
```sql
-- ❌ WRONG: Multiple subqueries
SELECT 
    customer_id,
    (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count,
    (SELECT SUM(order_amount) FROM orders WHERE customer_id = c.customer_id) as total_spent
FROM customers c;

-- ✅ CORRECT: Single subquery or JOIN
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(order_amount) as total_spent
FROM orders
GROUP BY customer_id;
```

### 3. CTE Without Recursive When Needed
```sql
-- ❌ WRONG: Trying to use regular CTE for hierarchical data
WITH employee_hierarchy AS (
    SELECT employee_id, employee_name, manager_id
    FROM employees
    WHERE manager_id IS NULL
)
SELECT * FROM employee_hierarchy;  -- Only gets top level

-- ✅ CORRECT: Use recursive CTE
WITH RECURSIVE employee_hierarchy AS (
    SELECT employee_id, employee_name, manager_id, 0 as level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    SELECT e.employee_id, e.employee_name, e.manager_id, eh.level + 1
    FROM employees e
    INNER JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
)
SELECT * FROM employee_hierarchy;
```

---

## 💡 Pro Tips for Data Engineers

### 1. Use CTEs for Readability
```sql
-- Break complex logic into readable steps
WITH customer_summary AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(order_amount) as total_spent
    FROM orders
    GROUP BY customer_id
),
customer_segments AS (
    SELECT 
        customer_id,
        order_count,
        total_spent,
        CASE 
            WHEN total_spent > 2000 THEN 'Premium'
            ELSE 'Standard'
        END as segment
    FROM customer_summary
)
SELECT * FROM customer_segments;
```

### 2. Test CTEs Step by Step
```sql
-- Test each CTE individually
WITH raw_data AS (
    SELECT * FROM raw_table WHERE date >= '2024-01-01'
)
SELECT * FROM raw_data LIMIT 10;  -- Test this first

-- Then add the next CTE
WITH raw_data AS (
    SELECT * FROM raw_table WHERE date >= '2024-01-01'
),
processed_data AS (
    SELECT *, UPPER(name) as clean_name FROM raw_data
)
SELECT * FROM processed_data LIMIT 10;  -- Test this next
```

### 3. Use CTEs for Data Quality Checks
```sql
-- Build data quality checks step by step
WITH data_checks AS (
    SELECT 
        'customers' as table_name,
        COUNT(*) as total_records,
        COUNT(CASE WHEN email IS NULL THEN 1 END) as null_emails
    FROM customers
),
quality_metrics AS (
    SELECT 
        table_name,
        total_records,
        null_emails,
        ROUND(null_emails * 100.0 / total_records, 2) as error_rate
    FROM data_checks
)
SELECT * FROM quality_metrics;
```

---

## 🎯 EPAM Interview Scenarios

### Scenario 1: Complex Customer Analysis
**Problem**: Analyze customer behavior using multiple data sources.

```sql
-- EPAM Interview Solution
WITH customer_orders AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(order_amount) as total_spent,
        AVG(order_amount) as avg_order_value
    FROM orders
    GROUP BY customer_id
),
customer_segments AS (
    SELECT 
        customer_id,
        order_count,
        total_spent,
        avg_order_value,
        CASE 
            WHEN total_spent > 5000 THEN 'VIP'
            WHEN total_spent > 2000 THEN 'Premium'
            WHEN total_spent > 500 THEN 'Standard'
            ELSE 'Basic'
        END as segment
    FROM customer_orders
)
SELECT 
    segment,
    COUNT(*) as customer_count,
    AVG(total_spent) as avg_spent,
    SUM(total_spent) as total_revenue
FROM customer_segments
GROUP BY segment
ORDER BY total_revenue DESC;
```

### Scenario 2: Data Pipeline with CTEs
**Problem**: Build a data transformation pipeline.

```sql
-- EPAM Interview Solution
WITH raw_data AS (
    SELECT 
        customer_id,
        TRIM(UPPER(customer_name)) as customer_name,
        LOWER(TRIM(email)) as email
    FROM raw_customer_table
),
validated_data AS (
    SELECT 
        *,
        CASE 
            WHEN email LIKE '%@%' THEN 'Valid'
            ELSE 'Invalid'
        END as email_status
    FROM raw_data
)
SELECT 
    customer_id,
    customer_name,
    email,
    email_status
FROM validated_data
WHERE email_status = 'Valid';
```

---

## 🚀 Practice Exercises

**See**: `01_SQL/exercises/04_Subqueries_CTEs_Exercises.md`

**Master these patterns**:
1. ✅ Scalar subqueries for simple calculations
2. ✅ Column subqueries for multiple values
3. ✅ Table subqueries for complex analysis
4. ✅ CTEs for readable complex queries
5. ✅ Recursive CTEs for hierarchical data
6. ✅ Multi-step data pipelines
7. ✅ Performance optimization
8. ✅ Real-world scenarios

**Target Time**: Solve complex subquery/CTE problems in < 20 minutes

---

## 📚 Quick Reference Cheat Sheet

### Subquery Types
- **Scalar**: Single value (1 row, 1 column)
- **Column**: Single column (multiple rows, 1 column)
- **Row**: Single row (1 row, multiple columns)
- **Table**: Complete table (multiple rows, multiple columns)

### CTE Syntax
```sql
WITH cte_name AS (
    SELECT ...
),
another_cte AS (
    SELECT ...
)
SELECT ... FROM cte_name;
```

### Recursive CTE Syntax
```sql
WITH RECURSIVE cte_name AS (
    -- Base case
    SELECT ... WHERE condition
    
    UNION ALL
    
    -- Recursive case
    SELECT ... FROM table JOIN cte_name ON ...
)
SELECT * FROM cte_name;
```

### Performance Tips
- Use JOINs instead of correlated subqueries when possible
- Use CTEs for readability and maintainability
- Test CTEs step by step
- Consider window functions for complex calculations

---

## 🎯 Next Steps

1. **Practice complex subquery scenarios** until you can solve them in < 20 minutes
2. **Complete all exercises** in `01_SQL/exercises/04_Subqueries_CTEs_Exercises.md`
3. **Review solutions** only after attempting
4. **Move to**: Query Performance Optimization

**You're now ready to master complex data transformations!** 🚀

---

**Key Takeaway**: Subqueries and CTEs are about **breaking complex problems into manageable steps**. Use CTEs for readability, subqueries for simple calculations, and always consider performance implications.

**Next Module**: `01_SQL/06_Query_Performance.md`

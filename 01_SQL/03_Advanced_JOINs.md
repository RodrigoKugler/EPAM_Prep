# SQL Advanced JOINs - Data Engineering Mastery

## 🎯 Learning Objectives

By the end of this module, you will be able to:
- **Master all JOIN types** (INNER, LEFT, RIGHT, FULL OUTER, CROSS, SELF)
- **Solve complex multi-table scenarios** like a data engineer
- **Choose the right JOIN** for each business requirement
- **Handle data reconciliation** and missing record detection
- **Optimize JOIN performance** for large datasets
- **Implement real-world patterns** using our epam_practice.db database
- **Debug JOIN issues** and validate results

---

## 🔥 Why Advanced JOINs Matter for EPAM

JOINs are the **backbone of data engineering**. Here's why:

1. **Data Integration**: Combining data from multiple sources
2. **Data Warehousing**: Star and snowflake schema implementations
3. **Data Reconciliation**: Finding missing or mismatched records
4. **ETL Pipelines**: Transforming and enriching data
5. **Real-time Analytics**: Joining streaming and batch data
6. **Data Quality**: Cross-table validation and consistency checks

**EPAM will test your JOIN skills in technical interviews. Master this = you're ready for complex data engineering challenges.**

---

## 📚 What Are JOINs?

JOINs combine rows from two or more tables based on related columns. Think of them as "connecting" related data across tables.

### Visual JOIN Types Overview

```
INNER JOIN:     A ∩ B    (Only matching records)
LEFT JOIN:      A ∪ (A ∩ B)    (All A + matching B)
RIGHT JOIN:     B ∪ (A ∩ B)    (All B + matching A)
FULL OUTER:     A ∪ B    (All records from both tables)
CROSS JOIN:     A × B    (Cartesian product - every A with every B)
SELF JOIN:      A ⋈ A    (Table joined with itself)
```

### Key Difference from Simple SELECT

```sql
-- Simple SELECT: Only one table
SELECT customer_id, first_name, last_name FROM customers;

-- JOIN: Combine data from multiple tables
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    o.order_date,
    o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

**Key Insight**: JOINs let you **combine related data** from different tables into a single result set.

---

## 🗄️ Our Database Schema (epam_practice.db)

**Before diving into JOINs, let's understand our database structure:**

### **Key Tables for JOINs:**
- **customers**: customer_id, first_name, last_name, city, customer_segment, total_spent, is_vip
- **orders**: order_id, customer_id, order_date, total_amount, order_status
- **order_items**: order_item_id, order_id, product_id, quantity, total_price
- **products**: product_id, product_name, category_id, price
- **categories**: category_id, category_name, parent_category_id
- **employees**: employee_id, first_name, last_name, department_id, salary, manager_id, job_title
- **departments**: department_id, department_name, manager_id, budget
- **sales**: sale_id, rep_id, territory_id, sale_date, total_amount, commission_earned
- **sales_reps**: rep_id, rep_name, territory_id, commission_rate, quota
- **sales_territories**: territory_id, territory_name, region, target_revenue

### **Quick Schema Check:**
```sql
-- Verify our database structure
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;

-- Check record counts
SELECT 'customers' as table_name, COUNT(*) as record_count FROM customers
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'employees', COUNT(*) FROM employees;
```

---

## 🔥 Core JOIN Types - Complete Guide

### 1. INNER JOIN - Exact Matches Only

**Purpose**: Returns only records that have matching values in both tables

```sql
-- Basic INNER JOIN
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    o.order_date,
    o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
ORDER BY o.order_date
LIMIT 10;
```

**Real-World Example**: Customer Order Analysis
```sql
-- Find customers who have made orders with detailed information
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.customer_segment,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_value,
    MIN(o.order_date) as first_order_date,
    MAX(o.order_date) as last_order_date
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.customer_segment
ORDER BY total_spent DESC
LIMIT 10;
```

**When to Use INNER JOIN**:
- You need exact matches from both tables
- Data quality is high (no missing relationships)
- Performance is critical (smallest result set)

---

### 2. LEFT JOIN - Preserve Left Table

**Purpose**: Returns all records from the left table, plus matching records from the right table

```sql
-- Basic LEFT JOIN
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    o.order_date,
    o.total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_date
LIMIT 10;
```

**Real-World Example**: Customer Analysis with Optional Orders
```sql
-- Find all customers and their order history (including customers with no orders)
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.customer_segment,
    COUNT(o.order_id) as total_orders,
    COALESCE(SUM(o.total_amount), 0) as total_spent,
    COALESCE(AVG(o.total_amount), 0) as avg_order_value,
    CASE 
        WHEN COUNT(o.order_id) = 0 THEN 'No Orders'
        WHEN COUNT(o.order_id) = 1 THEN 'Single Order'
        ELSE 'Multiple Orders'
    END as customer_status
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.customer_segment
ORDER BY total_spent DESC
LIMIT 10;
```

**Real-World Example**: Data Reconciliation
```sql
-- Find customers who haven't made any orders
SELECT 
    'Customers with no orders' as analysis_type,
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.customer_segment,
    c.total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.customer_id IS NULL
ORDER BY c.customer_id
LIMIT 10;
```

**When to Use LEFT JOIN**:
- You need all records from the left table
- You want to include records with no matches
- Data reconciliation and missing record detection

---

### 3. RIGHT JOIN - Preserve Right Table

**Purpose**: Returns all records from the right table, plus matching records from the left table

```sql
-- Basic RIGHT JOIN
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    o.order_date,
    o.total_amount
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id
ORDER BY o.order_date
LIMIT 10;
```

**Real-World Example**: Order Analysis with Customer Details
```sql
-- Find all orders and their customer information (including orphaned orders)
SELECT 
    o.order_id,
    o.order_date,
    o.total_amount,
    o.order_status,
    COALESCE(c.first_name || ' ' || c.last_name, 'Unknown Customer') as customer_name,
    COALESCE(c.customer_segment, 'Unknown Segment') as customer_segment
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id
ORDER BY o.order_date DESC
LIMIT 10;
```

**When to Use RIGHT JOIN**:
- You need all records from the right table
- You want to include orphaned records
- Less common than LEFT JOIN (LEFT JOIN is preferred)

---

### 4. FULL OUTER JOIN - All Records

**Purpose**: Returns all records from both tables, with NULLs for non-matching records

```sql
-- Basic FULL OUTER JOIN (SQLite doesn't support FULL OUTER JOIN directly)
-- We simulate it with UNION of LEFT and RIGHT JOINs
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    o.order_date,
    o.total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id

UNION ALL

SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    o.order_date,
    o.total_amount
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL
ORDER BY customer_id, order_date
LIMIT 10;
```

**Real-World Example**: Complete Data Reconciliation
```sql
-- Find all customers and orders (including orphaned records)
WITH customer_orders AS (
    SELECT 
        c.customer_id,
        c.first_name || ' ' || c.last_name as customer_name,
        c.customer_segment,
        o.order_id,
        o.order_date,
        o.total_amount,
        'Customer with Orders' as record_type
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    
    UNION ALL
    
    SELECT 
        c.customer_id,
        c.first_name || ' ' || c.last_name as customer_name,
        c.customer_segment,
        NULL as order_id,
        NULL as order_date,
        NULL as total_amount,
        'Customer with No Orders' as record_type
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.customer_id IS NULL
    
    UNION ALL
    
    SELECT 
        NULL as customer_id,
        'Unknown Customer' as customer_name,
        NULL as customer_segment,
        o.order_id,
        o.order_date,
        o.total_amount,
        'Orphaned Order' as record_type
    FROM customers c
    RIGHT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.customer_id IS NULL
)
SELECT * FROM customer_orders
ORDER BY customer_id, order_date
LIMIT 20;
```

**When to Use FULL OUTER JOIN**:
- Complete data reconciliation
- Finding all records from both tables
- Data quality analysis

---

### 5. CROSS JOIN - Cartesian Product

**Purpose**: Returns the Cartesian product of two tables (every row from first table with every row from second table)

```sql
-- Basic CROSS JOIN (use with caution!)
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    p.product_id,
    p.product_name
FROM customers c
CROSS JOIN products p
LIMIT 10;  -- Always use LIMIT with CROSS JOIN!
```

**Real-World Example**: Product Recommendations
```sql
-- Generate customer-product combinations for analysis
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.customer_segment,
    p.product_id,
    p.product_name,
    p.price,
    cat.category_name
FROM customers c
CROSS JOIN products p
INNER JOIN categories cat ON p.category_id = cat.category_id
WHERE c.customer_segment = 'Premium'  -- Filter to reduce results
LIMIT 20;
```

**When to Use CROSS JOIN**:
- Generating all possible combinations
- Data analysis and reporting
- **Use with caution** - can create very large result sets

---

### 6. SELF JOIN - Table Joined with Itself

**Purpose**: Join a table with itself to find relationships within the same table

```sql
-- Basic SELF JOIN - Employee hierarchy
SELECT 
    e1.employee_id,
    e1.first_name || ' ' || e1.last_name as employee_name,
    e1.job_title,
    d1.department_name,
    e2.first_name || ' ' || e2.last_name as manager_name,
    e2.job_title as manager_title
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.employee_id
LEFT JOIN departments d1 ON e1.department_id = d1.department_id
ORDER BY e1.department_id, e1.employee_id;
```

**Real-World Example**: Employee Hierarchy Analysis
```sql
-- Complete employee hierarchy with department information
SELECT 
    e1.employee_id,
    e1.first_name || ' ' || e1.last_name as employee_name,
    e1.job_title,
    d.department_name,
    e1.salary,
    e2.first_name || ' ' || e2.last_name as manager_name,
    e2.job_title as manager_title,
    e2.salary as manager_salary,
    CASE 
        WHEN e1.manager_id IS NULL THEN 'Top Level'
        WHEN e2.manager_id IS NULL THEN 'Middle Management'
        ELSE 'Regular Employee'
    END as hierarchy_level
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.employee_id
LEFT JOIN departments d ON e1.department_id = d.department_id
ORDER BY d.department_name, e1.salary DESC;
```

**Real-World Example**: Duplicate Detection
```sql
-- Find potential duplicate customers
SELECT 
    c1.customer_id as customer_1_id,
    c1.first_name || ' ' || c1.last_name as customer_1_name,
    c1.city as customer_1_city,
    c2.customer_id as customer_2_id,
    c2.first_name || ' ' || c2.last_name as customer_2_name,
    c2.city as customer_2_city,
    'Potential Duplicate' as issue_type
FROM customers c1
INNER JOIN customers c2 ON c1.customer_id < c2.customer_id
WHERE LOWER(c1.first_name) = LOWER(c2.first_name) 
   AND LOWER(c1.last_name) = LOWER(c2.last_name)
   AND c1.city = c2.city
ORDER BY c1.customer_id;
```

**When to Use SELF JOIN**:
- Hierarchical data (employees, categories, regions)
- Finding duplicates within a table
- Comparing records within the same table
- Sequential data analysis (previous/next records)

---

## 🎯 Multiple JOINs - Complex Scenarios

### Scenario 1: Complete Order Analysis

```sql
-- Multi-table JOIN for comprehensive order analysis
SELECT 
    o.order_id,
    o.order_date,
    o.total_amount,
    o.order_status,
    c.first_name || ' ' || c.last_name as customer_name,
    c.customer_segment,
    p.product_name,
    cat.category_name,
    oi.quantity,
    oi.total_price as line_total
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
INNER JOIN categories cat ON p.category_id = cat.category_id
WHERE o.order_date >= '2024-01-01'
ORDER BY o.order_date DESC, o.total_amount DESC
LIMIT 20;
```

### Scenario 2: Sales Performance Analysis

```sql
-- Sales rep performance with territory information
SELECT 
    sr.rep_name,
    st.territory_name,
    st.region,
    COUNT(s.sale_id) as total_sales,
    SUM(s.total_amount) as total_revenue,
    SUM(s.commission_earned) as total_commission,
    AVG(s.total_amount) as avg_sale_amount,
    MIN(s.sale_date) as first_sale_date,
    MAX(s.sale_date) as last_sale_date
FROM sales_reps sr
INNER JOIN sales_territories st ON sr.territory_id = st.territory_id
INNER JOIN sales s ON sr.rep_id = s.rep_id
WHERE s.sale_date >= '2024-01-01'
GROUP BY sr.rep_id, sr.rep_name, st.territory_name, st.region
ORDER BY total_revenue DESC;
```

### Scenario 3: Product Performance Analysis

```sql
-- Product performance across categories
SELECT 
    cat.category_name,
    p.product_name,
    p.price,
    COUNT(oi.order_item_id) as times_ordered,
    SUM(oi.quantity) as total_quantity_sold,
    SUM(oi.total_price) as total_revenue,
    AVG(oi.quantity) as avg_quantity_per_order,
    COUNT(DISTINCT o.customer_id) as unique_customers
FROM products p
INNER JOIN categories cat ON p.category_id = cat.category_id
INNER JOIN order_items oi ON p.product_id = oi.product_id
INNER JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY cat.category_name, p.product_id, p.product_name, p.price
ORDER BY total_revenue DESC
LIMIT 20;
```

---

## 🚀 Performance Optimization Tips

### 1. Use Appropriate JOIN Types
```sql
-- Good: Use INNER JOIN when you only need matches
SELECT c.customer_id, o.order_date, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- Avoid: Using LEFT JOIN when you don't need NULLs
SELECT c.customer_id, o.order_date, o.total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.customer_id IS NOT NULL;  -- This is inefficient
```

### 2. Filter Early
```sql
-- Good: Filter in WHERE clause
SELECT c.customer_id, o.order_date, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01';

-- Avoid: Filtering after JOIN
SELECT c.customer_id, o.order_date, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01';
```

### 3. Use LIMIT for Large Result Sets
```sql
-- Always use LIMIT when testing or when result set might be large
SELECT c.customer_id, o.order_date, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
ORDER BY o.order_date DESC
LIMIT 100;
```

---

## 🎯 EPAM Interview Scenarios

### Scenario 1: Customer Analysis
**Question**: "Find all customers who have made orders in the last 3 months and calculate their total spending."

```sql
-- Solution
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.customer_segment,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_value
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= date('now', '-3 months')
GROUP BY c.customer_id, c.first_name, c.last_name, c.customer_segment
ORDER BY total_spent DESC;
```

### Scenario 2: Employee Hierarchy
**Question**: "Show the management chain for all employees in the Engineering department."

```sql
-- Solution
SELECT 
    e1.first_name || ' ' || e1.last_name as employee_name,
    e1.job_title,
    d.department_name,
    e2.first_name || ' ' || e2.last_name as manager_name,
    e2.job_title as manager_title
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.employee_id
INNER JOIN departments d ON e1.department_id = d.department_id
WHERE d.department_name LIKE '%Engineering%'
ORDER BY d.department_name, e1.last_name;
```

### Scenario 3: Product Performance
**Question**: "Find the top 5 products by revenue and show their category information."

```sql
-- Solution
SELECT 
    p.product_name,
    cat.category_name,
    p.price,
    SUM(oi.total_price) as total_revenue,
    SUM(oi.quantity) as total_quantity_sold,
    COUNT(DISTINCT o.customer_id) as unique_customers
FROM products p
INNER JOIN categories cat ON p.category_id = cat.category_id
INNER JOIN order_items oi ON p.product_id = oi.product_id
INNER JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_id, p.product_name, cat.category_name, p.price
ORDER BY total_revenue DESC
LIMIT 5;
```

---

## ⚠️ Common Mistakes and How to Avoid Them

### 1. Missing JOIN Conditions
```sql
-- ✗ WRONG: Missing JOIN condition
SELECT c.customer_id, o.order_date
FROM customers c, orders o;

-- ✓ CORRECT: Proper JOIN condition
SELECT c.customer_id, o.order_date
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

### 2. Using CROSS JOIN Unintentionally
```sql
-- ✗ WRONG: This creates a Cartesian product
SELECT c.customer_id, o.order_date
FROM customers c, orders o
WHERE c.customer_id = o.customer_id;

-- ✓ CORRECT: Use proper JOIN syntax
SELECT c.customer_id, o.order_date
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

### 3. Not Handling NULLs Properly
```sql
-- ✗ WRONG: NULLs in calculations
SELECT 
    c.customer_id,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;

-- ✓ CORRECT: Handle NULLs with COALESCE
SELECT 
    c.customer_id,
    COUNT(o.order_id) as order_count,
    COALESCE(SUM(o.total_amount), 0) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;
```

---

## 🎯 Interview Success Tips

### 1. Explain Your Thought Process
When solving JOIN problems:

1. **Identify the tables needed** - "I need customer and order data"
2. **Determine the relationship** - "Customers have many orders"
3. **Choose the JOIN type** - "I'll use INNER JOIN for exact matches"
4. **Add the JOIN condition** - "ON c.customer_id = o.customer_id"
5. **Filter and group as needed** - "WHERE and GROUP BY clauses"

### 2. Start Simple, Then Add Complexity
```sql
-- Step 1: Basic JOIN
SELECT c.customer_id, o.order_date
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- Step 2: Add more columns
SELECT c.customer_id, c.first_name, o.order_date, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- Step 3: Add filtering and grouping
SELECT c.customer_id, COUNT(o.order_id) as order_count
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;
```

### 3. Test with Sample Data
```sql
-- Always test JOINs with sample data first
SELECT c.customer_id, o.order_date, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE c.customer_id IN (1, 2, 3)  -- Test with specific records
ORDER BY c.customer_id, o.order_date;
```

---

## 📚 Quick Reference Cheat Sheet

### JOIN Types Summary
- **INNER JOIN**: Only matching records
- **LEFT JOIN**: All left + matching right
- **RIGHT JOIN**: All right + matching left  
- **FULL OUTER JOIN**: All records from both tables
- **CROSS JOIN**: Cartesian product (use carefully!)
- **SELF JOIN**: Table joined with itself

### Performance Tips
- Start with smallest/filtered table
- Use appropriate indexes
- Filter in WHERE, not JOIN conditions
- Validate results with counts
- Test with sample data first

### Data Engineering Patterns
- **Customer-Order Analysis**: INNER JOIN for active customers
- **Data Reconciliation**: LEFT JOIN to find missing records
- **Hierarchical Data**: SELF JOIN for employee hierarchies
- **Product Analysis**: Multiple JOINs for comprehensive reports

---

## 🎯 Next Steps

1. **Practice complex JOIN scenarios** until you can solve them in < 15 minutes
2. **Complete all exercises** in `01_SQL/exercises/03_JOINs_Exercises.md`
3. **Review solutions** only after attempting
4. **Move to**: Subqueries and CTEs

**You're now ready to master complex data integration scenarios!** 🚀

---

**Key Takeaway**: JOINs are about **combining data from multiple sources**. Master the different types, understand when to use each, and always validate your results. This is essential for data engineering work.

**Next Module**: `01_SQL/04_Subqueries_CTEs.md`

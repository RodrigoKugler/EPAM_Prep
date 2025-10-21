# EPAM Enhanced Database - Quick Reference Guide

## 🚀 **Quick Start**

### **Access the Database**
```bash
# Navigate to database directory
cd database

# Open with SQLite command line
sqlite3 epam_practice.db

# Or use DBeaver/any SQL client to connect to:
# File: database/epam_practice.db
```

### **Verify Database Setup**
```sql
-- Check table count and record counts
SELECT 
    name as table_name,
    (SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=m.name) as exists
FROM sqlite_master m 
WHERE type='table' 
ORDER BY name;

-- Check total records across all tables
SELECT 'customers' as table_name, COUNT(*) as record_count FROM customers
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'employees', COUNT(*) FROM employees
UNION ALL SELECT 'sales', COUNT(*) FROM sales;
```

---

## 📊 **Table Overview**

### **Business Tables**
| Table | Records | Purpose | Key Columns |
|-------|---------|---------|-------------|
| `customers` | 500 | Customer profiles | customer_id, first_name, last_name, city, customer_segment |
| `products` | 54 | Product catalog | product_id, product_name, category_id, price |
| `orders` | 2,000 | Order transactions | order_id, customer_id, order_date, total_amount, order_status |
| `order_items` | 6,017 | Order line items | order_item_id, order_id, product_id, quantity, total_price |
| `categories` | 9 | Product categories | category_id, category_name, parent_category_id |
| `warehouses` | 5 | Distribution centers | warehouse_id, warehouse_name, location, capacity |

### **HR Tables**
| Table | Records | Purpose | Key Columns |
|-------|---------|---------|-------------|
| `employees` | 200 | Employee directory | employee_id, first_name, last_name, department_id, salary, manager_id |
| `departments` | 8 | Organizational units | department_id, department_name, manager_id, budget |
| `salaries` | 600 | Salary history | salary_id, employee_id, salary_amount, effective_date |

### **Sales & Finance Tables**
| Table | Records | Purpose | Key Columns |
|-------|---------|---------|-------------|
| `sales` | 44,020 | Daily sales transactions | sale_id, rep_id, territory_id, sale_date, total_amount |
| `sales_reps` | 50 | Sales representatives | rep_id, rep_name, territory_id, commission_rate, quota |
| `sales_territories` | 6 | Geographic regions | territory_id, territory_name, region, target_revenue |
| `monthly_revenue` | 24 | Financial time series | month_id, year, month, revenue, expenses, profit |

---

## 🎯 **Common Query Patterns**

### **1. Window Functions - Running Totals**
```sql
-- Customer running totals (EPAM Classic Problem)
SELECT 
    customer_id, 
    order_date, 
    total_amount,
    SUM(total_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM orders 
WHERE customer_id <= 5
ORDER BY customer_id, order_date;
```

### **2. Employee Hierarchy (Self-Join)**
```sql
-- Employee management chain
SELECT 
    e.first_name || ' ' || e.last_name as employee,
    e.job_title,
    d.department_name,
    m.first_name || ' ' || m.last_name as manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
LEFT JOIN departments d ON e.department_id = d.department_id
ORDER BY d.department_name, e.last_name;
```

### **3. Complex Multi-Table Join**
```sql
-- Top products by revenue with customer demographics
SELECT 
    c.category_name,
    p.product_name,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    SUM(oi.quantity) as total_quantity,
    SUM(oi.total_price) as total_revenue
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY c.category_name, p.product_name
ORDER BY total_revenue DESC
LIMIT 10;
```

### **4. Sales Performance Analysis**
```sql
-- Sales rep performance with rankings
SELECT 
    sr.rep_name,
    st.territory_name,
    COUNT(s.sale_id) as total_sales,
    SUM(s.total_amount) as total_revenue,
    SUM(s.commission_earned) as total_commission,
    RANK() OVER (ORDER BY SUM(s.total_amount) DESC) as revenue_rank
FROM sales_reps sr
JOIN sales_territories st ON sr.territory_id = st.territory_id
JOIN sales s ON sr.rep_id = s.rep_id
GROUP BY sr.rep_id, sr.rep_name, st.territory_name
ORDER BY total_revenue DESC;
```

### **5. Time Series Analysis**
```sql
-- Monthly revenue trends with moving averages
SELECT 
    year,
    month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY year, month) as prev_month_revenue,
    revenue - LAG(revenue, 1) OVER (ORDER BY year, month) as month_over_month_change,
    AVG(revenue) OVER (
        ORDER BY year, month 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as moving_avg_3_months
FROM monthly_revenue
ORDER BY year, month;
```

---

## 🔍 **Sample Data Exploration**

### **Customer Segments**
```sql
SELECT 
    customer_segment,
    COUNT(*) as customer_count,
    AVG(total_spent) as avg_spent,
    COUNT(CASE WHEN is_vip = 1 THEN 1 END) as vip_count
FROM customers
GROUP BY customer_segment
ORDER BY avg_spent DESC;
```

### **Product Categories**
```sql
SELECT 
    c.category_name,
    COUNT(p.product_id) as product_count,
    AVG(p.price) as avg_price,
    MIN(p.price) as min_price,
    MAX(p.price) as max_price
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_id, c.category_name
ORDER BY product_count DESC;
```

### **Order Status Distribution**
```sql
SELECT 
    order_status,
    COUNT(*) as order_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) as percentage
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;
```

### **Employee Salary Ranges by Department**
```sql
SELECT 
    d.department_name,
    COUNT(e.employee_id) as employee_count,
    ROUND(AVG(e.salary), 2) as avg_salary,
    ROUND(MIN(e.salary), 2) as min_salary,
    ROUND(MAX(e.salary), 2) as max_salary
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name
ORDER BY avg_salary DESC;
```

---

## 🎯 **EPAM Interview Practice Scenarios**

### **Scenario 1: Customer Analysis**
**Question**: "Find customers who have made orders in the last 3 months and calculate their total spending."

```sql
-- Your solution here
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= date('now', '-3 months')
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC;
```

### **Scenario 2: Employee Hierarchy**
**Question**: "Show the management chain for all employees in the Engineering department."

```sql
-- Your solution here
WITH RECURSIVE emp_hierarchy AS (
    SELECT employee_id, first_name, last_name, job_title, manager_id, 1 as level
    FROM employees 
    WHERE department_id = 4  -- Engineering
    
    UNION ALL
    
    SELECT e.employee_id, e.first_name, e.last_name, e.job_title, e.manager_id, eh.level + 1
    FROM employees e
    JOIN emp_hierarchy eh ON e.employee_id = eh.manager_id
)
SELECT 
    REPEAT('  ', level-1) || first_name || ' ' || last_name as hierarchy,
    job_title,
    level
FROM emp_hierarchy
ORDER BY level, last_name;
```

### **Scenario 3: Sales Performance**
**Question**: "Rank sales territories by total revenue and show the top 3."

```sql
-- Your solution here
SELECT 
    st.territory_name,
    st.region,
    SUM(s.total_amount) as total_revenue,
    COUNT(DISTINCT sr.rep_id) as rep_count,
    RANK() OVER (ORDER BY SUM(s.total_amount) DESC) as revenue_rank
FROM sales_territories st
JOIN sales_reps sr ON st.territory_id = sr.territory_id
JOIN sales s ON sr.rep_id = s.rep_id
GROUP BY st.territory_id, st.territory_name, st.region
HAVING RANK() OVER (ORDER BY SUM(s.total_amount) DESC) <= 3
ORDER BY total_revenue DESC;
```

---

## 🚀 **Performance Tips**

### **Use Indexes Effectively**
```sql
-- Check which indexes are available
SELECT name, sql FROM sqlite_master WHERE type='index';

-- Common indexed columns for optimal performance:
-- orders: customer_id, order_date, order_status
-- products: category_id, price
-- employees: department_id, manager_id
-- sales: rep_id, sale_date, territory_id
```

### **Query Optimization**
```sql
-- Use LIMIT for large result sets
SELECT * FROM sales ORDER BY sale_date DESC LIMIT 100;

-- Use specific column selection instead of *
SELECT customer_id, first_name, last_name FROM customers;

-- Use appropriate WHERE clauses
SELECT * FROM orders WHERE order_date >= '2024-01-01';
```

---

## 📚 **Learning Path**

### **Beginner Level**
1. Basic SELECT queries on single tables
2. Simple WHERE and ORDER BY clauses
3. Basic aggregation (COUNT, SUM, AVG)

### **Intermediate Level**
1. JOINs between 2-3 tables
2. GROUP BY with aggregation
3. Basic window functions (ROW_NUMBER, RANK)

### **Advanced Level**
1. Complex multi-table JOINs
2. Advanced window functions (LAG, LEAD, running totals)
3. Recursive queries (CTEs)
4. Performance optimization

### **Expert Level**
1. Complex business logic queries
2. Advanced analytics and reporting
3. Query optimization and indexing strategies
4. Real-world data engineering scenarios

---

**Happy SQL Practicing!** 🎯

Remember: This database is designed to mirror real-world business scenarios. Use it to practice not just SQL syntax, but also business analysis and data engineering thinking!


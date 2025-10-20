# SQL Subqueries & CTEs - Practice Exercises

## 🎯 Exercise Guidelines

- **Time Target**: 15-20 minutes per exercise
- **Approach**: Start with simple subqueries, then build complexity
- **Readability**: Use CTEs to break complex logic into steps
- **Performance**: Consider when to use JOINs instead of subqueries

---

## 📚 Exercise 1: Basic Subqueries

### Problem 1.1: Customer Analysis with Scalar Subqueries
**Tables**: `customers`, `orders`

**Task**: Create a customer analysis report using scalar subqueries to calculate metrics for each customer.

**Expected Output**:
```
customer_id | customer_name | order_count | total_spent | avg_order_value | last_order_date
1          | Alice Johnson | 5           | 1250.00     | 250.00         | 2024-01-15
2          | Bob Smith     | 3           | 750.00      | 250.00         | 2024-01-10
3          | Carol Davis   | 0           | 0.00        | 0.00           | NULL
```

**Hint**: Use scalar subqueries in the SELECT clause

---

### Problem 1.2: Product Performance Analysis
**Tables**: `products`, `order_items`, `orders`

**Task**: Analyze product performance using subqueries to find products with above-average sales.

**Expected Output**:
```
product_id | product_name    | total_quantity | total_revenue | avg_order_value | performance_status
1          | Laptop Pro      | 25             | 37500.00      | 1500.00         | Above Average
2          | Mouse Wireless  | 15             | 450.00        | 30.00           | Below Average
3          | Keyboard RGB    | 20             | 1200.00       | 60.00           | Above Average
```

**Hint**: Use subqueries to calculate averages and compare

---

## 🔥 Exercise 2: Column and Row Subqueries

### Problem 2.1: Customer Product History
**Tables**: `customers`, `orders`, `order_items`, `products`

**Task**: Find customers and their product purchase history using column subqueries.

**Expected Output**:
```
customer_id | customer_name | products_purchased                    | total_products
1          | Alice Johnson | Laptop Pro, Mouse, Keyboard           | 3
2          | Bob Smith     | Laptop Pro, Mouse                     | 2
3          | Carol Davis   | NULL                                  | 0
```

**Hint**: Use column subqueries with GROUP_CONCAT or similar functions

---

### Problem 2.2: Order Details Analysis
**Tables**: `orders`, `customers`

**Task**: Analyze order details using row subqueries to get first and last order information.

**Expected Output**:
```
customer_id | customer_name | first_order_date | first_order_amount | last_order_date | last_order_amount
1          | Alice Johnson | 2023-06-15      | 500.00             | 2024-01-15      | 300.00
2          | Bob Smith     | 2023-08-22      | 250.00             | 2024-01-10      | 400.00
```

**Hint**: Use row subqueries to get multiple columns from a single row

---

## 🎯 Exercise 3: Table Subqueries

### Problem 3.1: Customer Segmentation Analysis
**Tables**: `customers`, `orders`

**Task**: Create a customer segmentation analysis using table subqueries.

**Expected Output**:
```
customer_segment | customer_count | avg_total_spent | avg_order_count | total_revenue
VIP             | 5              | 5000.00         | 15.0            | 25000.00
Premium         | 12             | 2500.00         | 8.0             | 30000.00
Standard        | 25             | 800.00          | 3.0             | 20000.00
Basic           | 8              | 200.00          | 1.0             | 1600.00
```

**Hint**: Use table subqueries to create intermediate results

---

### Problem 3.2: Product Category Performance
**Tables**: `products`, `categories`, `order_items`, `orders`

**Task**: Analyze product category performance using table subqueries.

**Expected Output**:
```
category_name | total_products | total_quantity_sold | total_revenue | avg_product_price
Electronics   | 15             | 150                 | 45000.00      | 300.00
Clothing      | 25             | 200                 | 8000.00       | 40.00
Books         | 10             | 75                  | 1500.00       | 20.00
```

**Hint**: Use table subqueries to aggregate data by category

---

## 🔧 Exercise 4: Basic CTEs

### Problem 4.1: Customer Lifetime Value Analysis
**Tables**: `customers`, `orders`

**Task**: Calculate customer lifetime value using CTEs for readable, step-by-step analysis.

**Expected Output**:
```
customer_id | customer_name | customer_segment | total_orders | total_spent | avg_order_value | customer_lifetime_days
1          | Alice Johnson | Premium          | 12           | 2400.00     | 200.00          | 275
2          | Bob Smith     | Standard         | 8            | 960.00      | 120.00          | 198
3          | Carol Davis   | Premium          | 15           | 3750.00     | 250.00          | 325
```

**Hint**: Use multiple CTEs to break down the calculation

---

### Problem 4.2: Data Quality Assessment
**Tables**: `customers`, `orders`

**Task**: Create a data quality assessment using CTEs to identify data issues.

**Expected Output**:
```
quality_check | total_records | valid_records | invalid_records | error_rate_pct
Customers with Valid Emails | 50 | 45 | 5 | 10.00
Customers with Valid Names | 50 | 48 | 2 | 4.00
Customers with Orders | 50 | 35 | 15 | 30.00
Complete Customer Records | 50 | 32 | 18 | 36.00
```

**Hint**: Use CTEs to build data quality checks step by step

---

## 🚀 Exercise 5: Advanced CTEs

### Problem 5.1: ETL Data Pipeline
**Tables**: `raw_customer_data`, `customer_segments`, `regions`

**Task**: Build an ETL pipeline using CTEs to transform raw customer data.

**Expected Output**:
```
customer_id | customer_name | email | phone | customer_segment | region_name | data_quality_score
1          | ALICE JOHNSON | alice@email.com | 1234567890 | Premium | North | High Quality
2          | BOB SMITH     | bob@email.com | 0987654321 | Standard | South | High Quality
3          | CAROL DAVIS   | carol@email.com | 1122334455 | Premium | East | Medium Quality
```

**Hint**: Use multiple CTEs for each step of the ETL process

---

### Problem 5.2: Complex Business Analytics
**Tables**: `customers`, `orders`, `order_items`, `products`, `categories`

**Task**: Create a comprehensive business analytics report using advanced CTEs.

**Expected Output**:
```
customer_segment | category_name | total_customers | total_orders | total_revenue | avg_order_value
Premium | Electronics | 8 | 45 | 22500.00 | 500.00
Premium | Clothing | 8 | 30 | 6000.00 | 200.00
Standard | Electronics | 15 | 60 | 18000.00 | 300.00
Standard | Clothing | 15 | 40 | 4000.00 | 100.00
```

**Hint**: Use multiple CTEs to build complex analytics step by step

---

## 🎯 Exercise 6: Recursive CTEs

### Problem 6.1: Employee Hierarchy
**Tables**: `employees`

**Task**: Build a complete employee hierarchy using recursive CTEs.

**Expected Output**:
```
employee_id | employee_name | manager_id | manager_name | hierarchy_level | hierarchy_path
1           | John CEO      | NULL       | NULL         | 1               | John CEO
2           | Alice VP      | 1          | John CEO     | 2               | John CEO -> Alice VP
3           | Bob Director  | 2          | Alice VP     | 3               | John CEO -> Alice VP -> Bob Director
4           | Carol Manager | 3          | Bob Director | 4               | John CEO -> Alice VP -> Bob Director -> Carol Manager
```

**Hint**: Use recursive CTEs to build hierarchical data

---

### Problem 6.2: Product Category Hierarchy
**Tables**: `product_categories`

**Task**: Build a product category hierarchy using recursive CTEs.

**Expected Output**:
```
category_id | category_name | parent_category_id | hierarchy_level | full_path
1           | Electronics   | NULL               | 1               | Electronics
2           | Computers     | 1                  | 2               | Electronics > Computers
3           | Laptops       | 2                  | 3               | Electronics > Computers > Laptops
4           | Desktops      | 2                  | 3               | Electronics > Computers > Desktops
```

**Hint**: Use recursive CTEs to build category hierarchies

---

## 🔥 Exercise 7: Performance Optimization

### Problem 7.1: Optimize Correlated Subqueries
**Tables**: `customers`, `orders`

**Task**: Rewrite correlated subqueries using JOINs for better performance.

**Given Query** (inefficient):
```sql
SELECT 
    customer_id,
    customer_name,
    (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count,
    (SELECT SUM(order_amount) FROM orders WHERE customer_id = c.customer_id) as total_spent
FROM customers c;
```

**Expected Output**: Same results but with better performance

**Hint**: Convert to JOINs with GROUP BY

---

### Problem 7.2: Optimize Multiple Subqueries
**Tables**: `customers`, `orders`, `order_items`, `products`

**Task**: Optimize multiple subqueries using CTEs or JOINs.

**Given Query** (inefficient):
```sql
SELECT 
    customer_id,
    (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count,
    (SELECT SUM(order_amount) FROM orders WHERE customer_id = c.customer_id) as total_spent,
    (SELECT COUNT(DISTINCT product_id) FROM order_items oi 
     INNER JOIN orders o ON oi.order_id = o.order_id 
     WHERE o.customer_id = c.customer_id) as unique_products
FROM customers c;
```

**Expected Output**: Same results but with better performance

**Hint**: Use CTEs to combine the logic

---

## 🎯 Exercise 8: Real-World Scenarios

### Problem 8.1: Customer Churn Analysis
**Tables**: `customers`, `orders`

**Task**: Analyze customer churn using CTEs to identify at-risk customers.

**Expected Output**:
```
customer_id | customer_name | last_order_date | days_since_last_order | churn_risk
1          | Alice Johnson | 2024-01-15     | 30                    | Low
2          | Bob Smith     | 2023-12-01     | 75                    | High
3          | Carol Davis   | 2023-11-15     | 90                    | Critical
```

**Hint**: Use CTEs to calculate time-based metrics

---

### Problem 8.2: Product Recommendation Engine
**Tables**: `customers`, `orders`, `order_items`, `products`

**Task**: Build a product recommendation engine using CTEs.

**Expected Output**:
```
customer_id | customer_name | recommended_products | recommendation_reason
1          | Alice Johnson | Mouse, Keyboard     | Similar customers bought these
2          | Bob Smith     | Laptop Pro, Mouse   | Popular in your segment
3          | Carol Davis   | Books, Clothing     | Trending products
```

**Hint**: Use CTEs to analyze customer behavior and product popularity

---

## 💡 Exercise 9: Advanced Patterns

### Problem 9.1: Time-Series Analysis with CTEs
**Tables**: `daily_sales`, `products`, `regions`

**Task**: Analyze sales trends using CTEs for time-series analysis.

**Expected Output**:
```
date | region_name | product_category | daily_sales | 7_day_avg | 30_day_avg | trend
2024-01-15 | North | Electronics | 5000.00 | 4500.00 | 4200.00 | Up
2024-01-16 | North | Electronics | 4800.00 | 4600.00 | 4250.00 | Down
2024-01-17 | North | Electronics | 5200.00 | 4700.00 | 4300.00 | Up
```

**Hint**: Use CTEs to calculate moving averages and trends

---

### Problem 9.2: Cohort Analysis
**Tables**: `customers`, `orders`

**Task**: Perform cohort analysis using CTEs to analyze customer retention.

**Expected Output**:
```
cohort_month | customer_count | month_1_retention | month_2_retention | month_3_retention
2023-10 | 100 | 85.00 | 72.00 | 65.00
2023-11 | 120 | 88.00 | 75.00 | 68.00
2023-12 | 150 | 90.00 | 78.00 | 70.00
```

**Hint**: Use CTEs to build cohort analysis step by step

---

## 🎯 Challenge Exercises

### Challenge 1: Complex Data Pipeline
**Task**: Build a comprehensive data pipeline using CTEs for customer data processing.

**Requirements**:
- Extract data from multiple sources
- Clean and validate data
- Enrich with additional information
- Calculate business metrics
- Generate quality reports

### Challenge 2: Advanced Analytics Engine
**Task**: Create an advanced analytics engine using CTEs for business intelligence.

**Requirements**:
- Customer segmentation
- Product performance analysis
- Sales trend analysis
- Predictive metrics
- Comprehensive reporting

### Challenge 3: Data Quality Framework
**Task**: Build a comprehensive data quality framework using CTEs.

**Requirements**:
- Data validation rules
- Quality scoring
- Issue identification
- Trend analysis
- Automated reporting

---

## 📚 Exercise Solutions

**Solutions are available in**: `01_SQL/solutions/04_Subqueries_CTEs_Solutions.md`

**Remember**: 
- Attempt each exercise before checking solutions
- Focus on understanding the logic, not just getting the right answer
- Practice explaining your approach
- Time yourself to improve speed

---

## 🎯 Success Criteria

**By completing these exercises, you should be able to**:
- ✅ Write scalar, column, row, and table subqueries
- ✅ Use CTEs for readable complex queries
- ✅ Implement recursive CTEs for hierarchical data
- ✅ Optimize subquery performance
- ✅ Build multi-step data pipelines
- ✅ Handle complex business logic
- ✅ Debug subquery and CTE issues
- ✅ Explain your approach clearly

**Target**: Solve any subquery/CTE problem in under 20 minutes! 🚀


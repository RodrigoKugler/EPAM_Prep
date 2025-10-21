# SQL Advanced JOINs - Practice Exercises

## 🎯 Exercise Guidelines

- **Time Target**: 10-15 minutes per exercise
- **Approach**: Start simple, then add complexity
- **Validation**: Always check your results with sample data
- **Performance**: Consider which JOIN type is most efficient

---

## 📚 Exercise 1: Basic JOIN Types

### Problem 1.1: Customer Order Analysis
**Tables**: `customers`, `orders`

**Task**: Create a report showing all customers and their order information. Include customers who haven't placed any orders.

**Expected Output**:
```
customer_id | customer_name | order_count | total_spent | customer_status
1          | Alice Johnson | 3           | 450.00      | Active Customer
2          | Bob Smith     | 0           | 0.00        | No Orders
3          | Carol Davis   | 2           | 320.50      | Active Customer
```

**Hint**: Use LEFT JOIN to preserve all customers

---

### Problem 1.2: Product Sales Analysis
**Tables**: `products`, `order_items`

**Task**: Find all products and their sales performance. Include products that haven't been sold.

**Expected Output**:
```
product_id | product_name    | total_quantity_sold | total_revenue | sales_status
1          | Laptop Pro      | 25                  | 37500.00      | High Sales
2          | Mouse Wireless  | 0                   | 0.00          | No Sales
3          | Keyboard RGB    | 15                  | 2250.00       | Moderate Sales
```

---

## 🔥 Exercise 2: Data Reconciliation

### Problem 2.1: System Data Comparison
**Tables**: `system_a_customers`, `system_b_customers`

**Task**: Compare customer data between two systems and identify discrepancies.

**Expected Output**:
```
customer_id | system_a_name | system_b_name | system_a_email | system_b_email | issue_type
1          | Alice Johnson | Alice Johnson | alice@email.com | alice@email.com | Perfect Match
2          | Bob Smith     | Robert Smith  | bob@email.com   | robert@email.com | Name Mismatch
3          | Carol Davis   | NULL          | carol@email.com | NULL            | Missing in System B
4          | NULL          | David Wilson  | NULL            | david@email.com  | Missing in System A
```

**Hint**: Use FULL OUTER JOIN for complete comparison

---

### Problem 2.2: Order Reconciliation
**Tables**: `web_orders`, `mobile_orders`

**Task**: Find orders that exist in one system but not the other, and identify potential duplicates.

**Expected Output**:
```
order_id | web_amount | mobile_amount | web_date    | mobile_date  | reconciliation_status
1001     | 150.00     | 150.00       | 2024-01-15  | 2024-01-15   | Perfect Match
1002     | 200.00     | NULL         | 2024-01-16  | NULL         | Only in Web
1003     | NULL       | 175.00       | NULL        | 2024-01-17   | Only in Mobile
1004     | 100.00     | 100.00       | 2024-01-18  | 2024-01-19   | Date Mismatch
```

---

## 🎯 Exercise 3: Star Schema Queries

### Problem 3.1: Sales Performance Report
**Tables**: `fact_sales`, `dim_customers`, `dim_products`, `dim_dates`

**Task**: Create a comprehensive sales report by customer segment, product category, and time period.

**Expected Output**:
```
customer_segment | product_category | year | quarter | total_orders | total_revenue | avg_order_value
Premium          | Electronics     | 2024 | Q1      | 45           | 67500.00      | 1500.00
Standard         | Electronics     | 2024 | Q1      | 120          | 48000.00      | 400.00
Premium          | Clothing        | 2024 | Q1      | 30           | 15000.00      | 500.00
Standard         | Clothing        | 2024 | Q1      | 85           | 17000.00      | 200.00
```

---

### Problem 3.2: Customer Journey Analysis
**Tables**: `fact_orders`, `dim_customers`, `dim_dates`

**Task**: Analyze customer behavior over time, including first purchase and customer lifetime value.

**Expected Output**:
```
customer_id | customer_name | customer_segment | first_order_date | total_orders | total_spent | avg_order_value | customer_lifetime_days
1           | Alice Johnson | Premium          | 2023-06-15      | 12           | 2400.00     | 200.00          | 275
2           | Bob Smith     | Standard         | 2023-08-22      | 8            | 960.00      | 120.00          | 198
3           | Carol Davis   | Premium          | 2023-05-10      | 15           | 3750.00     | 250.00          | 325
```

---

## 🔧 Exercise 4: Self JOINs

### Problem 4.1: Employee Hierarchy
**Tables**: `employees`

**Task**: Create an employee hierarchy report showing each employee and their manager.

**Expected Output**:
```
employee_id | employee_name | manager_id | manager_name | hierarchy_level
1           | John CEO      | NULL       | NULL         | 1
2           | Alice VP      | 1          | John CEO     | 2
3           | Bob Director  | 2          | Alice VP     | 3
4           | Carol Manager | 3          | Bob Director | 4
5           | David Analyst | 4          | Carol Manager| 5
```

**Hint**: Use SELF JOIN with LEFT JOIN to include top-level employees

---

### Problem 4.2: Duplicate Customer Detection
**Tables**: `customers`

**Task**: Find potential duplicate customers based on similar names or email addresses.

**Expected Output**:
```
customer_1_id | customer_1_name | customer_1_email | customer_2_id | customer_2_name | customer_2_email | duplicate_reason
1             | Alice Johnson   | alice@email.com  | 5             | Alice J.        | alice@email.com  | Same Email
2             | Bob Smith       | bob@email.com    | 7             | Robert Smith    | robert@email.com | Similar Name
3             | Carol Davis     | carol@email.com  | 9             | Carol Davis     | carol.davis@email.com | Same Name
```

**Hint**: Use SELF JOIN with inequality condition to avoid comparing same record

---

## 🚀 Exercise 5: Complex Multi-Table JOINs

### Problem 5.1: ETL Data Enrichment
**Tables**: `raw_transactions`, `customers`, `products`, `regions`

**Task**: Enrich raw transaction data with customer, product, and regional information.

**Expected Output**:
```
transaction_id | transaction_date | customer_name | customer_segment | product_name | product_category | region_name | amount | enriched_status
1001          | 2024-01-15      | Alice Johnson | Premium          | Laptop Pro   | Electronics      | North       | 1500.00 | Fully Enriched
1002          | 2024-01-16      | Bob Smith     | Standard         | Mouse        | Electronics      | South       | 25.00   | Fully Enriched
1003          | 2024-01-17      | Unknown       | Unknown          | Unknown      | Unknown          | Unknown     | 100.00  | Missing Data
```

---

### Problem 5.2: Comprehensive Data Quality Check
**Tables**: `orders`, `customers`, `products`, `order_items`

**Task**: Create a data quality dashboard showing various data quality metrics.

**Expected Output**:
```
quality_check | total_records | valid_records | invalid_records | error_rate_pct
Orders with Valid Customers | 150 | 145 | 5 | 3.33
Orders with Valid Products | 150 | 148 | 2 | 1.33
Orders with Positive Amounts | 150 | 150 | 0 | 0.00
Orders with Valid Dates | 150 | 149 | 1 | 0.67
Complete Orders | 150 | 144 | 6 | 4.00
```

---

## 🎯 Exercise 6: Performance Optimization

### Problem 6.1: Efficient Customer Analysis
**Tables**: `customers` (1M records), `orders` (10M records)

**Task**: Find top 100 customers by total spending efficiently.

**Expected Output**:
```
customer_id | customer_name | customer_segment | total_spent | order_count | avg_order_value
1           | Alice Johnson | Premium          | 25000.00    | 125         | 200.00
2           | Bob Smith     | Premium          | 22000.00    | 110         | 200.00
3           | Carol Davis   | Premium          | 20000.00    | 100         | 200.00
...
```

**Hint**: Consider which table to start with and what indexes you'd need

---

### Problem 6.2: Optimized Data Reconciliation
**Tables**: `system_a_data` (500K records), `system_b_data` (500K records)

**Task**: Efficiently find all discrepancies between two large datasets.

**Expected Output**:
```
discrepancy_type | count | percentage
Perfect Matches | 450000 | 90.00
Missing in System A | 25000 | 5.00
Missing in System B | 20000 | 4.00
Data Mismatches | 5000 | 1.00
```

---

## 🔥 Exercise 7: Real-World Scenarios

### Problem 7.1: E-commerce Analytics
**Tables**: `customers`, `orders`, `order_items`, `products`, `categories`

**Task**: Create a comprehensive e-commerce analytics report.

**Expected Output**:
```
customer_segment | category_name | month | total_orders | total_revenue | avg_order_value | unique_customers
Premium | Electronics | 2024-01 | 45 | 67500.00 | 1500.00 | 30
Standard | Electronics | 2024-01 | 120 | 48000.00 | 400.00 | 85
Premium | Clothing | 2024-01 | 30 | 15000.00 | 500.00 | 25
Standard | Clothing | 2024-01 | 85 | 17000.00 | 200.00 | 70
```

---

### Problem 7.2: Data Migration Validation
**Tables**: `old_system_orders`, `new_system_orders`, `customers`

**Task**: Validate data migration from old system to new system.

**Expected Output**:
```
validation_check | old_system_count | new_system_count | difference | status
Total Orders | 10000 | 10000 | 0 | PASS
Total Customers | 2500 | 2500 | 0 | PASS
Total Revenue | 1500000.00 | 1500000.00 | 0.00 | PASS
Orders by Premium Customers | 3000 | 2995 | -5 | FAIL
Orders by Standard Customers | 7000 | 7005 | +5 | FAIL
```

---

## 💡 Exercise 8: Advanced Patterns

### Problem 8.1: Time-Series Data Analysis
**Tables**: `daily_sales`, `products`, `regions`

**Task**: Analyze sales trends with moving averages and period comparisons.

**Expected Output**:
```
date | region_name | product_category | daily_sales | 7_day_avg | 30_day_avg | vs_previous_day_pct
2024-01-15 | North | Electronics | 5000.00 | 4500.00 | 4200.00 | 5.26
2024-01-16 | North | Electronics | 4800.00 | 4600.00 | 4250.00 | -4.00
2024-01-17 | North | Electronics | 5200.00 | 4700.00 | 4300.00 | 8.33
```

---

### Problem 8.2: Customer Cohort Analysis
**Tables**: `customers`, `orders`

**Task**: Analyze customer retention and cohort performance.

**Expected Output**:
```
cohort_month | customer_count | month_1_retention | month_2_retention | month_3_retention
2023-10 | 100 | 85.00 | 72.00 | 65.00
2023-11 | 120 | 88.00 | 75.00 | 68.00
2023-12 | 150 | 90.00 | 78.00 | 70.00
```

---

## 🎯 Challenge Exercises

### Challenge 1: Complex Data Warehouse Query
**Task**: Create a comprehensive business intelligence report with multiple dimensions and calculated metrics.

**Requirements**:
- Use at least 5 tables
- Include time-based analysis
- Calculate multiple business metrics
- Handle NULL values appropriately
- Optimize for performance

### Challenge 2: Data Quality Assessment
**Task**: Build a comprehensive data quality assessment framework.

**Requirements**:
- Check for missing data
- Identify duplicates
- Validate data consistency
- Calculate quality scores
- Generate quality reports

### Challenge 3: Real-Time Analytics Pipeline
**Task**: Design queries for a real-time analytics system.

**Requirements**:
- Handle streaming data
- Calculate real-time metrics
- Optimize for low latency
- Handle data freshness
- Scale to large volumes

---

## 📚 Exercise Solutions

**Solutions are available in**: `01_SQL/solutions/03_JOINs_Solutions.md`

**Remember**: 
- Attempt each exercise before checking solutions
- Focus on understanding the logic, not just getting the right answer
- Practice explaining your approach
- Time yourself to improve speed

---

## 🎯 Success Criteria

**By completing these exercises, you should be able to**:
- ✅ Choose the right JOIN type for any scenario
- ✅ Solve complex multi-table queries
- ✅ Optimize JOIN performance
- ✅ Handle data quality issues
- ✅ Implement data reconciliation patterns
- ✅ Build star schema queries
- ✅ Debug JOIN problems
- ✅ Explain your approach clearly

**Target**: Solve any JOIN problem in under 15 minutes! 🚀



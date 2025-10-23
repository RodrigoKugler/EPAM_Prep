# SQL Window Functions - Complete Mastery Guide

## 🎯 Learning Objectives

By the end of this module, you will be able to:
- **Master all window functions** (ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, FIRST_VALUE, LAST_VALUE)
- **Understand PARTITION BY** and use it effectively
- **Control frame specifications** (ROWS vs RANGE, boundaries)
- **Solve EPAM's favorite cumulative problems** in under 10 minutes
- **Apply window functions** to real business scenarios using our epam_practice.db database
- **Optimize window function queries** for performance
- **Explain concepts clearly** in technical interviews

---

## 🔥 Why Window Functions Matter for EPAM

Window functions are **EPAM's #1 favorite SQL topic**. Here's why:

1. **They test analytical thinking** - Can you solve cumulative problems?
2. **They're used in real data pipelines** - ETL processes, reporting, analytics
3. **They separate beginners from experts** - Advanced SQL mastery
4. **They're efficient** - Better performance than self-joins for many problems

**EPAM will almost certainly ask you to solve a cumulative/running total problem. Master this module = 80% of SQL interview success.**

---

## 📚 What Are Window Functions?

Window functions perform calculations across a set of rows **without collapsing them** (unlike GROUP BY). Think of them as "peeking through a window" at related rows.

### Key Difference from GROUP BY

```sql
-- GROUP BY: Collapses rows (loses individual records)
SELECT 
    d.department_name,
    AVG(e.salary) as avg_salary,
    COUNT(*) as employee_count
FROM employees e
JOIN departments d ON e.department_id = d.department_id
GROUP BY d.department_name;
-- Result: Only 8 rows (one per department)

-- WINDOW FUNCTION: Keeps all rows (preserves individual records)
SELECT 
    e.first_name || ' ' || e.last_name as employee_name,
    d.department_name,
    e.salary,
    AVG(e.salary) OVER (PARTITION BY e.department_id) as dept_avg_salary,
    COUNT(*) OVER (PARTITION BY e.department_id) as dept_employee_count
FROM employees e
JOIN departments d ON e.department_id = d.department_id;
-- Result: All employee rows with their department statistics
```

**Key Insight**: Window functions let you **compare each row to its peers** without losing the original data.

---

## 🗄️ Our Database Schema (epam_practice.db)

**Before diving into window functions, let's understand our database structure:**

### **Key Tables for Window Functions:**
- **employees**: employee_id, first_name, last_name, department_id, salary, manager_id, job_title
- **departments**: department_id, department_name, manager_id, budget
- **customers**: customer_id, first_name, last_name, city, customer_segment, total_spent, is_vip
- **orders**: order_id, customer_id, order_date, total_amount, order_status
- **sales**: sale_id, rep_id, territory_id, sale_date, total_amount, commission_earned
- **sales_reps**: rep_id, rep_name, territory_id, commission_rate, quota
- **sales_territories**: territory_id, territory_name, region, target_revenue

### **Quick Schema Check:**
```sql
-- Verify our database structure
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;

-- Check record counts
SELECT 'employees' as table_name, COUNT(*) as record_count FROM employees
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'customers', COUNT(*) FROM customers
UNION ALL SELECT 'sales', COUNT(*) FROM sales;
```

---

## 🔥 Core Window Functions - Complete Guide

### 1. ROW_NUMBER() - Sequential Numbering

**Purpose**: Assigns unique sequential numbers (1, 2, 3, 4...)

```sql
-- Basic usage - Global numbering
SELECT 
    c.first_name || ' ' || c.last_name as customer_name,
    o.order_date,
    o.total_amount,
    ROW_NUMBER() OVER (ORDER BY o.order_date) as order_sequence
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.order_date
LIMIT 10;
```

**Real-World Example**: Customer order history
```sql
-- Number each customer's orders chronologically
SELECT 
    o.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    o.order_date,
    o.total_amount,
    ROW_NUMBER() OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
    ) as order_number_for_customer
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.customer_id <= 5
ORDER BY o.customer_id, o.order_date;
```

**Use Cases**:
- Pagination (LIMIT with OFFSET)
- Assigning unique IDs
- Finding first/last occurrence per group

---

### 2. RANK() - Ranking with Gaps

**Purpose**: Assigns ranks with gaps for ties (like sports rankings)

```sql
-- Rank employees by salary
SELECT 
    e.first_name || ' ' || e.last_name as employee_name,
    d.department_name,
    e.salary,
    RANK() OVER (ORDER BY e.salary DESC) as salary_rank
FROM employees e
JOIN departments d ON e.department_id = d.department_id
ORDER BY e.salary DESC
LIMIT 10;
```

**Real-World Example**: Sales leaderboard
```sql
-- Monthly sales ranking across all territories
SELECT 
    sr.rep_name,
    st.territory_name,
    SUM(s.total_amount) as monthly_sales,
    RANK() OVER (ORDER BY SUM(s.total_amount) DESC) as overall_rank,
    RANK() OVER (PARTITION BY st.territory_id ORDER BY SUM(s.total_amount) DESC) as territory_rank
FROM sales_reps sr
JOIN sales_territories st ON sr.territory_id = st.territory_id
JOIN sales s ON sr.rep_id = s.rep_id
WHERE s.sale_date >= '2024-01-01'
GROUP BY sr.rep_id, sr.rep_name, st.territory_name
ORDER BY monthly_sales DESC
LIMIT 10;
```

**Use Cases**:
- Sports rankings
- Performance rankings
- Competitive analysis

---

### 3. DENSE_RANK() - Ranking Without Gaps

**Purpose**: Assigns ranks WITHOUT gaps for ties

```sql
-- Same query as RANK, but with DENSE_RANK
SELECT 
    e.first_name || ' ' || e.last_name as employee_name,
    d.department_name,
    e.salary,
    DENSE_RANK() OVER (ORDER BY e.salary DESC) as salary_rank
FROM employees e
JOIN departments d ON e.department_id = d.department_id
ORDER BY e.salary DESC
LIMIT 10;
```

**When to use DENSE_RANK vs RANK**:
- **RANK**: When gaps make sense (sports, competitions)
- **DENSE_RANK**: When you need consecutive numbers (percentiles, quartiles)

---

### 4. LAG() and LEAD() - Time Travel Functions

**Purpose**: Access previous/next row values

#### LAG() - Look Back
```sql
-- Compare current order with previous order
SELECT 
    o.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    o.order_date,
    o.total_amount,
    LAG(o.total_amount, 1) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
    ) as previous_order_amount,
    o.total_amount - LAG(o.total_amount, 1) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
    ) as amount_change
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.customer_id <= 3
ORDER BY o.customer_id, o.order_date;
```

#### LEAD() - Look Forward
```sql
-- Compare current order with next order
SELECT 
    o.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    o.order_date,
    o.total_amount,
    LEAD(o.order_date, 1) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
    ) as next_order_date
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.customer_id <= 3
ORDER BY o.customer_id, o.order_date;
```

**Use Cases**:
- Period-over-period analysis
- Trend detection
- Customer behavior analysis
- Financial analysis (YoY, MoM comparisons)

---

### 5. FIRST_VALUE() and LAST_VALUE() - Boundary Values

**Purpose**: Get first/last value in a window

```sql
-- Get first and last order amounts for each customer
SELECT 
    o.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    o.order_date,
    o.total_amount,
    FIRST_VALUE(o.total_amount) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as first_order_amount,
    LAST_VALUE(o.total_amount) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as last_order_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.customer_id <= 3
ORDER BY o.customer_id, o.order_date;
```

**Use Cases**:
- Customer journey analysis
- Performance tracking
- Baseline comparisons

---

### 6. Aggregate Functions with OVER() - Running Calculations

**Purpose**: Calculate running totals, averages, counts, etc.

#### Running Total (Most Important!)
```sql
-- Classic running total
SELECT 
    o.order_date,
    o.total_amount,
    SUM(o.total_amount) OVER (
        ORDER BY o.order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM orders o
ORDER BY o.order_date
LIMIT 10;
```

#### Moving Average
```sql
-- 7-day moving average
SELECT 
    s.sale_date,
    s.total_amount,
    AVG(s.total_amount) OVER (
        ORDER BY s.sale_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7_days
FROM sales s
ORDER BY s.sale_date
LIMIT 10;
```

#### Running Count
```sql
-- Count orders up to each date
SELECT 
    o.order_date,
    o.total_amount,
    COUNT(*) OVER (
        ORDER BY o.order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_count
FROM orders o
ORDER BY o.order_date
LIMIT 10;
```

---

## 🔧 Supporting Functions - Essential Tools

### JULIANDAY() - Date Arithmetic

**Purpose**: Convert dates to numbers for easy arithmetic

```sql
-- Days since last order
SELECT 
    o.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    o.order_date,
    LAG(o.order_date) OVER (PARTITION BY o.customer_id ORDER BY o.order_date) as prev_order_date,
    JULIANDAY(o.order_date) - JULIANDAY(LAG(o.order_date) OVER (PARTITION BY o.customer_id ORDER BY o.order_date)) as days_since_last_order
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.customer_id <= 3
ORDER BY o.customer_id, o.order_date;
```

### ROUND() - Professional Results

**Purpose**: Round numeric values to specified decimal places

```sql
-- Rounding averages
SELECT 
    e.department_id,
    d.department_name,
    e.first_name || ' ' || e.last_name as employee_name,
    e.salary,
    AVG(e.salary) OVER (PARTITION BY e.department_id) as raw_avg,
    ROUND(AVG(e.salary) OVER (PARTITION BY e.department_id), 2) as rounded_avg
FROM employees e
JOIN departments d ON e.department_id = d.department_id
ORDER BY e.department_id, e.salary DESC;
```

### CONCAT() - String Concatenation

**Purpose**: Combine strings for readable results

```sql
-- Combine first and last names
SELECT 
    e.first_name || ' ' || e.last_name as full_name,
    d.department_name,
    e.salary,
    RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) as dept_rank
FROM employees e
JOIN departments d ON e.department_id = d.department_id
ORDER BY e.department_id, e.salary DESC;
```

---

## 🎯 PARTITION BY - The Game Changer

**PARTITION BY divides data into groups, applying window function to each group separately.**

### Without PARTITION BY (Global Window)
```sql
-- One window for entire table
SELECT 
    e.first_name || ' ' || e.last_name as employee_name,
    e.salary,
    RANK() OVER (ORDER BY e.salary DESC) as global_salary_rank
FROM employees e
ORDER BY e.salary DESC
LIMIT 10;
```

### With PARTITION BY (Grouped Windows)
```sql
-- Separate window for each department
SELECT 
    e.first_name || ' ' || e.last_name as employee_name,
    d.department_name,
    e.salary,
    RANK() OVER (
        PARTITION BY e.department_id 
        ORDER BY e.salary DESC
    ) as dept_salary_rank
FROM employees e
JOIN departments d ON e.department_id = d.department_id
ORDER BY e.department_id, e.salary DESC;
```

**Key Insight**: PARTITION BY **resets the window** for each group.

### Real-World Example: Department Analysis
```sql
-- Comprehensive department analysis
SELECT 
    e.first_name || ' ' || e.last_name as employee_name,
    d.department_name,
    e.salary,
    -- Global rankings
    RANK() OVER (ORDER BY e.salary DESC) as global_rank,
    RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) as dept_rank,
    -- Department statistics
    AVG(e.salary) OVER (PARTITION BY e.department_id) as dept_avg_salary,
    MAX(e.salary) OVER (PARTITION BY e.department_id) as dept_max_salary,
    -- Salary position within department
    e.salary - AVG(e.salary) OVER (PARTITION BY e.department_id) as salary_vs_dept_avg
FROM employees e
JOIN departments d ON e.department_id = d.department_id
ORDER BY e.department_id, e.salary DESC;
```

---

## 🔧 Frame Specifications - Advanced Control

**Frame specifications control EXACTLY which rows are included in the window.**

### Syntax
```sql
OVER (
    [PARTITION BY column]
    ORDER BY column
    {ROWS | RANGE} BETWEEN frame_start AND frame_end
)
```

### ROWS vs RANGE

**ROWS**: Physical row count (what you usually want)
```sql
-- Last 3 physical rows
AVG(amount) OVER (
    ORDER BY date 
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
```

**RANGE**: Logical value range (handles ties)
```sql
-- All rows with values within range (handles duplicate dates)
AVG(amount) OVER (
    ORDER BY date 
    RANGE BETWEEN INTERVAL '2' DAY PRECEDING AND CURRENT ROW
)
```

### Frame Boundaries Reference

| Boundary | Meaning | Example |
|----------|---------|---------|
| `UNBOUNDED PRECEDING` | Start of partition | All rows from beginning |
| `N PRECEDING` | N rows before current | Last 5 rows |
| `CURRENT ROW` | Current row | Just this row |
| `N FOLLOWING` | N rows after current | Next 3 rows |
| `UNBOUNDED FOLLOWING` | End of partition | All rows to end |

### Common Frame Patterns

#### 1. Running Total (Cumulative)
```sql
SUM(amount) OVER (
    ORDER BY date 
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

#### 2. Moving Average
```sql
-- Last 7 rows
AVG(amount) OVER (
    ORDER BY date 
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)
```

#### 3. Centered Moving Average
```sql
-- 3 before + current + 3 after
AVG(amount) OVER (
    ORDER BY date 
    ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING
)
```

---

## 🔧 CTEs (Common Table Expressions) - The WITH Clause

**Now that you understand window functions, let's learn how to use CTEs to make them more powerful and readable!**

### What are CTEs?

CTEs (Common Table Expressions) are **temporary named result sets** that exist only for the duration of a single query. Think of them as "temporary tables" that you create on-the-fly.

### Why Use CTEs with Window Functions?

1. **Break complex logic into steps** - Easier to read and debug
2. **Reuse calculations** - Define once, use multiple times
3. **EPAM loves them** - Shows advanced SQL thinking
4. **Performance** - Often more efficient than subqueries

### Basic CTE Syntax:

```sql
WITH cte_name AS (
    -- Your query here
    SELECT column1, column2
    FROM table_name
    WHERE condition
)
SELECT *
FROM cte_name
WHERE additional_condition;
```

### CTE with Window Functions - Step by Step:

**Problem**: "Find the top 3 highest-paid employees in each department"

```sql
WITH ranked_employees AS (
    SELECT 
        e.employee_id,
        e.first_name || ' ' || e.last_name as employee_name,
        e.department_id,
        d.department_name,
        e.salary,
        ROW_NUMBER() OVER (
            PARTITION BY e.department_id 
            ORDER BY e.salary DESC
        ) as dept_rank
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
)
SELECT employee_name, department_name, salary, dept_rank
FROM ranked_employees
WHERE dept_rank <= 3
ORDER BY department_name, dept_rank;
```

---

## 🎯 EPAM Interview Example - The Classic Problem

**This is THE problem EPAM asks. Master this = you're ready.**

### Problem Statement
Calculate cumulative count and cumulative sum of orders per customer.

**Given**: Our orders table with customer_id, order_date, total_amount

**Expected Output**:
```
customer_id | order_date | total_amount | order_count_history | order_value_history
------------|------------|--------------|-------------------|-------------------
201         | 2024-01-01 | 150.00       | 1                 | 150.00
201         | 2024-01-05 | 200.00       | 2                 | 350.00
201         | 2024-01-10 | 100.00       | 3                 | 450.00
202         | 2024-01-02 | 300.00       | 1                 | 300.00
202         | 2024-01-08 | 250.00       | 2                 | 550.00
```

### Solution (Master This!)
```sql
SELECT 
    o.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    o.order_date,
    o.total_amount,
    -- Cumulative count: ROW_NUMBER resets for each customer
    ROW_NUMBER() OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
    ) as order_count_history,
    -- Cumulative sum: SUM with explicit frame
    SUM(o.total_amount) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as order_value_history
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.customer_id <= 5
ORDER BY o.customer_id, o.order_date;
```

### Step-by-Step Explanation

1. **PARTITION BY o.customer_id**: Creates separate windows for each customer
2. **ORDER BY o.order_date**: Orders within each window chronologically
3. **ROW_NUMBER()**: Counts 1, 2, 3... for each customer's orders
4. **SUM() with frame**: Adds all previous values up to current row

**Practice this solution until you can write it in under 5 minutes!**

---

## 💡 Advanced Patterns and Real-World Applications

**These patterns are EPAM's favorites for testing advanced SQL skills. Master these = guaranteed interview success!**

### 1. Top N per Group - The Classic EPAM Pattern ⭐⭐⭐

**Business Scenario**: "Find the top 3 highest-performing employees in each department for our quarterly review."

```sql
WITH ranked_employees AS (
    SELECT 
        e.first_name || ' ' || e.last_name as employee_name,
        d.department_name,
        e.salary,
        ROW_NUMBER() OVER (
            PARTITION BY e.department_id 
            ORDER BY e.salary DESC
        ) as dept_rank
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
)
SELECT employee_name, department_name, salary, dept_rank
FROM ranked_employees
WHERE dept_rank <= 3
ORDER BY department_name, dept_rank;
```

### 2. Customer Churn Analysis - Gap Analysis ⭐⭐⭐

**Business Scenario**: "We need to identify customers who haven't ordered in over 30 days to trigger re-engagement campaigns."

```sql
WITH order_gaps AS (
    SELECT 
        o.customer_id,
        c.first_name || ' ' || c.last_name as customer_name,
        o.order_date,
        LAG(o.order_date) OVER (
            PARTITION BY o.customer_id 
            ORDER BY o.order_date
        ) as prev_order_date,
        JULIANDAY(o.order_date) - JULIANDAY(LAG(o.order_date) OVER (
            PARTITION BY o.customer_id 
            ORDER BY o.order_date
        )) as days_since_last_order
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
)
SELECT 
    customer_id,
    customer_name,
    order_date,
    prev_order_date,
    ROUND(days_since_last_order, 0) as days_since_last_order,
    CASE 
        WHEN days_since_last_order > 90 THEN 'High Risk'
        WHEN days_since_last_order > 30 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END as churn_risk
FROM order_gaps
WHERE days_since_last_order > 30
ORDER BY days_since_last_order DESC
LIMIT 20;
```

### 3. Performance Comparison - Benchmarking Analysis ⭐⭐⭐

**Business Scenario**: "We need to compare each employee's performance against their department average for our annual review process."

```sql
SELECT 
    e.first_name || ' ' || e.last_name as employee_name,
    d.department_name,
    e.salary,
    ROUND(AVG(e.salary) OVER (PARTITION BY e.department_id), 2) as dept_avg,
    ROUND(e.salary - AVG(e.salary) OVER (PARTITION BY e.department_id), 2) as salary_diff,
    ROUND((e.salary * 100.0 / AVG(e.salary) OVER (PARTITION BY e.department_id)) - 100, 2) as percent_vs_dept_avg
FROM employees e
JOIN departments d ON e.department_id = d.department_id
ORDER BY e.department_id, e.salary DESC;
```

---

## ⚠️ Common Mistakes and How to Avoid Them

### 1. Forgetting ORDER BY in Frame Specification
```sql
-- ✗ WRONG: No ORDER BY with frame
SUM(amount) OVER (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)

-- ✓ CORRECT: ORDER BY required with frame
SUM(amount) OVER (
    ORDER BY date 
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
```

### 2. LAST_VALUE() Without Frame Specification ⚠️ **CRITICAL**
```sql
-- ✗ WRONG: LAST_VALUE() without frame only looks at current row
SELECT 
    o.customer_id,
    o.order_date,
    o.total_amount,
    LAST_VALUE(o.total_amount) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
    ) as last_value  -- This is WRONG! Shows current row, not last row
FROM orders o;

-- ✓ CORRECT: LAST_VALUE() needs frame to see entire partition
SELECT 
    o.customer_id,
    o.order_date,
    o.total_amount,
    LAST_VALUE(o.total_amount) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as last_value  -- This shows actual last row in partition
FROM orders o;
```

### 3. Missing PARTITION BY When Needed
```sql
-- ✗ WRONG: Global ranking when you want per-group
SELECT *, RANK() OVER (ORDER BY sales DESC) as rank FROM sales_by_region;

-- ✓ CORRECT: Separate ranking per region
SELECT *, RANK() OVER (PARTITION BY region ORDER BY sales DESC) as region_rank FROM sales_by_region;
```

---

## 🎯 Interview Success Tips

### 1. Explain Your Thought Process
When solving window function problems:

1. **Identify the pattern**: "This looks like a running total problem"
2. **Choose the function**: "I need SUM() with OVER()"
3. **Determine partitioning**: "Do I need PARTITION BY? Yes, per customer"
4. **Set the ordering**: "ORDER BY date for chronological order"
5. **Define the frame**: "ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW"

### 2. Start Simple, Then Add Complexity
```sql
-- Step 1: Basic window function
SELECT *, SUM(total_amount) OVER (ORDER BY order_date) as running_total FROM orders;

-- Step 2: Add partitioning
SELECT *, SUM(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date) as running_total FROM orders;

-- Step 3: Add explicit frame
SELECT *, SUM(total_amount) OVER (
    PARTITION BY customer_id 
    ORDER BY order_date 
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
) as running_total FROM orders;
```

### 3. Test with Sample Data
Always test your solution with the provided sample data:
```sql
-- Test your solution
SELECT 
    o.customer_id,
    o.order_date,
    o.total_amount,
    ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.order_date) as count_history,
    SUM(o.total_amount) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as value_history
FROM orders o
WHERE o.customer_id <= 3
ORDER BY o.customer_id, o.order_date;
```

---

## 📚 Quick Reference Cheat Sheet

### Window Function Syntax
```sql
FUNCTION() OVER (
    [PARTITION BY column1, column2]
    ORDER BY column [ASC|DESC]
    [ROWS | RANGE] BETWEEN start AND end
)
```

### Common Functions
- `ROW_NUMBER()` - Sequential numbering (1, 2, 3...)
- `RANK()` - Ranking with gaps
- `DENSE_RANK()` - Ranking without gaps
- `LAG(column, n)` - Previous row value
- `LEAD(column, n)` - Next row value
- `FIRST_VALUE(column)` - First value in window
- `LAST_VALUE(column)` - **NEEDS FRAME!** Use `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`
- `SUM/AVG/COUNT/MIN/MAX(column)` - Aggregates

### Frame Boundaries
- `UNBOUNDED PRECEDING` - Start of partition
- `N PRECEDING` - N rows before
- `CURRENT ROW` - Current row
- `N FOLLOWING` - N rows after
- `UNBOUNDED FOLLOWING` - End of partition

### EPAM Interview Template
```sql
-- For cumulative problems:
SELECT 
    [columns],
    ROW_NUMBER() OVER (PARTITION BY [group] ORDER BY [date]) as count_history,
    SUM([value]) OVER (
        PARTITION BY [group] 
        ORDER BY [date]
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as value_history
FROM [table]
ORDER BY [group], [date];
```

---

## 🎯 Next Steps

1. **Practice the EPAM cumulative problem** until you can solve it in < 10 minutes
2. **Complete all exercises** in `01_SQL/exercises/02_Window_Functions_Exercises.md`
3. **Review solutions** only after attempting
4. **Move to**: Advanced JOINs and Query Optimization

**You're now ready to master EPAM's favorite SQL topic!** 🚀

---

**Key Takeaway**: Window functions are about **comparing rows to their peers** without losing the original data. Master PARTITION BY and frame specifications, and you'll solve any cumulative problem EPAM throws at you.

**Next Module**: `01_SQL/03_Advanced_JOINs.md`

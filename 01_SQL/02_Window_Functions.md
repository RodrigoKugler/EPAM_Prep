olum# SQL Window Functions - Complete Mastery Guide

## 🎯 Learning Objectives

By the end of this module, you will be able to:
- **Master all window functions** (ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, FIRST_VALUE, LAST_VALUE)
- **Understand PARTITION BY** and use it effectively
- **Control frame specifications** (ROWS vs RANGE, boundaries)
- **Solve EPAM's favorite cumulative problems** in under 10 minutes
- **Apply window functions** to real business scenarios
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
    department,
    AVG(salary) as avg_salary,
    COUNT(*) as employee_count
FROM employees
GROUP BY department;
-- Result: Only 3 rows (one per department)

-- WINDOW FUNCTION: Keeps all rows (preserves individual records)
SELECT 
    employee_name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg_salary,
    COUNT(*) OVER (PARTITION BY department) as dept_employee_count
FROM employees;
-- Result: All employee rows with their department statistics
```

**Key Insight**: Window functions let you **compare each row to its peers** without losing the original data.

---

## 🔥 Core Window Functions - Complete Guide

### 1. ROW_NUMBER() - Sequential Numbering

**Purpose**: Assigns unique sequential numbers (1, 2, 3, 4...)

```sql
-- Basic usage
SELECT 
    customer_name,
    order_date,
    order_amount,
    ROW_NUMBER() OVER (ORDER BY order_date) as order_sequence
FROM orders;
```

**Real-World Example**: Customer order history
```sql
-- Number each customer's orders chronologically
SELECT 
    customer_id,
    order_date,
    order_amount,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as order_number_for_customer
FROM orders;
```

**Result**:
| customer_id | order_date | order_amount | order_number_for_customer |
|-------------|------------|--------------|---------------------------|
| A | 2024-01-01 | 100 | 1 |
| A | 2024-01-15 | 150 | 2 |
| A | 2024-02-01 | 200 | 3 |
| B | 2024-01-05 | 75 | 1 |
| B | 2024-01-20 | 125 | 2 |

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
    employee_name,
    department,
    salary,
    RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;
```

**Example Results**:
| employee_name | department | salary | salary_rank |
|---------------|------------|--------|-------------|
| Alice | Sales | 100000 | 1 |
| Bob | IT | 100000 | 1 |
| Charlie | Sales | 95000 | 3 | ← Gap! (no rank 2) |
| Dave | IT | 90000 | 4 |

**Real-World Example**: Sales leaderboard
```sql
-- Monthly sales ranking across all regions
SELECT 
    sales_rep_name,
    region,
    monthly_sales,
    RANK() OVER (ORDER BY monthly_sales DESC) as overall_rank,
    RANK() OVER (PARTITION BY region ORDER BY monthly_sales DESC) as region_rank
FROM monthly_sales;
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
    employee_name,
    department,
    salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;
```

**Example Results**:
| employee_name | department | salary | salary_rank |
|---------------|------------|--------|-------------|
| Alice | Sales | 100000 | 1 |
| Bob | IT | 100000 | 1 |
| Charlie | Sales | 95000 | 2 | ← No gap! |
| Dave | IT | 90000 | 3 |

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
    customer_id,
    order_date,
    order_amount,
    LAG(order_amount, 1) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as previous_order_amount,
    order_amount - LAG(order_amount, 1) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as amount_change
FROM orders;
```

#### LEAD() - Look Forward
```sql
-- Compare current order with next order
SELECT 
    customer_id,
    order_date,
    order_amount,
    LEAD(order_date, 1) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as next_order_date,
    JULIANDAY(LEAD(order_date, 1) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    )) - JULIANDAY(order_date) as days_until_next_order
FROM orders;
```

**Real-World Example**: Customer behavior analysis
```sql
-- Analyze customer order patterns
SELECT 
    customer_id,
    order_date,
    order_amount,
    -- Previous order info
    LAG(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_amount,
    LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_date,
    -- Calculate metrics
    order_amount - LAG(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date) as amount_growth,
    JULIANDAY(order_date) - JULIANDAY(LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)) as days_since_last_order
FROM orders
WHERE customer_id = 'A';
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
    customer_id,
    order_date,
    order_amount,
    FIRST_VALUE(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as first_order_amount,
    LAST_VALUE(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as last_order_amount
FROM orders;
```

**Real-World Example**: Customer journey analysis
```sql
-- Track customer value progression
SELECT 
    customer_id,
    order_date,
    order_amount,
    FIRST_VALUE(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as first_purchase,
    LAST_VALUE(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as latest_purchase,
    -- Calculate growth
    order_amount - FIRST_VALUE(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as growth_from_first
FROM orders;
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
    order_date,
    order_amount,
    SUM(order_amount) OVER (
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM orders;
```

#### Moving Average
```sql
-- 7-day moving average
SELECT 
    order_date,
    order_amount,
    AVG(order_amount) OVER (
        ORDER BY order_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7_days
FROM orders;
```

#### Running Count
```sql
-- Count orders up to each date
SELECT 
    order_date,
    order_amount,
    COUNT(*) OVER (
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_count
FROM orders;
```

**Real-World Example**: Financial dashboard
```sql
-- Monthly financial metrics
SELECT 
    month,
    revenue,
    -- Running totals
    SUM(revenue) OVER (ORDER BY month) as cumulative_revenue,
    AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg_3_months,
    -- Percent of total
    revenue * 100.0 / SUM(revenue) OVER () as percent_of_total
FROM monthly_financials;
```

---

## 🎯 PARTITION BY - The Game Changer

**PARTITION BY divides data into groups, applying window function to each group separately.**

### Without PARTITION BY (Global Window)
```sql
-- One window for entire table
SELECT 
    employee_name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as global_salary_rank
FROM employees;
```

### With PARTITION BY (Grouped Windows)
```sql
-- Separate window for each department
SELECT 
    employee_name,
    department,
    salary,
    RANK() OVER (
        PARTITION BY department 
        ORDER BY salary DESC
    ) as dept_salary_rank
FROM employees;
```

**Result Comparison**:
| employee_name | department | salary | global_rank | dept_rank |
|---------------|------------|--------|-------------|-----------|
| Alice | Sales | 100000 | 1 | 1 |
| Bob | IT | 110000 | 1 | 1 |
| Charlie | Sales | 95000 | 3 | 2 |
| Dave | IT | 105000 | 2 | 2 |

**Key Insight**: PARTITION BY **resets the window** for each group.

### Real-World Example: Department Analysis
```sql
-- Comprehensive department analysis
SELECT 
    employee_name,
    department,
    salary,
    -- Global rankings
    RANK() OVER (ORDER BY salary DESC) as global_rank,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank,
    -- Department statistics
    AVG(salary) OVER (PARTITION BY department) as dept_avg_salary,
    MAX(salary) OVER (PARTITION BY department) as dept_max_salary,
    -- Salary position within department
    salary - AVG(salary) OVER (PARTITION BY department) as salary_vs_dept_avg,
    -- Percentile within department
    NTILE(4) OVER (PARTITION BY department ORDER BY salary DESC) as dept_quartile
FROM employees;
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

-- Last 30 days (if daily data)
AVG(amount) OVER (
    ORDER BY date 
    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
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

#### 4. Future Cumulative (Reverse Running Total)
```sql
-- From current to end
SUM(amount) OVER (
    ORDER BY date 
    ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
)
```

#### 5. Rolling Window
```sql
-- Last 12 months
SUM(amount) OVER (
    ORDER BY date 
    ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
)
```

---

## 🎯 EPAM Interview Example - The Classic Problem

**This is THE problem EPAM asks. Master this = you're ready.**

### Problem Statement
Calculate cumulative count and cumulative sum of orders per customer.

**Given**:
```sql
-- Orders table
+-----+------------+--------------+---------------+
| cid |  order_id  |  order_date  |  order_value  |
+-----+------------+--------------+---------------+
|  A  |   qwerty   |     1-Jan    |      10       |
|  A  |   asdfgh   |     3-Jan    |      20       |
|  A  |   zxcvbn   |     10-Jan   |      30       |
|  B  |   uiopyy   |     2-Jan    |      40       |
|  B  |   lkjhgf   |     6-Jan    |      50       |
|  B  |   mnbvcx   |     8-Jan    |      60       |
|  B  |   rtyfgh   |     10-Jan   |      70       |
|  C  |   fghcvb   |     1-Feb    |      80       |
|  C  |   bnmghj   |     1-Feb    |      90       |
|  C  |   wersdf   |     3-Feb    |      100      |
|  C  |   asdzxc   |     4-Feb    |      110      |
+-----+------------+--------------+---------------+
```

**Expected Output**:
```sql
+-----+------------+--------------+---------------+---------------------+---------------------+
| cid |  order_id  |  order_date  |  order_value  | order_count_history | order_value_history |
+-----+------------+--------------+---------------+---------------------+---------------------+
|  A  |   qwerty   |     1-Jan    |      10       |         1           |         10          |
|  A  |   asdfgh   |     3-Jan    |      20       |         2           |         30          |
|  A  |   zxcvbn   |     10-Jan   |      30       |         3           |         60          |
|  B  |   uiopyy   |     2-Jan    |      40       |         1           |         40          |
|  B  |   lkjhgf   |     6-Jan    |      50       |         2           |         90          |
|  B  |   mnbvcx   |     8-Jan    |      60       |         3           |         150         |
|  B  |   rtyfgh   |     10-Jan   |      70       |         4           |         220         |
|  C  |   fghcvb   |     1-Feb    |      80       |         1           |         80          |
|  C  |   bnmghj   |     1-Feb    |      90       |         2           |         170         |
|  C  |   wersdf   |     3-Feb    |      100      |         3           |         270         |
|  C  |   asdzxc   |     4-Feb    |      110      |         4           |         380         |
+-----+------------+--------------+---------------+---------------------+---------------------+
```

### Solution (Master This!)
```sql
SELECT 
    cid,
    order_id,
    order_date,
    order_value,
    -- Cumulative count: ROW_NUMBER resets for each customer
    ROW_NUMBER() OVER (
        PARTITION BY cid 
        ORDER BY order_date
    ) as order_count_history,
    -- Cumulative sum: SUM with explicit frame
    SUM(order_value) OVER (
        PARTITION BY cid 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as order_value_history
FROM orders
ORDER BY cid, order_date;
```

### Step-by-Step Explanation

1. **PARTITION BY cid**: Creates separate windows for each customer
2. **ORDER BY order_date**: Orders within each window chronologically
3. **ROW_NUMBER()**: Counts 1, 2, 3... for each customer's orders
4. **SUM() with frame**: Adds all previous values up to current row

### Why This Works
- **PARTITION BY cid**: Resets counters for each customer
- **ORDER BY order_date**: Ensures chronological order
- **ROW_NUMBER()**: Gives sequential count (1, 2, 3...)
- **SUM() with ROWS BETWEEN**: Creates running total

**Practice this solution until you can write it in under 5 minutes!**

---

## 💡 Advanced Patterns and Real-World Applications

### 1. Top N per Group
```sql
-- Top 3 highest-paid employees in each department
WITH ranked_employees AS (
    SELECT 
        employee_name,
        department,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department 
            ORDER BY salary DESC
        ) as dept_rank
    FROM employees
)
SELECT employee_name, department, salary
FROM ranked_employees
WHERE dept_rank <= 3;
```

### 2. Percentile Analysis
```sql
-- Salary quartiles within departments
SELECT 
    employee_name,
    department,
    salary,
    NTILE(4) OVER (
        PARTITION BY department 
        ORDER BY salary DESC
    ) as salary_quartile
FROM employees;
-- 1 = top 25%, 4 = bottom 25%
```

### 3. Gap Analysis
```sql
-- Find gaps in order sequences
WITH order_gaps AS (
    SELECT 
        customer_id,
        order_date,
        LAG(order_date) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date
        ) as prev_order_date,
        JULIANDAY(order_date) - JULIANDAY(LAG(order_date) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date
        )) as days_since_last_order
    FROM orders
)
SELECT *
FROM order_gaps
WHERE days_since_last_order > 30;  -- Gaps > 30 days
```

### 4. Performance Comparison
```sql
-- Compare each employee to department average
SELECT 
    employee_name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department) as salary_diff,
    (salary * 100.0 / AVG(salary) OVER (PARTITION BY department)) - 100 as percent_vs_dept_avg
FROM employees;
```

### 5. Trend Analysis
```sql
-- Month-over-month growth
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(order_amount) as monthly_total
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
    month,
    monthly_total,
    LAG(monthly_total, 1) OVER (ORDER BY month) as prev_month,
    monthly_total - LAG(monthly_total, 1) OVER (ORDER BY month) as growth,
    (monthly_total * 100.0 / LAG(monthly_total, 1) OVER (ORDER BY month)) - 100 as growth_percent
FROM monthly_sales;
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

### 2. Using Wrong Frame Default
```sql
-- ⚠️ DANGEROUS: Default might not be what you expect
SUM(amount) OVER (ORDER BY date)
-- Default: RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
-- This handles ties differently than ROWS!

-- ✓ EXPLICIT: Be clear about what you want
SUM(amount) OVER (
    ORDER BY date 
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

### 3. Confusing RANK vs DENSE_RANK
```sql
-- Use RANK for sports-style rankings (with gaps)
SELECT *, RANK() OVER (ORDER BY score DESC) as position FROM players;

-- Use DENSE_RANK for consecutive numbering
SELECT *, DENSE_RANK() OVER (ORDER BY score DESC) as position FROM players;
```

### 4. Performance Issues with Large Windows
```sql
-- ⚠️ SLOW: Large unbounded windows
SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

-- ✓ FASTER: Limited windows when possible
SUM(amount) OVER (ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)
```

### 5. Missing PARTITION BY When Needed
```sql
-- ✗ WRONG: Global ranking when you want per-group
SELECT *, RANK() OVER (ORDER BY sales DESC) as rank FROM sales_by_region;

-- ✓ CORRECT: Separate ranking per region
SELECT *, RANK() OVER (PARTITION BY region ORDER BY sales DESC) as region_rank FROM sales_by_region;
```

---

## 🚀 Performance Optimization Tips

### 1. Use Appropriate Frame Sizes
```sql
-- Good: Limited window
AVG(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)

-- Avoid: Unbounded windows on large datasets
AVG(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

### 2. Index Your ORDER BY Columns
```sql
-- Create index for better window function performance
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
```

### 3. Consider Alternatives for Simple Cases
```sql
-- For simple running totals, sometimes a self-join is faster
SELECT 
    o1.order_date,
    o1.amount,
    SUM(o2.amount) as running_total
FROM orders o1
JOIN orders o2 ON o2.order_date <= o1.order_date
GROUP BY o1.order_date, o1.amount
ORDER BY o1.order_date;
```

### 4. Use CTEs for Complex Window Functions
```sql
-- Break complex queries into steps
WITH customer_totals AS (
    SELECT 
        customer_id,
        SUM(order_amount) as total_spent
    FROM orders
    GROUP BY customer_id
),
customer_ranked AS (
    SELECT 
        customer_id,
        total_spent,
        RANK() OVER (ORDER BY total_spent DESC) as spending_rank
    FROM customer_totals
)
SELECT * FROM customer_ranked WHERE spending_rank <= 10;
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
SELECT *, SUM(amount) OVER (ORDER BY date) as running_total FROM orders;

-- Step 2: Add partitioning
SELECT *, SUM(amount) OVER (PARTITION BY customer ORDER BY date) as running_total FROM orders;

-- Step 3: Add explicit frame
SELECT *, SUM(amount) OVER (
    PARTITION BY customer 
    ORDER BY date 
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
) as running_total FROM orders;
```

### 3. Test with Sample Data
Always test your solution with the provided sample data:
```sql
-- Test your solution
SELECT 
    cid,
    order_id,
    order_date,
    order_value,
    ROW_NUMBER() OVER (PARTITION BY cid ORDER BY order_date) as count_history,
    SUM(order_value) OVER (
        PARTITION BY cid 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as value_history
FROM orders
ORDER BY cid, order_date;
```

### 4. Know the EPAM Patterns
- **Running totals**: SUM() with OVER()
- **Sequential numbering**: ROW_NUMBER()
- **Ranking within groups**: RANK() with PARTITION BY
- **Period comparisons**: LAG()/LEAD()
- **Moving averages**: AVG() with ROWS BETWEEN

---

## 🏋️ Practice Exercises

**See**: `01_SQL/exercises/02_Window_Functions_Exercises.md`

**Master these patterns**:
1. ✅ Running totals (EPAM favorite!)
2. ✅ Moving averages
3. ✅ Ranking within groups
4. ✅ Period-over-period comparisons
5. ✅ Top N per group
6. ✅ Gap analysis
7. ✅ Percentile calculations
8. ✅ Performance comparisons

**Target Time**: Solve cumulative problems in < 10 minutes

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
- `LAST_VALUE(column)` - Last value in window
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
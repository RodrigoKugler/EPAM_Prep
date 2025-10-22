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

## 🔧 CTEs (Common Table Expressions) - The WITH Clause

**Before diving into window functions, you need to understand CTEs. They're essential for complex queries and EPAM interviews!**

### **What are CTEs?**

CTEs (Common Table Expressions) are **temporary named result sets** that exist only for the duration of a single query. Think of them as "temporary tables" that you create on-the-fly.

### **Why Use CTEs with Window Functions?**

1. **Break complex logic into steps** - Easier to read and debug
2. **Reuse calculations** - Define once, use multiple times
3. **EPAM loves them** - Shows advanced SQL thinking
4. **Performance** - Often more efficient than subqueries

### **Basic CTE Syntax:**

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

### **CTE with Window Functions - Step by Step:**

**Problem**: "Find the top 3 highest-paid employees in each department"

**Step 1: Create the CTE with Window Function**
```sql
WITH ranked_employees AS (
    SELECT 
        employee_id,
        CONCAT(first_name, ' ', last_name) as employee_name,
        department_id,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department_id 
            ORDER BY salary DESC
        ) as dept_rank
    FROM employees
)
-- CTE is now available for use
```

**Step 2: Use the CTE in Main Query**
```sql
WITH ranked_employees AS (
    SELECT 
        employee_id,
        CONCAT(first_name, ' ', last_name) as employee_name,
        department_id,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department_id 
            ORDER BY salary DESC
        ) as dept_rank
    FROM employees
)
SELECT employee_name, department_id, salary, dept_rank
FROM ranked_employees
WHERE dept_rank <= 3
ORDER BY department_id, dept_rank;
```

### **Multiple CTEs (Chained CTEs):**

```sql
-- You can have multiple CTEs
WITH 
-- First CTE: Calculate rankings
ranked_employees AS (
    SELECT 
        employee_id,
        CONCAT(first_name, ' ', last_name) as employee_name,
        department_id,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department_id 
            ORDER BY salary DESC
        ) as dept_rank
    FROM employees
),
-- Second CTE: Filter top 3
top_performers AS (
    SELECT *
    FROM ranked_employees
    WHERE dept_rank <= 3
)
-- Main query: Add final formatting
SELECT 
    employee_name,
    department_id,
    salary,
    dept_rank,
    'Top ' || dept_rank || ' in Department' as performance_status
FROM top_performers
ORDER BY department_id, dept_rank;
```

### **CTE vs Subquery Comparison:**

**Subquery (Harder to Read):**
```sql
SELECT employee_name, department_id, salary
FROM (
    SELECT 
        CONCAT(first_name, ' ', last_name) as employee_name,
        department_id,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department_id 
            ORDER BY salary DESC
        ) as dept_rank
    FROM employees
) ranked_employees
WHERE dept_rank <= 3;
```

**CTE (Easier to Read):**
```sql
WITH ranked_employees AS (
    SELECT 
        CONCAT(first_name, ' ', last_name) as employee_name,
        department_id,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department_id 
            ORDER BY salary DESC
        ) as dept_rank
    FROM employees
)
SELECT employee_name, department_id, salary
FROM ranked_employees
WHERE dept_rank <= 3;
```

### **CTE Best Practices:**

1. **Use descriptive names** - `ranked_employees` not `cte1`
2. **One concept per CTE** - Don't mix too many calculations
3. **Order logically** - Most specific CTEs first
4. **Test incrementally** - Run each CTE separately first

### **Common CTE Patterns with Window Functions:**

#### **Pattern 1: Ranking + Filtering**
```sql
WITH ranked_data AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY group ORDER BY value DESC) as rank
    FROM table_name
)
SELECT * FROM ranked_data WHERE rank <= 3;
```

#### **Pattern 2: Calculations + Aggregations**
```sql
WITH calculated_data AS (
    SELECT *, 
           LAG(value) OVER (PARTITION BY group ORDER BY date) as prev_value,
           value - LAG(value) OVER (PARTITION BY group ORDER BY date) as change
    FROM table_name
)
SELECT group, AVG(change) as avg_change
FROM calculated_data
GROUP BY group;
```

#### **Pattern 3: Multiple Window Functions**
```sql
WITH multi_calculations AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY group ORDER BY value DESC) as rank,
           AVG(value) OVER (PARTITION BY group) as group_avg,
           LAG(value) OVER (PARTITION BY group ORDER BY date) as prev_value
    FROM table_name
)
SELECT * FROM multi_calculations WHERE rank <= 5;
```

### **EPAM Interview Tips for CTEs:**

1. **Always explain your approach** - "I'll use a CTE to break this into steps"
2. **Name CTEs meaningfully** - Shows you understand the data
3. **Test each step** - "Let me verify this CTE works first"
4. **Consider performance** - CTEs can be more efficient than subqueries

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

**These patterns are EPAM's favorites for testing advanced SQL skills. Master these = guaranteed interview success!**

---

### 1. Top N per Group - The Classic EPAM Pattern ⭐⭐⭐

**Business Scenario**: "Find the top 3 highest-performing employees in each department for our quarterly review."

#### **The Problem:**
- Need to rank employees within each department
- Get only the top 3 from each department
- Preserve all employee data for analysis

#### **Step-by-Step Solution:**

**Step 1: Create Rankings with Window Functions**
```sql
-- Use ROW_NUMBER() for unique rankings (no ties)
WITH ranked_employees AS (
    SELECT 
        CONCAT(first_name, ' ', last_name) as employee_name,
        department_id,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department_id 
            ORDER BY salary DESC
        ) as dept_rank
    FROM employees
)
SELECT employee_name, department_id, salary, dept_rank
FROM ranked_employees
WHERE dept_rank <= 3
ORDER BY department_id, dept_rank;
```

**Step 2: Handle Ties with RANK() (Alternative)**
```sql
-- Use RANK() if you want to handle ties differently
WITH ranked_employees AS (
    SELECT 
        CONCAT(first_name, ' ', last_name) as employee_name,
        department_id,
        salary,
        RANK() OVER (
            PARTITION BY department_id 
            ORDER BY salary DESC
        ) as dept_rank
    FROM employees
)
SELECT employee_name, department_id, salary, dept_rank
FROM ranked_employees
WHERE dept_rank <= 3
ORDER BY department_id, dept_rank;
```

#### **Key Concepts:**
- **PARTITION BY department_id**: Separate rankings per department
- **ORDER BY salary DESC**: Highest salary = rank 1
- **ROW_NUMBER() vs RANK()**: ROW_NUMBER() gives unique ranks, RANK() handles ties
- **CTE Pattern**: Clean, readable query structure

#### **Real-World Applications:**
- **HR Analytics**: Top performers per department
- **Sales Management**: Best sales reps per region
- **Customer Analysis**: Highest-spending customers per segment
- **Product Analysis**: Best-selling products per category

---

### 2. Percentile Analysis - Statistical Insights ⭐⭐⭐

**Business Scenario**: "We need to categorize our employees into performance quartiles for compensation planning."

#### **The Problem:**
- Divide employees into equal groups (quartiles, deciles, etc.)
- Each group should have roughly the same number of employees
- Need to understand distribution within departments

#### **Comprehensive Solution:**

**Basic Quartile Analysis:**
```sql
-- Salary quartiles within departments
SELECT 
    CONCAT(first_name, ' ', last_name) as employee_name,
    department_id,
    salary,
    NTILE(4) OVER (
        PARTITION BY department_id 
        ORDER BY salary DESC
    ) as salary_quartile,
    -- Add context
    COUNT(*) OVER (PARTITION BY department_id) as dept_size,
    AVG(salary) OVER (PARTITION BY department_id) as dept_avg_salary
FROM employees
ORDER BY department_id, salary_quartile, salary DESC;
```

**Advanced Percentile Analysis:**
```sql
-- Comprehensive percentile analysis
WITH percentile_analysis AS (
    SELECT 
        CONCAT(first_name, ' ', last_name) as employee_name,
        department_id,
        salary,
        -- Quartiles
        NTILE(4) OVER (PARTITION BY department_id ORDER BY salary DESC) as quartile,
        -- Deciles
        NTILE(10) OVER (PARTITION BY department_id ORDER BY salary DESC) as decile,
        -- Percentiles
        PERCENT_RANK() OVER (PARTITION BY department_id ORDER BY salary) * 100 as percentile,
        -- Department statistics
        AVG(salary) OVER (PARTITION BY department_id) as dept_avg,
        MIN(salary) OVER (PARTITION BY department_id) as dept_min,
        MAX(salary) OVER (PARTITION BY department_id) as dept_max
    FROM employees
)
SELECT 
    employee_name,
    department_id,
    salary,
    quartile,
    decile,
    ROUND(percentile, 2) as percentile,
    ROUND(salary - dept_avg, 2) as salary_vs_avg,
    CASE 
        WHEN quartile = 1 THEN 'Top 25%'
        WHEN quartile = 2 THEN '25-50%'
        WHEN quartile = 3 THEN '50-75%'
        ELSE 'Bottom 25%'
    END as performance_tier
FROM percentile_analysis
ORDER BY department_id, quartile, salary DESC;
```

#### **Key Concepts:**
- **NTILE(n)**: Divides into n equal groups
- **PERCENT_RANK()**: Returns percentile (0-1, multiply by 100 for percentage)
- **PARTITION BY**: Separate analysis per department
- **CASE statements**: Add business context

#### **Real-World Applications:**
- **Compensation Planning**: Salary quartiles for raises
- **Performance Management**: Employee performance tiers
- **Customer Segmentation**: Value-based customer groups
- **Risk Assessment**: Credit score percentiles

---

### 3. Gap Analysis - Finding Patterns in Time Series ⭐⭐⭐

**Business Scenario**: "We need to identify customers who haven't ordered in over 30 days to trigger re-engagement campaigns."

#### **The Problem:**
- Find gaps in customer order sequences
- Identify customers at risk of churning
- Calculate time between orders

#### **Comprehensive Solution:**

**Basic Gap Analysis:**
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
SELECT 
    customer_id,
    order_date,
    prev_order_date,
    days_since_last_order,
    CASE 
        WHEN days_since_last_order > 90 THEN 'High Risk'
        WHEN days_since_last_order > 30 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END as churn_risk
FROM order_gaps
WHERE days_since_last_order > 30  -- Gaps > 30 days
ORDER BY days_since_last_order DESC;
```

**Advanced Gap Analysis with Customer Context:**
```sql
-- Comprehensive gap analysis with customer insights
WITH customer_order_analysis AS (
    SELECT 
        o.customer_id,
        c.first_name,
        c.last_name,
        o.order_date,
        o.total_amount,
        LAG(o.order_date) OVER (
            PARTITION BY o.customer_id 
            ORDER BY o.order_date
        ) as prev_order_date,
        LAG(o.total_amount) OVER (
            PARTITION BY o.customer_id 
            ORDER BY o.order_date
        ) as prev_order_amount,
        JULIANDAY(o.order_date) - JULIANDAY(LAG(o.order_date) OVER (
            PARTITION BY o.customer_id 
            ORDER BY o.order_date
        )) as days_since_last_order,
        -- Customer statistics
        COUNT(*) OVER (PARTITION BY o.customer_id) as total_orders,
        AVG(o.total_amount) OVER (PARTITION BY o.customer_id) as avg_order_value,
        SUM(o.total_amount) OVER (PARTITION BY o.customer_id) as lifetime_value
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
),
gap_analysis AS (
    SELECT 
        customer_id,
        first_name,
        last_name,
        order_date,
        total_amount,
        prev_order_date,
        prev_order_amount,
        days_since_last_order,
        total_orders,
        avg_order_value,
        lifetime_value,
        -- Gap analysis
        CASE 
            WHEN days_since_last_order > 90 THEN 'High Risk'
            WHEN days_since_last_order > 30 THEN 'Medium Risk'
            ELSE 'Low Risk'
        END as churn_risk,
        -- Order value change
        total_amount - prev_order_amount as order_value_change
    FROM customer_order_analysis
    WHERE days_since_last_order > 30
)
SELECT 
    customer_id,
    CONCAT(first_name, ' ', last_name) as customer_name,
    order_date,
    total_amount,
    days_since_last_order,
    churn_risk,
    total_orders,
    ROUND(avg_order_value, 2) as avg_order_value,
    ROUND(lifetime_value, 2) as lifetime_value,
    ROUND(order_value_change, 2) as order_value_change
FROM gap_analysis
ORDER BY days_since_last_order DESC, lifetime_value DESC;
```

#### **Key Concepts:**
- **LAG() function**: Access previous row values
- **JULIANDAY()**: Calculate date differences
- **PARTITION BY**: Separate analysis per customer
- **CASE statements**: Categorize risk levels
- **CTEs**: Break complex queries into steps

#### **Real-World Applications:**
- **Customer Retention**: Identify at-risk customers
- **Inventory Management**: Find gaps in product sales
- **Employee Analysis**: Track attendance patterns
- **Financial Analysis**: Identify payment gaps

---

### 4. Performance Comparison - Benchmarking Analysis ⭐⭐⭐

**Business Scenario**: "We need to compare each employee's performance against their department average for our annual review process."

#### **The Problem:**
- Compare individual performance to group averages
- Calculate percentage differences
- Identify over/under performers

#### **Comprehensive Solution:**

**Basic Performance Comparison:**
```sql
-- Compare each employee to department average
SELECT 
    CONCAT(first_name, ' ', last_name) as employee_name,
    department_id,
    salary,
    AVG(salary) OVER (PARTITION BY department_id) as dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department_id) as salary_diff,
    ROUND((salary * 100.0 / AVG(salary) OVER (PARTITION BY department_id)) - 100, 2) as percent_vs_dept_avg
FROM employees
ORDER BY department_id, salary DESC;
```

**Advanced Performance Analysis:**
```sql
-- Comprehensive performance analysis
WITH department_stats AS (
    SELECT 
        department_id,
        AVG(salary) as dept_avg,
        MIN(salary) as dept_min,
        MAX(salary) as dept_max,
        COUNT(*) as dept_size,
        STDDEV(salary) as dept_stddev
    FROM employees
    GROUP BY department_id
),
employee_analysis AS (
    SELECT 
        e.employee_id,
        CONCAT(e.first_name, ' ', e.last_name) as employee_name,
        e.department_id,
        e.salary,
        d.dept_avg,
        d.dept_min,
        d.dept_max,
        d.dept_size,
        d.dept_stddev,
        -- Performance metrics
        e.salary - d.dept_avg as salary_diff,
        ROUND((e.salary * 100.0 / d.dept_avg) - 100, 2) as percent_vs_avg,
        ROUND((e.salary - d.dept_min) * 100.0 / (d.dept_max - d.dept_min), 2) as percentile_in_dept,
        -- Z-score (how many standard deviations from mean)
        ROUND((e.salary - d.dept_avg) / d.dept_stddev, 2) as z_score,
        -- Performance tier
        CASE 
            WHEN e.salary > d.dept_max * 0.9 THEN 'Top 10%'
            WHEN e.salary > d.dept_avg * 1.1 THEN 'Above Average'
            WHEN e.salary > d.dept_avg * 0.9 THEN 'Average'
            ELSE 'Below Average'
        END as performance_tier
    FROM employees e
    JOIN department_stats d ON e.department_id = d.department_id
)
SELECT 
    employee_name,
    department_id,
    salary,
    ROUND(dept_avg, 2) as dept_avg,
    ROUND(salary_diff, 2) as salary_diff,
    percent_vs_avg || '%' as percent_vs_avg,
    percentile_in_dept || '%' as percentile_in_dept,
    z_score,
    performance_tier,
    dept_size
FROM employee_analysis
ORDER BY department_id, salary DESC;
```

#### **Key Concepts:**
- **Window functions with aggregates**: AVG() OVER (PARTITION BY)
- **Mathematical calculations**: Percentage differences, z-scores
- **CASE statements**: Performance categorization
- **Statistical analysis**: Standard deviation, percentiles

#### **Real-World Applications:**
- **Performance Reviews**: Employee vs department benchmarks
- **Sales Analysis**: Rep performance vs team average
- **Financial Analysis**: Department budget vs actual spending
- **Quality Control**: Product quality vs standards

---

### 5. Trend Analysis - Time Series Intelligence ⭐⭐⭐

**Business Scenario**: "We need to analyze month-over-month growth trends to identify seasonal patterns and forecast future performance."

#### **The Problem:**
- Calculate period-over-period changes
- Identify growth trends
- Handle seasonal variations

#### **Comprehensive Solution:**

**Basic Trend Analysis:**
```sql
-- Month-over-month growth
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(total_amount) as monthly_total,
        COUNT(*) as order_count
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
),
trend_analysis AS (
    SELECT 
        month,
        monthly_total,
        order_count,
        LAG(monthly_total, 1) OVER (ORDER BY month) as prev_month_total,
        LAG(order_count, 1) OVER (ORDER BY month) as prev_month_orders,
        monthly_total - LAG(monthly_total, 1) OVER (ORDER BY month) as revenue_growth,
        ROUND((monthly_total * 100.0 / LAG(monthly_total, 1) OVER (ORDER BY month)) - 100, 2) as revenue_growth_percent,
        order_count - LAG(order_count, 1) OVER (ORDER BY month) as order_growth,
        ROUND((order_count * 100.0 / LAG(order_count, 1) OVER (ORDER BY month)) - 100, 2) as order_growth_percent
    FROM monthly_sales
)
SELECT 
    month,
    monthly_total,
    order_count,
    prev_month_total,
    revenue_growth,
    revenue_growth_percent || '%' as revenue_growth_percent,
    order_growth,
    order_growth_percent || '%' as order_growth_percent,
    CASE 
        WHEN revenue_growth_percent > 10 THEN 'Strong Growth'
        WHEN revenue_growth_percent > 0 THEN 'Positive Growth'
        WHEN revenue_growth_percent > -10 THEN 'Slight Decline'
        ELSE 'Significant Decline'
    END as trend_category
FROM trend_analysis
ORDER BY month;
```

**Advanced Trend Analysis with Moving Averages:**
```sql
-- Comprehensive trend analysis with moving averages
WITH monthly_metrics AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(total_amount) as revenue,
        COUNT(*) as orders,
        COUNT(DISTINCT customer_id) as unique_customers,
        AVG(total_amount) as avg_order_value
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
),
trend_analysis AS (
    SELECT 
        month,
        revenue,
        orders,
        unique_customers,
        avg_order_value,
        -- Previous month values
        LAG(revenue, 1) OVER (ORDER BY month) as prev_revenue,
        LAG(orders, 1) OVER (ORDER BY month) as prev_orders,
        LAG(unique_customers, 1) OVER (ORDER BY month) as prev_customers,
        LAG(avg_order_value, 1) OVER (ORDER BY month) as prev_avg_order_value,
        -- 3-month moving averages
        AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as revenue_3m_avg,
        AVG(orders) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as orders_3m_avg,
        AVG(unique_customers) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as customers_3m_avg,
        -- Growth calculations
        revenue - LAG(revenue, 1) OVER (ORDER BY month) as revenue_growth,
        ROUND((revenue * 100.0 / LAG(revenue, 1) OVER (ORDER BY month)) - 100, 2) as revenue_growth_percent,
        orders - LAG(orders, 1) OVER (ORDER BY month) as order_growth,
        ROUND((orders * 100.0 / LAG(orders, 1) OVER (ORDER BY month)) - 100, 2) as order_growth_percent
    FROM monthly_metrics
)
SELECT 
    month,
    ROUND(revenue, 2) as revenue,
    ROUND(prev_revenue, 2) as prev_revenue,
    ROUND(revenue_growth, 2) as revenue_growth,
    revenue_growth_percent || '%' as revenue_growth_percent,
    ROUND(revenue_3m_avg, 2) as revenue_3m_avg,
    orders,
    prev_orders,
    order_growth,
    order_growth_percent || '%' as order_growth_percent,
    ROUND(orders_3m_avg, 2) as orders_3m_avg,
    ROUND(avg_order_value, 2) as avg_order_value,
    ROUND(prev_avg_order_value, 2) as prev_avg_order_value,
    -- Trend analysis
    CASE 
        WHEN revenue_growth_percent > 15 THEN 'Exceptional Growth'
        WHEN revenue_growth_percent > 5 THEN 'Strong Growth'
        WHEN revenue_growth_percent > 0 THEN 'Positive Growth'
        WHEN revenue_growth_percent > -5 THEN 'Slight Decline'
        ELSE 'Significant Decline'
    END as revenue_trend,
    CASE 
        WHEN revenue > revenue_3m_avg * 1.1 THEN 'Above Trend'
        WHEN revenue > revenue_3m_avg * 0.9 THEN 'On Trend'
        ELSE 'Below Trend'
    END as vs_trend
FROM trend_analysis
ORDER BY month;
```

#### **Key Concepts:**
- **LAG() function**: Access previous period values
- **Moving averages**: AVG() OVER (ROWS BETWEEN)
- **Growth calculations**: Period-over-period changes
- **Trend categorization**: CASE statements for business insights

#### **Real-World Applications:**
- **Business Intelligence**: Revenue trend analysis
- **Financial Planning**: Budget vs actual trends
- **Marketing Analysis**: Campaign performance over time
- **Operations**: Efficiency trend monitoring

---

## 🎯 **EPAM Interview Success Tips for Advanced Patterns**

### **1. Always Start with Business Context**
- "This is a top N per group problem for HR analytics"
- "We need to find customer churn patterns using gap analysis"
- "Let's analyze revenue trends with moving averages"

### **2. Break Complex Problems into Steps**
- Use CTEs to break down complex logic
- Start with basic window functions, then add complexity
- Test each step before moving to the next

### **3. Consider Performance Implications**
- Use appropriate frame sizes
- Index your PARTITION BY and ORDER BY columns
- Consider alternatives for very large datasets

### **4. Add Business Value**
- Include meaningful column names
- Add context with CASE statements
- Calculate relevant business metrics

**Master these patterns, and you'll be ready for any EPAM window function challenge!** 🚀

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

### 6. LAST_VALUE() Without Frame Specification ⚠️ **CRITICAL**
```sql
-- ✗ WRONG: LAST_VALUE() without frame only looks at current row
SELECT 
    customer_id,
    order_date,
    order_amount,
    LAST_VALUE(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as last_value  -- This is WRONG! Shows current row, not last row
FROM orders;

-- ✓ CORRECT: LAST_VALUE() needs frame to see entire partition
SELECT 
    customer_id,
    order_date,
    order_amount,
    LAST_VALUE(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as last_value  -- This shows actual last row in partition
FROM orders;
```

**Why This Matters:**
- **Without frame**: LAST_VALUE() = current row's value
- **With frame**: LAST_VALUE() = last row's value in entire partition
- **This is a VERY common mistake** in interviews!

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
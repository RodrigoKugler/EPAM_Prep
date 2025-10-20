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

## 📚 Module Structure Overview

```
📖 THEORY SECTIONS
├── 1. Window Functions Fundamentals
├── 2. Ranking Functions Mastery
├── 3. Analytical Functions (LAG/LEAD)
├── 4. Aggregate Window Functions
├── 5. Frame Specifications Deep Dive
└── 6. PARTITION BY Mastery

💡 PRACTICAL EXAMPLES
├── EPAM Classic Problems
├── Business Scenario Applications
├── Performance Optimization
└── Real-World Use Cases

🎯 EPAM INTERVIEW FOCUS
├── The Classic Cumulative Problem
├── Advanced Patterns & Variations
├── Common Mistakes & Solutions
└── Interview Success Strategies
```

---

## 📖 THEORY SECTIONS

---

## 📚 What Are Window Functions? - Deep Understanding

Window functions perform calculations across a set of rows **without collapsing them** (unlike GROUP BY). Think of them as "peeking through a window" at related rows.

### The Window Function Concept - Visual Understanding

Imagine you're looking at data through a **sliding window**. The window can:
- **Look at all rows** (no PARTITION BY)
- **Look at specific groups** (with PARTITION BY)
- **Look at a range of rows** (with frame specifications)
- **Move through the data** (with ORDER BY)

### Key Difference from GROUP BY - The Fundamental Distinction

**GROUP BY**: **Collapses** data into summary rows
**Window Functions**: **Preserves** all original rows while adding calculated values

#### GROUP BY Example - Data Collapse
```sql
-- GROUP BY: Collapses rows (loses individual records)
SELECT 
    department,
    AVG(salary) as avg_salary,
    COUNT(*) as employee_count
FROM employees
GROUP BY department;
-- Result: Only 3 rows (one per department)
-- Original employee details are LOST
```

**What happens**:
1. Database groups employees by department
2. Calculates average salary per department
3. **Collapses** all employees into one row per department
4. Individual employee information is **lost**

#### Window Function Example - Data Preservation
```sql
-- WINDOW FUNCTION: Keeps all rows (preserves individual records)
SELECT 
    employee_name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg_salary,
    COUNT(*) OVER (PARTITION BY department) as dept_employee_count
FROM employees;
-- Result: All employee rows with their department statistics
-- Original employee details are PRESERVED
```

**What happens**:
1. Database looks at each employee row
2. For each employee, calculates department average
3. **Preserves** all original employee information
4. **Adds** calculated values to each row

#### Visual Comparison

**Original Data**:
```
employee_name | department | salary
Alice        | Sales      | 80000
Bob          | Sales      | 90000
Charlie      | Sales      | 70000
David        | IT         | 95000
Eve          | IT         | 85000
```

**GROUP BY Result** (Data Collapsed):
```
department | avg_salary | employee_count
Sales      | 80000      | 3
IT         | 90000      | 2
```

**Window Function Result** (Data Preserved):
```
employee_name | department | salary | dept_avg_salary | dept_employee_count
Alice        | Sales      | 80000  | 80000           | 3
Bob          | Sales      | 90000  | 80000           | 3
Charlie      | Sales      | 70000  | 80000           | 3
David        | IT         | 95000  | 90000           | 2
Eve          | IT         | 85000  | 90000           | 2
```

### Why Window Functions Matter - The Business Value

#### 1. **Comparative Analysis**
```sql
-- Compare each employee to their department average
SELECT 
    employee_name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department) as salary_difference
FROM employees;
```

**Business Value**: "Is Alice paid above or below her department average?"

#### 2. **Ranking and Percentiles**
```sql
-- Rank employees within their department
SELECT 
    employee_name,
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;
```

**Business Value**: "Where does Alice rank among Sales employees?"

#### 3. **Trend Analysis**
```sql
-- Calculate running totals over time
SELECT 
    order_date,
    order_amount,
    SUM(order_amount) OVER (ORDER BY order_date) as running_total
FROM orders;
```

**Business Value**: "How much have we sold cumulatively by this date?"

### The Window Function Anatomy

Every window function has three parts:

```sql
FUNCTION() OVER (
    PARTITION BY column1, column2    -- 1. Divide into groups
    ORDER BY column3                 -- 2. Sort within groups
    ROWS BETWEEN start AND end       -- 3. Define the window frame
)
```

#### 1. **PARTITION BY** - "Which groups to look at"
- Divides data into separate groups
- Window function operates independently on each group
- Like creating separate "mini-tables" for each group

#### 2. **ORDER BY** - "How to sort within each group"
- Determines the order of rows within each partition
- Essential for functions like LAG, LEAD, running totals
- Defines the "sequence" of calculations

#### 3. **Frame Specification** - "Which rows to include in calculation"
- Defines exactly which rows are in the "window"
- Can be unbounded (all rows) or bounded (specific range)
- Controls the scope of the calculation

### Real-World Window Function Patterns

#### Pattern 1: **Peer Comparison**
"Compare each row to its group average"
```sql
SELECT 
    product_name,
    category,
    price,
    AVG(price) OVER (PARTITION BY category) as category_avg_price,
    price - AVG(price) OVER (PARTITION BY category) as price_vs_avg
FROM products;
```

#### Pattern 2: **Sequential Analysis**
"Compare each row to previous/next row"
```sql
SELECT 
    date,
    sales,
    LAG(sales, 1) OVER (ORDER BY date) as prev_day_sales,
    sales - LAG(sales, 1) OVER (ORDER BY date) as daily_change
FROM daily_sales;
```

#### Pattern 3: **Cumulative Calculations**
"Running totals and running averages"
```sql
SELECT 
    order_date,
    order_amount,
    SUM(order_amount) OVER (ORDER BY order_date) as cumulative_revenue,
    AVG(order_amount) OVER (ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7_days
FROM orders;
```

**Key Insight**: Window functions let you **compare each row to its peers** without losing the original data. This enables sophisticated analytical queries that would be impossible with GROUP BY alone.

---

## 🔥 Core Window Functions - Complete Guide

### 1. ROW_NUMBER() - Sequential Numbering Mastery

**Purpose**: Assigns unique sequential numbers (1, 2, 3, 4...) to rows based on their order

**Key Characteristics**:
- **Always unique** - No ties, no gaps
- **Based on ORDER BY** - Order determines numbering sequence
- **Resets with PARTITION BY** - Starts over for each partition

#### Basic ROW_NUMBER() - Global Numbering

```sql
-- Basic usage - Number all orders chronologically
SELECT 
    customer_name,
    order_date,
    order_amount,
    ROW_NUMBER() OVER (ORDER BY order_date) as order_sequence
FROM orders;
```

**What happens**:
1. Database sorts all orders by date
2. Assigns sequential numbers: 1, 2, 3, 4...
3. Each row gets a unique number

**Result**:
```
customer_name | order_date | order_amount | order_sequence
Alice        | 2024-01-01 | 100         | 1
Bob          | 2024-01-02 | 150         | 2
Carol        | 2024-01-03 | 200         | 3
David        | 2024-01-04 | 175         | 4
```

#### ROW_NUMBER() with PARTITION BY - Group Numbering

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

**What happens**:
1. Database divides orders by customer_id
2. Within each customer group, sorts by order_date
3. Assigns sequential numbers within each group
4. **Numbers reset for each customer**

**Result**:
| customer_id | order_date | order_amount | order_number_for_customer |
|-------------|------------|--------------|---------------------------|
| A | 2024-01-01 | 100 | 1 |
| A | 2024-01-15 | 150 | 2 |
| A | 2024-02-01 | 200 | 3 |
| B | 2024-01-05 | 75 | 1 |
| B | 2024-01-20 | 125 | 2 |
| C | 2024-01-10 | 300 | 1 |
| C | 2024-01-25 | 250 | 2 |

**Key Insight**: Notice how the numbering **resets to 1** for each customer!

#### ROW_NUMBER() vs Other Ranking Functions

**Sample Data** (employees with same salary):
```
employee_name | department | salary
Alice        | Sales      | 80000
Bob          | Sales      | 80000  ← Same salary as Alice
Charlie      | Sales      | 70000
David        | IT         | 90000
```

**ROW_NUMBER() - Always unique, no ties**:
```sql
SELECT 
    employee_name,
    department,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num
FROM employees;
```

**Result**:
```
employee_name | department | salary | row_num
David        | IT         | 90000  | 1
Alice        | Sales      | 80000  | 2      ← Alice gets 2
Bob          | Sales      | 80000  | 3      ← Bob gets 3 (different from Alice)
Charlie      | Sales      | 70000  | 4
```

**Key Point**: Even though Alice and Bob have the same salary, they get different row numbers. ROW_NUMBER() **never creates ties**.

#### Real-World Use Cases

##### 1. **Pagination** - "Show me page 2 of results"
```sql
-- Get the second page of customers (rows 11-20)
WITH numbered_customers AS (
    SELECT 
        customer_id,
        customer_name,
        ROW_NUMBER() OVER (ORDER BY customer_name) as row_num
    FROM customers
)
SELECT customer_id, customer_name
FROM numbered_customers
WHERE row_num BETWEEN 11 AND 20;
```

##### 2. **Finding First/Last Occurrence** - "What was the customer's first order?"
```sql
-- Find each customer's first order
WITH customer_orders AS (
    SELECT 
        customer_id,
        order_date,
        order_amount,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY order_date
        ) as order_sequence
    FROM orders
)
SELECT 
    customer_id,
    order_date,
    order_amount
FROM customer_orders
WHERE order_sequence = 1;  -- First order for each customer
```

##### 3. **Deduplication** - "Keep only the most recent record"
```sql
-- Keep only the most recent order for each customer
WITH customer_orders AS (
    SELECT 
        customer_id,
        order_date,
        order_amount,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY order_date DESC  -- Most recent first
        ) as order_rank
    FROM orders
)
SELECT 
    customer_id,
    order_date,
    order_amount
FROM customer_orders
WHERE order_rank = 1;  -- Most recent order for each customer
```

##### 4. **Assigning Unique IDs** - "Give each row a unique identifier"
```sql
-- Add unique sequential IDs to existing data
SELECT 
    ROW_NUMBER() OVER (ORDER BY customer_id) as unique_id,
    customer_id,
    customer_name,
    email
FROM customers;
```

#### Advanced ROW_NUMBER() Patterns

##### Pattern 1: **Multi-Column Ordering**
```sql
-- Order by multiple columns for consistent numbering
SELECT 
    customer_id,
    order_date,
    order_amount,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY order_date, order_amount  -- Consistent ordering
    ) as order_sequence
FROM orders;
```

##### Pattern 2: **Reverse Numbering**
```sql
-- Number from newest to oldest
SELECT 
    customer_id,
    order_date,
    order_amount,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY order_date DESC  -- Newest first
    ) as order_sequence
FROM orders;
```

##### Pattern 3: **Conditional Numbering**
```sql
-- Number only high-value orders
SELECT 
    customer_id,
    order_date,
    order_amount,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as order_sequence
FROM orders
WHERE order_amount > 1000;  -- Only high-value orders get numbered
```

#### Common Mistakes with ROW_NUMBER()

**❌ WRONG: Missing ORDER BY**
```sql
-- This will give unpredictable results
SELECT 
    customer_id,
    ROW_NUMBER() OVER (PARTITION BY customer_id) as row_num
FROM orders;
```

**✅ CORRECT: Always include ORDER BY**
```sql
-- Predictable, consistent numbering
SELECT 
    customer_id,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as row_num
FROM orders;
```

**❌ WRONG: Expecting ties**
```sql
-- ROW_NUMBER() never creates ties, even for identical values
SELECT 
    employee_name,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as rank
FROM employees;
-- Alice and Bob both have salary 80000, but get different row numbers
```

**✅ CORRECT: Use RANK() for ties**
```sql
-- Use RANK() if you want ties
SELECT 
    employee_name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as rank
FROM employees;
-- Alice and Bob both get rank 2
```

#### Performance Considerations

**ROW_NUMBER() Performance Tips**:
1. **Index your ORDER BY columns** for better performance
2. **Use PARTITION BY** to limit the scope of ordering
3. **Consider alternatives** for simple numbering tasks

```sql
-- Good: Indexed ORDER BY column
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

SELECT 
    customer_id,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY order_date  -- This column is indexed
    ) as order_sequence
FROM orders;
```

**Use Cases Summary**:
- **Pagination**: LIMIT with OFFSET
- **Assigning unique IDs**: Sequential numbering
- **Finding first/last occurrence**: WHERE row_number = 1
- **Deduplication**: Keep only one record per group
- **Data sampling**: Every Nth row

---

### 2. RANK() - Ranking with Gaps Mastery

**Purpose**: Assigns ranks with gaps for ties (like sports rankings)

**Key Characteristics**:
- **Creates ties** - Same values get the same rank
- **Leaves gaps** - After ties, skips rank numbers
- **Based on ORDER BY** - Order determines ranking sequence
- **Resets with PARTITION BY** - Starts over for each partition

#### Basic RANK() - Global Ranking

```sql
-- Rank employees by salary (highest first)
SELECT 
    employee_name,
    department,
    salary,
    RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;
```

**What happens**:
1. Database sorts employees by salary (highest first)
2. Assigns ranks: 1, 2, 3, 4...
. **Same values get same rank**
4. **Skips numbers after ties**

**Example Results**:
| employee_name | department | salary | salary_rank |
|---------------|------------|--------|-------------|
| Alice | Sales | 100000 | 1 |
| Bob | IT | 100000 | 1 | ← Tie! Both get rank 1 |
| Charlie | Sales | 95000 | 3 | ← Gap! (no rank 2) |
| Dave | IT | 90000 | 4 |

**Key Insight**: Alice and Bob both have salary 100000, so they both get rank 1. The next person (Charlie) gets rank 3, **skipping rank 2**.

#### RANK() with PARTITION BY - Group Ranking

```sql
-- Rank employees within each department
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

**What happens**:
1. Database divides employees by department
2. Within each department, sorts by salary (highest first)
3. Assigns ranks within each department
4. **Ranks reset for each department**

**Example Results**:
| employee_name | department | salary | dept_salary_rank |
|---------------|------------|--------|------------------|
| Bob | IT | 100000 | 1 |
| Dave | IT | 90000 | 2 |
| Alice | Sales | 100000 | 1 |
| Charlie | Sales | 95000 | 2 |

**Key Insight**: Notice how Bob (IT) and Alice (Sales) both get rank 1 within their respective departments!

#### RANK() vs ROW_NUMBER() vs DENSE_RANK() - The Complete Comparison

**Sample Data** (employees with duplicate salaries):
```
employee_name | department | salary
Alice        | Sales      | 100000
Bob          | IT         | 100000  ← Same salary as Alice
Charlie      | Sales      | 95000
David        | IT         | 90000
Eve          | Sales      | 90000   ← Same salary as David
```

**ROW_NUMBER() - Always unique, no ties**:
```sql
SELECT 
    employee_name,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num
FROM employees;
```

**Result**:
```
employee_name | salary | row_num
Alice        | 100000 | 1
Bob          | 100000 | 2      ← Different from Alice
Charlie      | 95000  | 3
David        | 90000  | 4
Eve          | 90000  | 5      ← Different from David
```

**RANK() - Creates ties, leaves gaps**:
```sql
SELECT 
    employee_name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as rank_num
FROM employees;
```

**Result**:
```
employee_name | salary | rank_num
Alice        | 100000 | 1
Bob          | 100000 | 1       ← Same as Alice (tie)
Charlie      | 95000  | 3       ← Gap! (no rank 2)
David        | 90000  | 4
Eve          | 90000  | 4       ← Same as David (tie)
```

**DENSE_RANK() - Creates ties, no gaps**:
```sql
SELECT 
    employee_name,
    salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank_num
FROM employees;
```

**Result**:
```
employee_name | salary | dense_rank_num
Alice        | 100000 | 1
Bob          | 100000 | 1       ← Same as Alice (tie)
Charlie      | 95000  | 2       ← No gap!
David        | 90000  | 3
Eve          | 90000  | 3       ← Same as David (tie)
```

#### When to Use RANK() - Decision Guide

**Use RANK() when**:
- **Sports rankings** - "Who finished 1st, 2nd, 3rd?"
- **Performance rankings** - "Top 10 sales reps"
- **Competitive analysis** - "Market position"
- **You want gaps** - "There's no 2nd place if two people tied for 1st"

**Don't use RANK() when**:
- **You need unique numbers** - Use ROW_NUMBER()
- **You don't want gaps** - Use DENSE_RANK()
- **Simple numbering** - Use ROW_NUMBER()

#### Real-World RANK() Examples

##### 1. **Sales Leaderboard** - "Top performers this month"
```sql
-- Monthly sales ranking across all regions
SELECT 
    sales_rep_name,
    region,
    monthly_sales,
    RANK() OVER (ORDER BY monthly_sales DESC) as overall_rank,
    RANK() OVER (PARTITION BY region ORDER BY monthly_sales DESC) as region_rank
FROM monthly_sales
ORDER BY overall_rank;
```

**Business Value**: "Who are our top 3 sales reps overall? Who's #1 in each region?"

##### 2. **Student Rankings** - "Class performance"
```sql
-- Rank students by GPA within each major
SELECT 
    student_name,
    major,
    gpa,
    RANK() OVER (
        PARTITION BY major 
        ORDER BY gpa DESC
    ) as major_rank
FROM students
ORDER BY major, major_rank;
```

**Business Value**: "Who's the top student in Computer Science? Who's in the top 10% of Engineering students?"

##### 3. **Product Performance** - "Best-selling products"
```sql
-- Rank products by sales within each category
SELECT 
    product_name,
    category,
    total_sales,
    RANK() OVER (
        PARTITION BY category 
        ORDER BY total_sales DESC
    ) as category_rank
FROM product_sales
ORDER BY category, category_rank;
```

**Business Value**: "What's our #1 product in Electronics? Which products are in the top 5 of their category?"

#### Advanced RANK() Patterns

##### Pattern 1: **Multi-Column Ranking**
```sql
-- Rank by multiple criteria
SELECT 
    employee_name,
    department,
    salary,
    years_experience,
    RANK() OVER (
        ORDER BY salary DESC, years_experience DESC
    ) as overall_rank
FROM employees;
```

**Logic**: First rank by salary, then by years of experience for ties.

##### Pattern 2: **Percentile Ranking**
```sql
-- Rank as percentiles
SELECT 
    employee_name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as rank,
    COUNT(*) OVER () as total_employees,
    (RANK() OVER (ORDER BY salary DESC) * 100.0 / COUNT(*) OVER ()) as percentile
FROM employees;
```

**Result**: "Alice is in the top 20% of earners"

##### Pattern 3: **Conditional Ranking**
```sql
-- Rank only high performers
SELECT 
    employee_name,
    department,
    salary,
    RANK() OVER (
        PARTITION BY department 
        ORDER BY salary DESC
    ) as dept_rank
FROM employees
WHERE salary > 75000;  -- Only rank high earners
```

#### Common Mistakes with RANK()

**❌ WRONG: Missing ORDER BY**
```sql
-- This will give unpredictable results
SELECT 
    employee_name,
    RANK() OVER (PARTITION BY department) as rank
FROM employees;
```

**✅ CORRECT: Always include ORDER BY**
```sql
-- Predictable, consistent ranking
SELECT 
    employee_name,
    RANK() OVER (
        PARTITION BY department 
        ORDER BY salary DESC
    ) as rank
FROM employees;
```

**❌ WRONG: Expecting unique ranks**
```sql
-- RANK() creates ties, don't expect unique numbers
SELECT 
    employee_name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as rank
FROM employees;
-- Alice and Bob both get rank 1
```

**✅ CORRECT: Understand that ties are normal**
```sql
-- Ties are expected with RANK()
SELECT 
    employee_name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as rank,
    CASE 
        WHEN RANK() OVER (ORDER BY salary DESC) = 1 THEN 'Winner'
        WHEN RANK() OVER (ORDER BY salary DESC) <= 3 THEN 'Top 3'
        ELSE 'Other'
    END as performance_tier
FROM employees;
```

#### Performance Considerations

**RANK() Performance Tips**:
1. **Index your ORDER BY columns** for better performance
2. **Use PARTITION BY** to limit the scope of ranking
3. **Consider alternatives** for simple ranking tasks

```sql
-- Good: Indexed ORDER BY column
CREATE INDEX idx_employees_salary ON employees(salary);

SELECT 
    employee_name,
    RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;
```

**Use Cases Summary**:
- **Sports rankings**: Tournament standings
- **Performance rankings**: Top performers
- **Competitive analysis**: Market position
- **Percentile analysis**: Performance tiers
- **Leaderboards**: Top N lists

---

### 3. DENSE_RANK() - Ranking Without Gaps Mastery

**Purpose**: Assigns ranks WITHOUT gaps for ties

**Key Characteristics**:
- **Creates ties** - Same values get the same rank
- **No gaps** - After ties, continues with next consecutive number
- **Based on ORDER BY** - Order determines ranking sequence
- **Resets with PARTITION BY** - Starts over for each partition

#### Basic DENSE_RANK() - Global Ranking Without Gaps

```sql
-- Rank employees by salary (highest first) without gaps
SELECT 
    employee_name,
    department,
    salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;
```

**What happens**:
1. Database sorts employees by salary (highest first)
2. Assigns ranks: 1, 2, 3, 4...
3. **Same values get same rank**
4. **Continues with next consecutive number after ties**

**Example Results**:
| employee_name | department | salary | salary_rank |
|---------------|------------|--------|-------------|
| Alice | Sales | 100000 | 1 |
| Bob | IT | 100000 | 1 | ← Tie! Both get rank 1 |
| Charlie | Sales | 95000 | 2 | ← No gap! Continues with 2 |
| Dave | IT | 90000 | 3 |

**Key Insight**: Alice and Bob both have salary 100000, so they both get rank 1. The next person (Charlie) gets rank 2, **continuing consecutively without gaps**.

#### DENSE_RANK() vs RANK() - The Gap Difference

**Sample Data** (employees with duplicate salaries):
```
employee_name | department | salary
Alice        | Sales      | 100000
Bob          | IT         | 100000  ← Same salary as Alice
Charlie      | Sales      | 95000
David        | IT         | 90000
Eve          | Sales      | 90000   ← Same salary as David
Frank        | IT         | 85000
```

**RANK() - Creates gaps after ties**:
```sql
SELECT 
    employee_name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as rank_num
FROM employees;
```

**Result**:
```
employee_name | salary | rank_num
Alice        | 100000 | 1
Bob          | 100000 | 1       ← Tie
Charlie      | 95000  | 3       ← Gap! (no rank 2)
David        | 90000  | 4
Eve          | 90000  | 4       ← Tie
Frank        | 85000  | 6       ← Gap! (no rank 5)
```

**DENSE_RANK() - No gaps after ties**:
```sql
SELECT 
    employee_name,
    salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank_num
FROM employees;
```

**Result**:
```
employee_name | salary | dense_rank_num
Alice        | 100000 | 1
Bob          | 100000 | 1       ← Tie
Charlie      | 95000  | 2       ← No gap!
David        | 90000  | 3
Eve          | 90000  | 3       ← Tie
Frank        | 85000  | 4       ← No gap!
```

#### When to Use DENSE_RANK() - Decision Guide

**Use DENSE_RANK() when**:
- **Percentiles** - "Top 10%, 20%, 30%..."
- **Quartiles** - "1st quartile, 2nd quartile, 3rd quartile, 4th quartile"
- **Tiers** - "Gold, Silver, Bronze tiers"
- **You need consecutive numbers** - "1, 2, 3, 4..." without gaps
- **Categorical rankings** - "High, Medium, Low performance"

**Don't use DENSE_RANK() when**:
- **Sports rankings** - Use RANK() (gaps make sense)
- **Competitive analysis** - Use RANK() (gaps show competition)
- **You want gaps** - Use RANK()

#### Real-World DENSE_RANK() Examples

##### 1. **Performance Tiers** - "Gold, Silver, Bronze"
```sql
-- Create performance tiers without gaps
SELECT 
    employee_name,
    department,
    salary,
    DENSE_RANK() OVER (
        PARTITION BY department 
        ORDER BY salary DESC
    ) as performance_tier,
    CASE 
        WHEN DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) = 1 THEN 'Gold'
        WHEN DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) = 2 THEN 'Silver'
        WHEN DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) = 3 THEN 'Bronze'
        ELSE 'Other'
    END as tier_name
FROM employees
ORDER BY department, performance_tier;
```

**Business Value**: "Who are our Gold, Silver, Bronze performers in each department?"

##### 2. **Percentile Analysis** - "Top 10%, 20%, 30%..."
```sql
-- Create percentiles without gaps
SELECT 
    student_name,
    major,
    gpa,
    DENSE_RANK() OVER (
        PARTITION BY major 
        ORDER BY gpa DESC
    ) as gpa_rank,
    COUNT(*) OVER (PARTITION BY major) as total_students,
    (DENSE_RANK() OVER (PARTITION BY major ORDER BY gpa DESC) * 100.0 / 
     COUNT(*) OVER (PARTITION BY major)) as percentile
FROM students
ORDER BY major, gpa_rank;
```

**Business Value**: "What percentile is each student in their major?"

##### 3. **Product Categories** - "Premium, Standard, Basic"
```sql
-- Categorize products by price without gaps
SELECT 
    product_name,
    category,
    price,
    DENSE_RANK() OVER (
        PARTITION BY category 
        ORDER BY price DESC
    ) as price_tier,
    CASE 
        WHEN DENSE_RANK() OVER (PARTITION BY category ORDER BY price DESC) = 1 THEN 'Premium'
        WHEN DENSE_RANK() OVER (PARTITION BY category ORDER BY price DESC) = 2 THEN 'Standard'
        ELSE 'Basic'
    END as tier_name
FROM products
ORDER BY category, price_tier;
```

**Business Value**: "What tier is each product in its category?"

#### Advanced DENSE_RANK() Patterns

##### Pattern 1: **Quartile Analysis**
```sql
-- Create quartiles (4 groups) without gaps
SELECT 
    employee_name,
    salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) as rank,
    CEIL(DENSE_RANK() OVER (ORDER BY salary DESC) * 4.0 / COUNT(*) OVER ()) as quartile
FROM employees;
```

**Result**: "Alice is in the 1st quartile, Bob is in the 1st quartile, Charlie is in the 2nd quartile"

##### Pattern 2: **Multi-Column Dense Ranking**
```sql
-- Rank by multiple criteria without gaps
SELECT 
    employee_name,
    department,
    salary,
    years_experience,
    DENSE_RANK() OVER (
        ORDER BY salary DESC, years_experience DESC
    ) as overall_rank
FROM employees;
```

**Logic**: First rank by salary, then by years of experience for ties, without gaps.

##### Pattern 3: **Conditional Dense Ranking**
```sql
-- Rank only high performers without gaps
SELECT 
    employee_name,
    department,
    salary,
    DENSE_RANK() OVER (
        PARTITION BY department 
        ORDER BY salary DESC
    ) as dept_rank
FROM employees
WHERE salary > 75000;  -- Only rank high earners
```

#### Common Mistakes with DENSE_RANK()

**❌ WRONG: Using DENSE_RANK() for sports rankings**
```sql
-- Sports rankings should have gaps
SELECT 
    athlete_name,
    score,
    DENSE_RANK() OVER (ORDER BY score DESC) as rank
FROM athletes;
-- If two athletes tie for 1st, the next athlete should be 3rd, not 2nd
```

**✅ CORRECT: Use RANK() for sports rankings**
```sql
-- Sports rankings should have gaps
SELECT 
    athlete_name,
    score,
    RANK() OVER (ORDER BY score DESC) as rank
FROM athletes;
-- If two athletes tie for 1st, the next athlete is 3rd
```

**❌ WRONG: Expecting gaps**
```sql
-- DENSE_RANK() never creates gaps
SELECT 
    employee_name,
    salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) as rank
FROM employees;
-- Alice and Bob both get rank 1, Charlie gets rank 2 (no gap)
```

**✅ CORRECT: Understand that DENSE_RANK() has no gaps**
```sql
-- DENSE_RANK() creates consecutive numbers
SELECT 
    employee_name,
    salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) as rank,
    CASE 
        WHEN DENSE_RANK() OVER (ORDER BY salary DESC) = 1 THEN 'Top Tier'
        WHEN DENSE_RANK() OVER (ORDER BY salary DESC) = 2 THEN 'Second Tier'
        WHEN DENSE_RANK() OVER (ORDER BY salary DESC) = 3 THEN 'Third Tier'
        ELSE 'Other'
    END as tier
FROM employees;
```

#### Performance Considerations

**DENSE_RANK() Performance Tips**:
1. **Index your ORDER BY columns** for better performance
2. **Use PARTITION BY** to limit the scope of ranking
3. **Consider alternatives** for simple ranking tasks

```sql
-- Good: Indexed ORDER BY column
CREATE INDEX idx_employees_salary ON employees(salary);

SELECT 
    employee_name,
    DENSE_RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;
```

**Use Cases Summary**:
- **Percentiles**: Performance percentiles
- **Quartiles**: Data quartiles
- **Tiers**: Performance tiers
- **Categories**: Product categories
- **Consecutive numbering**: When gaps don't make sense

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

## 💡 PRACTICAL EXAMPLES

### EPAM Classic Problems - Master These!

#### Problem 1: The Classic Cumulative Orders (EPAM's Favorite)
**"Calculate running total of orders per customer with order count"**

```sql
-- This is THE problem EPAM asks most often
SELECT 
    customer_id,
    order_id,
    order_date,
    order_amount,
    -- Cumulative count: ROW_NUMBER resets for each customer
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as order_count_history,
    -- Cumulative sum: SUM with explicit frame
    SUM(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as order_value_history
FROM orders
ORDER BY customer_id, order_date;
```

#### Problem 2: Sales Performance Ranking
**"Rank sales reps within each region by total sales"**

```sql
SELECT 
    sales_rep_id,
    region,
    total_sales,
    RANK() OVER (
        PARTITION BY region 
        ORDER BY total_sales DESC
    ) as region_rank,
    DENSE_RANK() OVER (
        ORDER BY total_sales DESC
    ) as global_rank
FROM sales_performance
ORDER BY region, region_rank;
```

#### Problem 3: Customer Behavior Analysis
**"Find customers with increasing order values over time"**

```sql
WITH customer_trends AS (
    SELECT 
        customer_id,
        order_date,
        order_amount,
        LAG(order_amount, 1) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date
        ) as prev_order_amount,
        order_amount - LAG(order_amount, 1) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date
        ) as order_growth
    FROM orders
)
SELECT 
    customer_id,
    COUNT(*) as total_orders,
    AVG(order_growth) as avg_growth,
    SUM(CASE WHEN order_growth > 0 THEN 1 ELSE 0 END) as increasing_orders
FROM customer_trends
WHERE prev_order_amount IS NOT NULL
GROUP BY customer_id
HAVING AVG(order_growth) > 0
ORDER BY avg_growth DESC;
```

---

## 🎯 EPAM INTERVIEW FOCUS

### The Classic Cumulative Problem - Master This!

This is **THE problem** EPAM asks in 90% of SQL interviews:

**Problem Statement**: Calculate cumulative count and cumulative sum of orders per customer.

**Sample Data**:
```sql
-- Orders table
customer_id | order_id | order_date | order_amount
A          | 1        | 2024-01-01 | 100
A          | 2        | 2024-01-05 | 150
A          | 3        | 2024-01-10 | 200
B          | 4        | 2024-01-02 | 300
B          | 5        | 2024-01-08 | 250
```

**Expected Output**:
```sql
customer_id | order_id | order_date | order_amount | order_count_history | order_value_history
A          | 1        | 2024-01-01 | 100         | 1                   | 100
A          | 2        | 2024-01-05 | 150         | 2                   | 250
A          | 3        | 2024-01-10 | 200         | 3                   | 450
B          | 4        | 2024-01-02 | 300         | 1                   | 300
B          | 5        | 2024-01-08 | 250         | 2                   | 550
```

**Solution** (Memorize this pattern!):
```sql
SELECT 
    customer_id,
    order_id,
    order_date,
    order_amount,
    -- Cumulative count: ROW_NUMBER resets for each customer
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as order_count_history,
    -- Cumulative sum: SUM with explicit frame
    SUM(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as order_value_history
FROM orders
ORDER BY customer_id, order_date;
```

### Interview Success Strategy

1. **Recognize the pattern**: "This is a cumulative/running total problem"
2. **Choose the right functions**: ROW_NUMBER() for count, SUM() for totals
3. **Use PARTITION BY**: Reset counters for each group
4. **Set proper ORDER BY**: Chronological order for time series
5. **Define the frame**: ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
6. **Test with sample data**: Always verify your logic

### Common Interview Variations

#### Variation 1: Moving Averages
```sql
-- 7-day moving average
SELECT 
    date,
    sales,
    AVG(sales) OVER (
        ORDER BY date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7_days
FROM daily_sales;
```

#### Variation 2: Top N per Group
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

#### Variation 3: Period-over-Period Analysis
```sql
-- Month-over-month growth
SELECT 
    month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY month) as prev_month_revenue,
    revenue - LAG(revenue, 1) OVER (ORDER BY month) as growth,
    (revenue * 100.0 / LAG(revenue, 1) OVER (ORDER BY month)) - 100 as growth_percent
FROM monthly_revenue;
```

---

## 🚀 Performance Optimization

### Window Function Performance Tips

1. **Index your ORDER BY columns**
   ```sql
   CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
   ```

2. **Use PARTITION BY to limit scope**
   ```sql
   -- Good: Limited partition
   ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date)
   
   -- Avoid: Global window on large datasets
   ROW_NUMBER() OVER (ORDER BY order_date)
   ```

3. **Choose appropriate frame sizes**
   ```sql
   -- Good: Limited frame
   AVG(sales) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
   
   -- Avoid: Unbounded frames on large datasets
   AVG(sales) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
   ```

---

## 🏋️ Practice Strategy

### Master These Patterns in Order

1. **Basic ROW_NUMBER()** - Sequential numbering
2. **RANK() vs DENSE_RANK()** - Ranking with/without gaps
3. **PARTITION BY** - Group-based calculations
4. **Running totals** - SUM() with OVER()
5. **LAG/LEAD** - Time series analysis
6. **Frame specifications** - Precise window control
7. **Complex combinations** - Multiple window functions

### Time Targets for EPAM Interview

- **Basic window function**: 3-5 minutes
- **Cumulative problem**: 5-8 minutes
- **Complex ranking**: 7-10 minutes
- **Multiple window functions**: 10-15 minutes

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
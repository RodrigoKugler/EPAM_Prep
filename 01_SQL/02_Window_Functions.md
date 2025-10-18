# SQL Window Functions - Deep Dive

## 🎯 Learning Objectives

Master all window functions:
- ROW_NUMBER, RANK, DENSE_RANK
- LAG, LEAD
- FIRST_VALUE, LAST_VALUE
- SUM, AVG, COUNT with OVER()
- Frame specifications (ROWS vs RANGE)

---

## 📚 What Are Window Functions?

Window functions perform calculations across a set of rows **without collapsing them** (unlike GROUP BY).

### Key Difference from GROUP BY

```sql
-- GROUP BY: Collapses rows
SELECT 
    department,
    AVG(salary) as avg_salary
FROM employees
GROUP BY department;
-- Result: One row per department

-- WINDOW FUNCTION: Keeps all rows
SELECT 
    name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg_salary
FROM employees;
-- Result: All employee rows with their department average
```

---

## 🔥 Core Window Functions

### 1. ROW_NUMBER()
Assigns unique sequential numbers to rows

```sql
SELECT 
    customer_name,
    order_date,
    order_amount,
    ROW_NUMBER() OVER (ORDER BY order_date) as order_sequence
FROM orders;
```

**Use Case**: Assigning unique IDs, numbering results

### 2. RANK()
Assigns ranks with gaps for ties

```sql
SELECT 
    employee_name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;
```

Example results:
| employee_name | salary | salary_rank |
|---------------|--------|-------------|
| Alice | 100000 | 1 |
| Bob | 100000 | 1 |
| Charlie | 95000 | 3 |  ← Gap!

### 3. DENSE_RANK()
Assigns ranks WITHOUT gaps for ties

```sql
SELECT 
    employee_name,
    salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;
```

Example results:
| employee_name | salary | salary_rank |
|---------------|--------|-------------|
| Alice | 100000 | 1 |
| Bob | 100000 | 1 |
| Charlie | 95000 | 2 |  ← No gap!

### 4. LAG() and LEAD()
Access previous/next rows

```sql
-- LAG: Get previous row's value
SELECT 
    order_date,
    order_amount,
    LAG(order_amount, 1) OVER (ORDER BY order_date) as previous_order,
    order_amount - LAG(order_amount, 1) OVER (ORDER BY order_date) as difference
FROM orders;

-- LEAD: Get next row's value
SELECT 
    order_date,
    order_amount,
    LEAD(order_amount, 1) OVER (ORDER BY order_date) as next_order
FROM orders;
```

**Use Cases**:
- Period-over-period comparisons
- Calculate differences between consecutive rows
- Trend analysis

### 5. FIRST_VALUE() and LAST_VALUE()
Get first/last value in window

```sql
SELECT 
    order_date,
    order_amount,
    FIRST_VALUE(order_amount) OVER (
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as first_order_amount,
    LAST_VALUE(order_amount) OVER (
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as last_order_amount
FROM orders;
```

### 6. Aggregate Functions with OVER()
SUM, AVG, COUNT, MIN, MAX can be window functions

```sql
-- Running total
SELECT 
    order_date,
    order_amount,
    SUM(order_amount) OVER (ORDER BY order_date) as running_total
FROM orders;

-- Moving average (last 3 orders)
SELECT 
    order_date,
    order_amount,
    AVG(order_amount) OVER (
        ORDER BY order_date 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as moving_avg_3
FROM orders;
```

---

## 🎯 PARTITION BY - The Game Changer

PARTITION BY divides data into groups, applying window function to each group separately.

```sql
-- Rank employees within their department
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

Result:
| employee_name | department | salary | dept_salary_rank |
|---------------|------------|--------|------------------|
| Alice | Sales | 100000 | 1 |
| Bob | Sales | 95000 | 2 |
| Charlie | IT | 110000 | 1 |  ← Rank resets for IT!
| Dave | IT | 105000 | 2 |

---

## 🔧 Frame Specifications - Advanced

Control EXACTLY which rows are included in the window.

### Syntax
```sql
OVER (
    [PARTITION BY column]
    ORDER BY column
    {ROWS | RANGE} BETWEEN frame_start AND frame_end
)
```

### ROWS vs RANGE

**ROWS**: Physical row count
**RANGE**: Logical value range (handles ties)

```sql
-- ROWS: Exactly last 3 rows
AVG(amount) OVER (
    ORDER BY date 
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)

-- RANGE: All rows with values within range
AVG(amount) OVER (
    ORDER BY date 
    RANGE BETWEEN INTERVAL '2' DAY PRECEDING AND CURRENT ROW
)
```

### Frame Boundaries

| Boundary | Meaning |
|----------|---------|
| `UNBOUNDED PRECEDING` | Start of partition |
| `N PRECEDING` | N rows before current |
| `CURRENT ROW` | Current row |
| `N FOLLOWING` | N rows after current |
| `UNBOUNDED FOLLOWING` | End of partition |

### Common Frame Patterns

```sql
-- Running total (all rows from start to current)
SUM(amount) OVER (
    ORDER BY date 
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)

-- Moving average (last 7 rows)
AVG(amount) OVER (
    ORDER BY date 
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)

-- Centered moving average (3 before, current, 3 after)
AVG(amount) OVER (
    ORDER BY date 
    ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING
)

-- Cumulative from current to end
SUM(amount) OVER (
    ORDER BY date 
    ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
)
```

---

## 🎯 EPAM Interview Example - Solved

**Problem**: Calculate cumulative count and cumulative sum per customer

```sql
-- Orders table
/*
+-----+------------+--------------+---------------+
| cid |  order_id  |  order_date  |  order_value  |
+-----+------------+--------------+---------------+
|  A  |   qwerty   |     1-Jan    |      10       |
|  A  |   asdfgh   |     3-Jan    |      20       |
|  A  |   zxcvbn   |     10-Jan   |      30       |
|  B  |   uiopyy   |     2-Jan    |      40       |
+-----+------------+--------------+---------------+
*/

-- SOLUTION:
SELECT 
    cid,
    order_id,
    order_date,
    order_value,
    -- Cumulative count
    ROW_NUMBER() OVER (
        PARTITION BY cid 
        ORDER BY order_date
    ) as order_count_history,
    -- Cumulative sum
    SUM(order_value) OVER (
        PARTITION BY cid 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as order_value_history
FROM orders
ORDER BY cid, order_date;
```

**Key Points**:
- `PARTITION BY cid` - Reset for each customer
- `ORDER BY order_date` - Chronological order
- `ROW_NUMBER()` - Sequential count (1, 2, 3...)
- `SUM() with frame` - Running total

---

## 💡 Pro Tips

1. **PARTITION BY is optional**
   ```sql
   -- Without PARTITION BY: One window for entire table
   ROW_NUMBER() OVER (ORDER BY date)
   ```

2. **ORDER BY matters**
   ```sql
   -- Different ORDER BY = Different results
   RANK() OVER (ORDER BY salary DESC)  -- Rank by salary
   RANK() OVER (ORDER BY hire_date)    -- Rank by seniority
   ```

3. **Multiple window functions in one query**
   ```sql
   SELECT 
       name,
       salary,
       RANK() OVER (ORDER BY salary DESC) as overall_rank,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank,
       NTILE(4) OVER (ORDER BY salary) as quartile
   FROM employees;
   ```

4. **Use NTILE for percentiles**
   ```sql
   -- Divide into 4 equal groups (quartiles)
   SELECT 
       name,
       salary,
       NTILE(4) OVER (ORDER BY salary) as salary_quartile
   FROM employees;
   -- 1 = bottom 25%, 4 = top 25%
   ```

---

## ⚠️ Common Mistakes

1. **Forgetting ORDER BY in frame specification**
   ```sql
   -- ✗ WRONG: No ORDER BY with frame
   SUM(amount) OVER (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
   
   -- ✓ CORRECT
   SUM(amount) OVER (
       ORDER BY date 
       ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
   )
   ```

2. **Using wrong frame default**
   ```sql
   -- This might not do what you expect!
   SUM(amount) OVER (ORDER BY date)
   -- Default frame: RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
   
   -- Be explicit for clarity
   SUM(amount) OVER (
       ORDER BY date 
       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
   )
   ```

3. **Confusing RANK vs DENSE_RANK**
   - Use RANK() when you want gaps for ties (like sports rankings)
   - Use DENSE_RANK() when you want consecutive ranks

---

## 🚀 Practice Exercises

See: `01_SQL/exercises/02_Window_Functions_Exercises.md`

Master these patterns:
1. Running totals
2. Moving averages
3. Ranking within groups
4. Period-over-period comparisons
5. Top N per group

---

## 📚 Further Reading

- Window Functions vs GROUP BY performance
- Optimization techniques for window functions
- Complex frame specifications
- Window functions in different SQL dialects

**Next Module**: JOINs Deep Dive

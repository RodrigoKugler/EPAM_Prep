# SQL Basics & Fundamentals - Complete Mastery Guide

## 🎯 Learning Objectives

By the end of this module, you will be able to:
- **Master SQL SELECT statements** with all clauses and their execution order
- **Understand WHERE vs HAVING** and apply them correctly in business scenarios
- **Use aggregate functions effectively** for data analysis and reporting
- **Write clean, readable SQL queries** following professional standards
- **Solve real-world business problems** using SQL fundamentals
- **Explain SQL concepts clearly** in technical interviews

---

## 🔥 Why SQL Basics Matter for EPAM

SQL fundamentals are the **foundation of data engineering**. Here's why they're critical:

1. **Every data pipeline starts with SQL** - Data extraction, transformation, and loading
2. **They test logical thinking** - Can you structure queries correctly?
3. **They're used in real data engineering** - ETL processes, data quality, analytics
4. **They separate beginners from professionals** - Proper SQL structure and optimization

**EPAM will test your SQL fundamentals through complex business scenarios. Master this module = solid foundation for all advanced SQL topics.**

---

## 📚 Module Structure Overview

```
📖 THEORY SECTIONS
├── 1. SQL Query Anatomy & Execution Order
├── 2. WHERE vs HAVING Deep Dive
├── 3. Aggregate Functions Mastery
├── 4. GROUP BY Rules & Patterns
└── 5. Professional SQL Standards

💡 PRACTICAL EXAMPLES
├── Business Scenario Examples
├── Step-by-Step Query Building
├── Common Patterns & Anti-Patterns
└── Performance Considerations

🎯 EPAM INTERVIEW FOCUS
├── Classic Interview Problems
├── Common Mistakes to Avoid
├── Interview Success Tips
└── Quick Reference Guide
```

---

## 📖 THEORY SECTIONS

### 1. SQL Query Anatomy & Execution Order

#### The Complete SELECT Statement Structure

```sql
SELECT 
    column1,
    column2,
    AGGREGATE_FUNCTION(column3) as alias
FROM 
    table_name
WHERE 
    condition
GROUP BY 
    column1, column2
HAVING 
    aggregate_condition
ORDER BY 
    column1 DESC
LIMIT 10;
```

#### SQL Execution Order - The Critical Understanding

**SQL processes clauses in this specific order** (NOT the order you write them):

```
1. FROM     → Get the table(s)
2. WHERE    → Filter individual rows
3. GROUP BY → Group the filtered rows
4. HAVING   → Filter the groups
5. SELECT   → Choose columns and calculate expressions
6. ORDER BY → Sort the results
7. LIMIT    → Limit the number of rows returned
```

#### Visual Execution Flow

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  FROM   │───▶│  WHERE  │───▶│GROUP BY │───▶│ HAVING  │───▶│ SELECT  │
│ (Table) │    │(Filter) │    │(Group)  │    │(Filter) │    │(Columns)│
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
                                                                    │
┌─────────┐    ┌─────────┐                                        │
│ LIMIT   │◀───│ORDER BY │◀────────────────────────────────────────┘
│(Limit)  │    │ (Sort)  │
└─────────┘    └─────────┘
```

#### Why Execution Order Matters

Understanding execution order helps you:
- **Write efficient queries** - Filter early with WHERE, not HAVING
- **Debug query logic** - Know what data is available at each step
- **Optimize performance** - Understand what indexes to create
- **Explain your approach** - Show professional SQL knowledge

#### Step-by-Step Example

```sql
-- Query: Find departments with average salary > 75000, ordered by avg salary
SELECT 
    department,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary
FROM employees
WHERE hire_date >= '2020-01-01'
GROUP BY department
HAVING AVG(salary) > 75000
ORDER BY avg_salary DESC
LIMIT 5;
```

**Execution Steps**:
1. **FROM employees** - Get all employee records
2. **WHERE hire_date >= '2020-01-01'** - Keep only recent hires
3. **GROUP BY department** - Group employees by department
4. **HAVING AVG(salary) > 75000** - Keep only departments with high avg salary
5. **SELECT department, COUNT(*), AVG(salary)** - Choose columns and calculate
6. **ORDER BY avg_salary DESC** - Sort by average salary (highest first)
7. **LIMIT 5** - Return only top 5 departments

### 2. WHERE vs HAVING - The Critical Difference

#### The Fundamental Distinction

**WHERE filters INDIVIDUAL ROWS**  
**HAVING filters GROUPS OF ROWS**

This is the **#1 most important concept** in SQL fundamentals and a **favorite EPAM interview topic**.

#### Visual Comparison

```
WHERE CLAUSE:
┌─────────┐    ┌─────────┐    ┌─────────┐
│  Row 1  │───▶│ Filter  │───▶│  Row 1  │
│  Row 2  │    │(WHERE)  │    │  Row 2  │
│  Row 3  │    │         │    │  Row 3  │
└─────────┘    └─────────┘    └─────────┘

HAVING CLAUSE:
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Row 1  │    │ Group   │    │ Group A │───▶│ Filter  │───▶│ Group A │
│  Row 2  │───▶│ (GROUP  │───▶│ Group B │    │(HAVING) │    │ Group B │
│  Row 3  │    │  BY)    │    │ Group C │    │         │    │         │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
```

#### WHERE Clause - Row-Level Filtering

**Purpose**: Filters rows BEFORE any grouping or aggregation happens

**When to use**: 
- Filter individual records
- Use with any columns (aggregated or not)
- Applied to the raw data

```sql
-- Filter individual orders over $100
SELECT customer_id, order_date, amount
FROM orders
WHERE amount > 100;
```

**What happens**: 
1. Database looks at each order row
2. Keeps only orders where amount > 100
3. Returns the filtered individual orders

#### HAVING Clause - Group-Level Filtering

**Purpose**: Filters groups AFTER grouping and aggregation happens

**When to use**:
- Filter based on aggregated values (SUM, COUNT, AVG, etc.)
- Use with GROUP BY
- Applied to grouped results

```sql
-- Filter customer groups with total spend over $1000
SELECT customer_id, SUM(amount) as total_spent
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 1000;
```

**What happens**:
1. Database groups orders by customer_id
2. Calculates SUM(amount) for each group
3. Keeps only groups where total > 1000
4. Returns the filtered groups

#### Side-by-Side Comparison

**Sample Data**:
```sql
-- Orders table
customer_id | order_date | amount
1          | 2024-01-01 | 50
1          | 2024-01-02 | 200
1          | 2024-01-03 | 800
2          | 2024-01-01 | 300
2          | 2024-01-02 | 400
3          | 2024-01-01 | 100
```

**WHERE Example**:
```sql
SELECT customer_id, order_date, amount
FROM orders
WHERE amount > 150;
```

**Result**: Individual orders over $150
```
customer_id | order_date | amount
1          | 2024-01-02 | 200
1          | 2024-01-03 | 800
2          | 2024-01-01 | 300
2          | 2024-01-02 | 400
```

**HAVING Example**:
```sql
SELECT customer_id, SUM(amount) as total_spent
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 1000;
```

**Result**: Customer groups with total spend over $1000
```
customer_id | total_spent
1          | 1050
2          | 700
```

**Key Insight**: Customer 2 had individual orders over $150 (WHERE would include them), but their total spend is only $700 (HAVING excludes them).

#### Real-World Scenarios

**Scenario 1: Sales Analysis**
```sql
-- WHERE: Get high-value individual orders
SELECT order_id, customer_id, amount
FROM orders
WHERE amount > 500;

-- HAVING: Get customers with high total spend
SELECT customer_id, COUNT(*) as order_count, SUM(amount) as total_spent
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 2000;
```

**Scenario 2: Employee Analysis**
```sql
-- WHERE: Get employees in specific departments
SELECT employee_name, department, salary
FROM employees
WHERE department = 'Sales';

-- HAVING: Get departments with high average salary
SELECT department, COUNT(*) as employee_count, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 75000;
```

#### Common Mistakes

**❌ WRONG: Using HAVING without GROUP BY**
```sql
-- This will cause an error
SELECT customer_id, amount
FROM orders
HAVING amount > 100;  -- Error! No GROUP BY
```

**❌ WRONG: Using WHERE with aggregated functions**
```sql
-- This will cause an error
SELECT customer_id, SUM(amount) as total
FROM orders
WHERE SUM(amount) > 1000;  -- Error! WHERE can't use aggregate functions
GROUP BY customer_id;
```

**✅ CORRECT: Combining WHERE and HAVING**
```sql
-- Filter individual orders first, then filter groups
SELECT customer_id, SUM(amount) as total_spent
FROM orders
WHERE order_date >= '2024-01-01'  -- Filter individual orders
GROUP BY customer_id
HAVING SUM(amount) > 1000;        -- Filter groups
```

#### Execution Order

**SQL processes clauses in this order**:
1. **FROM** - Get the table
2. **WHERE** - Filter individual rows
3. **GROUP BY** - Group the filtered rows
4. **HAVING** - Filter the groups
5. **SELECT** - Choose columns
6. **ORDER BY** - Sort results

```sql
-- Example showing the execution order
SELECT customer_id, SUM(amount) as total_spent
FROM orders                    -- 1. Get orders table
WHERE amount > 50              -- 2. Keep only orders > $50
GROUP BY customer_id           -- 3. Group by customer
HAVING SUM(amount) > 500       -- 4. Keep only groups with total > $500
ORDER BY total_spent DESC;     -- 5. Sort by total spend
```

#### Quick Decision Guide

**Use WHERE when**:
- Filtering individual rows
- Working with non-aggregated columns
- Need to reduce data before grouping

**Use HAVING when**:
- Filtering based on aggregated values (SUM, COUNT, AVG, etc.)
- Working with GROUP BY
- Need to filter groups after aggregation

**Remember**: WHERE = "Which rows to include", HAVING = "Which groups to include"

### 3. WHERE Filtering with Multiple Elements

#### Using IN Operator - The Clean Way

**Purpose**: Filter rows where a column matches any value in a list

```sql
-- Find employees in specific departments
SELECT employee_id, first_name, department
FROM employees
WHERE department IN ('Sales', 'Marketing', 'IT');
```

**Benefits of IN:**
- ✅ **Clean and readable** - easy to understand
- ✅ **Efficient performance** - database optimized
- ✅ **Easy to maintain** - simple to add/remove values
- ✅ **Handles many values** - works with long lists

#### Using OR Operator - For Complex Conditions

**Purpose**: Filter rows where multiple conditions are true (any one can be true)

```sql
-- Same result using OR
SELECT employee_id, first_name, department
FROM employees
WHERE department = 'Sales' 
   OR department = 'Marketing' 
   OR department = 'IT';
```

**When to use OR:**
- ✅ **Complex conditions** - not just equality checks
- ✅ **Different operators** - mix of =, >, <, LIKE, etc.
- ✅ **Few values** - 2-3 items maximum

#### Using AND for Multiple Criteria

**Purpose**: Filter rows where ALL conditions must be true

```sql
-- Find employees meeting multiple criteria
SELECT employee_id, first_name, department, salary
FROM employees
WHERE department = 'Sales' 
  AND salary > 50000
  AND hire_date > '2020-01-01';
```

#### Combining IN, OR, and AND

```sql
-- Complex filtering with multiple elements
SELECT * FROM employees
WHERE (department IN ('Sales', 'Marketing') OR department = 'IT')
  AND salary > 50000
  AND hire_date > '2020-01-01';
```

#### Real-World Examples

**Example 1: Department Filtering**
```sql
-- Find employees in Sales or Marketing (using IN)
SELECT * FROM employees
WHERE department IN ('Sales', 'Marketing');

-- Equivalent using OR
SELECT * FROM employees
WHERE department = 'Sales' OR department = 'Marketing';
```

**Example 2: Salary Range**
```sql
-- Using BETWEEN for ranges
SELECT * FROM employees
WHERE salary BETWEEN 40000 AND 70000;

-- Equivalent using AND
SELECT * FROM employees
WHERE salary >= 40000 AND salary <= 70000;
```

**Example 3: Complex Business Logic**
```sql
-- Find high-performing employees in key departments
SELECT * FROM employees
WHERE department IN ('Sales', 'Marketing', 'IT')
  AND salary > 60000
  AND performance_rating >= 4;
```

#### Decision Guide: IN vs OR vs AND

| **Scenario** | **Use** | **Example** |
|-------------|---------|-------------|
| **Multiple exact matches** | `IN` | `WHERE department IN ('Sales', 'Marketing')` |
| **Different operators** | `OR` | `WHERE salary > 50000 OR hire_date < '2020-01-01'` |
| **All conditions must be true** | `AND` | `WHERE department = 'Sales' AND salary > 50000` |
| **Complex combinations** | **Mix them** | `WHERE (dept IN ('A','B')) AND (salary > 50K)` |

### 4. Aggregate Functions Mastery

#### The Complete Aggregate Function Toolkit

| Function | Purpose | Use Cases | Example |
|----------|---------|-----------|---------|
| `COUNT()` | Count rows/values | Record counting, validation | `COUNT(*)`, `COUNT(DISTINCT col)` |
| `SUM()` | Sum numerical values | Financial totals, quantities | `SUM(amount)`, `SUM(quantity)` |
| `AVG()` | Calculate average | Performance metrics, trends | `AVG(salary)`, `AVG(rating)` |
| `MIN()` | Find minimum value | Best performance, earliest date | `MIN(price)`, `MIN(order_date)` |
| `MAX()` | Find maximum value | Highest score, latest date | `MAX(score)`, `MAX(created_at)` |

#### COUNT() - The Most Important Aggregate

```sql
-- Count all rows (including NULLs)
SELECT COUNT(*) FROM employees;

-- Count non-NULL values in a column
SELECT COUNT(salary) FROM employees;

-- Count distinct values
SELECT COUNT(DISTINCT department) FROM employees;

-- Count with conditions
SELECT COUNT(*) FROM employees WHERE salary > 50000;
```

#### SUM() and AVG() - Financial Analysis

```sql
-- Total sales by department
SELECT 
    department,
    SUM(salary) as total_payroll,
    AVG(salary) as avg_salary,
    COUNT(*) as employee_count
FROM employees
GROUP BY department;
```

#### MIN() and MAX() - Range Analysis

```sql
-- Salary range analysis
SELECT 
    department,
    MIN(salary) as min_salary,
    MAX(salary) as max_salary,
    MAX(salary) - MIN(salary) as salary_range
FROM employees
GROUP BY department;
```

#### Advanced Aggregate Patterns

```sql
-- Conditional aggregation
SELECT 
    department,
    COUNT(*) as total_employees,
    SUM(CASE WHEN salary > 75000 THEN 1 ELSE 0 END) as high_earners,
    AVG(CASE WHEN gender = 'F' THEN salary END) as avg_female_salary
FROM employees
GROUP BY department;
```

### 4. GROUP BY Rules & Patterns

#### The Golden Rule of GROUP BY

**Every non-aggregated column in SELECT must be in GROUP BY**

```sql
-- ✓ CORRECT: All non-aggregated columns in SELECT are in GROUP BY
SELECT 
    department, 
    position,
    COUNT(*) as employees,
    AVG(salary) as avg_salary
FROM employees
GROUP BY department, position;

-- ✗ WRONG: position not in GROUP BY
SELECT 
    department, 
    position,
    COUNT(*) as employees
FROM employees
GROUP BY department;  -- Error!
```

#### GROUP BY Patterns for Business Analysis

```sql
-- Pattern 1: Single-level grouping
SELECT department, COUNT(*) as employee_count
FROM employees
GROUP BY department;

-- Pattern 2: Multi-level grouping
SELECT 
    department,
    position,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary
FROM employees
GROUP BY department, position;

-- Pattern 3: Time-based grouping
SELECT 
    DATE_TRUNC('month', hire_date) as hire_month,
    COUNT(*) as new_hires
FROM employees
GROUP BY DATE_TRUNC('month', hire_date)
ORDER BY hire_month;
```

#### GROUP BY with HAVING - The Complete Pattern

```sql
-- Find departments with more than 10 employees and avg salary > 70000
SELECT 
    department,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary
FROM employees
WHERE hire_date >= '2020-01-01'  -- Filter individuals first
GROUP BY department
HAVING COUNT(*) > 10 AND AVG(salary) > 70000  -- Filter groups after
ORDER BY avg_salary DESC;
```

---

## 💡 PRACTICAL EXAMPLES

### Business Scenario 1: Sales Analysis

```sql
-- Monthly sales performance analysis
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as total_orders,
    SUM(order_amount) as total_revenue,
    AVG(order_amount) as avg_order_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY DATE_TRUNC('month', order_date)
HAVING SUM(order_amount) > 100000  -- Only months with > $100K revenue
ORDER BY month;
```

### Business Scenario 2: Employee Performance

```sql
-- Department performance analysis
SELECT 
    department,
    COUNT(*) as total_employees,
    AVG(salary) as avg_salary,
    MIN(salary) as min_salary,
    MAX(salary) as max_salary,
    MAX(salary) - MIN(salary) as salary_range,
    SUM(CASE WHEN performance_rating >= 4 THEN 1 ELSE 0 END) as high_performers
FROM employees
WHERE status = 'active'
GROUP BY department
HAVING COUNT(*) >= 5  -- Only departments with 5+ employees
ORDER BY avg_salary DESC;
```

---

## 🎯 EPAM INTERVIEW FOCUS

### Classic Interview Problems

#### Problem 1: Customer Analysis
**"Find customers who have made more than 5 orders with a total value over $1000"**

```sql
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(order_amount) as total_spent
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5 AND SUM(order_amount) > 1000
ORDER BY total_spent DESC;
```

#### Problem 2: Product Performance
**"Which products have sold more than 100 units in the last 3 months?"**

```sql
SELECT 
    product_id,
    product_name,
    SUM(quantity) as total_sold,
    SUM(quantity * unit_price) as total_revenue
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_date >= DATE('now', '-3 months')
GROUP BY product_id, product_name
HAVING SUM(quantity) > 100
ORDER BY total_sold DESC;
```

### Common Interview Mistakes to Avoid

#### ❌ Mistake 1: Using HAVING instead of WHERE for individual row filtering
```sql
-- WRONG (slower, less clear)
SELECT customer_id, SUM(amount)
FROM orders
GROUP BY customer_id
HAVING amount > 100;  -- This will cause an error!

-- CORRECT
SELECT customer_id, SUM(amount)
FROM orders
WHERE amount > 100
GROUP BY customer_id;
```

#### ❌ Mistake 2: Missing columns in GROUP BY
```sql
-- WRONG (will cause error)
SELECT department, position, COUNT(*)
FROM employees
GROUP BY department;  -- position missing from GROUP BY

-- CORRECT
SELECT department, position, COUNT(*)
FROM employees
GROUP BY department, position;
```

### Interview Success Tips

1. **Start with the business question** - "What are we trying to find?"
2. **Identify the grouping** - "What are we grouping by?"
3. **Choose the right filters** - "WHERE for rows, HAVING for groups"
4. **Test with sample data** - Always verify your logic
5. **Explain your approach** - Show your thinking process

---

## 🚀 Quick Reference Guide

### SQL Clause Quick Reference

| Clause | Purpose | When to Use | Example |
|--------|---------|-------------|---------|
| `WHERE` | Filter individual rows | Before grouping | `WHERE salary > 50000` |
| `GROUP BY` | Group rows together | With aggregates | `GROUP BY department` |
| `HAVING` | Filter groups | After grouping | `HAVING COUNT(*) > 10` |
| `ORDER BY` | Sort results | Final step | `ORDER BY salary DESC` |
| `LIMIT` | Limit rows returned | Final step | `LIMIT 10` |

### Aggregate Function Quick Reference

| Function | What it does | Common use cases |
|----------|--------------|------------------|
| `COUNT(*)` | Count all rows | Total records, validation |
| `COUNT(column)` | Count non-NULL values | Data quality checks |
| `SUM(column)` | Sum numerical values | Financial totals |
| `AVG(column)` | Calculate average | Performance metrics |
| `MIN(column)` | Find minimum | Best performance, earliest |
| `MAX(column)` | Find maximum | Highest score, latest |

### Decision Tree: WHERE vs HAVING

```
Do you need to filter based on:
├── Individual row values? → Use WHERE
└── Grouped/aggregated values? → Use HAVING

Examples:
├── "Orders over $100" → WHERE amount > 100
├── "Customers with >5 orders" → HAVING COUNT(*) > 5
├── "Departments with avg salary > $70K" → HAVING AVG(salary) > 70000
└── "Active employees only" → WHERE status = 'active'
```

---

## 🏋️ Practice Strategy

### Step-by-Step Query Building Process

1. **Understand the business question**
2. **Identify what you're grouping by** (if any)
3. **Choose your filters** (WHERE vs HAVING)
4. **Select your columns and aggregates**
5. **Add sorting and limiting**
6. **Test with sample data**

### Time Targets for EPAM Interview

- **Basic queries**: 2-3 minutes
- **GROUP BY queries**: 3-5 minutes
- **Complex WHERE/HAVING**: 5-7 minutes
- **Multi-table queries**: 7-10 minutes

---

## 🎯 Next Steps

After mastering SQL basics:
1. **Complete exercises** in `01_SQL/exercises/01_Basics_Exercises.md`
2. **Move to Window Functions** - The advanced SQL topic
3. **Practice with real data** using our enhanced database
4. **Build confidence** with timed practice sessions

**You now have the foundation for all advanced SQL topics!** 🚀

---

## 💡 Best Practices

1. **Use meaningful aliases**
   ```sql
   SELECT 
       e.name as employee_name,
       d.name as department_name
   FROM employees e
   JOIN departments d ON e.dept_id = d.id;
   ```

2. **Format for readability**
   ```sql
   -- Good
   SELECT 
       column1,
       column2,
       column3
   FROM table_name
   WHERE condition = true;
   
   -- Bad
   SELECT column1,column2,column3 FROM table_name WHERE condition=true;
   ```

3. **Use DISTINCT carefully** (it's expensive)
   ```sql
   -- Only when necessary
   SELECT DISTINCT customer_id FROM orders;
   ```

---

## 🔍 Common Patterns

### Pattern 1: Top N Records
```sql
-- Top 5 customers by spending
SELECT 
    customer_name,
    SUM(order_amount) as total_spent
FROM orders
GROUP BY customer_name
ORDER BY total_spent DESC
LIMIT 5;
```

### Pattern 2: Filtering with IN
```sql
-- Orders from specific customers
SELECT *
FROM orders
WHERE customer_id IN (101, 102, 103);
```

### Pattern 3: Date Filtering
```sql
-- Orders from last 30 days
SELECT *
FROM orders
WHERE order_date >= DATE('now', '-30 days');
```

---

## 🎯 Quick Reference

### Comparison Operators
- `=` Equal to
- `!=` or `<>` Not equal to
- `>` Greater than
- `<` Less than
- `>=` Greater than or equal
- `<=` Less than or equal
- `BETWEEN` Range check
- `IN` Match any in list
- `LIKE` Pattern matching
- `IS NULL` / `IS NOT NULL` Null check

### Logical Operators
- `AND` Both conditions true
- `OR` Either condition true
- `NOT` Negates condition

### Wildcards (with LIKE)
- `%` Any number of characters
- `_` Single character

```sql
-- Names starting with 'A'
WHERE name LIKE 'A%'

-- Names with 'a' as second character
WHERE name LIKE '_a%'
```

---

## ⚠️ Common Mistakes

1. **Using HAVING instead of WHERE**
   ```sql
   -- ✗ WRONG (slower)
   SELECT * FROM orders
   GROUP BY order_id
   HAVING amount > 100;
   
   -- ✓ CORRECT (faster)
   SELECT * FROM orders
   WHERE amount > 100;
   ```

2. **Forgetting quotes for strings**
   ```sql
   -- ✗ WRONG
   WHERE name = John
   
   -- ✓ CORRECT
   WHERE name = 'John'
   ```

3. **Confusing NULL handling**
   ```sql
   -- ✗ WRONG (won't work)
   WHERE bonus = NULL
   
   -- ✓ CORRECT
   WHERE bonus IS NULL
   ```

---

## 📝 Practice Strategy

1. Write query skeleton first (SELECT...FROM)
2. Add WHERE conditions
3. Add GROUP BY if aggregating
4. Add HAVING if filtering groups
5. Add ORDER BY for sorting
6. Add LIMIT if needed

---

## 🚀 Next Steps

After mastering basics:
1. Move to Window Functions
2. Learn JOINs in depth
3. Practice query optimization

**See exercises in**: `01_SQL/exercises/01_Basics_Exercises.md`

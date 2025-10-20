# SQL Basics & Fundamentals

## 🎯 Learning Objectives

By the end of this module, you will:
- Master SQL SELECT, FROM, WHERE statements
- Understand GROUP BY and HAVING clauses
- Use aggregate functions effectively
- Write clean, readable SQL queries

---

## 📚 Core Concepts

### 1. SELECT Statement Structure

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

### 2. WHERE vs HAVING - The Critical Difference

**The fundamental difference**: WHERE filters **individual rows**, HAVING filters **groups of rows**.

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

### 3. Aggregate Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `COUNT()` | Count rows | `COUNT(*)`, `COUNT(DISTINCT col)` |
| `SUM()` | Sum values | `SUM(amount)` |
| `AVG()` | Average | `AVG(salary)` |
| `MIN()` | Minimum | `MIN(price)` |
| `MAX()` | Maximum | `MAX(score)` |

### 4. GROUP BY Rules

```sql
-- ✓ CORRECT: All non-aggregated columns in SELECT must be in GROUP BY
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

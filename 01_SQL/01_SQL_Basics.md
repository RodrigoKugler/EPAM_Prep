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

### 2. WHERE vs HAVING

**WHERE**: Filters rows BEFORE grouping
```sql
-- Get orders over $100
SELECT customer_id, order_date, amount
FROM orders
WHERE amount > 100;
```

**HAVING**: Filters groups AFTER aggregation
```sql
-- Get customers with total spend over $1000
SELECT customer_id, SUM(amount) as total
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 1000;
```

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

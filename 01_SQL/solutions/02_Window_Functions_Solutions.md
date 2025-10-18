# Window Functions - Solutions

## ⚠️ Attempt exercises FIRST before viewing solutions!

---

## Solution 1: ROW_NUMBER
```sql
SELECT 
    order_id,
    customer_id,
    order_date,
    amount,
    ROW_NUMBER() OVER (ORDER BY order_date) as row_num
FROM orders;
```

---

## Solution 2: RANK by Salary
```sql
SELECT 
    employee_name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;
```

---

## Solution 3: DENSE_RANK
```sql
SELECT 
    employee_name,
    salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;
```

---

## Solution 4: Running Total - EPAM STYLE ⭐
```sql
SELECT 
    customer_id,
    order_id,
    order_date,
    order_value,
    SUM(order_value) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM orders;
```

---

## Solution 5: Running Count - EPAM STYLE ⭐
```sql
SELECT 
    customer_id,
    order_id,
    order_date,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as order_count_history
FROM orders;
```

---

## Solution 6: LAG - Previous Value
```sql
SELECT 
    customer_id,
    order_date,
    amount,
    LAG(amount, 1) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as previous_amount
FROM orders;
```

---

## Solution 7: LEAD - Next Value
```sql
SELECT 
    customer_id,
    order_date,
    amount,
    LEAD(amount, 1) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as next_amount
FROM orders;
```

---

## Solution 8: Period-over-Period Comparison
```sql
SELECT 
    customer_id,
    order_date,
    amount,
    LAG(amount, 1) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as previous_amount,
    amount - LAG(amount, 1) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as difference
FROM orders;
```

---

## Solution 9: FIRST_VALUE and LAST_VALUE
```sql
SELECT 
    customer_id,
    order_date,
    amount,
    FIRST_VALUE(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as first_order_amount,
    LAST_VALUE(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as last_order_amount
FROM orders;
```

---

## Solution 10: Moving Average (3-Period)
```sql
SELECT 
    order_date,
    amount,
    AVG(amount) OVER (
        ORDER BY order_date 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as moving_avg_3
FROM orders;
```

---

## Solution 11: Ranking Within Groups
```sql
SELECT 
    employee_name,
    department,
    salary,
    RANK() OVER (
        PARTITION BY department 
        ORDER BY salary DESC
    ) as dept_rank
FROM employees;
```

---

## Solution 12: NTILE - Quartiles
```sql
SELECT 
    employee_name,
    salary,
    NTILE(4) OVER (ORDER BY salary) as salary_quartile
FROM employees;
```

---

## Solution 13: Top N per Group
```sql
WITH ranked AS (
    SELECT 
        employee_name,
        department,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department 
            ORDER BY salary DESC
        ) as rank
    FROM employees
)
SELECT employee_name, department, salary
FROM ranked
WHERE rank <= 3;
```

---

## Solution 14: Percentage of Total
```sql
SELECT 
    customer_id,
    order_id,
    order_value,
    SUM(order_value) OVER (PARTITION BY customer_id) as customer_total,
    ROUND(order_value * 100.0 / 
          SUM(order_value) OVER (PARTITION BY customer_id), 2) as percentage
FROM orders;
```

---

## Solution 15: Days Since Last Order
```sql
SELECT 
    customer_id,
    order_date,
    JULIANDAY(order_date) - JULIANDAY(LAG(order_date, 1) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    )) as days_since_last_order
FROM orders;
```

---

## EPAM Problem 1: Full Running Totals Solution
```sql
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
- `PARTITION BY cid` resets the window for each customer
- `ROW_NUMBER()` gives 1, 2, 3... for each customer
- `SUM() with frame` creates running total
- `ORDER BY order_date` ensures chronological order

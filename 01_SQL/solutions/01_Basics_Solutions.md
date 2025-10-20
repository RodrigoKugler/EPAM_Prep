# SQL Basics - Solutions

## ⚠️ Attempt exercises FIRST before viewing solutions!

## 🚀 Enhanced Database Examples
These solutions work with the **Enhanced Database** (`database/epam_practice.db`):
- **46,774+ records** across 16 tables
- **Real-world business scenarios**: customers, orders, products, employees
- **Performance optimized**: 18 indexes for advanced practice

**Database Guide**: See `database/DATABASE_QUICK_REFERENCE.md`

---

## Solution 1: Basic SELECT
```sql
SELECT * FROM employees;
```

**Explanation**: The simplest SELECT statement. The asterisk (*) selects all columns from the employees table.

---

## Solution 2: Filtering with WHERE
```sql
SELECT * 
FROM employees
WHERE salary > 50000;
```

**Explanation**: WHERE filters individual rows before any grouping. This keeps only employees with salary greater than 50,000.

---

## Solution 3: Using LIKE
```sql
SELECT * 
FROM employees
WHERE name LIKE 'J%';
```

**Explanation**: LIKE with 'J%' matches any name starting with 'J'. The % wildcard represents any number of characters.

---

## Solution 4: COUNT and GROUP BY
```sql
SELECT 
    department,
    COUNT(*) as employee_count
FROM employees
GROUP BY department;
```

**Explanation**: GROUP BY groups employees by department, then COUNT(*) counts the number of employees in each group. All non-aggregated columns (department) must be in GROUP BY.

---

## Solution 5: SUM Aggregation
```sql
SELECT 
    department,
    SUM(salary) as total_salary
FROM employees
GROUP BY department;
```

**Explanation**: SUM() adds up all salary values within each department group. This gives us the total salary expense per department.

---

## Solution 6: AVG with HAVING ⭐ EPAM FAVORITE
```sql
SELECT 
    department,
    AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 60000;
```

**Explanation**: This is a classic WHERE vs HAVING question! 
- AVG(salary) is calculated AFTER grouping
- HAVING filters groups based on aggregated values
- WHERE would be used to filter individual employees before grouping
- **EPAM Focus**: This tests understanding of WHERE vs HAVING distinction

---

## Solution 7: Multiple Conditions
```sql
SELECT * 
FROM employees
WHERE department IN ('Sales', 'Marketing')
  AND salary > 50000;
```

**Explanation**: IN operator is cleaner than multiple OR conditions. This finds employees in either Sales OR Marketing departments, AND with salary > 50000.

---

## Solution 8: ORDER BY
```sql
SELECT * 
FROM employees
ORDER BY salary DESC, name ASC;
```

**Explanation**: ORDER BY sorts results. DESC means descending (highest first), ASC means ascending (alphabetical). When salaries are equal, names are sorted alphabetically.

---

## Solution 9: DISTINCT
```sql
SELECT DISTINCT department 
FROM employees;
```

---

## Solution 10: IN Operator
```sql
SELECT * 
FROM employees
WHERE department_id IN (1, 3, 5);
```

---

## Solution 11: BETWEEN
```sql
SELECT * 
FROM employees
WHERE salary BETWEEN 40000 AND 70000;
```

---

## Solution 12: NULL Handling
```sql
SELECT * 
FROM employees
WHERE manager_id IS NULL;
```

---

## Solution 13: Case-Insensitive Search
```sql
SELECT * 
FROM employees
WHERE LOWER(job_title) LIKE '%manager%';
```

---

## Solution 14: Multiple Aggregations
```sql
SELECT 
    department,
    COUNT(*) as emp_count,
    AVG(salary) as avg_sal,
    MIN(salary) as min_sal,
    MAX(salary) as max_sal
FROM employees
GROUP BY department;
```

---

## Solution 15: Complex Filtering
```sql
SELECT 
    department,
    COUNT(*) as emp_count,
    AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING COUNT(*) > 5 AND AVG(salary) > 55000;
```

---

## Bonus Challenge 1: Top 5 Departments
```sql
SELECT 
    department,
    SUM(salary) as total_salary_expense
FROM employees
GROUP BY department
ORDER BY total_salary_expense DESC
LIMIT 5;
```

---

## Bonus Challenge 2: Salary Statistics
```sql
SELECT 
    department,
    COUNT(*) as emp_count,
    SUM(salary) as total_salary,
    AVG(salary) as avg_salary,
    MIN(salary) as min_salary,
    MAX(salary) as max_salary
FROM employees
GROUP BY department
ORDER BY department;
```

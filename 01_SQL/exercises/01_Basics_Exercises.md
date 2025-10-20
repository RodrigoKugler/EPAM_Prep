# SQL Basics - Practice Exercises

## 📝 Instructions
- Solve each exercise independently using the **Enhanced Database**: `database/epam_practice.db`
- Time yourself (aim for < 5 minutes each)
- Check solutions ONLY after attempting
- Solutions in: `01_SQL/solutions/01_Basics_Solutions.md`

## 🚀 Enhanced Database Available!
- **46,774+ records** across 16 tables
- **Real-world business scenarios**: customers, orders, products, employees
- **Performance optimized**: 18 indexes for advanced practice
- **EPAM interview ready**: All classic scenarios supported

**Database Guide**: See `database/DATABASE_QUICK_REFERENCE.md`

---

## Exercise 1: Basic SELECT
Write a query to select all columns from the `employees` table.

**Expected columns**: All

---

## Exercise 2: Filtering with WHERE
Write a query to find all employees with salary greater than 50000.

**Table**: employees  
**Columns**: emp_id, name, department, salary

---

## Exercise 3: Using LIKE
Write a query to find all employees whose name starts with 'J'.

---

## Exercise 4: COUNT and GROUP BY
Write a query to count the number of employees in each department.

**Expected columns**: department, employee_count

---

## Exercise 5: SUM Aggregation
Write a query to find the total salary expense per department.

**Expected columns**: department, total_salary

---

## Exercise 6: AVG with HAVING
Write a query to find departments where the average salary is above 60000.

**Expected columns**: department, avg_salary

---

## Exercise 7: Multiple Conditions
Write a query to find employees in 'Sales' or 'Marketing' departments with salary > 50000.

---

## Exercise 8: ORDER BY
Write a query to list all employees ordered by salary (highest first), then by name alphabetically.

---

## Exercise 9: DISTINCT
Write a query to find all unique departments in the employees table.

---

## Exercise 10: IN Operator
Write a query to find employees in departments with IDs 1, 3, and 5.

---

## Exercise 11: BETWEEN
Write a query to find employees with salaries between 40000 and 70000 (inclusive).

---

## Exercise 12: NULL Handling
Write a query to find all employees who have a NULL value in the manager_id column.

---

## Exercise 13: Case-Insensitive Search
Write a query to find employees with 'manager' in their job title (case-insensitive).

---

## Exercise 14: Multiple Aggregations
Write a query to show department name, employee count, average salary, min salary, and max salary.

**Expected columns**: department, emp_count, avg_sal, min_sal, max_sal

---

## Exercise 15: Complex Filtering
Write a query to find departments with more than 5 employees AND average salary > 55000.

---

## 🎯 Bonus Challenges

### Challenge 1: Top 5 Departments
Find the 5 departments with the highest total salary expense.

### Challenge 2: Salary Statistics
For each department, show count, sum, avg, min, max salary, all in one query.

### Challenge 3: Advanced Filtering
Find employees whose salary is above their department's average salary. 
(Hint: You'll need to use this concept after learning JOINs/Subqueries)

---

**Next**: Window Functions Exercises

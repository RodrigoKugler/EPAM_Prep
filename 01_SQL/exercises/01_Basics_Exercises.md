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
**Time target**: 2 minutes  
**Hint**: Use the simplest SELECT statement

---

## Exercise 2: Filtering with WHERE
Write a query to find all employees with salary greater than 50000.

**Table**: employees  
**Columns**: emp_id, name, department, salary  
**Time target**: 3 minutes  
**Hint**: Filter individual rows before any grouping

---

## Exercise 3: Using LIKE
Write a query to find all employees whose name starts with 'J'.

**Time target**: 3 minutes  
**Hint**: Use the wildcard character for pattern matching

---

## Exercise 4: COUNT and GROUP BY
Write a query to count the number of employees in each department.

**Expected columns**: department, employee_count  
**Time target**: 4 minutes  
**Hint**: Remember the GROUP BY rule - all non-aggregated columns must be in GROUP BY

---

## Exercise 5: SUM Aggregation
Write a query to find the total salary expense per department.

**Expected columns**: department, total_salary  
**Time target**: 4 minutes  
**Hint**: SUM() is an aggregate function that needs GROUP BY

---

## Exercise 6: AVG with HAVING ⭐ EPAM FAVORITE
Write a query to find departments where the average salary is above 60000.

**Expected columns**: department, avg_salary  
**Time target**: 5 minutes  
**Hint**: This tests WHERE vs HAVING understanding - use HAVING for group-level filtering  
**EPAM Focus**: This is a classic WHERE vs HAVING interview question

---

## Exercise 7: Multiple Conditions
Write a query to find employees in 'Sales' or 'Marketing' departments with salary > 50000.

**Time target**: 4 minutes  
**Hint**: Use OR for multiple department conditions, AND for salary condition

---

## Exercise 8: ORDER BY
Write a query to list all employees ordered by salary (highest first), then by name alphabetically.

**Time target**: 3 minutes  
**Hint**: Use DESC for descending order, ASC for ascending (default)

---

## Exercise 9: DISTINCT
Write a query to find all unique departments in the employees table.

**Time target**: 2 minutes  
**Hint**: DISTINCT removes duplicate values

---

## Exercise 10: IN Operator
Write a query to find employees in departments with IDs 1, 3, and 5.

**Time target**: 3 minutes  
**Hint**: IN operator is cleaner than multiple OR conditions

---

## Exercise 11: BETWEEN
Write a query to find employees with salaries between 40000 and 70000 (inclusive).

**Time target**: 3 minutes  
**Hint**: BETWEEN is inclusive of both boundary values

---

## Exercise 12: NULL Handling ⭐ IMPORTANT
Write a query to find all employees who have a NULL value in the manager_id column.

**Time target**: 4 minutes  
**Hint**: Use IS NULL, not = NULL (common interview mistake!)

---

## Exercise 13: Case-Insensitive Search
Write a query to find employees with 'manager' in their job title (case-insensitive).

**Time target**: 4 minutes  
**Hint**: Use UPPER() or LOWER() functions for case-insensitive matching

---

## Exercise 14: Multiple Aggregations ⭐ EPAM FAVORITE
Write a query to show department name, employee count, average salary, min salary, and max salary.

**Expected columns**: department, emp_count, avg_sal, min_sal, max_sal  
**Time target**: 6 minutes  
**Hint**: Multiple aggregate functions in one query - remember GROUP BY rule  
**EPAM Focus**: This tests understanding of multiple aggregations and GROUP BY

---

## Exercise 15: Complex Filtering ⭐ EPAM FAVORITE
Write a query to find departments with more than 5 employees AND average salary > 55000.

**Time target**: 7 minutes  
**Hint**: Use HAVING for both conditions - both are group-level filters  
**EPAM Focus**: This combines WHERE vs HAVING with multiple conditions

---

## 🎯 Bonus Challenges

### Challenge 1: Top 5 Departments ⭐ EPAM STYLE
Find the 5 departments with the highest total salary expense.

**Time target**: 8 minutes  
**Hint**: Combine SUM(), GROUP BY, and ORDER BY with LIMIT  
**EPAM Focus**: This tests business analysis thinking

### Challenge 2: Comprehensive Salary Statistics ⭐ EPAM STYLE
For each department, show count, sum, avg, min, max salary, all in one query.

**Time target**: 10 minutes  
**Hint**: Multiple aggregate functions with proper GROUP BY  
**EPAM Focus**: This tests comprehensive aggregation understanding

### Challenge 3: Advanced Filtering ⭐ ADVANCED
Find employees whose salary is above their department's average salary. 
(Hint: You'll need to use this concept after learning JOINs/Subqueries)

**Time target**: 15 minutes (after learning JOINs)  
**Hint**: This requires comparing individual values to group averages  
**EPAM Focus**: This tests advanced analytical thinking

---

## 🚀 EPAM Interview Simulation

### Simulation 1: Business Analysis
**Scenario**: "We need to analyze our workforce. Find departments with high salary costs and many employees."

**Requirements**:
1. Find departments with more than 10 employees
2. Where the total salary expense is over $1,000,000
3. Order by total salary expense (highest first)
4. Show department name, employee count, total salary, and average salary

**Time target**: 10 minutes  
**EPAM Focus**: Real business scenario with multiple requirements

### Simulation 2: Data Quality Check
**Scenario**: "We suspect some data quality issues. Help us identify problems."

**Requirements**:
1. Find employees with missing manager information
2. Find departments with no employees
3. Find employees with salary = 0 or NULL
4. Show the count of each issue type

**Time target**: 12 minutes  
**EPAM Focus**: Data quality and business logic understanding

---

## 📊 Progress Tracking

### Exercise Completion Checklist
- [ ] Exercise 1: Basic SELECT (2 min target)
- [ ] Exercise 2: WHERE filtering (3 min target)
- [ ] Exercise 3: LIKE pattern matching (3 min target)
- [ ] Exercise 4: COUNT and GROUP BY (4 min target)
- [ ] Exercise 5: SUM aggregation (4 min target)
- [ ] Exercise 6: AVG with HAVING ⭐ (5 min target)
- [ ] Exercise 7: Multiple conditions (4 min target)
- [ ] Exercise 8: ORDER BY sorting (3 min target)
- [ ] Exercise 9: DISTINCT values (2 min target)
- [ ] Exercise 10: IN operator (3 min target)
- [ ] Exercise 11: BETWEEN range (3 min target)
- [ ] Exercise 12: NULL handling ⭐ (4 min target)
- [ ] Exercise 13: Case-insensitive search (4 min target)
- [ ] Exercise 14: Multiple aggregations ⭐ (6 min target)
- [ ] Exercise 15: Complex filtering ⭐ (7 min target)

### Bonus Challenges
- [ ] Challenge 1: Top 5 departments (8 min target)
- [ ] Challenge 2: Salary statistics (10 min target)
- [ ] Challenge 3: Advanced filtering (15 min target)

### EPAM Simulations
- [ ] Simulation 1: Business analysis (10 min target)
- [ ] Simulation 2: Data quality check (12 min target)

---

## 🎯 Success Criteria

### Basic Mastery (All exercises)
- Complete all 15 exercises
- Stay within time targets
- Understand WHERE vs HAVING distinction
- Master GROUP BY rules

### Advanced Mastery (Bonus + Simulations)
- Complete all bonus challenges
- Successfully complete EPAM simulations
- Demonstrate business analysis thinking
- Show data quality awareness

### EPAM Interview Ready
- Can solve WHERE vs HAVING problems in < 5 minutes
- Can handle multiple aggregations confidently
- Can approach business scenarios systematically
- Can explain your thinking process clearly

---

**Next**: Window Functions Exercises - The Advanced SQL Topic!

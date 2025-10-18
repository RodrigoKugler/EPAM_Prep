# Window Functions - Practice Exercises

## 📝 Instructions
- These are CRITICAL for EPAM interviews
- Master every type of window function
- Time yourself: < 10 minutes per exercise
- Solutions in: `01_SQL/solutions/02_Window_Functions_Solutions.md`

---

## Exercise 1: ROW_NUMBER
Write a query to assign a sequential number to each order, ordered by order_date.

**Table**: orders (order_id, customer_id, order_date, amount)  
**Expected**: All columns + row_num

---

## Exercise 2: RANK by Salary
Write a query to rank employees by salary (highest first). Include ties.

**Expected**: employee_name, salary, salary_rank

---

## Exercise 3: DENSE_RANK
Same as Exercise 2, but use DENSE_RANK to avoid gaps in ranking.

---

## Exercise 4: Running Total - EPAM STYLE ⭐
Write a query to calculate the cumulative sum of order values for each customer.

**Table**: orders (customer_id, order_id, order_date, order_value)  
**Expected**: customer_id, order_id, order_date, order_value, running_total  
**PARTITION BY**: customer_id  
**ORDER BY**: order_date

This is the EXACT type EPAM asks!

---

## Exercise 5: Running Count - EPAM STYLE ⭐
Write a query to show the cumulative count of orders for each customer.

**Expected**: customer_id, order_id, order_date, order_count_history  
**Hint**: Use ROW_NUMBER()

---

## Exercise 6: LAG - Previous Value
Write a query to show each order's amount and the previous order's amount for the same customer.

**Expected**: customer_id, order_date, amount, previous_amount

---

## Exercise 7: LEAD - Next Value
Write a query to show each order's amount and the next order's amount.

---

## Exercise 8: Period-over-Period Comparison
Calculate the difference between current order amount and previous order amount for each customer.

**Expected**: customer_id, order_date, amount, previous_amount, difference

---

## Exercise 9: FIRST_VALUE and LAST_VALUE
For each customer's order, show the first order amount and last order amount of that customer.

---

## Exercise 10: Moving Average (3-Period)
Calculate a 3-period moving average of order amounts.

**Frame**: ROWS BETWEEN 2 PRECEDING AND CURRENT ROW

---

## Exercise 11: Ranking Within Groups
Rank employees by salary within their department (department-wise ranking).

**Expected**: employee_name, department, salary, dept_rank

---

## Exercise 12: NTILE - Quartiles
Divide employees into 4 equal groups (quartiles) based on salary.

**Expected**: employee_name, salary, salary_quartile

---

## Exercise 13: Top N per Group
Find the top 3 highest-paid employees in each department.

**Hint**: Use ROW_NUMBER() with PARTITION BY department, then filter WHERE row_num <= 3

---

## Exercise 14: Percentage of Total
Calculate each order's percentage of the customer's total spending.

**Expected**: customer_id, order_value, customer_total, percentage

---

## Exercise 15: Days Since Last Order
Calculate the number of days between consecutive orders for each customer.

**Hint**: Use LAG() to get previous order date, then calculate difference

---

## 🔥 EPAM INTERVIEW SIMULATION

### Problem 1: Full Running Totals (10 min) ⭐⭐⭐
Given the orders table below:

```
+-----+------------+--------------+---------------+
| cid |  order_id  |  order_date  |  order_value  |
+-----+------------+--------------+---------------+
|  A  |   qwerty   |     1-Jan    |      10       |
|  A  |   asdfgh   |     3-Jan    |      20       |
|  A  |   zxcvbn   |     10-Jan   |      30       |
|  B  |   uiopyy   |     2-Jan    |      40       |
|  B  |   lkjhgf   |     6-Jan    |      50       |
+-----+------------+--------------+---------------+
```

Write SQL to generate:
```
+-----+------------+--------------+---------------+---------------------+---------------------+
| cid |  order_id  |  order_date  |  order_value  | order_count_history | order_value_history |
+-----+------------+--------------+---------------+---------------------+---------------------+
|  A  |   qwerty   |     1-Jan    |      10       |         1           |         10          |
|  A  |   asdfgh   |     3-Jan    |      20       |         2           |         30          |
|  A  |   zxcvbn   |     10-Jan   |      30       |         3           |         60          |
|  B  |   uiopyy   |     2-Jan    |      40       |         1           |         40          |
|  B  |   lkjhgf   |     6-Jan    |      50       |         2           |         90          |
+-----+------------+--------------+---------------+---------------------+---------------------+
```

### Problem 2: Product Performance Analysis (15 min) ⭐⭐⭐
For each product, show:
- Current month sales
- Previous month sales
- Month-over-month growth percentage
- Rank by current month sales

### Problem 3: Customer Cohort Analysis (20 min) ⭐⭐⭐⭐
- Group customers by registration month
- Calculate cumulative revenue per cohort
- Rank cohorts by total revenue

---

**Master these and you'll ACE the SQL interview!** 🚀

# Window Functions - Practice Exercises (Enhanced)

## 📝 Instructions
- These are CRITICAL for EPAM interviews
- Master every type of window function
- Time yourself: < 10 minutes per exercise
- Solutions in: `01_SQL/solutions/02_Window_Functions_Solutions.md`

## 🚀 Enhanced Database Available!
- **46,774+ records** across 16 tables
- **Real-world scenarios**: 2,000 orders, 500 customers, 44,020 sales transactions
- **Time series data**: Perfect for running totals and window functions
- **Performance optimized**: 18 indexes for advanced practice

**Database Guide**: See `database/DATABASE_QUICK_REFERENCE.md`

---

## 🎯 **Level 1: Basic Functions (Beginner)**

### Exercise 1: ROW_NUMBER - Sequential Ordering ⭐
**Time Target**: 5 minutes

Write a query to assign a sequential number to each order, ordered by order_date.

**Expected Output**:
```
order_id | customer_id | order_date | total_amount | order_sequence
---------|-------------|------------|--------------|---------------
1001     | 201         | 2024-01-01 | 150.00       | 1
1002     | 202         | 2024-01-02 | 300.00       | 2
1003     | 201         | 2024-01-05 | 200.00       | 3
```

**Hint**: Use `ROW_NUMBER() OVER (ORDER BY order_date)`

---

### Exercise 2: RANK - Salary Ranking ⭐
**Time Target**: 5 minutes

Write a query to rank employees by salary (highest first). Include ties.

**Expected Output**:
```
employee_name | department_name | salary | salary_rank
--------------|-----------------|--------|------------
John Smith    | Engineering     | 95000  | 1
Jane Doe      | Engineering     | 90000  | 2
Bob Johnson   | Sales           | 90000  | 2
```

**Hint**: Use `RANK() OVER (ORDER BY salary DESC)`

---

### Exercise 3: DENSE_RANK - Ranking Without Gaps ⭐
**Time Target**: 5 minutes

Same as Exercise 2, but use DENSE_RANK to avoid gaps in ranking.

**Expected Output**:
```
employee_name | department_name | salary | salary_rank
--------------|-----------------|--------|------------
John Smith    | Engineering     | 95000  | 1
Jane Doe      | Engineering     | 90000  | 2
Bob Johnson   | Sales           | 90000  | 2
```

**Hint**: Use `DENSE_RANK() OVER (ORDER BY salary DESC)`

---

### Exercise 4: PARTITION BY - Department Ranking ⭐
**Time Target**: 7 minutes

Rank employees by salary within their department (department-wise ranking).

**Expected Output**:
```
employee_name | department_name | salary | dept_rank
--------------|-----------------|--------|----------
John Smith    | Engineering     | 95000  | 1
Jane Doe      | Engineering     | 90000  | 2
Bob Johnson   | Sales           | 90000  | 1
```

**Hint**: Use `RANK() OVER (PARTITION BY department_id ORDER BY salary DESC)`

---

### Exercise 5: NTILE - Quartiles ⭐
**Time Target**: 7 minutes

Divide employees into 4 equal groups (quartiles) based on salary.

**Expected Output**:
```
employee_name | salary | salary_quartile
--------------|--------|----------------
John Smith    | 95000  | 1
Jane Doe      | 90000  | 1
Bob Johnson   | 85000  | 2
```

**Hint**: Use `NTILE(4) OVER (ORDER BY salary DESC)`

---

## 🎯 **Level 2: Advanced Functions (Intermediate)**

### Exercise 6: LAG - Previous Value ⭐⭐
**Time Target**: 8 minutes

Write a query to show each order's amount and the previous order's amount for the same customer.

**Expected Output**:
```
customer_id | order_date | total_amount | previous_amount
------------|------------|--------------|----------------
201         | 2024-01-01 | 150.00       | NULL
201         | 2024-01-05 | 200.00       | 150.00
201         | 2024-01-10 | 100.00       | 200.00
```

**Hint**: Use `LAG(total_amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date)`

---

### Exercise 7: LEAD - Next Value ⭐⭐
**Time Target**: 8 minutes

Write a query to show each order's amount and the next order's amount for the same customer.

**Expected Output**:
```
customer_id | order_date | total_amount | next_amount
------------|------------|--------------|------------
201         | 2024-01-01 | 150.00       | 200.00
201         | 2024-01-05 | 200.00       | 100.00
201         | 2024-01-10 | 100.00       | NULL
```

**Hint**: Use `LEAD(total_amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date)`

---

### Exercise 8: Period-over-Period Comparison ⭐⭐
**Time Target**: 10 minutes

Calculate the difference between current order amount and previous order amount for each customer.

**Expected Output**:
```
customer_id | order_date | total_amount | previous_amount | amount_change
------------|------------|--------------|-----------------|--------------
201         | 2024-01-01 | 150.00       | NULL            | NULL
201         | 2024-01-05 | 200.00       | 150.00          | 50.00
201         | 2024-01-10 | 100.00       | 200.00          | -100.00
```

**Hint**: Use `LAG()` and subtract values

---

### Exercise 9: FIRST_VALUE and LAST_VALUE ⭐⭐
**Time Target**: 10 minutes

For each customer's order, show the first order amount and last order amount of that customer.

**Expected Output**:
```
customer_id | order_date | total_amount | first_amount | last_amount
------------|------------|--------------|--------------|------------
201         | 2024-01-01 | 150.00       | 150.00       | 100.00
201         | 2024-01-05 | 200.00       | 150.00       | 100.00
201         | 2024-01-10 | 100.00       | 150.00       | 100.00
```

**Hint**: Use `FIRST_VALUE()` and `LAST_VALUE()` with proper frame specification

---

### Exercise 10: Moving Average (3-Period) ⭐⭐
**Time Target**: 10 minutes

Calculate a 3-period moving average of order amounts.

**Expected Output**:
```
order_date | total_amount | moving_avg_3_period
-----------|--------------|--------------------
2024-01-01 | 150.00       | 150.00
2024-01-02 | 300.00       | 225.00
2024-01-05 | 200.00       | 216.67
2024-01-10 | 100.00       | 200.00
```

**Hint**: Use `AVG(total_amount) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`

---

## 🎯 **Level 3: Complex Patterns (Advanced)**

### Exercise 11: Running Total - EPAM STYLE ⭐⭐⭐
**Time Target**: 10 minutes

Write a query to calculate the cumulative sum of order values for each customer.

**Expected Output**:
```
customer_id | order_id | order_date | total_amount | running_total
------------|----------|------------|--------------|--------------
201         | 1001     | 2024-01-01 | 150.00       | 150.00
201         | 1003     | 2024-01-05 | 200.00       | 350.00
201         | 1005     | 2024-01-10 | 100.00       | 450.00
202         | 1002     | 2024-01-02 | 300.00       | 300.00
202         | 1004     | 2024-01-08 | 250.00       | 550.00
```

**Hint**: Use `SUM(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`

---

### Exercise 12: Running Count - EPAM STYLE ⭐⭐⭐
**Time Target**: 10 minutes

Write a query to show the cumulative count of orders for each customer.

**Expected Output**:
```
customer_id | order_id | order_date | order_count_history
------------|----------|------------|--------------------
201         | 1001     | 2024-01-01 | 1
201         | 1003     | 2024-01-05 | 2
201         | 1005     | 2024-01-10 | 3
202         | 1002     | 2024-01-02 | 1
202         | 1004     | 2024-01-08 | 2
```

**Hint**: Use `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date)`

---

### Exercise 13: Top N per Group ⭐⭐⭐
**Time Target**: 12 minutes

Find the top 3 highest-paid employees in each department.

**Expected Output**:
```
employee_name | department_name | salary | dept_rank
--------------|-----------------|--------|----------
John Smith    | Engineering     | 95000  | 1
Jane Doe      | Engineering     | 90000  | 2
Bob Johnson   | Sales           | 90000  | 1
```

**Hint**: Use CTE with `ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC)`

---

### Exercise 14: Percentage of Total ⭐⭐⭐
**Time Target**: 12 minutes

Calculate each order's percentage of the customer's total spending.

**Expected Output**:
```
customer_id | total_amount | customer_total | percentage
------------|--------------|----------------|-----------
201         | 150.00       | 450.00         | 33.33
201         | 200.00       | 450.00         | 44.44
201         | 100.00       | 450.00         | 22.22
```

**Hint**: Use `SUM(total_amount) OVER (PARTITION BY customer_id)` for total

---

### Exercise 15: Days Since Last Order ⭐⭐⭐
**Time Target**: 15 minutes

Calculate the number of days between consecutive orders for each customer.

**Expected Output**:
```
customer_id | order_date | total_amount | prev_order_date | days_since_last_order
------------|------------|--------------|-----------------|---------------------
201         | 2024-01-01 | 150.00       | NULL            | NULL
201         | 2024-01-05 | 200.00       | 2024-01-01      | 4
201         | 2024-01-10 | 100.00       | 2024-01-05      | 5
```

**Hint**: Use `LAG()` and `JULIANDAY()` for date difference

---

## 🔥 **Level 4: EPAM Interview Simulation (Expert)**

### Problem 1: Full Running Totals (10 min) ⭐⭐⭐
**Time Target**: 10 minutes

Given the orders table, write SQL to generate cumulative count and cumulative sum:

**Expected Output**:
```
customer_id | order_id | order_date | total_amount | order_count_history | order_value_history
------------|----------|------------|--------------|--------------------|--------------------
201         | 1001     | 2024-01-01 | 150.00       | 1                  | 150.00
201         | 1003     | 2024-01-05 | 200.00       | 2                  | 350.00
201         | 1005     | 2024-01-10 | 100.00       | 3                  | 450.00
202         | 1002     | 2024-01-02 | 300.00       | 1                  | 300.00
202         | 1004     | 2024-01-08 | 250.00       | 2                  | 550.00
```

**This is the EXACT type EPAM asks!**

---

### Problem 2: Sales Performance Analysis (15 min) ⭐⭐⭐
**Time Target**: 15 minutes

For each sales rep, show:
- Current month sales
- Previous month sales
- Month-over-month growth percentage
- Rank by current month sales

**Expected Output**:
```
rep_name | current_month | prev_month | growth_percent | sales_rank
---------|---------------|------------|----------------|------------
John     | 50000.00      | 45000.00   | 11.11          | 1
Jane     | 48000.00      | 42000.00   | 14.29          | 2
```

---

### Problem 3: Customer Cohort Analysis (20 min) ⭐⭐⭐⭐
**Time Target**: 20 minutes

- Group customers by registration month
- Calculate cumulative revenue per cohort
- Rank cohorts by total revenue

**Expected Output**:
```
cohort_month | customer_count | total_revenue | revenue_rank
-------------|----------------|---------------|-------------
2024-01      | 150            | 75000.00      | 1
2024-02      | 120            | 60000.00      | 2
```

---

## 🎯 **Progress Tracking**

### **Beginner Level (Level 1)**
- [ ] Exercise 1: ROW_NUMBER
- [ ] Exercise 2: RANK
- [ ] Exercise 3: DENSE_RANK
- [ ] Exercise 4: PARTITION BY
- [ ] Exercise 5: NTILE

### **Intermediate Level (Level 2)**
- [ ] Exercise 6: LAG
- [ ] Exercise 7: LEAD
- [ ] Exercise 8: Period-over-Period
- [ ] Exercise 9: FIRST_VALUE/LAST_VALUE
- [ ] Exercise 10: Moving Average

### **Advanced Level (Level 3)**
- [ ] Exercise 11: Running Total
- [ ] Exercise 12: Running Count
- [ ] Exercise 13: Top N per Group
- [ ] Exercise 14: Percentage of Total
- [ ] Exercise 15: Days Since Last Order

### **Expert Level (Level 4)**
- [ ] Problem 1: Full Running Totals
- [ ] Problem 2: Sales Performance Analysis
- [ ] Problem 3: Customer Cohort Analysis

---

## 🎯 **Success Criteria**

**Complete all exercises and you'll be ready for EPAM's window function questions!**

### **Beginner Success**: Complete Level 1 in under 35 minutes
### **Intermediate Success**: Complete Level 2 in under 50 minutes
### **Advanced Success**: Complete Level 3 in under 75 minutes
### **Expert Success**: Complete Level 4 in under 45 minutes

**Total Time Target**: Under 3 hours for complete mastery

---

## 🚀 **EPAM Interview Readiness**

**Master these exercises and you'll ACE the SQL interview!**

1. **Level 1-2**: Foundation knowledge (30% of interview)
2. **Level 3**: Advanced patterns (50% of interview)
3. **Level 4**: Expert problem-solving (20% of interview)

**Focus on Level 3 and 4 for maximum impact!** 🚀💪

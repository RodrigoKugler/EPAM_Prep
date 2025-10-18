# EPAM Interview - Technical Coding Questions

## 🎯 Purpose
These are the ACTUAL coding problems from EPAM interviews.
Practice solving each in < 15 minutes total.

---

## 📊 SQL Problems (From EPAM PDF)

### Problem 1: Cumulative Orders ⭐⭐⭐ [CRITICAL]
**Time Limit**: 10 minutes

**Given**:
```
Orders Table:
+-----+------------+--------------+---------------+
| cid |  order_id  |  order_date  |  order_value  |
+-----+------------+--------------+---------------+
|  A  |   qwerty   |     1-Jan    |      10       |
|  A  |   asdfgh   |     3-Jan    |      20       |
|  A  |   zxcvbn   |     10-Jan   |      30       |
|  B  |   uiopyy   |     2-Jan    |      40       |
|  B  |   lkjhgf   |     6-Jan    |      50       |
|  B  |   mnbvcx   |     8-Jan    |      60       |
|  B  |   rtyfgh   |     10-Jan   |      70       |
|  C  |   fghcvb   |     1-Feb    |      80       |
|  C  |   bnmghj   |     1-Feb    |      90       |
|  C  |   wersdf   |     3-Feb    |      100      |
|  C  |   asdzxc   |     4-Feb    |      110      |
+-----+------------+--------------+---------------+
```

**Task**: Write SQL for generating cumulative/running count of orders and cumulative/running order values for every order per customer.

**Expected Output**:
```
+-----+------------+--------------+---------------+---------------------+---------------------+
| cid |  order_id  |  order_date  |  order_value  | order_count_history | order_value_history |
+-----+------------+--------------+---------------+---------------------+---------------------+
|  A  |   qwerty   |     1-Jan    |      10       |         1           |         10          |
|  A  |   asdfgh   |     3-Jan    |      20       |         2           |         30          |
|  A  |   zxcvbn   |     10-Jan   |      30       |         3           |         60          |
|  B  |   uiopyy   |     2-Jan    |      40       |         1           |         40          |
|  B  |   lkjhgf   |     6-Jan    |      50       |         2           |         90          |
|  B  |   mnbvcx   |     8-Jan    |      60       |         3           |         150         |
|  B  |   rtyfgh   |     10-Jan   |      70       |         4           |         220         |
|  C  |   fghcvb   |     1-Feb    |      80       |         1           |         80          |
|  C  |   bnmghj   |     1-Feb    |      90       |         2           |         170         |
|  C  |   wersdf   |     3-Feb    |      100      |         3           |         270         |
|  C  |   asdzxc   |     4-Feb    |      110      |         4           |         380         |
+-----+------------+--------------+---------------+---------------------+---------------------+
```

**Your Solution**:
```sql
-- Write your solution here


```

**Hints**:
- Use ROW_NUMBER() for cumulative count
- Use SUM() with OVER() for cumulative sum
- PARTITION BY customer
- ORDER BY date

---

### Problem 2: Managers with 5+ Direct Reports ⭐⭐
**Time Limit**: 5 minutes

**Given**:
```
Employee table:
+-----+-------+------------+-----------+
| id  | name  | department | managerId |
+-----+-------+------------+-----------+
| 101 | John  | A          | null      |
| 102 | Dan   | A          | 101       |
| 103 | James | A          | 101       |
| 104 | Amy   | A          | 101       |
| 105 | Anne  | A          | 101       |
| 106 | Ron   | B          | 101       |
+-----+-------+------------+-----------+
```

**Task**: Write a solution to find managers with at least five direct reports.

**Expected Output**:
```
+------+
| name |
+------+
| John |
+------+
```

**Your Solution**:
```sql
-- Write your solution here


```

**Hint**: GROUP BY managerId, then filter with HAVING COUNT(*) >= 5

---

### Problem 3: Employee Bonus ⭐⭐
**Time Limit**: 7 minutes

**Given**:
```
Employee table:
+-------+--------+------------+--------+
| empId | name   | supervisor | salary |
+-------+--------+------------+--------+
| 3     | Brad   | null       | 4000   |
| 1     | John   | 3          | 1000   |
| 2     | Dan    | 3          | 2000   |
| 4     | Thomas | 3          | 4000   |
+-------+--------+------------+--------+

Bonus table:
+-------+-------+
| empId | bonus |
+-------+-------+
| 2     | 500   |
| 4     | 2000  |
+-------+-------+
```

**Task**: Write a solution to report the name and bonus amount of each employee with a bonus less than 1000.

**Expected Output**:
```
+------+-------+
| name | bonus |
+------+-------+
| Brad | null  |
| John | null  |
| Dan  | 500   |
+------+-------+
```

**Your Solution**:
```sql
-- Write your solution here


```

**Hint**: LEFT JOIN to include employees with no bonus

---

### Problem 4: Employees with Same Salary ⭐⭐
**Time Limit**: 5 minutes

**Given**:
```
employees table:
emp_id | emp_name | job_name  | manager_id | start_date  | salary  | commission | dep_id
-------|----------|-----------|------------|-------------|---------|------------|-------
68319  | KAYLING  | PRESIDENT |            | 1991-11-18  | 6000.00 |            | 1001
66928  | BLAZE    | MANAGER   | 68319      | 1991-05-01  | 2750.00 |            | 3001
67832  | CLARE    | MANAGER   | 68319      | 1991-06-09  | 2550.00 |            | 1001
65646  | JONAS    | MANAGER   | 68319      | 1991-04-02  | 2957.00 |            | 2001
67858  | SCARLET  | ANALYST   | 65646      | 1997-04-19  | 3100.00 |            | 2001
69062  | FRANK    | ANALYST   | 65646      | 1991-12-03  | 3100.00 |            | 2001
63679  | SANDRINE | CLERK     | 69062      | 1990-12-18  | 900.00  |            | 2001
```

**Task**: List emp_name with the same salary in the same departments

**Your Solution**:
```sql
-- Write your solution here


```

---

### Problem 5: Classes with 5+ Students ⭐
**Time Limit**: 3 minutes

**Given**:
```
Courses table:
+---------+----------+
| student | class    |
+---------+----------+
| A       | Math     |
| B       | English  |
| C       | Math     |
| D       | Biology  |
| E       | Math     |
| F       | Computer |
| G       | Math     |
| H       | Math     |
| I       | Math     |
+---------+----------+
```

**Task**: Write a solution to find all the classes that have at least five students.

**Expected Output**:
```
+---------+
| class   |
+---------+
| Math    |
+---------+
```

**Your Solution**:
```sql
-- Write your solution here


```

---

### Problem 6: First Year Sales ⭐⭐
**Time Limit**: 8 minutes

**Given**:
```
Sales table:
+---------+------------+------+----------+-------+
| sale_id | product_id | year | quantity | price |
+---------+------------+------+----------+-------+
| 1       | 100        | 2008 | 10       | 5000  |
| 2       | 100        | 2009 | 12       | 5000  |
| 7       | 200        | 2011 | 15       | 9000  |
+---------+------------+------+----------+-------+

Product table:
+------------+--------------+
| product_id | product_name |
+------------+--------------+
| 100        | Nokia        |
| 200        | Apple        |
| 300        | Samsung      |
+------------+--------------+
```

**Task**: Write a solution to select the product id, year, quantity, and price for the first year of every product sold. Return the resulting table ordered by product_id.

**Expected Output**:
```
+------------+------------+----------+-------+
| product_id | first_year | quantity | price |
+------------+------------+----------+-------+
| 100        | 2008       | 10       | 5000  |
| 200        | 2011       | 15       | 9000  |
+------------+------------+----------+-------+
```

**Your Solution**:
```sql
-- Write your solution here


```

**Hint**: Use window function RANK() or MIN()

---

### Problem 7: Simple Student Lookup ⭐
**Time Limit**: 2 minutes

**Given**:
```
Input:
+------------+---------+-----+
| student_id | name    | age |
+------------+---------+-----+
| 101        | Ulysses | 13  |
| 53         | William | 10  |
| 128        | Henry   | 6   |
| 3          | Henry   | 11  |
+------------+---------+-----+
```

**Task**: Write a solution to select the name and age of the student with student_id = 101

**Expected Output**:
```
+---------+-----+
| name    | age |
+---------+-----+
| Ulysses | 13  |
+---------+-----+
```

**Your Solution**:
```sql
-- Write your solution here


```

---

## 🐍 Python Problems (From EPAM PDF)

### Problem 8: Word Counting ⭐⭐⭐ [CRITICAL]
**Time Limit**: 10 minutes

**Task**: Write a Python code that can count words separated by space and print the result. The code should read one line from standard input and output for each unique word the number of times it occurs (case insensitive) in "word count" format.

**Input**: `"apple aPPle banana baNAna TEST s Apple S Test s Te te est"`

**Expected Output**:
```
banana 2
test 2
s 3
te 2
est 1
apple 3
```

**Your Solution**:
```python
# Write your solution here






```

**Hints**:
- Use `.lower()` for case-insensitive
- Use `.split()` to split by space
- Use dictionary or Counter

---

### Problem 9: Extract Email Domains ⭐⭐⭐ [CRITICAL]
**Time Limit**: 12 minutes

**Input - JSON file**:
```json
{
  "data": [
    {"id": 1, "name": "John Doe", "email": "john.doe@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane.smith@exxxample.com"},
    {"id": 3, "name": "Bob Johnson", "email": "bob.johnson@example.com"},
    {"id": 4, "name": "Sarah Denth", "email": "sarah.denth@dummydata.com"}
  ]
}
```

**Task**: Write Python code to get unique email domains

**Expected Output**: `{"example.com", "exxxample.com", "dummydata.com"}`

**Your Solution**:
```python
# Write your solution here









```

**Hints**:
- Use `json.load()` to read JSON
- Split email by '@' and take second part
- Use set for unique values

---

## ⏱️ Speed Challenge

Can you solve all 9 problems in under 60 minutes?

### Recommended Time Allocation:
- Problem 1 (Cumulative): 10 min
- Problem 2 (Managers): 5 min
- Problem 3 (Bonus): 7 min
- Problem 4 (Same Salary): 5 min
- Problem 5 (Classes): 3 min
- Problem 6 (First Year): 8 min
- Problem 7 (Student): 2 min
- Problem 8 (Word Count): 10 min
- Problem 9 (Domains): 10 min
**Total**: 60 minutes

---

## 🎯 Interview Day Checklist

Before the interview, make sure you can:
- [ ] Solve Problem 1 (Cumulative) in < 10 min
- [ ] Solve Problem 8 (Word Count) in < 10 min
- [ ] Solve Problem 9 (Email Domains) in < 12 min
- [ ] Explain your solution clearly
- [ ] Handle follow-up questions
- [ ] Optimize your solution if asked

---

## 📝 Practice Log

Track your solve times:

| Problem | Attempt 1 | Attempt 2 | Attempt 3 | Best Time | Target |
|---------|-----------|-----------|-----------|-----------|--------|
| 1. Cumulative | __ min | __ min | __ min | __ min | < 10 min |
| 2. Managers | __ min | __ min | __ min | __ min | < 5 min |
| 3. Bonus | __ min | __ min | __ min | __ min | < 7 min |
| 4. Same Salary | __ min | __ min | __ min | __ min | < 5 min |
| 5. Classes | __ min | __ min | __ min | __ min | < 3 min |
| 6. First Year | __ min | __ min | __ min | __ min | < 8 min |
| 7. Student | __ min | __ min | __ min | __ min | < 2 min |
| 8. Word Count | __ min | __ min | __ min | __ min | < 10 min |
| 9. Domains | __ min | __ min | __ min | __ min | < 12 min |

**Goal**: All under target time by interview day!

---

**Solutions**: See `08_Interview_Prep/Technical_Solutions.md` (attempt first!)

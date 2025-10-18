# EPAM Technical Problems - Solutions

## ⚠️ Attempt ALL problems FIRST before viewing solutions!

---

## Problem 1 Solution: Cumulative Orders
```sql
SELECT 
    cid,
    order_id,
    order_date,
    order_value,
    ROW_NUMBER() OVER (
        PARTITION BY cid 
        ORDER BY order_date
    ) as order_count_history,
    SUM(order_value) OVER (
        PARTITION BY cid 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as order_value_history
FROM orders
ORDER BY cid, order_date;
```

**Explanation**:
- `PARTITION BY cid`: Reset numbering for each customer
- `ROW_NUMBER()`: Sequential count (1, 2, 3...)
- `SUM()` with frame: Running total
- `ORDER BY order_date`: Chronological order

---

## Problem 2 Solution: Managers with 5+ Reports
```sql
SELECT 
    e2.name
FROM employee e1
JOIN employee e2 ON e1.managerId = e2.id
GROUP BY e1.managerId, e2.name
HAVING COUNT(*) >= 5;
```

**Alternative Solution**:
```sql
SELECT name
FROM employee
WHERE id IN (
    SELECT managerId
    FROM employee
    WHERE managerId IS NOT NULL
    GROUP BY managerId
    HAVING COUNT(*) >= 5
);
```

---

## Problem 3 Solution: Employee Bonus
```sql
SELECT 
    e.name,
    b.bonus
FROM employee e
LEFT JOIN bonus b ON e.empId = b.empId
WHERE b.bonus < 1000 OR b.bonus IS NULL;
```

**Key Point**: LEFT JOIN to include employees with no bonus (NULL)

---

## Problem 4 Solution: Employees with Same Salary
```sql
SELECT e1.emp_name
FROM employees e1
JOIN employees e2 ON e1.salary = e2.salary 
                  AND e1.dep_id = e2.dep_id 
                  AND e1.emp_id != e2.emp_id
GROUP BY e1.emp_name;
```

**Alternative with Window Function**:
```sql
SELECT emp_name
FROM (
    SELECT 
        emp_name,
        salary,
        dep_id,
        COUNT(*) OVER (PARTITION BY salary, dep_id) as count_same_salary
    FROM employees
)
WHERE count_same_salary > 1;
```

---

## Problem 5 Solution: Classes with 5+ Students
```sql
SELECT class
FROM courses
GROUP BY class
HAVING COUNT(*) >= 5;
```

**Simple**: Just GROUP BY and HAVING

---

## Problem 6 Solution: First Year Sales
```sql
SELECT 
    product_id,
    year as first_year,
    quantity,
    price
FROM (
    SELECT 
        product_id,
        year,
        quantity,
        price,
        RANK() OVER (PARTITION BY product_id ORDER BY year) as year_rank
    FROM sales
)
WHERE year_rank = 1
ORDER BY product_id;
```

**Alternative with MIN**:
```sql
SELECT 
    s.product_id,
    s.year as first_year,
    s.quantity,
    s.price
FROM sales s
WHERE s.year = (
    SELECT MIN(year) 
    FROM sales s2 
    WHERE s2.product_id = s.product_id
)
ORDER BY s.product_id;
```

---

## Problem 7 Solution: Simple Student Lookup
```sql
SELECT name, age
FROM students
WHERE student_id = 101;
```

**Simplest**: Just a WHERE clause

---

## Problem 8 Solution: Word Counting (Python)

### Solution 1: Using Dictionary
```python
def count_words(text):
    # Convert to lowercase and split
    words = text.lower().split()
    
    # Count words
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    
    # Print results
    for word, count in word_count.items():
        print(f"{word} {count}")

# Test
input_text = "apple aPPle banana baNAna TEST s Apple S Test s Te te est"
count_words(input_text)
```

### Solution 2: Using Counter (Better!)
```python
from collections import Counter

def count_words_v2(text):
    words = text.lower().split()
    word_count = Counter(words)
    
    for word, count in word_count.items():
        print(f"{word} {count}")

# Test
input_text = "apple aPPle banana baNAna TEST s Apple S Test s Te te est"
count_words_v2(input_text)
```

### Solution 3: One-Liner
```python
from collections import Counter

text = "apple aPPle banana baNAna TEST s Apple S Test s Te te est"
for word, count in Counter(text.lower().split()).items():
    print(f"{word} {count}")
```

**Key Points**:
- Use `.lower()` for case-insensitive
- Use `.split()` to separate words
- Counter automatically counts occurrences

---

## Problem 9 Solution: Extract Email Domains (Python)

### Solution 1: Explicit
```python
import json

def extract_domains(filename):
    # Read JSON file
    with open(filename, 'r') as file:
        data = json.load(file)
    
    # Extract domains
    domains = set()
    for user in data['data']:
        email = user['email']
        domain = email.split('@')[1]
        domains.add(domain)
    
    return domains

# Test
result = extract_domains('users.json')
print(result)
# Output: {'example.com', 'exxxample.com', 'dummydata.com'}
```

### Solution 2: List Comprehension
```python
import json

def extract_domains_v2(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    domains = {user['email'].split('@')[1] for user in data['data']}
    return domains

# Test
result = extract_domains_v2('users.json')
print(result)
```

### Solution 3: One-Liner (Advanced)
```python
import json

with open('users.json') as f:
    domains = {u['email'].split('@')[1] for u in json.load(f)['data']}
    print(domains)
```

**Key Points**:
- Use `json.load()` to read JSON file
- Split email by '@' and take index 1 (second part)
- Use set `{}` for unique values

---

## 🎯 Interview Tips

### For SQL Problems:
1. **Read carefully**: Understand what's asked
2. **Check sample data**: Understand the structure
3. **Start with FROM**: Build query step by step
4. **Test with sample**: Verify output matches expected
5. **Explain**: Walk through your logic

### For Python Problems:
1. **Import first**: `import json`, `from collections import Counter`
2. **Handle errors**: Use try-except for file operations
3. **Test with examples**: Run with sample data
4. **Keep it simple**: Don't overcomplicate
5. **Comment your code**: Show your thought process

---

## 📝 Common Mistakes to Avoid

### SQL:
- Forgetting `PARTITION BY` in window functions
- Using `HAVING` when `WHERE` is appropriate
- Incorrect JOIN types (INNER vs LEFT)
- Not handling NULL values
- Forgetting `ORDER BY` in window functions

### Python:
- Not handling case sensitivity (use `.lower()`)
- Forgetting to import libraries
- Not handling missing JSON keys
- Using mutable default arguments
- Not closing files (use `with` statement)

---

**You're ready for the interview! 🚀**

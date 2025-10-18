# 🚀 EPAM Interview - Quick Reference Guide

## 📋 Last-Minute Review Before Interview

---

## 🔵 SQL - Essential Patterns

### Window Function Template
```sql
SELECT 
    column1,
    column2,
    WINDOW_FUNCTION() OVER (
        PARTITION BY group_column 
        ORDER BY sort_column
        ROWS BETWEEN start AND end
    ) as result
FROM table;
```

### Common Window Functions
```sql
-- Running total
SUM(amount) OVER (PARTITION BY customer ORDER BY date)

-- Row numbering  
ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC)

-- Previous value
LAG(amount, 1) OVER (PARTITION BY customer ORDER BY date)

-- Next value
LEAD(amount, 1) OVER (PARTITION BY customer ORDER BY date)

-- Ranking (with gaps)
RANK() OVER (ORDER BY salary DESC)

-- Ranking (no gaps)
DENSE_RANK() OVER (ORDER BY salary DESC)

-- Quartiles
NTILE(4) OVER (ORDER BY salary)
```

### EPAM Cumulative Pattern ⭐
```sql
SELECT 
    customer_id,
    order_id,
    order_date,
    order_value,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as count_history,
    SUM(order_value) OVER (PARTITION BY customer_id ORDER BY order_date 
                           ROWS UNBOUNDED PRECEDING) as value_history
FROM orders;
```

### JOIN Quick Reference
```sql
-- INNER JOIN (only matches)
SELECT * FROM a INNER JOIN b ON a.id = b.id;

-- LEFT JOIN (all from left)
SELECT * FROM a LEFT JOIN b ON a.id = b.id;

-- Find managers with 5+ reports
SELECT m.name
FROM employee e
JOIN employee m ON e.managerId = m.id
GROUP BY m.id, m.name
HAVING COUNT(*) >= 5;
```

### Aggregation Pattern
```sql
-- GROUP BY with HAVING
SELECT 
    department,
    COUNT(*) as emp_count,
    AVG(salary) as avg_sal
FROM employees
GROUP BY department
HAVING COUNT(*) >= 5;
```

---

## 🐍 Python - Essential Patterns

### Word Counting (EPAM Style) ⭐
```python
from collections import Counter

text = "apple aPPle banana baNAna"
word_count = Counter(text.lower().split())

for word, count in word_count.items():
    print(f"{word} {count}")
```

### JSON Email Domains (EPAM Style) ⭐
```python
import json

with open('data.json') as f:
    data = json.load(f)

domains = {user['email'].split('@')[1] for user in data['data']}
print(domains)
```

### String Manipulation
```python
# Case conversion
text.lower()
text.upper()
text.title()

# Splitting and joining
words = text.split()        # Split by space
parts = text.split(',')     # Split by comma
result = ' '.join(words)    # Join with space

# Stripping
text.strip()                # Both ends
text.lstrip()               # Left only
text.rstrip()               # Right only

# Checking
text.startswith('A')
text.endswith('z')
'substring' in text
```

### JSON Processing
```python
import json

# Read JSON
with open('file.json') as f:
    data = json.load(f)

# Write JSON
with open('file.json', 'w') as f:
    json.dump(data, f, indent=2)

# Parse string
data = json.loads(json_string)

# Convert to string
json_string = json.dumps(data)

# Safe access
data.get('key', default_value)
```

### List Comprehensions
```python
# Basic
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(10) if x % 2 == 0]

# Dict comprehension
{k: v for k, v in items}

# Set comprehension
{x for x in items}
```

---

## 🎯 Conceptual Q&A Cheat Sheet

### SQL Concepts

**Q: WHERE vs HAVING?**
- WHERE: Filters rows before grouping
- HAVING: Filters groups after aggregation

**Q: ACID Properties?**
- **A**tomicity: All or nothing
- **C**onsistency: Valid state
- **I**solation: No interference
- **D**urability: Permanent once committed

**Q: OLTP vs OLAP?**
- **OLTP**: Transactions, normalized, many users, current data
- **OLAP**: Analysis, denormalized, few users, historical data

**Q: Window Functions vs GROUP BY?**
- Window: Keeps all rows
- GROUP BY: Collapses rows

### Data Warehousing

**Q: Star vs Snowflake Schema?**
- **Star**: Denormalized dimensions, faster queries
- **Snowflake**: Normalized dimensions, less storage

**Q: SCD Types?**
- **Type 1**: Overwrite (no history)
- **Type 2**: New row (full history)
- **Type 3**: New column (limited history)

**Q: Fact vs Dimension?**
- **Fact**: Measurements (sales amount, quantity)
- **Dimension**: Context (customer name, product, date)

### ETL/ELT

**Q: ETL vs ELT?**
- **ETL**: Transform before loading (traditional)
- **ELT**: Load then transform (cloud warehouses)

**Q: Incremental Load?**
Load only new/changed data since last load
- Timestamp-based
- Flag-based
- CDC (Change Data Capture)

### Cloud & Big Data

**Q: Data Lake vs Data Warehouse?**
- **Lake**: Raw data, all types, schema-on-read
- **Warehouse**: Processed data, structured, schema-on-write

**Q: Apache Airflow?**
Workflow orchestration platform
- **DAG**: Workflow definition
- **Operators**: Tasks
- **Sensors**: Wait for conditions

**Q: BigQuery Partitioning?**
Divide table into smaller chunks
- Faster queries (scan less data)
- Lower cost (pay per data scanned)

---

## ⏱️ Time Management

### Interview Timing
- SQL Window Functions: < 10 min
- SQL JOINs: < 5-7 min  
- Python Word Count: < 10 min
- Python JSON Parse: < 12 min
- Explain solution: 2-3 min

### Problem-Solving Approach
1. **Read carefully** (30 sec)
2. **Understand sample data** (30 sec)
3. **Plan approach** (1 min)
4. **Write code** (5-8 min)
5. **Test with example** (1 min)
6. **Explain** (2 min)

---

## 🎯 The 9 EPAM Problems - Quick Reference

1. **Cumulative Orders**: ROW_NUMBER + SUM with PARTITION BY
2. **5+ Reports**: GROUP BY managerId, HAVING COUNT >= 5
3. **Bonus < 1000**: LEFT JOIN, WHERE bonus < 1000 OR NULL
4. **Same Salary**: SELF JOIN on salary and department
5. **5+ Students**: GROUP BY class, HAVING COUNT >= 5
6. **First Year**: RANK() OVER (PARTITION BY product ORDER BY year)
7. **Student Lookup**: WHERE student_id = 101
8. **Word Count**: Counter(text.lower().split())
9. **Email Domains**: {email.split('@')[1] for email in emails}

---

## 💡 Common Mistakes to Avoid

### SQL
- ❌ Forgetting PARTITION BY in window functions
- ❌ Using HAVING when WHERE is appropriate
- ❌ Wrong JOIN type (INNER when need LEFT)
- ❌ Not handling NULL values
- ❌ Missing ORDER BY in window functions

### Python
- ❌ Not using .lower() for case-insensitive
- ❌ Forgetting to import libraries
- ❌ Not handling missing JSON keys
- ❌ Using split(' ') instead of split()
- ❌ Not using 'with' for file operations

---

## 🎤 Interview Tips

### Technical
1. **Explain as you code**: Think out loud
2. **Test with examples**: Verify output
3. **Handle edge cases**: NULL, empty, duplicates
4. **Ask clarifications**: Don't assume
5. **Optimize if needed**: But working solution first

### Behavioral
1. **Stay calm**: Breathe, take your time
2. **Be honest**: "I don't know, but here's how I'd find out"
3. **Show problem-solving**: Explain your reasoning
4. **Be collaborative**: Ask questions, discuss trade-offs
5. **Follow up**: "Would you like me to optimize this?"

---

## 📊 SQL Function Cheat Sheet

### Aggregate Functions
```sql
COUNT(*)              -- Count rows
COUNT(DISTINCT col)   -- Count unique values
SUM(col)              -- Sum values
AVG(col)              -- Average
MIN(col)              -- Minimum
MAX(col)              -- Maximum
```

### String Functions
```sql
UPPER(col)            -- Uppercase
LOWER(col)            -- Lowercase
LENGTH(col)           -- String length
SUBSTR(col, start, len)  -- Substring
CONCAT(col1, col2)    -- Concatenate
col LIKE '%pattern%'  -- Pattern matching
```

### Date Functions (SQLite)
```sql
DATE('now')           -- Current date
JULIANDAY(date)       -- Convert to Julian day
DATE(date, '+1 day')  -- Add days
STRFTIME('%Y-%m', date)  -- Format date
```

---

## 🐍 Python Function Cheat Sheet

### String Methods
```python
str.lower()           # Lowercase
str.upper()           # Uppercase
str.split()           # Split by whitespace
str.split(',')        # Split by comma
str.strip()           # Remove whitespace
str.replace(old, new) # Replace
str.startswith(sub)   # Check start
str.endswith(sub)     # Check end
'sub' in str          # Check contains
```

### Collections
```python
from collections import Counter

Counter(items)        # Count occurrences
dict.get(key, default)  # Safe dict access
set(items)            # Unique values
list(items)           # Convert to list
```

---

## 🚀 Last-Minute Checklist

### 30 Minutes Before
- [ ] Review this quick reference
- [ ] Run through 2-3 practice problems
- [ ] Test your environment (if remote)
- [ ] Have pen and paper ready

### During Interview
- [ ] Read problem carefully
- [ ] Ask clarifying questions
- [ ] Explain your approach
- [ ] Write clean, formatted code
- [ ] Test with provided examples
- [ ] Discuss time/space complexity if asked

---

**You're prepared. You're ready. Go ace that interview!** 🚀💪

---

**For detailed explanations, see:**
- Conceptual Questions: `08_Interview_Prep/Conceptual_Questions.md`
- Technical Problems: `08_Interview_Prep/Technical_Questions.md`
- Solutions: `08_Interview_Prep/Technical_Solutions.md`


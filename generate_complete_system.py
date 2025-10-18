"""
COMPLETE TRAINING SYSTEM GENERATOR
Generates ALL remaining training materials, exercises, solutions, and interview prep
"""

import os

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ {path}")

# =============================================================================
# SQL EXERCISES
# =============================================================================

SQL_BASICS_EXERCISES = """# SQL Basics - Practice Exercises

## 📝 Instructions
- Solve each exercise independently
- Time yourself (aim for < 5 minutes each)
- Check solutions ONLY after attempting
- Solutions in: `01_SQL/solutions/01_Basics_Solutions.md`

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
"""

SQL_WINDOW_EXERCISES = """# Window Functions - Practice Exercises

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
"""

# =============================================================================
# PYTHON MODULES
# =============================================================================

PYTHON_JSON = """# Python JSON Processing - Complete Guide

## 🎯 Learning Objectives

Master JSON handling in Python:
- Parse JSON files and strings
- Extract nested data
- Transform JSON structures
- Handle errors gracefully
- Work with real-world JSON data

---

## 📚 Core Concepts

### 1. JSON Basics

```python
import json

# JSON is just a string representation of data
json_string = '{"name": "John", "age": 30, "city": "New York"}'

# Parse JSON string to Python dict
data = json.loads(json_string)
print(data['name'])  # Output: John

# Convert Python dict to JSON string
python_dict = {"product": "laptop", "price": 999}
json_output = json.dumps(python_dict)
print(json_output)  # Output: {"product": "laptop", "price": 999}
```

### 2. Reading JSON Files

```python
import json

# Read JSON from file
with open('data.json', 'r') as file:
    data = json.load(file)  # Note: load() not loads()
    print(data)

# Write JSON to file
output_data = {"status": "success", "count": 42}
with open('output.json', 'w') as file:
    json.dump(output_data, file, indent=2)  # indent for pretty printing
```

### 3. Nested JSON Access

```python
data = {
    "users": [
        {
            "id": 1,
            "name": "Alice",
            "contact": {
                "email": "alice@example.com",
                "phone": "123-456-7890"
            }
        },
        {
            "id": 2,
            "name": "Bob",
            "contact": {
                "email": "bob@example.com",
                "phone": "098-765-4321"
            }
        }
    ]
}

# Access nested data
first_user = data['users'][0]
email = data['users'][0]['contact']['email']
print(email)  # Output: alice@example.com

# Loop through array
for user in data['users']:
    print(user['name'], user['contact']['email'])
```

---

## 🔥 EPAM Interview Problem - Email Domain Extraction ⭐

**Given this JSON**:
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

**Write Python code to extract unique domains**:
```
Expected output: {"example.com", "exxxample.com", "dummydata.com"}
```

**Solution**:
```python
import json

def extract_domains(json_file):
    # Read JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Extract domains
    domains = set()
    for user in data['data']:
        email = user['email']
        domain = email.split('@')[1]  # Get part after @
        domains.add(domain)
    
    return domains

# Usage
result = extract_domains('users.json')
print(result)
# Output: {'example.com', 'exxxample.com', 'dummydata.com'}
```

**Alternative using list comprehension**:
```python
import json

def extract_domains_short(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    domains = {user['email'].split('@')[1] for user in data['data']}
    return domains
```

---

## 💡 Common Patterns

### Pattern 1: Filter JSON Data
```python
# Get all users from a specific domain
def filter_by_domain(data, target_domain):
    return [
        user for user in data['data'] 
        if user['email'].endswith(f'@{target_domain}')
    ]

users_from_example = filter_by_domain(data, 'example.com')
```

### Pattern 2: Transform JSON Structure
```python
# Convert list of users to dict keyed by ID
def users_list_to_dict(data):
    return {user['id']: user for user in data['data']}

users_dict = users_list_to_dict(data)
print(users_dict[1])  # Access by ID
```

### Pattern 3: Extract Specific Fields
```python
# Get just names and emails
def extract_contacts(data):
    return [
        {'name': user['name'], 'email': user['email']}
        for user in data['data']
    ]
```

### Pattern 4: Count by Category
```python
from collections import Counter

# Count users per domain
def count_by_domain(data):
    domains = [user['email'].split('@')[1] for user in data['data']]
    return Counter(domains)

domain_counts = count_by_domain(data)
print(domain_counts)
# Output: Counter({'example.com': 2, 'exxxample.com': 1, 'dummydata.com': 1})
```

---

## ⚠️ Error Handling

```python
import json

def safe_json_load(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Safe access to nested data
def safe_get(dictionary, *keys, default=None):
    for key in keys:
        try:
            dictionary = dictionary[key]
        except (KeyError, TypeError, IndexError):
            return default
    return dictionary

# Usage
email = safe_get(data, 'users', 0, 'contact', 'email', default='N/A')
```

---

## 🎯 JSON Handling Checklist

- [ ] Can parse JSON strings and files
- [ ] Can navigate nested JSON structures
- [ ] Can extract data using loops
- [ ] Can extract data using comprehensions
- [ ] Can use `get()` for safe access
- [ ] Can handle errors gracefully
- [ ] Can transform JSON structures
- [ ] Can convert between JSON and Python objects

---

## 🚀 Practice Exercises

See: `02_Python/exercises/02_JSON_Exercises.md`

Master these:
1. Extract email domains (EPAM style)
2. Filter nested JSON
3. Transform data structures
4. Aggregate JSON data
5. Handle malformed JSON

---

## 📚 Quick Reference

```python
# Reading
json.loads(string)  # Parse JSON string
json.load(file)     # Read from file

# Writing
json.dumps(obj)     # Convert to JSON string
json.dump(obj, file) # Write to file

# Pretty printing
json.dumps(obj, indent=2, sort_keys=True)

# Safe access
dict.get('key', default_value)
```

**Next Module**: File Operations
"""

PYTHON_STRING = """# Python String Manipulation - Complete Guide

## 🎯 Learning Objectives

Master string operations for interviews:
- String methods and manipulation
- Case conversion and formatting
- Splitting and joining
- Pattern matching and searching
- Word counting (EPAM favorite!)

---

## 📚 Core String Methods

### 1. Case Conversion
```python
text = "Hello World"

print(text.upper())       # "HELLO WORLD"
print(text.lower())       # "hello world"
print(text.capitalize())  # "Hello world"
print(text.title())       # "Hello World"
print(text.swapcase())    # "hELLO wORLD"
```

### 2. String Checking
```python
text = "hello123"

print(text.isalpha())     # False (has numbers)
print(text.isdigit())     # False (has letters)
print(text.isalnum())     # True (letters + numbers only)
print(text.isspace())     # False
print("   ".isspace())    # True
print(text.startswith('h'))  # True
print(text.endswith('3'))    # True
```

### 3. Splitting and Joining
```python
# Split by delimiter
text = "apple,banana,cherry"
fruits = text.split(',')
print(fruits)  # ['apple', 'banana', 'cherry']

# Split by whitespace (default)
sentence = "Hello world from Python"
words = sentence.split()
print(words)  # ['Hello', 'world', 'from', 'Python']

# Join list into string
words = ['Hello', 'World']
result = ' '.join(words)
print(result)  # "Hello World"

# Join with different delimiter
numbers = ['1', '2', '3']
csv = ','.join(numbers)
print(csv)  # "1,2,3"
```

### 4. Trimming Whitespace
```python
text = "  hello  world  "

print(text.strip())   # "hello  world" (both ends)
print(text.lstrip())  # "hello  world  " (left only)
print(text.rstrip())  # "  hello  world" (right only)

# Strip specific characters
text = "***hello***"
print(text.strip('*'))  # "hello"
```

### 5. Replacing
```python
text = "Hello World World"

print(text.replace('World', 'Python'))  # "Hello Python Python"
print(text.replace('World', 'Python', 1))  # "Hello Python World" (max 1 replacement)
```

### 6. Finding and Searching
```python
text = "Hello World"

print(text.find('World'))    # 6 (index of start)
print(text.find('Python'))   # -1 (not found)
print(text.index('World'))   # 6 (same as find)
# print(text.index('Python'))  # ValueError if not found

print('World' in text)       # True
print('Python' in text)      # False

print(text.count('o'))       # 2
```

---

## 🔥 EPAM Interview Problem - Word Counting ⭐

**Problem**: Count words separated by spaces (case-insensitive)

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

**Solution 1: Using Dictionary**
```python
def count_words(text):
    # Convert to lowercase and split
    words = text.lower().split()
    
    # Count words
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    
    # Print results
    for word, count in word_count.items():
        print(f"{word} {count}")

# Usage
input_text = "apple aPPle banana baNAna TEST s Apple S Test s Te te est"
count_words(input_text)
```

**Solution 2: Using Counter (Better!)**
```python
from collections import Counter

def count_words_v2(text):
    # Convert to lowercase and split
    words = text.lower().split()
    
    # Count words
    word_count = Counter(words)
    
    # Print results
    for word, count in word_count.items():
        print(f"{word} {count}")

# Usage
input_text = "apple aPPle banana baNAna TEST s Apple S Test s Te te est"
count_words_v2(input_text)
```

**Solution 3: One-liner with Counter**
```python
from collections import Counter

text = "apple aPPle banana baNAna TEST s Apple S Test s Te te est"
word_count = Counter(text.lower().split())

for word, count in word_count.items():
    print(f"{word} {count}")
```

---

## 💡 Common Patterns

### Pattern 1: Remove Punctuation
```python
import string

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

text = "Hello, World! How are you?"
clean = remove_punctuation(text)
print(clean)  # "Hello World How are you"
```

### Pattern 2: Extract Numbers from String
```python
def extract_numbers(text):
    return [int(s) for s in text.split() if s.isdigit()]

text = "Order 123 shipped 456 items"
numbers = extract_numbers(text)
print(numbers)  # [123, 456]
```

### Pattern 3: Title Case Formatting
```python
def format_name(name):
    return name.strip().title()

print(format_name("  john DOE  "))  # "John Doe"
```

### Pattern 4: Check if Palindrome
```python
def is_palindrome(text):
    # Remove spaces and convert to lowercase
    clean = text.replace(' ', '').lower()
    return clean == clean[::-1]

print(is_palindrome("A man a plan a canal Panama"))  # True
```

### Pattern 5: Word Frequency (Sorted)
```python
from collections import Counter

def word_frequency(text):
    words = text.lower().split()
    freq = Counter(words)
    
    # Sort by frequency (descending)
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)

text = "apple banana apple cherry banana apple"
freq = word_frequency(text)
for word, count in freq:
    print(f"{word}: {count}")

# Output:
# apple: 3
# banana: 2
# cherry: 1
```

---

## 🎯 String Slicing

```python
text = "Python"

print(text[0])      # 'P' (first character)
print(text[-1])     # 'n' (last character)
print(text[0:3])    # 'Pyt' (index 0 to 2)
print(text[2:])     # 'thon' (index 2 to end)
print(text[:4])     # 'Pyth' (start to index 3)
print(text[::2])    # 'Pto' (every 2nd character)
print(text[::-1])   # 'nohtyP' (reverse)
```

---

## 🎯 F-Strings (Python 3.6+)

```python
name = "Alice"
age = 30
salary = 75000.50

# Basic f-string
print(f"Name: {name}, Age: {age}")

# Expressions in f-strings
print(f"Next year: {age + 1}")

# Formatting numbers
print(f"Salary: ${salary:,.2f}")  # $75,000.50

# Padding and alignment
print(f"{name:>10}")   # Right align (width 10)
print(f"{name:<10}")   # Left align
print(f"{name:^10}")   # Center align
```

---

## ⚠️ Common Mistakes

1. **Strings are immutable**
   ```python
   text = "Hello"
   # text[0] = 'h'  # ERROR! Can't modify
   text = text.lower()  # Create new string
   ```

2. **Split vs Split with argument**
   ```python
   text = "a  b    c"  # Multiple spaces
   print(text.split(' '))   # ['a', '', 'b', '', '', '', 'c']
   print(text.split())      # ['a', 'b', 'c'] # Better!
   ```

3. **Strip only removes from ends**
   ```python
   text = "  hello  world  "
   print(text.strip())  # "hello  world" (not "helloworld")
   print(text.replace(' ', ''))  # "helloworld" (remove all)
   ```

---

## 🚀 Practice Exercises

See: `02_Python/exercises/01_String_Exercises.md`

Master these:
1. Word counting (EPAM style)
2. Case conversion challenges
3. String parsing
4. Pattern extraction
5. Text formatting

---

## 📚 Quick Reference

```python
# Case
.upper(), .lower(), .title(), .capitalize()

# Checking
.isalpha(), .isdigit(), .isalnum(), .isspace()
.startswith(), .endswith()

# Manipulation
.split(), .join(), .replace()
.strip(), .lstrip(), .rstrip()

# Searching
.find(), .index(), .count()
'substring' in string

# Slicing
string[start:end:step]
string[::-1]  # reverse
```

**Next Module**: JSON Processing
"""

# Continue in next part...

def generate_all_content():
    """Generate all training content"""
    
    print("Generating SQL exercises...")
    write_file('01_SQL/exercises/01_Basics_Exercises.md', SQL_BASICS_EXERCISES)
    write_file('01_SQL/exercises/02_Window_Functions_Exercises.md', SQL_WINDOW_EXERCISES)
    
    print("\nGenerating Python modules...")
    write_file('02_Python/01_String_Manipulation.md', PYTHON_STRING)
    write_file('02_Python/02_JSON_Processing.md', PYTHON_JSON)
    
    print("\n✅ Content generation complete!")

if __name__ == "__main__":
    print("="*70)
    print("Generating Complete Training System")
    print("="*70)
    print()
    
    generate_all_content()


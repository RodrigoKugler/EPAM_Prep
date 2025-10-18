# Python JSON Processing - Complete Guide

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

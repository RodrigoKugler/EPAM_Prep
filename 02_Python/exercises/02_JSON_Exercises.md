# Python Exercises - JSON Processing

## 📝 Instructions
- Solve WITHOUT looking at solutions first
- Create test JSON files as needed
- Solutions in: `02_Python/solutions/02_JSON_Solutions.md`

---

## Exercise 1: Email Domains - EPAM STYLE ⭐⭐⭐

Create a file `users.json`:
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

Write code to extract unique domains.

**Expected Output**: `{'example.com', 'exxxample.com', 'dummydata.com'}`

---

## Exercise 2: Filter by Domain
Using the same JSON, write code to get all users from "example.com".

---

## Exercise 3: Count by Domain
Using the same JSON, count users per domain.

**Expected Output**: `{'example.com': 2, 'exxxample.com': 1, 'dummydata.com': 1}`

---

## Exercise 4: Transform Structure
Transform the user list to a dictionary keyed by ID.

**Expected Output**:
```python
{
    1: {"name": "John Doe", "email": "john.doe@example.com"},
    2: {"name": "Jane Smith", "email": "jane.smith@exxxample.com"},
    ...
}
```

---

## Exercise 5: Nested JSON Extraction
Create `employees.json`:
```json
{
  "company": "TechCorp",
  "employees": [
    {
      "name": "Alice",
      "department": "Engineering",
      "contact": {"email": "alice@tech.com", "phone": "123-456"}
    },
    {
      "name": "Bob",
      "department": "Sales",
      "contact": {"email": "bob@tech.com", "phone": "789-012"}
    }
  ]
}
```

Extract all phone numbers.

**Expected Output**: `['123-456', '789-012']`

---

## Exercise 6: JSON to CSV
Convert JSON data to CSV format (as string or file).

---

## Exercise 7: Merge JSON Files
Write code to merge two JSON files with user data.

---

## Exercise 8: Validate JSON Structure
Write code to validate if a JSON file has required keys.

**Required keys**: `['id', 'name', 'email']`

---

## Exercise 9: Deep Copy and Modify
Read JSON, create a deep copy, and modify without affecting original.

---

## Exercise 10: Handle Missing Keys
Write code to safely extract nested data even if keys are missing.

---

**Time yourself: Aim for < 12 minutes per exercise!**

# Python String Manipulation - Complete Guide

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

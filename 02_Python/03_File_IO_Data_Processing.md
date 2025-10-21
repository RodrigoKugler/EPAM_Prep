# Python File I/O & Data Processing - Data Engineering Essentials

## 🎯 Learning Objectives

By the end of this module, you will be able to:
- **Master file operations** (read, write, append)
- **Process CSV files** with pandas and csv module
- **Handle Excel files** for data exchange
- **Work with large files** efficiently
- **Process multiple file formats** (CSV, Excel, TXT, JSON, Parquet)
- **Implement error handling** for file operations
- **Build robust data pipelines** with file processing

---

## 🔥 Why File I/O Matters for Data Engineering

File I/O is **fundamental to data engineering**:

1. **Data Ingestion**: Reading data from various sources
2. **ETL Pipelines**: Extract, Transform, Load workflows
3. **Data Exchange**: Sharing data between systems
4. **Data Storage**: Persisting processed data
5. **Batch Processing**: Processing large data files
6. **Data Archiving**: Long-term data storage

**EPAM will test your ability to process files efficiently. Master this = you're ready for real data engineering work.**

---

## 📚 File Operations - Foundation

### 1. Basic File Reading

```python
# Read entire file
with open('data.txt', 'r') as file:
    content = file.read()
    print(content)

# Read file line by line
with open('data.txt', 'r') as file:
    for line in file:
        print(line.strip())

# Read all lines into list
with open('data.txt', 'r') as file:
    lines = file.readlines()
    print(lines)
```

**Key Points**:
- Use `with` statement for automatic file closing
- `'r'` mode for reading (default)
- Always strip whitespace from lines
- `readlines()` loads entire file into memory

---

### 2. Basic File Writing

```python
# Write to file (overwrites existing)
with open('output.txt', 'w') as file:
    file.write('Hello, World!\n')
    file.write('Second line\n')

# Append to file
with open('output.txt', 'a') as file:
    file.write('Appended line\n')

# Write list of lines
lines = ['Line 1\n', 'Line 2\n', 'Line 3\n']
with open('output.txt', 'w') as file:
    file.writelines(lines)
```

**Key Points**:
- `'w'` mode overwrites existing file
- `'a'` mode appends to existing file
- Add `\n` manually for line breaks
- `writelines()` doesn't add line breaks automatically

---

### 3. File Modes Reference

| Mode | Description | Creates if Missing | Overwrites |
|------|-------------|-------------------|------------|
| `'r'` | Read only | No | N/A |
| `'w'` | Write only | Yes | Yes |
| `'a'` | Append only | Yes | No |
| `'r+'` | Read and write | No | No |
| `'w+'` | Read and write | Yes | Yes |
| `'rb'` | Read binary | No | N/A |
| `'wb'` | Write binary | Yes | Yes |

---

## 🔥 CSV Processing - Data Engineering Core

### 1. CSV with csv Module

```python
import csv

# Read CSV file
with open('customers.csv', 'r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # Get header row
    print(f"Header: {header}")
    
    for row in csv_reader:
        print(f"Customer: {row[0]}, Email: {row[1]}")

# Read CSV with DictReader (better for named columns)
with open('customers.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        print(f"Customer: {row['name']}, Email: {row['email']}")
```

**Write CSV**:
```python
import csv

# Write CSV file
data = [
    ['name', 'email', 'age'],
    ['Alice', 'alice@email.com', 30],
    ['Bob', 'bob@email.com', 25],
    ['Carol', 'carol@email.com', 35]
]

with open('output.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)

# Write CSV with DictWriter
data = [
    {'name': 'Alice', 'email': 'alice@email.com', 'age': 30},
    {'name': 'Bob', 'email': 'bob@email.com', 'age': 25},
    {'name': 'Carol', 'email': 'carol@email.com', 'age': 35}
]

with open('output.csv', 'w', newline='') as file:
    fieldnames = ['name', 'email', 'age']
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    csv_writer.writeheader()
    csv_writer.writerows(data)
```

---

### 2. CSV with Pandas (Recommended for Data Engineering)

```python
import pandas as pd

# Read CSV file
df = pd.read_csv('customers.csv')
print(df.head())

# Read CSV with specific options
df = pd.read_csv(
    'customers.csv',
    encoding='utf-8',
    sep=',',
    header=0,
    na_values=['NA', 'null', ''],
    parse_dates=['registration_date'],
    dtype={'customer_id': int, 'age': float}
)

# Write CSV file
df.to_csv('output.csv', index=False)

# Write CSV with specific options
df.to_csv(
    'output.csv',
    index=False,
    encoding='utf-8',
    sep=',',
    na_rep='NULL',
    date_format='%Y-%m-%d'
)
```

**Real-World Example**: ETL CSV Processing
```python
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_customer_csv(input_file, output_file):
    """ETL pipeline for customer CSV data"""
    try:
        # Extract
        logger.info(f"Reading CSV file: {input_file}")
        df = pd.read_csv(input_file)
        logger.info(f"Loaded {len(df)} records")
        
        # Transform
        # 1. Clean email addresses
        df['email'] = df['email'].str.lower().str.strip()
        
        # 2. Clean phone numbers
        df['phone'] = df['phone'].str.replace(r'[^\d]', '', regex=True)
        
        # 3. Validate data
        df = df[df['email'].str.contains('@', na=False)]
        df = df[df['phone'].str.len() == 10]
        
        # 4. Handle missing values
        df['middle_name'] = df['middle_name'].fillna('')
        df = df.dropna(subset=['customer_id', 'email'])
        
        # 5. Create derived columns
        df['full_name'] = df['first_name'] + ' ' + df['last_name']
        df['registration_year'] = pd.to_datetime(df['registration_date']).dt.year
        
        # 6. Remove duplicates
        df = df.drop_duplicates(subset=['customer_id'], keep='first')
        
        # Load
        logger.info(f"Writing processed data: {output_file}")
        df.to_csv(output_file, index=False)
        logger.info(f"Processed {len(df)} valid records")
        
        return {
            'total_records': len(df),
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict()
        }
        
    except FileNotFoundError:
        logger.error(f"File not found: {input_file}")
        raise
    except pd.errors.EmptyDataError:
        logger.error(f"Empty CSV file: {input_file}")
        raise
    except Exception as e:
        logger.error(f"Error processing CSV: {e}")
        raise

# Usage
result = process_customer_csv('raw_customers.csv', 'clean_customers.csv')
print(f"Processed {result['total_records']} records")
```

---

## 📊 Excel File Processing

### 1. Reading Excel Files

```python
import pandas as pd

# Read Excel file
df = pd.read_excel('customers.xlsx')
print(df.head())

# Read specific sheet
df = pd.read_excel('customers.xlsx', sheet_name='Sheet1')

# Read multiple sheets
excel_file = pd.ExcelFile('customers.xlsx')
for sheet_name in excel_file.sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    print(f"Sheet: {sheet_name}, Rows: {len(df)}")

# Read Excel with specific options
df = pd.read_excel(
    'customers.xlsx',
    sheet_name='Sheet1',
    header=0,
    usecols=['customer_id', 'name', 'email'],
    dtype={'customer_id': int},
    na_values=['NA', 'N/A', '']
)
```

---

### 2. Writing Excel Files

```python
import pandas as pd

# Write single sheet
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol'],
    'email': ['alice@email.com', 'bob@email.com', 'carol@email.com'],
    'age': [30, 25, 35]
})

df.to_excel('output.xlsx', index=False, sheet_name='Customers')

# Write multiple sheets
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    df_customers.to_excel(writer, sheet_name='Customers', index=False)
    df_orders.to_excel(writer, sheet_name='Orders', index=False)
    df_products.to_excel(writer, sheet_name='Products', index=False)
```

**Real-World Example**: Excel Report Generation
```python
import pandas as pd
from datetime import datetime

def generate_sales_report(orders_df, customers_df, output_file):
    """Generate Excel sales report with multiple sheets"""
    
    # Merge orders with customer data
    report_df = orders_df.merge(
        customers_df,
        on='customer_id',
        how='left'
    )
    
    # Create summary statistics
    summary = {
        'Total Orders': len(report_df),
        'Total Revenue': report_df['order_amount'].sum(),
        'Average Order Value': report_df['order_amount'].mean(),
        'Unique Customers': report_df['customer_id'].nunique()
    }
    
    summary_df = pd.DataFrame([summary])
    
    # Create sales by month
    report_df['order_month'] = pd.to_datetime(report_df['order_date']).dt.to_period('M')
    monthly_sales = report_df.groupby('order_month').agg({
        'order_id': 'count',
        'order_amount': 'sum'
    }).reset_index()
    monthly_sales.columns = ['Month', 'Order Count', 'Total Revenue']
    
    # Write to Excel with multiple sheets
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        monthly_sales.to_excel(writer, sheet_name='Monthly Sales', index=False)
        report_df.to_excel(writer, sheet_name='Detailed Data', index=False)
    
    print(f"Report generated: {output_file}")

# Usage
orders = pd.read_csv('orders.csv')
customers = pd.read_csv('customers.csv')
generate_sales_report(orders, customers, 'sales_report.xlsx')
```

---

## 🚀 Large File Processing

### 1. Processing Files in Chunks

```python
import pandas as pd

def process_large_csv(file_path, chunk_size=10000):
    """Process large CSV file in chunks"""
    total_rows = 0
    valid_rows = 0
    
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        total_rows += len(chunk)
        
        # Process chunk
        chunk_clean = chunk[chunk['email'].str.contains('@', na=False)]
        valid_rows += len(chunk_clean)
        
        # Write processed chunk to output
        mode = 'w' if total_rows == len(chunk) else 'a'
        header = (total_rows == len(chunk))
        chunk_clean.to_csv('output.csv', mode=mode, header=header, index=False)
    
    print(f"Processed {total_rows} rows, {valid_rows} valid rows")
    return total_rows, valid_rows

# Usage
process_large_csv('large_file.csv', chunk_size=50000)
```

---

### 2. Line-by-Line Processing

```python
def process_large_file_line_by_line(input_file, output_file):
    """Process large file line by line (memory efficient)"""
    total_lines = 0
    valid_lines = 0
    
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Process header
        header = infile.readline()
        outfile.write(header)
        
        for line in infile:
            total_lines += 1
            
            # Process line
            if validate_line(line):
                processed_line = transform_line(line)
                outfile.write(processed_line)
                valid_lines += 1
            
            # Progress indicator
            if total_lines % 100000 == 0:
                print(f"Processed {total_lines} lines...")
    
    print(f"Total: {total_lines}, Valid: {valid_lines}")
    return total_lines, valid_lines

def validate_line(line):
    """Validate line data"""
    parts = line.strip().split(',')
    return len(parts) >= 3 and '@' in parts[2]

def transform_line(line):
    """Transform line data"""
    parts = line.strip().split(',')
    parts[1] = parts[1].lower()  # Lowercase name
    parts[2] = parts[2].lower()  # Lowercase email
    return ','.join(parts) + '\n'

# Usage
process_large_file_line_by_line('large_input.csv', 'large_output.csv')
```

---

## 🎯 Multiple File Formats

### 1. Parquet Files (Efficient for Big Data)

```python
import pandas as pd

# Write Parquet
df = pd.read_csv('customers.csv')
df.to_parquet('customers.parquet', compression='snappy')

# Read Parquet
df = pd.read_parquet('customers.parquet')
print(df.head())

# Parquet is much faster and smaller than CSV
# Great for data lakes and big data processing
```

---

### 2. JSON Lines (JSONL) for Streaming

```python
import json
import pandas as pd

# Write JSON Lines
data = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@email.com'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@email.com'},
    {'id': 3, 'name': 'Carol', 'email': 'carol@email.com'}
]

with open('data.jsonl', 'w') as file:
    for item in data:
        file.write(json.dumps(item) + '\n')

# Read JSON Lines
data = []
with open('data.jsonl', 'r') as file:
    for line in file:
        data.append(json.loads(line))

# Or use pandas
df = pd.read_json('data.jsonl', lines=True)
```

---

### 3. Pickle (Python Objects)

```python
import pickle
import pandas as pd

# Save Python object
df = pd.read_csv('customers.csv')
with open('data.pkl', 'wb') as file:
    pickle.dump(df, file)

# Load Python object
with open('data.pkl', 'rb') as file:
    df = pickle.load(file)
```

---

## 🔧 Error Handling & Best Practices

### 1. Robust File Processing

```python
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_file_safely(input_file, output_file):
    """Process file with robust error handling"""
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Check if input file is readable
        if not os.access(input_file, os.R_OK):
            raise PermissionError(f"No read permission: {input_file}")
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Process file
        logger.info(f"Processing file: {input_file}")
        df = pd.read_csv(input_file)
        
        # Validate data
        if df.empty:
            raise ValueError(f"Empty dataframe from: {input_file}")
        
        # Process data
        df_processed = process_dataframe(df)
        
        # Write output
        df_processed.to_csv(output_file, index=False)
        logger.info(f"Successfully processed {len(df_processed)} records")
        
        return {
            'success': True,
            'records_processed': len(df_processed),
            'output_file': output_file
        }
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return {'success': False, 'error': str(e)}
    except PermissionError as e:
        logger.error(f"Permission error: {e}")
        return {'success': False, 'error': str(e)}
    except pd.errors.EmptyDataError:
        logger.error(f"Empty data file: {input_file}")
        return {'success': False, 'error': 'Empty data file'}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {'success': False, 'error': str(e)}

def process_dataframe(df):
    """Process dataframe with data quality checks"""
    # Your processing logic here
    return df
```

---

### 2. File Path Handling

```python
from pathlib import Path
import os

# Use Path for cross-platform compatibility
data_dir = Path('data')
input_file = data_dir / 'customers.csv'
output_file = data_dir / 'processed' / 'customers_clean.csv'

# Create directories
output_file.parent.mkdir(parents=True, exist_ok=True)

# Check file existence
if input_file.exists():
    print(f"File exists: {input_file}")

# Get file information
file_size = input_file.stat().st_size
print(f"File size: {file_size} bytes")

# List files in directory
for file in data_dir.glob('*.csv'):
    print(f"Found CSV: {file}")
```

---

## 🎯 EPAM Interview Scenarios

### Scenario 1: CSV Data Cleansing
**Problem**: Clean and validate customer data from CSV file.

```python
import pandas as pd
import re

def clean_customer_data(input_file, output_file):
    """Clean customer CSV data for EPAM interview"""
    # Read CSV
    df = pd.read_csv(input_file)
    
    # Clean email addresses
    df['email'] = df['email'].str.lower().str.strip()
    df = df[df['email'].str.contains('@', na=False)]
    
    # Clean phone numbers (remove non-digits)
    df['phone'] = df['phone'].str.replace(r'[^\d]', '', regex=True)
    df = df[df['phone'].str.len() == 10]
    
    # Clean names
    df['name'] = df['name'].str.title().str.strip()
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['email'], keep='first')
    
    # Sort by name
    df = df.sort_values('name')
    
    # Write output
    df.to_csv(output_file, index=False)
    
    return len(df)

# Usage
records = clean_customer_data('customers.csv', 'customers_clean.csv')
print(f"Processed {records} clean records")
```

### Scenario 2: Multi-File Processing
**Problem**: Process multiple CSV files and combine into one.

```python
import pandas as pd
from pathlib import Path

def combine_csv_files(input_dir, output_file):
    """Combine multiple CSV files into one"""
    all_data = []
    
    # Process each CSV file
    for csv_file in Path(input_dir).glob('*.csv'):
        df = pd.read_csv(csv_file)
        df['source_file'] = csv_file.name
        all_data.append(df)
    
    # Combine all dataframes
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Remove duplicates
    combined_df = combined_df.drop_duplicates()
    
    # Write output
    combined_df.to_csv(output_file, index=False)
    
    return len(combined_df)

# Usage
total = combine_csv_files('data/raw/', 'data/combined.csv')
print(f"Combined {total} records")
```

---

## 🚀 Practice Exercises

**See**: `02_Python/exercises/03_File_IO_Exercises.md`

**Master these patterns**:
1. ✅ Basic file reading and writing
2. ✅ CSV processing with pandas
3. ✅ Excel file handling
4. ✅ Large file processing
5. ✅ Error handling
6. ✅ Multi-file processing
7. ✅ Data validation
8. ✅ Real-world ETL scenarios

**Target Time**: Process any file format in < 15 minutes

---

## 📚 Quick Reference Cheat Sheet

### File Operations
```python
# Read
with open('file.txt', 'r') as f:
    content = f.read()

# Write
with open('file.txt', 'w') as f:
    f.write('Hello')

# Append
with open('file.txt', 'a') as f:
    f.write('World')
```

### CSV Operations
```python
# Read CSV
df = pd.read_csv('file.csv')

# Write CSV
df.to_csv('output.csv', index=False)

# Process in chunks
for chunk in pd.read_csv('large.csv', chunksize=10000):
    process(chunk)
```

### Excel Operations
```python
# Read Excel
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')

# Write Excel
df.to_excel('output.xlsx', index=False)

# Multiple sheets
with pd.ExcelWriter('output.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Sheet1')
    df2.to_excel(writer, sheet_name='Sheet2')
```

---

## 🎯 Next Steps

1. **Practice file processing** until you can handle any format in < 15 minutes
2. **Complete all exercises** in `02_Python/exercises/03_File_IO_Exercises.md`
3. **Review solutions** only after attempting
4. **Move to**: Pandas Data Engineering

**You're now ready to master data file processing!** 🚀

---

**Key Takeaway**: File I/O is about **efficiently processing data from various sources**. Master CSV, Excel, and large file handling, and you'll be ready for real data engineering work.

**Next Module**: `02_Python/04_Pandas_Data_Engineering.md`



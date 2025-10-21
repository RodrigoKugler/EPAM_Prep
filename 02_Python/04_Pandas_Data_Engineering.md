# Pandas for Data Engineering - Complete Mastery

## 🎯 Learning Objectives

By the end of this module, you will be able to:
- **Master DataFrame operations** for data manipulation
- **Clean and transform data** like a professional data engineer
- **Perform aggregations** and statistical analysis
- **Merge and join datasets** efficiently
- **Handle time series data** for analytics
- **Optimize pandas** for large datasets
- **Build production-ready** data pipelines with pandas

---

## 🔥 Why Pandas Matters for Data Engineering

Pandas is the **industry standard** for data manipulation:

1. **Data Transformation**: ETL pipeline core
2. **Data Cleaning**: Handle missing values, duplicates, outliers
3. **Data Analysis**: Statistical operations and aggregations
4. **Data Integration**: Merge data from multiple sources
5. **Performance**: Optimized for large datasets
6. **Industry Standard**: Used in 90% of data engineering projects

**EPAM will test your pandas skills. Master this = you're ready for production data engineering work.**

---

## 📚 DataFrame Basics - Foundation

### 1. Creating DataFrames

```python
import pandas as pd
import numpy as np

# From dictionary
data = {
    'name': ['Alice', 'Bob', 'Carol', 'David'],
    'age': [25, 30, 35, 28],
    'city': ['New York', 'London', 'Paris', 'Tokyo'],
    'salary': [70000, 80000, 90000, 75000]
}
df = pd.DataFrame(data)
print(df)

# From list of lists
data = [
    ['Alice', 25, 70000],
    ['Bob', 30, 80000],
    ['Carol', 35, 90000]
]
df = pd.DataFrame(data, columns=['name', 'age', 'salary'])

# From CSV
df = pd.read_csv('employees.csv')

# Create empty DataFrame
df = pd.DataFrame(columns=['name', 'age', 'salary'])
```

---

### 2. DataFrame Information

```python
# Shape and size
print(df.shape)  # (rows, columns)
print(len(df))  # number of rows
print(df.size)  # total elements

# Data types
print(df.dtypes)
print(df.info())

# Summary statistics
print(df.describe())

# First and last rows
print(df.head(10))
print(df.tail(10))

# Column names
print(df.columns.tolist())
```

---

## 🔥 Data Selection - Essential Skills

### 1. Select Columns

```python
# Single column (Series)
names = df['name']

# Multiple columns (DataFrame)
subset = df[['name', 'age', 'salary']]

# Select by position
first_col = df.iloc[:, 0]
first_three_cols = df.iloc[:, :3]
```

---

### 2. Select Rows

```python
# By index position
first_row = df.iloc[0]
first_five = df.iloc[:5]
last_row = df.iloc[-1]

# By index label
row = df.loc[0]
rows = df.loc[0:5]

# By condition (boolean indexing)
high_earners = df[df['salary'] > 75000]
adults = df[df['age'] >= 18]

# Multiple conditions
young_high_earners = df[(df['age'] < 30) & (df['salary'] > 70000)]
ny_or_london = df[(df['city'] == 'New York') | (df['city'] == 'London')]
```

---

### 3. loc vs iloc

```python
# iloc: integer position
df.iloc[0, 0]  # First row, first column
df.iloc[0:5, 0:3]  # First 5 rows, first 3 columns

# loc: label-based
df.loc[0, 'name']  # Row 0, 'name' column
df.loc[0:5, ['name', 'age']]  # Rows 0-5, specific columns

# Boolean indexing with loc
df.loc[df['age'] > 30, ['name', 'salary']]
```

---

## 🚀 Data Cleaning - Production-Ready

### 1. Missing Values

```python
# Check for missing values
print(df.isnull().sum())
print(df.isna().sum())

# Find rows with missing values
incomplete_rows = df[df.isnull().any(axis=1)]

# Drop missing values
df_clean = df.dropna()  # Drop any row with missing values
df_clean = df.dropna(subset=['email'])  # Drop only if email is missing
df_clean = df.dropna(thresh=3)  # Keep rows with at least 3 non-null values

# Fill missing values
df['age'] = df['age'].fillna(0)  # Fill with 0
df['name'] = df['name'].fillna('Unknown')  # Fill with string
df['salary'] = df['salary'].fillna(df['salary'].mean())  # Fill with mean
df['city'] = df['city'].fillna(method='ffill')  # Forward fill
df['city'] = df['city'].fillna(method='bfill')  # Backward fill
```

**Real-World Example**: ETL Data Cleaning
```python
def clean_customer_data(df):
    """Production-ready data cleaning"""
    # 1. Remove duplicates
    df = df.drop_duplicates(subset=['customer_id'], keep='first')
    
    # 2. Handle missing values strategically
    df['middle_name'] = df['middle_name'].fillna('')
    df['phone'] = df['phone'].fillna('Unknown')
    df = df.dropna(subset=['customer_id', 'email'])  # Critical fields
    
    # 3. Clean email addresses
    df['email'] = df['email'].str.lower().str.strip()
    
    # 4. Clean phone numbers
    df['phone'] = df['phone'].str.replace(r'[^\d]', '', regex=True)
    
    # 5. Standardize dates
    df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
    
    # 6. Remove invalid data
    df = df[df['email'].str.contains('@', na=False)]
    df = df[df['age'] > 0]
    df = df[df['salary'] >= 0]
    
    return df
```

---

### 2. Duplicates

```python
# Find duplicates
duplicates = df[df.duplicated()]
duplicate_emails = df[df.duplicated(subset=['email'], keep=False)]

# Remove duplicates
df_clean = df.drop_duplicates()
df_clean = df.drop_duplicates(subset=['email'], keep='first')
df_clean = df.drop_duplicates(subset=['email'], keep='last')
```

---

### 3. Data Types

```python
# Convert data types
df['age'] = df['age'].astype(int)
df['salary'] = df['salary'].astype(float)
df['is_active'] = df['is_active'].astype(bool)

# Convert to datetime
df['registration_date'] = pd.to_datetime(df['registration_date'])
df['order_date'] = pd.to_datetime(df['order_date'], format='%Y-%m-%d')

# Handle errors in conversion
df['age'] = pd.to_numeric(df['age'], errors='coerce')  # Invalid -> NaN
```

---

## 🎯 Data Transformation - ETL Core

### 1. Add and Modify Columns

```python
# Add new column
df['full_name'] = df['first_name'] + ' ' + df['last_name']
df['salary_monthly'] = df['salary'] / 12

# Modify existing column
df['email'] = df['email'].str.lower()
df['age'] = df['age'] + 1

# Conditional column
df['age_group'] = df['age'].apply(lambda x: 'Adult' if x >= 18 else 'Minor')
df['salary_category'] = pd.cut(
    df['salary'],
    bins=[0, 50000, 75000, 100000, float('inf')],
    labels=['Low', 'Medium', 'High', 'Very High']
)
```

---

### 2. Apply Functions

```python
# Apply function to column
def categorize_salary(salary):
    if salary > 80000:
        return 'High'
    elif salary > 60000:
        return 'Medium'
    else:
        return 'Low'

df['salary_level'] = df['salary'].apply(categorize_salary)

# Apply to multiple columns
def calculate_bonus(row):
    return row['salary'] * 0.1 if row['age'] > 30 else row['salary'] * 0.05

df['bonus'] = df.apply(calculate_bonus, axis=1)

# Apply with lambda
df['email_domain'] = df['email'].apply(lambda x: x.split('@')[1] if '@' in str(x) else '')

# Map values
gender_map = {'M': 'Male', 'F': 'Female'}
df['gender_full'] = df['gender'].map(gender_map)
```

---

### 3. String Operations

```python
# String methods
df['name'] = df['name'].str.upper()
df['name'] = df['name'].str.lower()
df['name'] = df['name'].str.title()
df['name'] = df['name'].str.strip()

# String contains
df_gmail = df[df['email'].str.contains('@gmail.com')]
df_valid_phone = df[df['phone'].str.match(r'^\d{10}$')]

# String replace
df['phone'] = df['phone'].str.replace(r'[^\d]', '', regex=True)
df['name'] = df['name'].str.replace('Mr. ', '')

# String split
df[['first_name', 'last_name']] = df['full_name'].str.split(' ', expand=True)
```

---

## 📊 Data Aggregation - Analytics Power

### 1. GroupBy Operations

```python
# Basic groupby
by_city = df.groupby('city').size()
avg_salary_by_city = df.groupby('city')['salary'].mean()

# Multiple aggregations
summary = df.groupby('city').agg({
    'salary': ['mean', 'median', 'min', 'max'],
    'age': ['mean', 'count'],
    'customer_id': 'nunique'
})

# Multiple group columns
summary = df.groupby(['city', 'department']).agg({
    'salary': 'mean',
    'employee_id': 'count'
})

# Custom aggregation
def salary_range(x):
    return x.max() - x.min()

df.groupby('department')['salary'].agg(['mean', 'std', salary_range])
```

**Real-World Example**: Sales Analytics
```python
def analyze_sales(orders_df):
    """Comprehensive sales analysis"""
    # Monthly sales summary
    orders_df['order_month'] = pd.to_datetime(orders_df['order_date']).dt.to_period('M')
    
    monthly_summary = orders_df.groupby('order_month').agg({
        'order_id': 'count',
        'order_amount': ['sum', 'mean', 'median'],
        'customer_id': 'nunique'
    })
    monthly_summary.columns = ['order_count', 'total_revenue', 'avg_order', 'median_order', 'unique_customers']
    
    # Customer segment analysis
    customer_summary = orders_df.groupby('customer_id').agg({
        'order_id': 'count',
        'order_amount': 'sum'
    }).reset_index()
    customer_summary.columns = ['customer_id', 'order_count', 'total_spent']
    
    # Segment customers
    customer_summary['segment'] = pd.cut(
        customer_summary['total_spent'],
        bins=[0, 500, 2000, float('inf')],
        labels=['Basic', 'Standard', 'Premium']
    )
    
    segment_summary = customer_summary.groupby('segment').agg({
        'customer_id': 'count',
        'total_spent': ['sum', 'mean']
    })
    
    return monthly_summary, customer_summary, segment_summary
```

---

### 2. Pivot Tables

```python
# Basic pivot
pivot = df.pivot_table(
    values='salary',
    index='department',
    columns='city',
    aggfunc='mean'
)

# Multiple aggregations
pivot = df.pivot_table(
    values='salary',
    index='department',
    columns='city',
    aggfunc=['mean', 'count', 'sum']
)

# Multiple values
pivot = df.pivot_table(
    values=['salary', 'age'],
    index='department',
    columns='city',
    aggfunc='mean'
)
```

---

## 🔗 Merging and Joining - Data Integration

### 1. Merge DataFrames

```python
# Inner join (default)
merged = pd.merge(df1, df2, on='customer_id')

# Left join
merged = pd.merge(df1, df2, on='customer_id', how='left')

# Right join
merged = pd.merge(df1, df2, on='customer_id', how='right')

# Outer join
merged = pd.merge(df1, df2, on='customer_id', how='outer')

# Merge on different column names
merged = pd.merge(df1, df2, left_on='cust_id', right_on='customer_id')

# Merge on multiple columns
merged = pd.merge(df1, df2, on=['customer_id', 'order_date'])
```

**Real-World Example**: Data Warehouse Integration
```python
def integrate_customer_data(customers_df, orders_df, products_df):
    """Integrate data from multiple sources"""
    # 1. Enrich orders with customer info
    orders_enriched = pd.merge(
        orders_df,
        customers_df[['customer_id', 'customer_name', 'customer_segment']],
        on='customer_id',
        how='left'
    )
    
    # 2. Add product information
    orders_full = pd.merge(
        orders_enriched,
        products_df[['product_id', 'product_name', 'product_category']],
        on='product_id',
        how='left'
    )
    
    # 3. Calculate metrics
    orders_full['revenue'] = orders_full['quantity'] * orders_full['unit_price']
    orders_full['order_year'] = pd.to_datetime(orders_full['order_date']).dt.year
    
    # 4. Handle missing data
    orders_full['customer_name'] = orders_full['customer_name'].fillna('Unknown')
    orders_full['product_name'] = orders_full['product_name'].fillna('Unknown')
    
    return orders_full
```

---

### 2. Concatenate DataFrames

```python
# Vertical concatenation (stack rows)
combined = pd.concat([df1, df2, df3], ignore_index=True)

# Horizontal concatenation (side by side)
combined = pd.concat([df1, df2], axis=1)

# Concatenate with keys
combined = pd.concat([df1, df2], keys=['Source1', 'Source2'])
```

---

## ⏰ Time Series Operations

### 1. Date Operations

```python
# Convert to datetime
df['order_date'] = pd.to_datetime(df['order_date'])

# Extract date components
df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month
df['day'] = df['order_date'].dt.day
df['day_of_week'] = df['order_date'].dt.dayofweek
df['day_name'] = df['order_date'].dt.day_name()
df['quarter'] = df['order_date'].dt.quarter

# Date arithmetic
df['days_since_order'] = (pd.Timestamp.now() - df['order_date']).dt.days
df['next_week'] = df['order_date'] + pd.Timedelta(days=7)

# Date filtering
recent_orders = df[df['order_date'] >= '2024-01-01']
last_30_days = df[df['order_date'] >= pd.Timestamp.now() - pd.Timedelta(days=30)]
```

---

### 2. Time-based Aggregation

```python
# Group by date
daily_sales = df.groupby(df['order_date'].dt.date)['order_amount'].sum()

# Resample time series
df.set_index('order_date', inplace=True)
monthly_sales = df['order_amount'].resample('M').sum()
weekly_avg = df['order_amount'].resample('W').mean()

# Rolling windows
df['moving_avg_7day'] = df['order_amount'].rolling(window=7).mean()
df['rolling_sum_30day'] = df['order_amount'].rolling(window=30).sum()
```

---

## 🚀 Performance Optimization

### 1. Vectorized Operations

```python
# ❌ SLOW: Iterating rows
for idx, row in df.iterrows():
    df.at[idx, 'total'] = row['quantity'] * row['price']

# ✅ FAST: Vectorized operation
df['total'] = df['quantity'] * df['price']

# ❌ SLOW: Apply with complex function
df['category'] = df['age'].apply(categorize_age)

# ✅ FAST: Vectorized with np.where
df['category'] = np.where(df['age'] > 18, 'Adult', 'Minor')
```

---

### 2. Memory Optimization

```python
# Check memory usage
print(df.memory_usage(deep=True))

# Optimize dtypes
df['customer_id'] = df['customer_id'].astype('int32')  # instead of int64
df['category'] = df['category'].astype('category')  # for categorical data

# Read CSV with optimized dtypes
df = pd.read_csv('large_file.csv', dtype={
    'customer_id': 'int32',
    'product_id': 'int32',
    'category': 'category'
})
```

---

### 3. Efficient Processing

```python
# Process large files in chunks
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    # Process each chunk
    processed = clean_data(chunk)
    processed.to_csv('output.csv', mode='a', header=False, index=False)

# Use query for filtering (faster for complex conditions)
df_filtered = df.query('age > 30 and salary > 70000')

# Use eval for calculations (faster for complex math)
df.eval('total = quantity * price', inplace=True)
```

---

## 🎯 EPAM Interview Scenarios

### Scenario 1: Customer Segmentation
**Problem**: Segment customers by total spend and order frequency.

```python
def segment_customers(orders_df, customers_df):
    """Segment customers for EPAM interview"""
    # Calculate customer metrics
    customer_metrics = orders_df.groupby('customer_id').agg({
        'order_id': 'count',
        'order_amount': 'sum'
    }).reset_index()
    customer_metrics.columns = ['customer_id', 'order_count', 'total_spent']
    
    # Merge with customer data
    customer_data = pd.merge(customers_df, customer_metrics, on='customer_id', how='left')
    customer_data['order_count'] = customer_data['order_count'].fillna(0)
    customer_data['total_spent'] = customer_data['total_spent'].fillna(0)
    
    # Segment customers
    customer_data['segment'] = 'Basic'
    customer_data.loc[
        (customer_data['total_spent'] > 2000) & (customer_data['order_count'] > 5),
        'segment'
    ] = 'Premium'
    customer_data.loc[
        (customer_data['total_spent'] > 500) & (customer_data['total_spent'] <= 2000),
        'segment'
    ] = 'Standard'
    
    return customer_data

# Usage
segmented = segment_customers(orders, customers)
print(segmented.groupby('segment').size())
```

---

## 🚀 Practice Exercises

**See**: `02_Python/exercises/04_Pandas_Exercises.md`

**Master these patterns**:
1. ✅ DataFrame creation and manipulation
2. ✅ Data cleaning and validation
3. ✅ Data transformation and feature engineering
4. ✅ GroupBy and aggregation
5. ✅ Merge and join operations
6. ✅ Time series analysis
7. ✅ Performance optimization
8. ✅ Real-world ETL scenarios

**Target Time**: Solve any pandas problem in < 20 minutes

---

## 📚 Quick Reference Cheat Sheet

### Essential Operations
```python
# Read/Write
df = pd.read_csv('file.csv')
df.to_csv('output.csv', index=False)

# Selection
df['column']
df[['col1', 'col2']]
df[df['age'] > 30]

# Cleaning
df.dropna()
df.fillna(0)
df.drop_duplicates()

# Transformation
df.groupby('column').agg({'value': 'sum'})
pd.merge(df1, df2, on='key')

# Analysis
df.describe()
df.value_counts()
df.groupby('column').size()
```

---

## 🎯 Next Steps

1. **Practice pandas operations** until fluent
2. **Complete all exercises** 
3. **Review solutions** after attempting
4. **Move to**: Data Validation & Error Handling

**You're now ready to master data manipulation with pandas!** 🚀

**Next Module**: `02_Python/05_Data_Validation_Error_Handling.md`



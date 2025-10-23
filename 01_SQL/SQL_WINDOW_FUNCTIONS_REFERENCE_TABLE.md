# SQL Window Functions - Complete Reference Table

## 🎯 All SQL Window Functions Ordered by Importance

### **TIER 1: ESSENTIAL (Must Know for EPAM Interviews)**

| Function | Category | Purpose | Syntax | Use Cases | EPAM Priority |
|----------|----------|---------|--------|-----------|---------------|
| **ROW_NUMBER()** | Ranking | Sequential numbering (1,2,3...) | `ROW_NUMBER() OVER (ORDER BY col)` | Pagination, Top N per group, Unique IDs | ⭐⭐⭐⭐⭐ |
| **RANK()** | Ranking | Ranking with gaps for ties | `RANK() OVER (ORDER BY col)` | Sports rankings, Performance rankings | ⭐⭐⭐⭐⭐ |
| **DENSE_RANK()** | Ranking | Ranking without gaps for ties | `DENSE_RANK() OVER (ORDER BY col)` | Percentiles, Quartiles, Consecutive rankings | ⭐⭐⭐⭐⭐ |
| **SUM()** | Aggregate | Running totals, cumulative sums | `SUM(col) OVER (ORDER BY col)` | Running totals, Cumulative analysis | ⭐⭐⭐⭐⭐ |
| **AVG()** | Aggregate | Running averages, moving averages | `AVG(col) OVER (ORDER BY col)` | Moving averages, Performance tracking | ⭐⭐⭐⭐⭐ |
| **COUNT()** | Aggregate | Running counts, cumulative counts | `COUNT(*) OVER (ORDER BY col)` | Order counting, Progress tracking | ⭐⭐⭐⭐⭐ |
| **LAG()** | Offset | Access previous row values | `LAG(col, n) OVER (ORDER BY col)` | Period-over-period analysis, Trend detection | ⭐⭐⭐⭐⭐ |
| **LEAD()** | Offset | Access next row values | `LEAD(col, n) OVER (ORDER BY col)` | Future value analysis, Gap analysis | ⭐⭐⭐⭐⭐ |

### **TIER 2: IMPORTANT (Common in Business Scenarios)**

| Function | Category | Purpose | Syntax | Use Cases | EPAM Priority |
|----------|----------|---------|--------|-----------|---------------|
| **FIRST_VALUE()** | Offset | First value in window | `FIRST_VALUE(col) OVER (ORDER BY col)` | Baseline comparisons, Customer journey | ⭐⭐⭐⭐ |
| **LAST_VALUE()** | Offset | Last value in window | `LAST_VALUE(col) OVER (ORDER BY col ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)` | Final values, End state analysis | ⭐⭐⭐⭐ |
| **MAX()** | Aggregate | Running maximum | `MAX(col) OVER (ORDER BY col)` | Peak detection, Performance tracking | ⭐⭐⭐⭐ |
| **MIN()** | Aggregate | Running minimum | `MIN(col) OVER (ORDER BY col)` | Low point detection, Range analysis | ⭐⭐⭐⭐ |
| **NTILE()** | Ranking | Divide rows into buckets | `NTILE(n) OVER (ORDER BY col)` | Percentiles, Quartiles, Deciles | ⭐⭐⭐⭐ |
| **PERCENT_RANK()** | Ranking | Relative rank as percentage | `PERCENT_RANK() OVER (ORDER BY col)` | Percentile analysis, Performance distribution | ⭐⭐⭐⭐ |
| **CUME_DIST()** | Ranking | Cumulative distribution | `CUME_DIST() OVER (ORDER BY col)` | Distribution analysis, Statistical analysis | ⭐⭐⭐⭐ |

### **TIER 3: ADVANCED (Specialized Use Cases)**

| Function | Category | Purpose | Syntax | Use Cases | EPAM Priority |
|----------|----------|---------|--------|-----------|---------------|
| **NTH_VALUE()** | Offset | Nth value in window | `NTH_VALUE(col, n) OVER (ORDER BY col)` | Specific position analysis | ⭐⭐⭐ |
| **STDDEV()** | Aggregate | Running standard deviation | `STDDEV(col) OVER (ORDER BY col)` | Volatility analysis, Risk assessment | ⭐⭐⭐ |
| **VARIANCE()** | Aggregate | Running variance | `VARIANCE(col) OVER (ORDER BY col)` | Statistical analysis, Data quality | ⭐⭐⭐ |
| **MEDIAN()** | Aggregate | Running median | `MEDIAN(col) OVER (ORDER BY col)` | Central tendency analysis | ⭐⭐⭐ |
| **MODE()** | Aggregate | Most frequent value | `MODE() OVER (ORDER BY col)` | Mode analysis, Frequency analysis | ⭐⭐ |

### **TIER 4: SPECIALIZED (Database-Specific)**

| Function | Category | Purpose | Syntax | Use Cases | EPAM Priority |
|----------|----------|---------|--------|-----------|---------------|
| **PERCENTILE_CONT()** | Ranking | Continuous percentile | `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY col) OVER ()` | Precise percentile calculations | ⭐⭐ |
| **PERCENTILE_DISC()** | Ranking | Discrete percentile | `PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY col) OVER ()` | Discrete percentile calculations | ⭐⭐ |
| **LISTAGG()** | Aggregate | Concatenate values | `LISTAGG(col, ',') WITHIN GROUP (ORDER BY col) OVER ()` | String aggregation, Comma-separated lists | ⭐⭐ |
| **JSON_ARRAYAGG()** | Aggregate | JSON array aggregation | `JSON_ARRAYAGG(col) OVER ()` | JSON data processing | ⭐ |
| **XMLAGG()** | Aggregate | XML aggregation | `XMLAGG(XMLELEMENT("item", col)) OVER ()` | XML data processing | ⭐ |

### **TIER 5: ANALYTICAL (Advanced Analytics)**

| Function | Category | Purpose | Syntax | Use Cases | EPAM Priority |
|----------|----------|---------|--------|-----------|---------------|
| **CORR()** | Aggregate | Correlation coefficient | `CORR(col1, col2) OVER ()` | Correlation analysis | ⭐ |
| **COVAR_POP()** | Aggregate | Population covariance | `COVAR_POP(col1, col2) OVER ()` | Statistical analysis | ⭐ |
| **COVAR_SAMP()** | Aggregate | Sample covariance | `COVAR_SAMP(col1, col2) OVER ()` | Statistical analysis | ⭐ |
| **REGR_SLOPE()** | Aggregate | Regression slope | `REGR_SLOPE(y, x) OVER ()` | Linear regression analysis | ⭐ |
| **REGR_INTERCEPT()** | Aggregate | Regression intercept | `REGR_INTERCEPT(y, x) OVER ()` | Linear regression analysis | ⭐ |
| **REGR_R2()** | Aggregate | R-squared value | `REGR_R2(y, x) OVER ()` | Regression quality | ⭐ |

---

## 🔧 Frame Specifications Reference

### **ROWS vs RANGE**

| Type | Description | Use Case | Example |
|------|-------------|----------|---------|
| **ROWS** | Physical row count | Moving windows, Sliding calculations | `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` |
| **RANGE** | Logical value range | Value-based windows, Handles ties | `RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW` |

### **Frame Boundaries**

| Boundary | Meaning | Example |
|----------|---------|---------|
| `UNBOUNDED PRECEDING` | Start of partition | All rows from beginning |
| `N PRECEDING` | N rows before current | Last 5 rows |
| `CURRENT ROW` | Current row only | Just this row |
| `N FOLLOWING` | N rows after current | Next 3 rows |
| `UNBOUNDED FOLLOWING` | End of partition | All rows to end |

---

## 🎯 Common Patterns by Business Use Case

### **Running Totals & Cumulative Analysis**
```sql
-- Running total
SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

-- Running count
COUNT(*) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

-- Running average
AVG(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

### **Moving Averages & Sliding Windows**
```sql
-- 7-day moving average
AVG(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)

-- 3-day centered average
AVG(amount) OVER (ORDER BY date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)

-- Last 10 rows
AVG(amount) OVER (ORDER BY date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW)
```

### **Ranking & Percentiles**
```sql
-- Top N per group
ROW_NUMBER() OVER (PARTITION BY group ORDER BY value DESC)

-- Percentile ranking
PERCENT_RANK() OVER (ORDER BY value)

-- Quartiles
NTILE(4) OVER (ORDER BY value)
```

### **Time Series Analysis**
```sql
-- Previous value
LAG(value, 1) OVER (PARTITION BY id ORDER BY date)

-- Next value
LEAD(value, 1) OVER (PARTITION BY id ORDER BY date)

-- First value in group
FIRST_VALUE(value) OVER (PARTITION BY id ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
```

---

## 🚀 EPAM Interview Success Formula

### **Master These 5 Functions = 90% Success Rate**
1. **ROW_NUMBER()** - For counting and pagination
2. **RANK()** - For competitive rankings
3. **SUM()** - For running totals (THE most important)
4. **LAG()** - For period-over-period analysis
5. **AVG()** - For moving averages

### **Essential Patterns to Memorize**
```sql
-- Pattern 1: Running Total (EPAM's #1 favorite)
SUM(amount) OVER (
    PARTITION BY group 
    ORDER BY date 
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)

-- Pattern 2: Top N per Group
ROW_NUMBER() OVER (
    PARTITION BY group 
    ORDER BY value DESC
)

-- Pattern 3: Period Comparison
LAG(value, 1) OVER (
    PARTITION BY group 
    ORDER BY date
)
```

---

## 📊 Database Compatibility

| Function | SQLite | PostgreSQL | MySQL | SQL Server | Oracle |
|----------|--------|------------|-------|------------|--------|
| ROW_NUMBER() | ✅ | ✅ | ✅ | ✅ | ✅ |
| RANK() | ✅ | ✅ | ✅ | ✅ | ✅ |
| DENSE_RANK() | ✅ | ✅ | ✅ | ✅ | ✅ |
| LAG/LEAD() | ✅ | ✅ | ✅ | ✅ | ✅ |
| FIRST_VALUE() | ✅ | ✅ | ✅ | ✅ | ✅ |
| LAST_VALUE() | ✅ | ✅ | ✅ | ✅ | ✅ |
| NTILE() | ✅ | ✅ | ✅ | ✅ | ✅ |
| PERCENT_RANK() | ✅ | ✅ | ✅ | ✅ | ✅ |
| CUME_DIST() | ✅ | ✅ | ✅ | ✅ | ✅ |
| NTH_VALUE() | ❌ | ✅ | ✅ | ✅ | ✅ |
| PERCENTILE_CONT() | ❌ | ✅ | ❌ | ✅ | ✅ |
| PERCENTILE_DISC() | ❌ | ✅ | ❌ | ✅ | ✅ |

---

## 🎯 Quick Decision Tree

**Need to count/rank?** → Use `ROW_NUMBER()`, `RANK()`, or `DENSE_RANK()`
**Need running totals?** → Use `SUM()` with `OVER()`
**Need to compare with previous/next?** → Use `LAG()` or `LEAD()`
**Need moving averages?** → Use `AVG()` with frame specification
**Need percentiles?** → Use `NTILE()`, `PERCENT_RANK()`, or `CUME_DIST()`
**Need first/last values?** → Use `FIRST_VALUE()` or `LAST_VALUE()`

---

**Remember**: Master the Tier 1 functions first - they cover 90% of EPAM interview questions and real-world scenarios!

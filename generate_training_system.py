"""
EPAM Data Integration Engineer - Complete Training System Generator
This script creates a comprehensive training environment with all materials
"""

import os
from datetime import datetime, timedelta

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✓ Created: {path}")

def write_file(path, content):
    """Write content to file"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Generated: {path}")

# =============================================================================
# MASTER GAME PLAN
# =============================================================================

MASTER_PLAN = """# 🎯 EPAM Data Integration Engineer - Master Training Plan

## 📊 Training Overview

**Goal**: Become proficient in all areas required for EPAM Data Integration Engineer role
**Duration**: 3 Weeks (Intensive) or 6 Weeks (Balanced)
**Method**: Structured learning + Hands-on practice + Mock interviews

---

## 📋 Content Coverage Matrix

Based on the official EPAM interview preparation guide, here's what we'll cover:

### Week 1: SQL & Database Fundamentals ⭐
| Topic | Priority | Time | Status |
|-------|----------|------|--------|
| SQL Basics & Syntax | HIGH | 2h | ⬜ |
| Window Functions (ROW_NUMBER, RANK, etc.) | CRITICAL | 4h | ⬜ |
| JOINs (INNER, LEFT, SELF) | CRITICAL | 3h | ⬜ |
| Subqueries & CTEs | HIGH | 2h | ⬜ |
| Aggregations & GROUP BY | HIGH | 2h | ⬜ |
| Query Optimization | MEDIUM | 2h | ⬜ |
| ACID Properties | HIGH | 1h | ⬜ |
| OLTP vs OLAP | HIGH | 1h | ⬜ |

**Total Week 1**: ~17 hours

### Week 2: Python & Data Processing ⭐
| Topic | Priority | Time | Status |
|-------|----------|------|--------|
| Python Basics Review | MEDIUM | 1h | ⬜ |
| String Manipulation | HIGH | 2h | ⬜ |
| File I/O Operations | HIGH | 2h | ⬜ |
| JSON Parsing & Processing | CRITICAL | 3h | ⬜ |
| Collections (dict, set, Counter) | HIGH | 2h | ⬜ |
| Pandas DataFrames | HIGH | 3h | ⬜ |
| REST API Integration | MEDIUM | 2h | ⬜ |
| Error Handling & Logging | MEDIUM | 2h | ⬜ |

**Total Week 2**: ~17 hours

### Week 3: Data Warehousing & ETL ⭐
| Topic | Priority | Time | Status |
|-------|----------|------|--------|
| Data Warehouse Concepts | CRITICAL | 2h | ⬜ |
| Star Schema | CRITICAL | 2h | ⬜ |
| Snowflake Schema | CRITICAL | 2h | ⬜ |
| Slowly Changing Dimensions (SCD) | CRITICAL | 3h | ⬜ |
| Data Vault | MEDIUM | 2h | ⬜ |
| ETL vs ELT | HIGH | 1h | ⬜ |
| Incremental Loads | HIGH | 2h | ⬜ |
| Data Quality & Validation | MEDIUM | 2h | ⬜ |

**Total Week 3**: ~16 hours

### Week 4: Cloud & Big Data Tools ⭐
| Topic | Priority | Time | Status |
|-------|----------|------|--------|
| Cloud Fundamentals (AWS/GCP) | HIGH | 2h | ⬜ |
| BigQuery Basics | HIGH | 3h | ⬜ |
| AWS Glue | MEDIUM | 2h | ⬜ |
| Redshift | MEDIUM | 2h | ⬜ |
| Databricks Concepts | MEDIUM | 2h | ⬜ |
| Delta Lake | MEDIUM | 1h | ⬜ |
| PySpark Basics | MEDIUM | 3h | ⬜ |
| Data Lake vs Data Warehouse | HIGH | 1h | ⬜ |

**Total Week 4**: ~16 hours

### Week 5: Apache Airflow & Orchestration ⭐
| Topic | Priority | Time | Status |
|-------|----------|------|--------|
| Airflow Architecture | CRITICAL | 2h | ⬜ |
| DAG Creation | CRITICAL | 3h | ⬜ |
| Operators (Bash, Python, SQL) | CRITICAL | 3h | ⬜ |
| Sensors & Triggers | HIGH | 2h | ⬜ |
| Task Dependencies | HIGH | 2h | ⬜ |
| Jinja Templates | MEDIUM | 1h | ⬜ |
| Airflow Best Practices | MEDIUM | 2h | ⬜ |
| Monitoring & Alerting | MEDIUM | 1h | ⬜ |

**Total Week 5**: ~16 hours

### Week 6: System Design & Mock Interviews ⭐
| Topic | Priority | Time | Status |
|-------|----------|------|--------|
| System Design Principles | HIGH | 3h | ⬜ |
| Scalability & Partitioning | HIGH | 2h | ⬜ |
| Data Pipeline Design | HIGH | 3h | ⬜ |
| CI/CD for Data Pipelines | MEDIUM | 2h | ⬜ |
| Mock Interview #1 | CRITICAL | 2h | ⬜ |
| Mock Interview #2 | CRITICAL | 2h | ⬜ |
| Review & Weak Spots | CRITICAL | 4h | ⬜ |

**Total Week 6**: ~18 hours

---

## 🎓 Learning Methodology

### 1. Read & Understand (30%)
- Study concepts from training materials
- Watch supplementary videos if needed
- Take notes on key points

### 2. Practice & Apply (50%)
- Complete all exercises
- Build small projects
- Code alongside examples

### 3. Test & Review (20%)
- Self-assessment quizzes
- Mock interview questions
- Review mistakes and retry

---

## 📈 Daily Routine (Intensive Track)

**Monday - Friday**:
- Morning (2-3 hours): New topic study + note-taking
- Afternoon (2-3 hours): Hands-on exercises
- Evening (1 hour): Review + flashcards

**Weekend**:
- Saturday: Practice day (4-6 hours)
- Sunday: Mock interview + review (3-4 hours)

---

## 🎯 Success Metrics

### Technical Proficiency
- [ ] Can write window functions without reference
- [ ] Can explain SCD types clearly with examples
- [ ] Can design a star schema for any business problem
- [ ] Can build a simple Airflow DAG from scratch
- [ ] Can parse JSON and manipulate data in Python
- [ ] Can optimize SQL queries
- [ ] Can explain ETL vs ELT with examples
- [ ] Can discuss cloud data solutions

### Interview Readiness
- [ ] Can solve SQL exercises in < 10 minutes
- [ ] Can solve Python exercises in < 15 minutes
- [ ] Can explain concepts clearly and concisely
- [ ] Can discuss trade-offs in design decisions
- [ ] Confident in answering "why" questions
- [ ] Can handle follow-up questions

---

## 📚 Training Materials Structure

```
EPAM_Prep/
├── 01_SQL/
│   ├── 01_SQL_Basics.md
│   ├── 02_Window_Functions.md
│   ├── 03_Joins_Deep_Dive.md
│   ├── 04_Query_Optimization.md
│   ├── exercises/ (problems only)
│   └── solutions/ (separate folder)
├── 02_Python/
│   ├── 01_String_Manipulation.md
│   ├── 02_JSON_Processing.md
│   ├── 03_File_Operations.md
│   ├── 04_Pandas_Basics.md
│   ├── exercises/
│   └── solutions/
├── 03_Data_Warehousing/
│   ├── 01_DWH_Concepts.md
│   ├── 02_Star_Snowflake_Schemas.md
│   ├── 03_SCD_Types.md
│   ├── 04_Data_Vault.md
│   ├── exercises/
│   └── solutions/
├── 04_ETL_ELT/
│   ├── 01_ETL_Fundamentals.md
│   ├── 02_Incremental_Loads.md
│   ├── 03_Data_Quality.md
│   ├── exercises/
│   └── solutions/
├── 05_Cloud_Platforms/
│   ├── 01_Cloud_Basics.md
│   ├── 02_BigQuery.md
│   ├── 03_AWS_Glue_Redshift.md
│   ├── 04_Databricks_Delta.md
│   ├── exercises/
│   └── solutions/
├── 06_Apache_Airflow/
│   ├── 01_Airflow_Architecture.md
│   ├── 02_DAG_Creation.md
│   ├── 03_Operators_Sensors.md
│   ├── exercises/
│   └── solutions/
├── 07_System_Design/
│   ├── 01_Design_Principles.md
│   ├── 02_Data_Pipeline_Design.md
│   ├── exercises/
│   └── solutions/
├── 08_Interview_Prep/
│   ├── Conceptual_Questions.md
│   ├── Technical_Questions.md
│   ├── Behavioral_Questions.md
│   └── Mock_Interviews.md
├── MASTER_GAME_PLAN.md (this file)
├── PROGRESS_TRACKER.md
├── QUICK_REFERENCE.md
└── database/
    ├── setup_database.py
    └── epam_practice.db
```

---

## 🚀 Getting Started

1. ✅ Review this master plan
2. ⬜ Set your target interview date
3. ⬜ Choose your track (Intensive 3-week or Balanced 6-week)
4. ⬜ Start with `01_SQL/01_SQL_Basics.md`
5. ⬜ Update `PROGRESS_TRACKER.md` daily
6. ⬜ Complete exercises for each topic
7. ⬜ Review solutions only after attempting
8. ⬜ Take mock interviews in Week 6

---

## 💡 Pro Tips

1. **Consistency > Intensity**: Better to study 2 hours daily than 14 hours on Sunday
2. **Active Learning**: Write code, don't just read
3. **Spaced Repetition**: Review previous topics regularly
4. **Teach Others**: Explain concepts to solidify understanding
5. **Real-World Context**: Connect concepts to actual job scenarios
6. **Don't Skip Fundamentals**: Strong basics = confident interviews
7. **Time Yourself**: Practice under interview conditions
8. **Ask "Why"**: Understand reasoning, not just syntax

---

## 📞 Mock Interview Schedule

### Mock Interview #1 (End of Week 3)
- **Focus**: SQL + Python basics
- **Duration**: 60 minutes
- **Format**: Live coding exercises
- **Topics**: Window functions, JSON parsing, string manipulation

### Mock Interview #2 (End of Week 5)
- **Focus**: Full stack (SQL + Python + Concepts)
- **Duration**: 90 minutes
- **Format**: Coding + System design
- **Topics**: All technical + conceptual questions

### Final Review (Week 6)
- **Focus**: Weak areas from mock interviews
- **Duration**: Self-paced
- **Format**: Deep dive + re-practice

---

## 🎖️ Certification Path (Optional but Recommended)

After completing this training:
- **AWS Certified Data Engineer**: Validates cloud skills
- **GCP Professional Data Engineer**: Shows GCP proficiency
- **Databricks Certified Associate Developer**: Proves big data knowledge

---

**Remember**: Excellence comes from consistent, deliberate practice. 
You've got this! 🚀

Last Updated: {datetime.now().strftime('%Y-%m-%d')}
"""

# =============================================================================
# PROGRESS TRACKER
# =============================================================================

PROGRESS_TRACKER = """# 📊 EPAM Training - Progress Tracker

**Start Date**: {start_date}
**Target Interview Date**: {target_date}
**Days Remaining**: {days_remaining}

---

## 🎯 Overall Progress

```
Week 1: SQL & Databases           [░░░░░░░░░░] 0%
Week 2: Python & Data Processing  [░░░░░░░░░░] 0%
Week 3: DWH & ETL                 [░░░░░░░░░░] 0%
Week 4: Cloud & Big Data          [░░░░░░░░░░] 0%
Week 5: Apache Airflow            [░░░░░░░░░░] 0%
Week 6: System Design & Mock      [░░░░░░░░░░] 0%

Overall Progress: 0%
```

---

## 📅 Week 1: SQL & Database Fundamentals

### Day 1: SQL Basics & Window Functions
- [ ] Read: `01_SQL/01_SQL_Basics.md`
- [ ] Read: `01_SQL/02_Window_Functions.md`
- [ ] Complete: ROW_NUMBER exercises (5)
- [ ] Complete: RANK/DENSE_RANK exercises (5)
- [ ] Complete: Cumulative sum exercises (5)
- [ ] Review: Solutions and note mistakes
- **Time Spent**: ___ hours
- **Confidence Level (1-10)**: ___

### Day 2: More Window Functions
- [ ] Read: `01_SQL/02_Window_Functions.md` (continued)
- [ ] Complete: LAG/LEAD exercises (5)
- [ ] Complete: FIRST_VALUE/LAST_VALUE exercises (5)
- [ ] Complete: Frame specification exercises (5)
- [ ] Practice: Speed round (solve 5 in 30 min)
- **Time Spent**: ___ hours
- **Confidence Level (1-10)**: ___

### Day 3: JOINs Deep Dive
- [ ] Read: `01_SQL/03_Joins_Deep_Dive.md`
- [ ] Complete: INNER JOIN exercises (5)
- [ ] Complete: LEFT/RIGHT JOIN exercises (5)
- [ ] Complete: SELF JOIN exercises (5)
- [ ] Complete: Complex multi-join exercises (3)
- **Time Spent**: ___ hours
- **Confidence Level (1-10)**: ___

### Day 4: Subqueries & CTEs
- [ ] Read: `01_SQL/04_Query_Optimization.md`
- [ ] Complete: Subquery exercises (5)
- [ ] Complete: CTE exercises (5)
- [ ] Complete: Recursive CTE exercises (3)
- [ ] Practice: Optimization challenges (3)
- **Time Spent**: ___ hours
- **Confidence Level (1-10)**: ___

### Day 5: OLTP vs OLAP & Review
- [ ] Study: ACID properties
- [ ] Study: OLTP vs OLAP differences
- [ ] Review: All Week 1 materials
- [ ] Complete: Week 1 mixed exercises (10)
- [ ] Self-test: Week 1 quiz
- **Time Spent**: ___ hours
- **Week 1 Assessment Score**: ___/100

---

## 📅 Week 2: Python & Data Processing

### Day 6: String Manipulation
- [ ] Read: `02_Python/01_String_Manipulation.md`
- [ ] Complete: Case manipulation exercises (5)
- [ ] Complete: String parsing exercises (5)
- [ ] Complete: Word counting exercise (from PDF)
- [ ] Complete: Pattern matching exercises (5)
- **Time Spent**: ___ hours
- **Confidence Level (1-10)**: ___

### Day 7: JSON Processing
- [ ] Read: `02_Python/02_JSON_Processing.md`
- [ ] Complete: JSON parsing exercises (5)
- [ ] Complete: Email domain extraction (from PDF)
- [ ] Complete: Nested JSON exercises (5)
- [ ] Complete: JSON transformation exercises (5)
- **Time Spent**: ___ hours
- **Confidence Level (1-10)**: ___

### Day 8: File Operations
- [ ] Read: `02_Python/03_File_Operations.md`
- [ ] Complete: File reading exercises (5)
- [ ] Complete: CSV processing exercises (5)
- [ ] Complete: File writing exercises (5)
- [ ] Complete: Error handling exercises (3)
- **Time Spent**: ___ hours
- **Confidence Level (1-10)**: ___

### Day 9: Pandas Basics
- [ ] Read: `02_Python/04_Pandas_Basics.md`
- [ ] Complete: DataFrame creation exercises (5)
- [ ] Complete: Data filtering exercises (5)
- [ ] Complete: GroupBy exercises (5)
- [ ] Complete: Data transformation exercises (5)
- **Time Spent**: ___ hours
- **Confidence Level (1-10)**: ___

### Day 10: Python Review
- [ ] Review: All Week 2 materials
- [ ] Complete: Week 2 mixed exercises (10)
- [ ] Self-test: Week 2 quiz
- [ ] Speed challenge: 5 Python problems in 45 min
- **Time Spent**: ___ hours
- **Week 2 Assessment Score**: ___/100

---

## 📅 Week 3: Data Warehousing & ETL

### Day 11: DWH Concepts
- [ ] Read: `03_Data_Warehousing/01_DWH_Concepts.md`
- [ ] Study: Fact vs Dimension tables
- [ ] Study: Normalization vs Denormalization
- [ ] Complete: Conceptual exercises (5)
- [ ] Draw: 3 sample DWH architectures
- **Time Spent**: ___ hours
- **Confidence Level (1-10)**: ___

### Day 12: Star & Snowflake Schemas
- [ ] Read: `03_Data_Warehousing/02_Star_Snowflake_Schemas.md`
- [ ] Design: 2 star schemas
- [ ] Design: 2 snowflake schemas
- [ ] Complete: Schema design exercises (5)
- [ ] Compare: When to use which
- **Time Spent**: ___ hours
- **Confidence Level (1-10)**: ___

### Day 13: Slowly Changing Dimensions
- [ ] Read: `03_Data_Warehousing/03_SCD_Types.md`
- [ ] Study: SCD Type 1, 2, 3
- [ ] Complete: SCD Type 1 exercises (3)
- [ ] Complete: SCD Type 2 exercises (3)
- [ ] Complete: SCD Type 3 exercises (2)
- **Time Spent**: ___ hours
- **Confidence Level (1-10)**: ___

### Day 14: ETL Fundamentals
- [ ] Read: `04_ETL_ELT/01_ETL_Fundamentals.md`
- [ ] Study: ETL vs ELT
- [ ] Study: Incremental loads
- [ ] Complete: ETL design exercises (3)
- [ ] Design: 2 ETL pipelines
- **Time Spent**: ___ hours
- **Confidence Level (1-10)**: ___

### Day 15: Week 3 Review
- [ ] Review: All Week 3 materials
- [ ] Complete: Week 3 mixed exercises
- [ ] Self-test: Week 3 quiz
- [ ] Prepare: Mock Interview #1
- **Time Spent**: ___ hours
- **Week 3 Assessment Score**: ___/100

---

## 🎤 Mock Interview #1 Results

**Date**: ___________
**Duration**: 60 minutes
**Score**: ___/100

### SQL Performance
- Window Functions: ___/25
- JOINs: ___/25
- Comments: 

### Python Performance
- String Manipulation: ___/25
- JSON Processing: ___/25
- Comments:

### Areas to Improve:
1. 
2. 
3. 

---

## 📅 Week 4-6: [Continue pattern...]

---

## 📈 Skills Assessment Matrix

Rate yourself (1-10) after each week:

| Skill | Week 1 | Week 3 | Week 6 | Target |
|-------|--------|--------|--------|--------|
| Window Functions | ___ | ___ | ___ | 9+ |
| JOINs | ___ | ___ | ___ | 9+ |
| Python Basics | ___ | ___ | ___ | 8+ |
| JSON Processing | ___ | ___ | ___ | 9+ |
| DWH Concepts | ___ | ___ | ___ | 8+ |
| Star Schema Design | ___ | ___ | ___ | 8+ |
| SCD Types | ___ | ___ | ___ | 8+ |
| ETL vs ELT | ___ | ___ | ___ | 8+ |
| Cloud Basics | ___ | ___ | ___ | 7+ |
| Airflow DAGs | ___ | ___ | ___ | 7+ |

---

## 🎯 Ready Checklist (Complete before interview)

### Technical Readiness
- [ ] Can solve window function problems in < 5 min
- [ ] Can explain all SCD types with examples
- [ ] Can design a star schema in < 10 min
- [ ] Can parse JSON in Python without reference
- [ ] Can explain ETL vs ELT clearly
- [ ] Can discuss cloud platforms confidently
- [ ] Can explain Airflow architecture

### Conceptual Readiness
- [ ] Can explain ACID properties
- [ ] Can compare OLTP vs OLAP
- [ ] Can discuss data quality approaches
- [ ] Can explain incremental loads
- [ ] Can discuss partitioning strategies
- [ ] Can explain CI/CD for data pipelines

### Mental Readiness
- [ ] Confident in abilities
- [ ] Prepared for follow-up questions
- [ ] Can explain reasoning behind solutions
- [ ] Ready to discuss trade-offs
- [ ] Comfortable with "I don't know, but..."

---

## 📊 Study Time Tracker

| Week | Planned | Actual | Topics Covered |
|------|---------|--------|----------------|
| 1 | 17h | ___h | SQL & Databases |
| 2 | 17h | ___h | Python & Data Processing |
| 3 | 16h | ___h | DWH & ETL |
| 4 | 16h | ___h | Cloud & Big Data |
| 5 | 16h | ___h | Apache Airflow |
| 6 | 18h | ___h | System Design & Mock |
| **Total** | **100h** | **___h** | |

---

**Last Updated**: ___________
**Next Milestone**: ___________
"""

def generate_master_files():
    """Generate master planning files"""
    
    # Calculate dates
    start_date = datetime.now().strftime('%Y-%m-%d')
    target_date = (datetime.now() + timedelta(days=42)).strftime('%Y-%m-%d')  # 6 weeks
    days_remaining = 42
    
    # Write master plan
    write_file('MASTER_GAME_PLAN.md', MASTER_PLAN)
    
    # Write progress tracker
    progress_content = PROGRESS_TRACKER.format(
        start_date=start_date,
        target_date=target_date,
        days_remaining=days_remaining
    )
    write_file('PROGRESS_TRACKER.md', progress_content)
    
    print("\n✅ Master planning files created!")

if __name__ == "__main__":
    print("="*70)
    print("EPAM Training System Generator - Phase 1: Master Plan")
    print("="*70)
    print()
    
    generate_master_files()
    
    print()
    print("="*70)
    print("✅ Phase 1 Complete!")
    print("="*70)
    print()
    print("Next: Run phase 2 to generate all training modules...")


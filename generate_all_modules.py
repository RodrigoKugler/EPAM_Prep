"""
Phase 2: Generate ALL Training Modules
Creates complete training materials with exercises and solutions separated
"""

import os

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)

def write_file(path, content):
    """Write content to file"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ {path}")

# Create directory structure
def create_structure():
    """Create the complete folder structure"""
    folders = [
        '01_SQL/exercises',
        '01_SQL/solutions',
        '02_Python/exercises',
        '02_Python/solutions',
        '03_Data_Warehousing/exercises',
        '03_Data_Warehousing/solutions',
        '04_ETL_ELT/exercises',
        '04_ETL_ELT/solutions',
        '05_Cloud_Platforms/exercises',
        '05_Cloud_Platforms/solutions',
        '06_Apache_Airflow/exercises',
        '06_Apache_Airflow/solutions',
        '07_System_Design/exercises',
        '07_System_Design/solutions',
        '08_Interview_Prep',
        'database'
    ]
    
    for folder in folders:
        create_directory(folder)
    
    print("✅ Directory structure created!\n")

if __name__ == "__main__":
    print("="*70)
    print("Phase 2: Creating Training Module Structure")
    print("="*70)
    print()
    
    create_structure()
    
    print("✅ Ready for module content generation!")


"""
Load.py
Load cleaned data into Oracle database using SQL*Loader
"""

import os
import subprocess
import sys
import cx_Oracle


def create_table(username, password):
    """Create table in Oracle before loading data"""
    print("\nCreating table in Oracle...")
    
    try:
        # Connect to Oracle
        dsn = cx_Oracle.makedsn('localhost', 1521, service_name='XEPDB1')
        connection = cx_Oracle.connect(username, password, dsn)
        cursor = connection.cursor()
        
        # SQL script to execute
        sql_script = """
BEGIN
   -- Drop table if exists
   BEGIN
      EXECUTE IMMEDIATE 'DROP TABLE autism_screening CASCADE CONSTRAINTS';
   EXCEPTION
      WHEN OTHERS THEN
         IF SQLCODE != -942 THEN RAISE; END IF;
   END;
   
   -- Drop sequence if exists
   BEGIN
      EXECUTE IMMEDIATE 'DROP SEQUENCE autism_screening_seq';
   EXCEPTION
      WHEN OTHERS THEN
         IF SQLCODE != -2289 THEN RAISE; END IF;
   END;
   
   -- Create sequence
   EXECUTE IMMEDIATE 'CREATE SEQUENCE autism_screening_seq START WITH 1 INCREMENT BY 1';
   
   -- Create table
   EXECUTE IMMEDIATE '
   CREATE TABLE autism_screening (
       id NUMBER PRIMARY KEY,
       A1_Score NUMBER(1) CHECK (A1_Score BETWEEN 0 AND 1) NOT NULL,
       A2_Score NUMBER(1) CHECK (A2_Score BETWEEN 0 AND 1) NOT NULL,
       A3_Score NUMBER(1) CHECK (A3_Score BETWEEN 0 AND 1) NOT NULL,
       A4_Score NUMBER(1) CHECK (A4_Score BETWEEN 0 AND 1) NOT NULL,
       A5_Score NUMBER(1) CHECK (A5_Score BETWEEN 0 AND 1) NOT NULL,
       A6_Score NUMBER(1) CHECK (A6_Score BETWEEN 0 AND 1) NOT NULL,
       A7_Score NUMBER(1) CHECK (A7_Score BETWEEN 0 AND 1) NOT NULL,
       A8_Score NUMBER(1) CHECK (A8_Score BETWEEN 0 AND 1) NOT NULL,
       A9_Score NUMBER(1) CHECK (A9_Score BETWEEN 0 AND 1) NOT NULL,
       A10_Score NUMBER(1) CHECK (A10_Score BETWEEN 0 AND 1) NOT NULL,
       age NUMBER CHECK (age > 0 AND age < 150) NOT NULL,
       gender CHAR(1) CHECK (gender IN (''m'', ''f'')) NOT NULL,
       ethnicity VARCHAR2(50) NOT NULL,
       jaundice VARCHAR2(3) CHECK (jaundice IN (''yes'', ''no'')) NOT NULL,
       autism VARCHAR2(3) CHECK (autism IN (''yes'', ''no'')) NOT NULL,
       country VARCHAR2(200) NOT NULL,
       result NUMBER CHECK (result >= 0) NOT NULL,
       relation VARCHAR2(50) NOT NULL,
       Class_ASD NUMBER(1) CHECK (Class_ASD IN (0, 1)) NOT NULL,
       age_group VARCHAR2(20) CHECK (age_group IN (''child'', ''adolescent'', ''adult'')) NOT NULL
   )';
   
   -- Create trigger for auto-increment
   EXECUTE IMMEDIATE '
   CREATE OR REPLACE TRIGGER autism_screening_id 
   BEFORE INSERT ON autism_screening 
   FOR EACH ROW
   BEGIN
     SELECT autism_screening_seq.NEXTVAL INTO :new.id FROM dual;
   END;';
   
END;
"""
        
        cursor.execute(sql_script)
        connection.commit()
        cursor.close()
        connection.close()
        
        print("✅ Table created successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error creating table: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def check_files_exist():
    """Check if required files exist"""
    print("Checking required files...")
    
    required_files = [
        'data/Autism_test_clean.csv',
        'Autism_Screening.ctl'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
            print(f"✗ Missing: {file}")
        else:
            print(f"✓ Found: {file}")
    
    if missing_files:
        print(f"\n⚠️ Missing {len(missing_files)} required file(s)")
        return False
    
    print("\n✅ All required files found")
    return True


def run_sqlldr(username, password, connection_string, control_file, log_file):
    """Execute SQL*Loader to load data into Oracle"""
    print("\nLoading data into Oracle database...")
    print(f"Control file: {control_file}")
    print(f"Log file: {log_file}")
    
    cmd = f'sqlldr {username}/{password}@{connection_string} control={control_file} log={log_file}'
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("\n✅ Data loaded successfully")
            return True
        else:
            print(f"\n⚠️ SQL*Loader completed with code: {result.returncode}")
            print(result.stdout)
            return False
            
    except Exception as e:
        print(f"\n✗ Error executing SQL*Loader: {str(e)}")
        return False


def main():
    """Main load pipeline"""
    print("\nAUTISM SCREENING DATA - LOAD TO ORACLE\n")
     
    USERNAME = 'SYSTEM'
    PASSWORD = 'SYSTEM'
    CONNECTION_STRING = '//localhost:1521/XEPDB1'
    CONTROL_FILE = 'Autism_Screening.ctl'
    LOG_FILE = 'load_data_Autism_Screening.log'
    
    if not check_files_exist():
        print("\n✗ Load aborted: Missing required files")
        sys.exit(1)
    
    print("Creating/Recreating table...")
    create_table(USERNAME, PASSWORD)
    
    print("Loading data...")
    success = run_sqlldr(USERNAME, PASSWORD, CONNECTION_STRING, CONTROL_FILE, LOG_FILE)
    
    if success:
        print(f"\n✅ LOAD COMPLETED")
        print(f"Check log: {LOG_FILE}\n")
    else:
        print(f"\n⚠️ LOAD COMPLETED WITH WARNINGS")
        print(f"Check log: {LOG_FILE}\n")


if __name__ == "__main__":
    main()
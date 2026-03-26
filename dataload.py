import oracledb
import pandas as pd
import os

# --- CONFIGURATION ---
LIB_DIR = r"C:\Users\neast\OneDrive\Desktop\oracle\instantclient_11_2"
DB_USER = "system"
DB_PASS = "Hermit2026!"
DB_DSN = "localhost:1521/xe"


def load_data():
    try:
        # 1. Initialize Thick Mode
        oracledb.init_oracle_client(lib_dir=LIB_DIR)
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = conn.cursor()
        print("✅ Connected to Oracle Database")

        # 2. Data Load Order
        data_to_load = [
            ('data/school.csv', 'SCHOOL'),
            ('data/course.csv', 'COURSE'),
            ('data/student.csv', 'STUDENT'),
            ('data/enrollment.csv', 'ENROLLMENT'),
            ('data/behavior_log.csv', 'BEHAVIOR_LOG')
        ]

        for file_path, table_name in data_to_load:
            if not os.path.exists(file_path):
                print(f"⚠️ File not found: {file_path}")
                continue

            # Load CSV
            df = pd.read_csv(file_path, skipinitialspace=True)
            df.columns = [c.upper().strip() for c in df.columns]

            # --- SPECIFIC CLEANING FOR STUDENT TABLE ---
            if table_name == 'STUDENT':
                # Force STUDENT_ID and AGE to be Integers (Fixes DPY-4004)
                df['STUDENT_ID'] = pd.to_numeric(df['STUDENT_ID'], errors='coerce').fillna(0).astype(int)
                df['AGE'] = pd.to_numeric(df['AGE'], errors='coerce').fillna(0).astype(int)

                # Handle the empty Address_Line_2 (Fixes the "Invalid" empty values)
                if 'ADDRESS_LINE_2' in df.columns:
                    df['ADDRESS_LINE_2'] = df['ADDRESS_LINE_2'].fillna('').astype(str)

                # Filter out any rows with ID 0 (empty rows at end of CSV)
                df = df[df['STUDENT_ID'] > 0]

            # Numeric cleaning for other tables
            numeric_cols = ['G1', 'G2', 'G3', 'CREDITS', 'HEALTH_STATUS', 'WORKDAY_ALCOHOL', 'WEEKEND_ALCOHOL']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

            # Date formatting for BEHAVIOR_LOG
            placeholders = []
            for col in df.columns:
                if 'DATE' in col:
                    placeholders.append("TO_DATE(:%d, 'YYYY-MM-DD')" % (df.columns.get_loc(col) + 1))
                else:
                    placeholders.append(":%d" % (df.columns.get_loc(col) + 1))

            # CRITICAL: Replace any remaining NaN with None so Oracle sees NULL
            df = df.where(pd.notnull(df), None)

            # Build and Execute SQL
            cols_str = ", ".join(df.columns)
            binds_str = ", ".join(placeholders)
            insert_sql = f"INSERT INTO {table_name} ({cols_str}) VALUES ({binds_str})"

            data_rows = [tuple(x) for x in df.values]

            try:
                cursor.executemany(insert_sql, data_rows)
                print(f"✅ Successfully loaded {table_name} ({len(df)} rows)")
            except oracledb.Error as e:
                print(f"❌ Error in {table_name}: {e}")
                if table_name == 'STUDENT':
                    print("🛑 Stopping Load: Enrollment cannot proceed without Students.")
                    break

        conn.commit()
        print("🚀 Data Load Process Complete!")

    except oracledb.Error as e:
        print(f"❌ Oracle Connection Error: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


if __name__ == "__main__":
    load_data()
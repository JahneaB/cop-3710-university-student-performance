import sqlite3
import pandas as pd

conn = sqlite3.connect("teammate_database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

# Drop tables if they already exist
cursor.execute("DROP TABLE IF EXISTS ENROLLMENT;")
cursor.execute("DROP TABLE IF EXISTS BEHAVIOR_LOG;")
cursor.execute("DROP TABLE IF EXISTS STUDENT;")
cursor.execute("DROP TABLE IF EXISTS COURSE;")
cursor.execute("DROP TABLE IF EXISTS SCHOOL;")

# SCHOOL
cursor.execute("""
CREATE TABLE SCHOOL (
    School_Name TEXT PRIMARY KEY,
    School_Type TEXT CHECK (School_Type IN ('GP', 'MS'))
)
""")

# COURSE
cursor.execute("""
CREATE TABLE COURSE (
    Course_Code TEXT PRIMARY KEY,
    Course_Name TEXT NOT NULL,
    Credits INTEGER NOT NULL
)
""")

# STUDENT
cursor.execute("""
CREATE TABLE STUDENT (
    Student_ID INTEGER PRIMARY KEY,
    First_Name TEXT NOT NULL,
    Last_Name TEXT NOT NULL,
    Age INTEGER,
    Address_Line_2 TEXT,
    School_Name TEXT,
    FOREIGN KEY (School_Name) REFERENCES SCHOOL(School_Name)
)
""")

# ENROLLMENT
cursor.execute("""
CREATE TABLE ENROLLMENT (
    Student_ID INTEGER,
    Course_Code TEXT,
    G1 INTEGER,
    G2 INTEGER,
    G3 INTEGER,
    PRIMARY KEY (Student_ID, Course_Code),
    FOREIGN KEY (Student_ID) REFERENCES STUDENT(Student_ID),
    FOREIGN KEY (Course_Code) REFERENCES COURSE(Course_Code)
)
""")

# BEHAVIOR_LOG
cursor.execute("""
CREATE TABLE BEHAVIOR_LOG (
    Student_ID INTEGER,
    Log_Date TEXT,
    Workday_Alcohol INTEGER CHECK (Workday_Alcohol BETWEEN 1 AND 5),
    Weekend_Alcohol INTEGER CHECK (Weekend_Alcohol BETWEEN 1 AND 5),
    Health_Status INTEGER NOT NULL,
    PRIMARY KEY (Student_ID, Log_Date),
    FOREIGN KEY (Student_ID) REFERENCES STUDENT(Student_ID) ON DELETE CASCADE
)
""")

conn.commit()

# Load CSVs
school = pd.read_csv("school.csv")
course = pd.read_csv("course.csv")
student = pd.read_csv("student.csv")
enrollment = pd.read_csv("enrollment.csv")
behavior = pd.read_csv("behavior_log.csv")

school.to_sql("SCHOOL", conn, if_exists="append", index=False)
course.to_sql("COURSE", conn, if_exists="append", index=False)
student.to_sql("STUDENT", conn, if_exists="append", index=False)
enrollment.to_sql("ENROLLMENT", conn, if_exists="append", index=False)
behavior.to_sql("BEHAVIOR_LOG", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("SQLite database created and CSV data loaded.")
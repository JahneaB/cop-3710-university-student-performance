import pandas as pd
import os

# 1. Setup
raw_df = pd.read_csv('student-mat.csv')

# create 'data' directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# 2. SCHOOL Table
# Kaggle 'school' column has 'GP' or 'MS'
school_data = raw_df[['school']].drop_duplicates()
school_data.columns = ['School_Name']
school_data['School_Type'] = school_data['School_Name'] # Both are 'GP' or 'MS'
school_data.to_csv('data/school.csv', index=False)

# 3. STUDENT Table
# Kaggle doesn't have Student IDs or Names, so we generate them to fit your schema
raw_df['Student_ID'] = range(1001, 1001 + len(raw_df))
raw_df['First_Name'] = "Student"
raw_df['Last_Name'] = raw_df['Student_ID'].astype(str)
raw_df['Address_Line_2'] = None # Optional field

student_df = raw_df[['Student_ID', 'First_Name', 'Last_Name', 'age', 'Address_Line_2', 'school']]
student_df.columns = ['Student_ID', 'First_Name', 'Last_Name', 'Age', 'Address_Line_2', 'School_Name']
student_df.to_csv('data/student.csv', index=False)

# 4. COURSE Table (Manual creation since Kaggle is one big list)
course_data = pd.DataFrame({
    'Course_Code': ['MATH101', 'POR101'],
    'Course_Name': ['Mathematics', 'Portuguese'],
    'Credits': [3, 3]
})
course_data.to_csv('data/course.csv', index=False)

# 5. ENROLLMENT Table (Associative Entity)
enrollment_df = raw_df[['Student_ID', 'G1', 'G2', 'G3']]
enrollment_df['Course_Code'] = 'MATH101' # Assigning all to Math for this example
enrollment_df.to_csv('data/enrollment.csv', index=False)

# 6. BEHAVIOR_LOG Table (Weak Entity)
behavior_df = raw_df[['Student_ID', 'Dalc', 'Walc', 'health']]
behavior_df.insert(1, 'Log_Date', '2026-03-26') # Today's Date
behavior_df.columns = ['Student_ID', 'Log_Date', 'Workday_Alcohol', 'Weekend_Alcohol', 'Health_Status']
behavior_df.to_csv('data/behavior_log.csv', index=False)

print("Success! Your 5 CSV files are ready in the /data folder.")
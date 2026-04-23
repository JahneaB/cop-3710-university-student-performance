# cop-3710-university-student-performance
University Student Performance & Enrollment Database
Course: COP3710 - Database Systems

Authors: Jahnea Bush & Justine Bailey


<ins>Project Summary</ins>

This project involves the design and implementation of a robust academic database system. The system tracks student demographics, course details, enrollments, grades, and behavioral data. Beyond simple storage, the database enforces academic integrity through prerequisite enforcement triggers and automates administrative tasks using GPA computation procedures and transcript generation queries.

The dataset used for this project is sourced from the Student Alcohol Consumption dataset, which provides a rich foundation for analyzing how social factors and study habits correlate with academic performance.

<ins>The Task</ins>

The primary objective of this project was to build a functional relational database that bridges the gap between raw data and actionable academic insights. We were tasked with:

Schema Modeling: Designing a relational structure to handle complex many-to-many relationships between students and courses.

Data Integrity: Implementing constraints and triggers to ensure enrollment rules (like prerequisites) are followed.

Insight Generation: Developing a user-facing application that allows administrators to identify at-risk students based on a combination of academic performance (G1, G2, G3 grades) and lifestyle indicators (alcohol consumption, health status).

<ins>Team Roles</ins>

Jahnea Bush: Solution Architect & Database Administrator (Schema design, Oracle 11g implementation, and SQL optimization).

Justine Bailey: Designer & Application Developer (Front-end interface using Streamlit, data preprocessing, and Python-Oracle integration).


<ins>Database Design</ins>

Implementation: Built using SQLite (standard Python integration).

Data Handling: Preprocessed using Python (pandas) and loaded from the UCI Student Alcohol dataset.

Scale: All tables are populated with over 100 records to ensure meaningful query results.

<ins>Key Features</ins>

Significant Improvement Tracking: Identifies students who have jumped significantly in performance between midterms (G1) and finals (G3).

Risk Factor Analysis: Correlates workday/weekend alcohol consumption with GPA to find behavioral patterns.

Automated Reporting: Real-time generation of top-performer lists by subject.

<ins>How to Use This Repo</ins>

Follow these steps to set up the environment and run the application:

Step 1: Initialize & Populate the Database
Run the setup script to initialize the schema and populate the tables with the preprocessed dataset.
python setup_dp.py

Step 2: Configure Credentials
Ensure teammate_database.db is in the root directory. If using a custom database name, update the connection string in use_app.py.

Step 3: Launch the Dashboard
Run the Streamlit application to interact with the database.
streamlit run use_app.py


<ins>Application Preview</ins>
The dashboard allows users to select from five different analytical features, including improvement tracking and health-risk indicators.


![Uploading image.png…]()
<img width="788" height="448" alt="Screenshot 2026-04-23 141940" src="https://github.com/user-attachments/assets/aeb52dae-9ed7-4d20-ae31-40c2900f3c95" />



<ins>ER Diagram</ins>

<img width="725" height="437" alt="Screenshot 2026-02-19 130843" src="https://github.com/user-attachments/assets/7ba1bb80-0b3d-4349-b25c-93f2e64597b6" />

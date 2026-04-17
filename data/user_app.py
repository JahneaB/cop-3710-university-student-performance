import sqlite3
import pandas as pd
import streamlit as st

conn = sqlite3.connect("teammate_database.db", check_same_thread=False)

st.title("University Student Performance Database")

option = st.selectbox(
    "Choose a feature",
    [
        "Find students whose grades improved significantly from G1 to G3",
        "View alcohol consumption vs average grades",
        "Compare students with higher health-risk indicators",
        "View top-performing students in each subject",
        "Find students below the school-wide average with higher risk indicators",
    ]
)

if option == "Find students whose grades improved significantly from G1 to G3":
    threshold = st.number_input("Enter improvement threshold", min_value=0, max_value=20, value=3)
    if st.button("Run Query"):
        query = """
        SELECT s.Student_ID,
               s.First_Name,
               s.Last_Name,
               e.G1,
               e.G3,
               (e.G3 - e.G1) AS Improvement
        FROM STUDENT s
        JOIN ENROLLMENT e ON s.Student_ID = e.Student_ID
        WHERE (e.G3 - e.G1) >= ?
        ORDER BY Improvement DESC
        """
        df = pd.read_sql_query(query, conn, params=(threshold,))
        st.dataframe(df)

elif option == "View alcohol consumption vs average grades":
    alcohol_type = st.selectbox(
        "Choose alcohol type",
        ["Workday_Alcohol", "Weekend_Alcohol"]
    )
    if st.button("Run Query"):
        query = f"""
        SELECT b.{alcohol_type},
               ROUND(AVG(e.G3), 2) AS Avg_Final_Grade
        FROM BEHAVIOR_LOG b
        JOIN ENROLLMENT e ON b.Student_ID = e.Student_ID
        GROUP BY b.{alcohol_type}
        ORDER BY b.{alcohol_type}
        """
        df = pd.read_sql_query(query, conn)
        st.dataframe(df)

elif option == "Compare students with higher health-risk indicators":
    threshold = st.number_input("Enter health-status threshold", min_value=1, max_value=5, value=3)
    if st.button("Run Query"):
        query = """
        SELECT CASE
               WHEN b.Health_Status > ? THEN 'Higher Risk'
               ELSE 'Lower Risk'
           END AS Risk_Group,
           ROUND(AVG(e.G3), 2) AS Avg_Final_Grade
        FROM BEHAVIOR_LOG b
        JOIN ENROLLMENT e ON b.Student_ID = e.Student_ID
        GROUP BY CASE
                 WHEN b.Health_Status > ? THEN 'Higher Risk'
                 ELSE 'Lower Risk'
             END
        """
        df = pd.read_sql_query(query, conn, params=(threshold, threshold))
        st.dataframe(df)

elif option == "View top-performing students in each subject":
    if st.button("Run Query"):
        query = """
        SELECT c.Course_Name,
               s.Student_ID,
               s.First_Name,
               s.Last_Name,
               e.G3
        FROM STUDENT s
        JOIN ENROLLMENT e ON s.Student_ID = e.Student_ID
        JOIN COURSE c ON e.Course_Code = c.Course_Code
        WHERE e.G3 = (
            SELECT MAX(e2.G3)
            FROM ENROLLMENT e2
            WHERE e2.Course_Code = e.Course_Code
        )
        ORDER BY c.Course_Name, e.G3 DESC
        """
        df = pd.read_sql_query(query, conn)

        if df.empty:
            st.write("No results found.")
        else:
            for _, row in df.iterrows():
                st.write(
                    f"Student {row['Student_ID']} is a top performer in {row['Course_Name']} "
                    f"with a final grade of {row['G3']}."
                )

elif option == "Find students below the school-wide average with higher risk indicators":
    alcohol_threshold = st.number_input("Enter alcohol threshold", min_value=1, max_value=5, value=3)
    health_threshold = st.number_input("Enter health-status threshold", min_value=1, max_value=5, value=3)

    if st.button("Run Query"):
        query = """
        SELECT s.Student_ID,
               s.First_Name,
               s.Last_Name,
               e.G3,
               b.Workday_Alcohol,
               b.Weekend_Alcohol,
               b.Health_Status
        FROM STUDENT s
        JOIN ENROLLMENT e ON s.Student_ID = e.Student_ID
        JOIN BEHAVIOR_LOG b ON s.Student_ID = b.Student_ID
        WHERE e.G3 < (
            SELECT AVG(G3)
            FROM ENROLLMENT
        )
        AND (
            b.Workday_Alcohol >= ?
            OR b.Weekend_Alcohol >= ?
            OR b.Health_Status >= ?
        )
        ORDER BY e.G3 ASC
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(alcohol_threshold, alcohol_threshold, health_threshold)
        )

        if df.empty:
            st.write("No students found who meet the criteria.")
        else:
            for _, row in df.iterrows():
                risk_flags = []

                if row["Workday Alcohol Consumption"] >= alcohol_threshold:
                    risk_flags.append("high workday alcohol use")
                if row["Weekend Alcohol Consumption"] >= alcohol_threshold:
                    risk_flags.append("high weekend alcohol use")
                if row["Health_Status"] >= health_threshold:
                    risk_flags.append("high health risk")

                risk_text = ", ".join(risk_flags)

                st.write(
                    f"Student {row['Student_ID']} has a below-average grade ({row['G3']}) "
                    f"and shows risk indicators: {risk_text}."
                )
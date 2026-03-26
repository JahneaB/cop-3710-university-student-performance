# cop-3710-university-student-performance

Part C: Relational Schema & Normalization
1. Relational Schema
The following tables represent the logical translation of the E/R diagram into a relational database structure.
Table: Student
Contains information regarding university students and their department affiliations.
•	Primary Key: Student_ID
•	Foreign Key: Dept_ID (References Department)
Student_ID (PK)	Name	Email	Dept_ID (FK)
101	J Bush	jbush@flpoly.edu	CS
102	Alex Smith	asmith@flpoly.edu	ME
Table: Courses
Stores details for available academic courses.
•	Primary Key: Course_ID
Course_ID (PK)	Course_Name	Credits
COP3710	Database 1	3
MAC2311	Calculus 1	4
Table: Enrollment
A junction table representing the many-to-many relationship between Students and Courses.
•	Primary Key: (Student_ID, Course_ID)
•	Foreign Keys: Student_ID (Ref Student), Course_ID (Ref Courses)
Student_ID (FK)	Course_ID (FK)	Grade
101	COP3710	A
________________________________________
2. Functional Dependencies (FDs)
The following nontrivial functional dependencies were identified based on real-world constraints:
•	Student: Student_ID -> {Name, Email, Dept_ID}
•	Courses: Course_ID -> {Course_Name, Credits}
•	Enrollment: {Student_ID, Course_ID} -> {Grade}
________________________________________
3. BCNF Normalization Analysis
Each relation in the schema was tested for Boyce-Codd Normal Form (BCNF). A relation is in BCNF if, for every non-trivial FD $X \rightarrow Y$, $X$ is a superkey.
•	Analysis: In all three tables (Student, Courses, and Enrollment), the determinant (the left side of the arrow) is the Primary Key.
•	Result: Because all determinants are superkeys, the schema is already in BCNF.
•	Redundancy Check: No data is unnecessarily repeated. For example, course credits are stored once in the Courses table rather than being repeated for every student enrollment, preventing update anomalies.

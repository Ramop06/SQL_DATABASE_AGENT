import sqlite3


connection = sqlite3.connect(
    "students.db"
)

cursor = connection.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    marks INTEGER NOT NULL,
    year INTEGER
)
""")


students = [

    ("Rahul", "CSE", 95, 4),
    ("Arjun", "CSE", 92, 4),
    ("Priya", "CSE", 90, 3),
    ("Sneha", "CSE", 88, 4),
    ("Kiran", "CSE", 86, 3),

    ("Ravi", "ECE", 94, 4),
    ("Anjali", "ECE", 89, 3),

    ("Vijay", "EEE", 91, 4),
    ("Meena", "EEE", 85, 3),

    ("Suresh", "IT", 93, 4),
    ("Divya", "IT", 87, 3)

]


cursor.execute(
    "DELETE FROM students"
)


cursor.executemany(
    """
    INSERT INTO students
    (name, department, marks, year)
    VALUES (?, ?, ?, ?)
    """,
    students
)


connection.commit()

connection.close()


print("Database created successfully!")
print("students.db is ready.")
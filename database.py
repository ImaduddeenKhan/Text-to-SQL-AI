import sqlite3
import os

# Define the database path explicitly
db_path = os.path.join(os.getcwd(), "student.db")
print(f"Database will be created at: {db_path}")  # Debugging step

try:
    # Connect to the database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create the table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS STUDENT (
        NAME    VARCHAR(25),
        COURSE   VARCHAR(25),
        SECTION VARCHAR(25),
        MARKS   INT
    );
    """
    cursor.execute(create_table_query)
    print("Table created successfully.")

    # Insert records
    sql_query = """INSERT INTO STUDENT (NAME, COURSE, SECTION, MARKS) VALUES (?, ?, ?, ?)"""
    values = [
        ('Student1', 'Data Science', 'A', 90),
        ('Student2', 'Data Science', 'B', 100),
        ('Student3', 'Data Science', 'A', 86),
        ('Student4', 'DEVOPS', 'A', 50),
        ('Student5', 'DEVOPS', 'A', 35)
    ]

    cursor.executemany(sql_query, values)
    connection.commit()
    print("Data inserted successfully.")

    # Fetch and display records
    print("\nFetching data from STUDENT table:")
    data = cursor.execute("SELECT * FROM STUDENT")

    for row in data:
        print(row)

except Exception as e:
    print("Error:", e)

finally:
    if connection:
        connection.close()
        print("Database connection closed.")

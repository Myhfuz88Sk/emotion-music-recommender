import pymysql
from pymysql.err import OperationalError, ProgrammingError

# Database connection config - update with your credentials
config = {
    'user': 'root',
    'password': '4566', # Remember to change this to your actual MySQL password
    'host': 'localhost',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

try:
    # Connect to MySQL server (no database specified yet)
    cnx = pymysql.connect(**config)
    cursor = cnx.cursor()

    # Create database if not exists
    cursor.execute("CREATE DATABASE IF NOT EXISTS emotion_music")
    print("Database 'emotion_music' created or already exists.")

    # Use the database
    cursor.execute("USE emotion_music")

    # Create table if not exists
    create_table_query = """
    CREATE TABLE IF NOT EXISTS emotion_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        text_input TEXT,
        predicted_emotion VARCHAR(50),
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_table_query)
    cnx.commit()  # Commit changes for DDL
    print("Table 'emotion_logs' created or already exists.")

except OperationalError as err:
    if err.args[0] == 1045:  # ER_ACCESS_DENIED_ERROR
        print("Access denied: Something is wrong with your MySQL user name or password. Please check `setup.py`.")
    else:
        print(f"Operational error: {err}")

except ProgrammingError as err:
    print(f"Programming error: {err}")

except Exception as err:
    print(f"An unexpected error occurred: {err}")

finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'cnx' in locals() and cnx:
        cnx.close()
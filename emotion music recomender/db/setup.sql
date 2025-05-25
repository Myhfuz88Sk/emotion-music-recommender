-- -- CREATE DATABASE IF NOT EXISTS emotion_music;
-- -- USE emotion_music;

-- -- CREATE TABLE IF NOT EXISTS emotion_logs (
-- --     id INT AUTO_INCREMENT PRIMARY KEY,
-- --     text_input TEXT,
-- --     predicted_emotion VARCHAR(50),
-- --     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
-- -- );


-- import mysql.connector
-- from mysql.connector import errorcode

-- # Database connection config - update with your credentials
-- config = {
--     'user': 'your_username',
--     'password': 'your_password',
--     'host': 'localhost',  # or your host
--     'raise_on_warnings': True
-- }

-- try:
--     # Connect to MySQL server (no database specified yet)
--     cnx = mysql.connector.connect(**config)
--     cursor = cnx.cursor()

--     # Create database if not exists
--     cursor.execute("CREATE DATABASE IF NOT EXISTS emotion_music")
--     print("Database created or exists already.")

--     # Use the database
--     cursor.execute("USE emotion_music")

--     # Create table if not exists
--     create_table_query = """
--     CREATE TABLE IF NOT EXISTS emotion_logs (
--         id INT AUTO_INCREMENT PRIMARY KEY,
--         text_input TEXT,
--         predicted_emotion VARCHAR(50),
--         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
--     )
--     """
--     cursor.execute(create_table_query)
--     print("Table created or exists already.")

-- except mysql.connector.Error as err:
--     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
--         print("Something is wrong with your user name or password")
--     else:
--         print(err)

-- finally:
--     cursor.close()
--     cnx.close()

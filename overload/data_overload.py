import sqlite3
import pyodbc
#import secret variables
import base64
from secrets_file import server,database,port,user,password
server=base64.b64decode(server.decode("utf-8")).decode()
database=base64.b64decode(database.decode("utf-8")).decode()
port=base64.b64decode(port.decode("utf-8")).decode()
user=base64.b64decode(user.decode("utf-8")).decode()
password=base64.b64decode(password.decode("utf-8")).decode()

# Connect to the SQLite database
sqlite_conn = sqlite3.connect('D:/projects/temp_base_vizok_maudau/part2.db')
sqlite_cursor = sqlite_conn.cursor()

# Connect to the SQL Server database
driver='SQL Server'
sql_server_conn = pyodbc.connect('DRIVER={};Server={};Database={};Port={};User ID={};Password={}'.format(driver,server,database,port,user,password))
sql_server_cursor = sql_server_conn.cursor()

# Fetch data from SQLite table
sqlite_cursor.execute("SELECT * FROM temp_table")
rows = sqlite_cursor.fetchall()

# Insert data into SQL Server table
for row in rows:
    # Construct your INSERT query here
    query = f"INSERT INTO Rozetka  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    sql_server_cursor.execute(query, row)

sql_server_conn.commit()

# Close connections
sqlite_cursor.close()
sqlite_conn.close()
sql_server_cursor.close()
sql_server_conn.close()

import pyodbc
import base64
import pandas as pd
from secrets_file import server,database,port,user,password
server=base64.b64decode(server.decode("utf-8")).decode()
database=base64.b64decode(database.decode("utf-8")).decode()
port=base64.b64decode(port.decode("utf-8")).decode()
user=base64.b64decode(user.decode("utf-8")).decode()
password=base64.b64decode(password.decode("utf-8")).decode()

driver='SQL Server'
sql_server_conn = pyodbc.connect('DRIVER={};Server={};Database={};Port={};User ID={};Password={}'.format(driver,server,database,port,user,password))
sql_server_cursor = sql_server_conn.cursor()

# Fetch data from SQLite table
sql_server_conn.execute("SELECT * FROM Rozetka")
df = pd.read_sql_query("SELECT * FROM Rozetka",sql_server_conn)

df1=df[df['name'].str.contains('_')]
print(df1['name'])
print(len(df[df['name'].str.contains('_')]))



df1.to_excel('./overload/check.xlsx')
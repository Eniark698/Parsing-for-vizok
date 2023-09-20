def gather():
  import pyodbc
  import base64
  import numpy as np
  import pandas as pd

  from secrets_file import server,database,port,user,password
  server=base64.b64decode(server.decode("utf-8")).decode()
  database=base64.b64decode(database.decode("utf-8")).decode()
  port=base64.b64decode(port.decode("utf-8")).decode()
  user=base64.b64decode(user.decode("utf-8")).decode()
  password=base64.b64decode(password.decode("utf-8")).decode()



  # Connect to the SQL Server database
  driver='ODBC driver 17 for SQL Server'
  sql_server_conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}')
  sql_server_cursor = sql_server_conn.cursor()

  # Fetch data from SQLite table
  df=pd.read_sql("""
                  SELECT  distinct trim(replace(replace([Name],'	',''),'  ','')) as name, Barcode as code
                  FROM [bi_fop_storozhuk].[dbo].[ProductAdministrative]
                  order by name asc, code asc;
                 """,sql_server_conn)

  df.to_excel('./google_shop/file_temp.xlsx', index=False)

  del(df)
  print('created excel file')
  # Close connections
  sql_server_cursor.close()
  sql_server_conn.close()


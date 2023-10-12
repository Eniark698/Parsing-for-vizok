def gather():
  import pyodbc
  import base64
  import pandas as pd
  from datetime import datetime
  import pytz
  from os import path,getcwd
  current_working_directory = getcwd()




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
                  SELECT  distinct trim(Name) as name, Barcode as code
                  FROM [bi_fop_storozhuk].[dbo].[ProductAdministrative]
                  order by name asc, code asc;
                 """,sql_server_conn)



  df=df.sample(frac=1, random_state=None)
  df.to_excel('./google_shop/file_temp_all.xlsx', index=False)


  print('created excel file(all)')
  # Close connections
  sql_server_cursor.close()
  sql_server_conn.close()

  dt_with_timezone = datetime.fromtimestamp(
                path.getmtime(current_working_directory +'\\google_shop\\file_temp_all.xlsx'), pytz.timezone("Europe/Kyiv")           
                              )

  return {'rows': len(df), 'modifiedTime': str(dt_with_timezone)}




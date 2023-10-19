def overload():
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
    sqlite_conn = sqlite3.connect('./google_shop/temp_name.db')
    sqlite_cursor = sqlite_conn.cursor()

    
    # Connect to the SQL Server database
    driver='ODBC driver 18 for SQL Server'
    sql_server_conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}')
    sql_server_cursor = sql_server_conn.cursor()


    # Fetch data from SQLite table
    sqlite_cursor.execute("SELECT * FROM temp_table")
    rows = sqlite_cursor.fetchall()

    #sql_server_cursor.execute('delete from Google_Shop_All;')

  
    # Assuming all data is correctly fetched and there's data to insert:
    if rows:
        # Insert data into SQL Server table
        placeholders = ', '.join(['?'] * len(rows[0])) # Prepare placeholders based on number of columns
        query = f"INSERT INTO Google_Shop VALUES ({placeholders})"
        
        # Execute the insert query for all rows at once
        sql_server_cursor.executemany(query, rows)
        
        sql_server_conn.commit()



    print('inserted(overload_limit)')

    # # Insert data into SQL Server table
    # for row in rows:
    #     # Construct your INSERT query here
    #     sql_server_cursor.execute('delete from Google_Shop;')
    #     query = f"INSERT INTO Google_Shop  VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
        
    #     #query = f"INSERT INTO Rozetka  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    #     sql_server_cursor.execute(query, row)

    # sql_server_conn.commit()

    # Close connections 
    sqlite_cursor.close()
    sqlite_conn.close()
    sql_server_cursor.close()
    sql_server_conn.close()

def gather(logging):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    import googleapiclient.discovery
    import sys
    from datetime import datetime
    import pytz
    import pandas as pd

    # Use the JSON key you downloaded to authenticate and establish a client
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "./google_shop/cred.json", scope
    )
    client = gspread.authorize(creds)

    # Open the Google Sheet using its name
    sheet = client.open("Google-Shop").sheet1  # open the first sheet

    # get mod time
    drive_service = googleapiclient.discovery.build("drive", "v3", credentials=creds)
    file_metadata = (
        drive_service.files()
        .get(
            fileId="1ekEkRbYe5IohpeVR694RSBBvA5fXvORaBv_5mD3Lmbw", fields="modifiedTime"
        )
        .execute()
    )
    dt = datetime.fromisoformat(file_metadata["modifiedTime"].replace("Z", "+00:00"))
    desired_timezone = pytz.timezone("Europe/Kyiv")
    dt_with_timezone = dt.astimezone(desired_timezone)

    # Retrieve all records
    records = sheet.get_all_records()
    df = pd.DataFrame(records)
    # Write shuffeled to file
    df = df.sample(frac=1, random_state=None)
    df.to_excel("./google_shop/file_temp.xlsx", index=False)

    # Delete all rows except the first one
    num_rows = sheet.row_count  # Get the total number of rows
    if num_rows > 1:  # If there's more than 1 row, delete the rest
        sheet.delete_rows(2, num_rows)  # Delete rows from 2 to the end
        deleted = True
    else:
        deleted = False

    logging.info("input part: ", {"rows": len(df), "modifiedTime": str(dt_with_timezone)})
    df = df.dropna(subset=["name"])
    if df.empty == True:
        # sys.exit('no data in excel file')
        logging.critical({'BAD':"no data in excel file, ending..."})
        sys.exit("no data in excel file")

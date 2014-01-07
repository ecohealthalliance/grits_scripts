Usage:
python gd_xlsx_to_mongo.py <filename> <database>
where,
filename = Name of Excel file in Google Drive to be downloaded
database = Name of Database in MongoDb to be created or updated

Libararies used:
1. PyDrive:
    Wrapper for Google Drive
2. PyMongo:
    Library for pushing data into local Mongo instance
3. XLRD:
    Library for parsing EXCEL files

Steps before running the script:
1. Log in to Google API's, goto Services and enable Drive API and Drive SDK
2. Goto Credentials and click on "CREATE NEW CLIENT ID"
3. In the pop - up box ** :
    1. Check on Web application
    2. Enter http://localhost:8090/ in both "Authorized Redirect URIs" and "Authorized Javascript Origins"
4. Click on button Create client ID
5. Click on Download JSON file to download authentication information and store in current working directory
6. Rename downloaded authentication file to client_secrets.json

Notes for file to be downloaded / uploaded:
1. All work - sheets should have header rows.
2. The mongo instance needs to be running on local machine.
3. Collections will be created in the specified Mongo database based on work - sheet names in Excel file.

**The configuration in Step 3 is for a web - application oriented authorization.

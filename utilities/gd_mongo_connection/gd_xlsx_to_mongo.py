# Script for pushing data from excel file
# in Google Drive to MongoDb instance in
# local machine. Please go through README.txt
# before executing script

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from xlrd import open_workbook
import pymongo
import sys
import argparse

# Create a Google Drive Service


def createConnection():
    gAuth = GoogleAuth()
    gAuth.LocalWebserverAuth()
    gDriveConn = GoogleDrive(gAuth)
    print "Created Google Drive Service"
    return gDriveConn

# Download excel file from Google Drive


def downloadExcel(conn, fileToDownload, downloadedFile):
    # Get list of all files in Google Drive
    fileList = conn.ListFile().GetList()

    # Iterate through list of all files to verify if
    # file to be downloaded is present
    for fileN in fileList:

        # If yes, extract file id and download file
        if fileN['title'] == fileToDownload:
            id_file = fileN['id']

            # Download file using file id
            outputFile = conn.CreateFile({'id': id_file})
            outputFile['downloadUrl'] = fileN['exportLinks'][
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
            outputFile.GetContentFile(downloadedFile)

    print "Downloaded Excel File"

# Convert downloaded excel file to a format which could be
# written into CSV files as well as pushed to Mongo instance


def writeExcelToMongo(downloadedFile, databaseName):
    print "Begin Converting Excel File"
    rowStr = ""
    header = []

    # Initialize Mongo connection
    connection = pymongo.MongoClient()
    db = getattr(connection, databaseName)

    # Create workbook object from downloaded file
    wbObj = open_workbook(downloadedFile)

    # Iterate through all sheets present in downloaded
    # file
    for sheetObj in wbObj.sheets():
        header = []

        # Extracting the header row from work-sheet
        for cols in range(sheetObj.ncols):
            header.append(
                unicode(sheetObj.cell(0, cols).value).encode('utf-8'))
        header = [h.replace(".", "") for h in header]

        # Iterate through all rows after header row in selected sheet
        # in workbook
        for rows in range(1, sheetObj.nrows):
            rowVal = []
            rowDict = {}
            # Iterate through all columns present in
            # selected sheet in workbook
            for cols in range(sheetObj.ncols):
            # Extract a particular cell for tuple (rows, cols) and convert
            # into unicode
                rowVal.append(unicode(sheetObj.cell(rows, cols).value).encode(
                    'utf-8'))

            # Push data into collection
            for h, val in zip(header, rowVal):
                rowDict[h] = val

            db[sheetObj.name].insert(rowDict)

    print "Completed pushing data to Mongo"

# Main function.


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename", help="Excel File to be downloaded from Google Drive", type=str)
    parser.add_argument(
        "database", help="Database in Mongo (running on local machine) to be created/updated", type=str)
    args = parser.parse_args()
    # First argument passed is the name of file to be downloaded
    fileToDownload = args.filename

    # Second argument passed is the name of database to be updated
    databaseName = args.database

    # Verifying file extension for Excel file format
    if fileToDownload[-5:] == ".xlsx":
        downloadedFile = fileToDownload
    else:
        downloadedFile = fileToDownload + ".xlsx"

    conn = createConnection()
    downloadExcel(conn, fileToDownload, downloadedFile)
    writeExcelToMongo(downloadedFile, databaseName)

if __name__ == '__main__':
    main()

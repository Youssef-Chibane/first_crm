import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'root',
)


cursorObject = database.cursor()

cursorObject.execute("CREATE DATABASE crmdb")
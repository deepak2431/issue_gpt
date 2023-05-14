import os
from sqlite3 import connect
from dotenv import load_dotenv

from sqlalchemy.engine import URL

load_dotenv()

server = os.getenv("SERVER")
user_name = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")

driver = "{ODBC Driver 17 for SQL Server}"

connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={user_name};PWD={password}"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})


class Config:
    FLASK_ENV = "development"
    TESTING = True

    # database config
    SQLALCHEMY_DATABASE_URI = connection_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # jwt config
    JWT_SECRET_KEY = "issue_app@#$!"

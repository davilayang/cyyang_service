# app/utilities.py

# import flask instances
from app.api import app, db

# function imports
from json import loads
from zipfile import ZipFile
from pandas import read_sql

def load_zip_data(zipPath, fileName):

    """
    load_zip_data

    Function to get data out of zipped file

    Args:
        zipPath (str): Path to a zipped file
        fileName (str): File name inside the zipped file

    Returns: 
        d (str): String loaded from zipped file

    """
    with ZipFile(zipPath) as zfile:
        d = loads(zfile.read(fileName).decode("utf-8"))

    return d

def get_dataframe_from_db(query):

    """
    get_dataframe_from_db

    Function to read a SQL query and then retrieve data from PostgreSQL
    database

    Args: 
        query (str): SQL query for retrieving data

    Returns: 
        dataframe (pandas DataFrame): contains the data retrieved with 
        query

    """

    dataframe = read_sql(query, con=db.engine)

    return dataframe


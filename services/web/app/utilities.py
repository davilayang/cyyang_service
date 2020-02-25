# web/app/utilities.py

from json import loads
from zipfile import ZipFile


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
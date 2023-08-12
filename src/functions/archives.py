import requests
import zipfile
import io
import os
import sys


class Archives:

    def __init__(self):
        """

        """

    @staticmethod
    def decompress(blob: str, path: str):
        """
        :param blob: A Zip archive's URL
        :param path: The local target directory of the extracts
        """

        try:
            req = requests.get(blob)
        except OSError as err:
            print(err)
            sys.exit(1)

        zipped_object = zipfile.ZipFile(io.BytesIO(req.content))
        zipped_object.extractall(path=path)

    @staticmethod
    def directory(path: str):
        """
        :param path: The local target directory of the extracts
        """

        if not os.path.exists(path=path):
            os.makedirs(path)

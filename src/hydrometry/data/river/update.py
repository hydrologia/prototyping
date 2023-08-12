"""
update.py
"""
import datetime
import logging
import os

import dask
import pandas as pd

import src.functions.directories
import src.functions.streams
import src.hydrometry.data.datatype
import src.hydrometry.data.parts


class Update:
    """
    Class Update
    """

    Attributes = src.hydrometry.data.datatype.DataType().Attributes
    Definitions = src.hydrometry.data.datatype.DataType().Definitions

    def __init__(self, attributes: list[Attributes], definitions: Definitions):
        """

        :param attributes: Refer to ...DataType().Attributes
        :param definitions: Refer to ... DataType().Definitions
        """

        self.__attributes = attributes
        self.__definitions = definitions

        # Instances
        self.__directories = src.functions.directories.Directories()
        self.__streams = src.functions.streams.Streams()
        self.__parts = src.hydrometry.data.parts.Parts()

        # Logging
        logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    @dask.delayed
    def __uri(self, attribute: Attributes) -> str:
        """

        :param attribute:
        :return:
        """

        return '{endpoint}/readings.csv?_limit=1000000&min-date={starting}&max-date={ending}'.format(
                endpoint=attribute.endpoint, starting=self.__definitions.starting, ending=self.__definitions.ending)

    @dask.delayed
    def __read(self, uri: str) -> pd.DataFrame:
        """

        :param uri:
        :return:
        """

        return self.__streams.api(uri=uri)

    @dask.delayed
    def __structure(self, blob: pd.DataFrame, value: str) -> pd.DataFrame:
        """

        :param blob:
        :param value:
        :return:
        """

        return self.__parts.structuring(blob=blob, value=value)

    @dask.delayed
    def __write(self, blob: pd.DataFrame, path: str) -> str:
        """

        :param blob:
        :param path:
        :return:
        """

        limit = datetime.datetime.strptime(self.__definitions.ending, '%Y-%m-%d') - datetime.timedelta(days=1)
        text = datetime.datetime.strftime(limit, '%Y-%m-%d')
        message = self.__streams.write(blob=blob, path=os.path.join(path, f'{text}.csv'))

        return f'{os.path.basename(os.path.dirname(path))}|{message}'

    def exc(self, river_: str):
        """

        :param river_:
        :return:
        """

        computation = []
        for attribute in self.__attributes:

            # Directory
            directory = os.path.join(self.__definitions.storage, river_, attribute.station_id, attribute.variable)
            self.__directories.create(path=directory)

            # Computations
            uri = self.__uri(attribute=attribute)
            readings = self.__read(uri=uri)
            structured = self.__structure(blob=readings, value=attribute.variable)
            message = self.__write(blob=structured, path=directory)
            computation.append(message)

        messages = dask.compute(computation, scheduler='processes')[0]

        self.__logger.info(messages)

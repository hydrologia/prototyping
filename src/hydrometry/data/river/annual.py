"""
annual.py
"""
import os
import logging

import dask
import numpy as np
import pandas as pd
import datetime

import src.functions.directories
import src.functions.streams
import src.hydrometry.data.datatype
import src.hydrometry.data.parts


class Annual:
    """
    Class Annual
    """
    Attributes = src.hydrometry.data.datatype.DataType().Attributes
    Definitions = src.hydrometry.data.datatype.DataType().Definitions

    def __init__(self, attributes: list[Attributes], definitions: Definitions, step: int):
        """

        :param attributes: Refer to ...DataType().Attributes
        :param definitions: Refer to ... DataType().Definitions
        :param step:
        """

        self.__attributes = attributes
        self.__definitions = definitions
        self.__step = step

        # Instances
        self.__directories = src.functions.directories.Directories()
        self.__streams = src.functions.streams.Streams()
        self.__parts = src.hydrometry.data.parts.Parts()

        # Logging
        logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    @dask.delayed
    def __uri(self, endpoint: str, starting: str) -> str:
        """

        :param endpoint:
        :param starting:
        :return:
        """

        value = datetime.datetime.strptime(starting, '%Y-%m-%d')
        ending = f'{value.year + self.__step}-01-01'

        return '{endpoint}/readings.csv?_limit=1000000&min-date={starting}&max-date={ending}'.format(
            endpoint=endpoint, starting=starting, ending=ending)

    @dask.delayed
    def __read(self, uri: str) -> pd.DataFrame:
        """

        :param uri:
        :return:
        """
        dtype = {'dateTime': object, 'date': object, 'value': np.float64}
        return self.__streams.api(uri=uri, usecols=['dateTime', 'date', 'value'], dtype=dtype)

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

        return self.__streams.write(blob=blob, path=path)

    def exc(self, river_: str, cycles: np.ndarray):
        """

        :param river_:
        :param cycles:
        :return:
        """

        for cycle in cycles:

            year = int(cycle.split('-', 2)[0]) + self.__step - 1
            computation = []
            for attribute in self.__attributes:

                # Directory
                directory = os.path.join(self.__definitions.storage, river_, attribute.station_id, attribute.variable)
                self.__directories.create(path=directory)

                # Computations
                uri = self.__uri(endpoint=attribute.endpoint, starting=str(cycle))
                readings = self.__read(uri=uri)
                structured = self.__structure(blob=readings, value=attribute.variable)
                message = self.__write(blob=structured, path=os.path.join(directory, f'{year}.csv'))
                computation.append(message)

            messages = dask.compute(computation, scheduler='processes')[0]

            self.__logger.info(messages)

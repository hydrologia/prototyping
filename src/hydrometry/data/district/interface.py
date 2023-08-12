"""
interface.py
"""
import collections
import os
import logging

import numpy as np
import pandas as pd

import config
import src.functions.directories
import src.functions.streams
import src.hydrometry.data.datatype
import src.hydrometry.data.district.annual
import src.hydrometry.data.district.update


class Interface:
    """
    Class Interface
    """

    Attributes = src.hydrometry.data.datatype.DataType().Attributes
    Definitions = src.hydrometry.data.datatype.DataType().Definitions

    def __init__(self, definitions: Definitions):
        """

        :param definitions: Refer to ...DataType().Definitions
        """

        self.__definitions = definitions

        # The physicochemical items
        configurations = config.Config()
        self.__physical_ = configurations.physical_

        # Instances for reading, writing, and setting-up directories
        self.__streams = src.functions.streams.Streams()
        self.__directories = src.functions.directories.Directories()

        # Logging
        logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __attributes(self, data: pd.DataFrame) -> list[Attributes]:
        """

        :param data:
        :return:
        """

        return [self.Attributes(endpoint=endpoint, station_id=station_id, variable=variable)
                for endpoint, station_id, variable in
                zip(data['endpoint'].to_numpy(), data['station_id'].to_numpy(), data['variable'].to_numpy())]

    def __stations_in_focus(self, district: str) -> pd.DataFrame:
        """

        :param district:
        :return:
        """

        # Read in the inventory of data sources/stations
        data = self.__streams.read(uri=self.__definitions.sources, header=0)

        # Gazetteer
        usecols = ['station_id', district]
        gazetteer = self.__streams.read(uri=self.__definitions.gazetteer, header=0, usecols=usecols)

        # ... and focusing on a district
        gazetteer = gazetteer.copy().loc[gazetteer[district] == 1, :]

        # Selecting
        return data.copy().merge(gazetteer, how='inner', on='station_id')

    def __measures_in_focus(self, data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        return data.copy().loc[data['variable'].isin(self.__physical_), :]

    def exc(self, restart: bool, district: str, cycles: np.ndarray):
        """

        :param cycles:
        :param district:
        :param restart:
        :return:
        """

        if restart:
            self.__directories.cleanup(path=os.path.join(self.__definitions.storage, district))

        # The stations & measures in focus.  Herein, the measures are the physicochemical measures.
        data = self.__stations_in_focus(district=district)
        data = self.__measures_in_focus(data=data)
        self.__logger.info(data)

        # Attributes
        attributes = self.__attributes(data=data)

        # Hence
        if restart:
            src.hydrometry.data.district.annual.Annual(attributes=attributes, definitions=self.__definitions).\
                exc(district=district, cycles=cycles)
        else:
            src.hydrometry.data.district.update.Update(attributes=attributes, definitions=self.__definitions).\
                exc(district=district)

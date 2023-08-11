import collections
import os
import logging

import numpy as np
import pandas as pd

import config
import src.functions.directories
import src.functions.streams
import src.hydrometry.data.datatype
import src.hydrometry.data.river.annual
import src.hydrometry.data.river.update


class Interface:
    """

    """

    Attributes = src.hydrometry.data.datatype.DataType().Attributes
    Definitions = src.hydrometry.data.datatype.DataType().Definitions

    def __init__(self, definitions: Definitions, step: int):
        """

        :param definitions: Refer to ...DataType().Definitions
        """

        self.__definitions = definitions
        self.__step = step

        # The properties of interest
        configurations = config.Config()
        self.__mixture = configurations.mixture

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

    def __stations_in_focus(self, river: str) -> pd.DataFrame:
        """

        :param
        :return:
        """

        # Read in the inventory of data sources/stations
        data = self.__streams.read(uri=self.__definitions.sources, header=0)

        # Gazetteer
        usecols = ['station_id', 'river_name']
        gazetteer = self.__streams.read(uri=self.__definitions.gazetteer, header=0, usecols=usecols)

        # ... and focusing on a district
        gazetteer = gazetteer.copy().loc[gazetteer['river_name'].str.lower() == river.lower(), :]

        # Selecting
        return data.copy().merge(gazetteer, how='inner', on='station_id')

    def __measures_in_focus(self, data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        return data.copy().loc[data['variable'].isin(self.__mixture), :]

    def exc(self, restart: bool, river: str, river_: str, cycles: np.ndarray, erase: bool = False):
        """

        :param restart:
        :param river: A river's full name
        :param river_: A river's single-word short name
        :param cycles:
        :param erase:
        :return:
        """

        if erase:
            self.__directories.cleanup(path=os.path.join(self.__definitions.storage, river_))

        # The stations & measures in focus.
        data = self.__stations_in_focus(river=river)
        data = self.__measures_in_focus(data=data)
        self.__logger.info(data)

        # Attributes
        attributes = self.__attributes(data=data)
        self.__logger.info(attributes)
        self.__logger.info(f'N: {len(attributes)}')

        # Hence
        if restart:
            src.hydrometry.data.river.annual.Annual(attributes=attributes, definitions=self.__definitions,
                                                    step=self.__step).exc(river_=river_, cycles=cycles)
        else:
            src.hydrometry.data.river.update.Update(attributes=attributes, definitions=self.__definitions).\
                exc(river_=river_)

import logging
import os.path

import pandas as pd

import src.functions.streams
import src.functions.directories
import src.functions.objects


class Menu:

    def __init__(self, source: str, storage: str):
        """

        :param source: The URI of the gazetteer
        :param storage: The storage area for the constructed menu
        """

        self.__source = source
        self.__storage = storage
        self.__fields = ['station_id', 'station_name', 'river_name']

        # Logging
        logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __gazetteer(self) -> pd.DataFrame:
        """

        :return:
        """

        excerpt = src.functions.streams.Streams().read(
            uri=self.__source, header=0, usecols=self.__fields)
        self.__logger.info(excerpt.head())

        return excerpt

    def __write(self, menu: dict, name: str = 'menu') -> str:
        """

        :param menu:
        :return:
        """

        message = src.functions.objects.Objects().write(
            nodes=menu, path=os.path.join(self.__storage, f'{name}.json'))

        return message

    def exc(self, keys: list, name: str = 'menu'):
        """

        :param keys:
        :param name: The menu's name
        :return:
        """

        # Constructing a dataframe form of the station keys
        reference = pd.DataFrame(data={'station_id': keys})

        # Fields from the stations' gazetteer
        gazetteer = self.__gazetteer()

        # Focusing on the stations in focus
        frame = gazetteer.merge(reference, how='inner', on='station_id')

        # Menu construction; subsequently saved.
        frame.rename(columns={'station_id': 'desc', 'station_name': 'name'}, inplace=True)
        menu = frame[['desc', 'name']].to_dict(orient='records')
        message = self.__write(menu=menu, name=name)

        self.__logger.info(message)

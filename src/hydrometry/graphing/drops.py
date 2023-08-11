import glob
import logging
import os

import config
import src.hydrometry.graphing.menu


class Drops:

    def __init__(self):
        """

        """

        self.__configurations = config.Config()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self, pathstr: str, trait: str):
        """

        :param pathstr:
        :param trait:
        :return:
        """

        entities = glob.glob(os.path.join(pathstr, trait, '*.json'))
        keys = [os.path.splitext(os.path.basename(entity))[0] for entity in entities]
        self.__logger.info(keys)

        src.hydrometry.graphing.menu.Menu(
            source=self.__configurations.gazetteer,
            storage=os.path.join(os.path.dirname(pathstr), 'menu')).exc(keys=keys, name=trait)

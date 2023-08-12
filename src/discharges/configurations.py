"""
configurations.py
"""
import collections
import datetime
import os

import numpy as np
import yaml


class Configurations:
    """
    Configurations
    """

    Parameters = collections.namedtuple(
        typename='Parameters', field_names=['root', 'client_id', 'client_secret'])

    def __init__(self):
        """

        """

        self.__root = 'https://prod-tw-opendata-app.uk-e1.cloudhub.io'

        self.__code = 'thames'

        self.__pathstr = os.path.join(os.getcwd(), 'services.yaml')

        starting = '2022-01-01'
        ending = datetime.date.today().strftime('%Y-%m-%d')
        self.dates = np.arange(starting, ending, dtype='datetime64[D]')

    def __keys(self) -> dict:

        with open(file=self.__pathstr, mode='r') as stream:
            try:
                nodes = yaml.load(stream=stream, Loader=yaml.CLoader)
            except yaml.YAMLError as err:
                raise Exception(err)

        # the dictionary of service keys in relation to the firm in focus
        dictionary: dict = [item for item in nodes['services'] if item['code'] == self.__code][0]

        return dictionary

    def exc(self) -> Parameters:

        keys = self.__keys()
        return self.Parameters(root=self.__root, client_id=keys['client_id'],
                               client_secret=keys['client_secret'])

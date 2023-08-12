"""
datatype.py
"""
import collections


class DataType:
    """
    DataType
    """

    Attributes = collections.namedtuple(typename='Attributes', field_names=['endpoint', 'station_id', 'variable'])
    """
    
    :param endpoint: The URL endpoint of a data set, the data set focuses on a single measurement only.
    :param station_id: The endpoint's station identification code
    :param variable: The name of the measurement field
    """

    Definitions = collections.namedtuple(typename='Definitions',
                                         field_names=['sources', 'gazetteer', 'storage', 'starting', 'ending'])
    """
    
    :param sources: Document URL of the inventory of measurements name strings per hydrometry station
    :param gazetteer: Document URL of the gazetteer of the hydrometry stations
    :param storage: The storage directory of the hydrometry data
    :param starting: Lower date boundary (included in calculations)
    :param ending: Upper date boundary (excluded from calculations)
    """

    def __init__(self):
        """

        """

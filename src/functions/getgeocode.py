import geopandas as gpd
import pandas as pd


class GetGeocode:

    def __init__(self):
        """

        """

    @staticmethod
    def exc(string):

        try:
            return gpd.tools.geocode(string, provider='nominatim', user_agent='spatial.analysis').loc[0, :]
        except LookupError:
            return pd.Series({'geometry': None, 'address': None})

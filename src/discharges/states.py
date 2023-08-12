import os
import datetime

import requests
import numpy as np
import pandas as pd
import dask

import src.discharges.configurations
import src.functions.streams
import src.functions.directories


class States:

    def __init__(self, storage: str):
        """

        :param storage:
        """

        self.__storage = storage

        # The <states> resource
        resource = '/data/STE/v1/DischargeCurrentStatus'

        # Rename
        self.__rename = {'LocationName': 'location_name', 'PermitNumber': 'permit_number', 'X': 'x', 'Y': 'y',
                         'LocationGridRef': 'location_grid_reference', 'ReceivingWaterCourse': 'receiving_water_course',
                         'AlertStatus': 'alert_status', 'StatusChange': 'status_change_datetime',
                         'AlertPast48Hours': 'alert_past_48_hours',
                         'MostRecentDischargeAlertStart': 'most_recent_discharge_alert_start',
                         'MostRecentDischargeAlertStop': 'most_recent_discharge_alert_stop'}

        # Overarching variables
        self.__configurations = src.discharges.configurations.Configurations()

        # Request arguments
        parameters = self.__configurations.exc()
        self.__url = '{root}{resource}'.format(root=parameters.root, resource=resource)
        self.__headers = {'client_id': parameters.client_id,'client_secret': parameters.client_secret}

        # Finally
        self.__streams = src.functions.streams.Streams()

    def __set_directories(self):
        """

        :return:
        """

        directories = src.functions.directories.Directories()
        directories.cleanup(path=self.__storage)
        directories.cleanup(path=self.__storage)

    @dask.delayed
    def __request(self, date: datetime.datetime) -> dict:
        """

        :param date:
        :return:
        """

        params = {'limit': 1000, 'offset': 0, 'col_1': 'StatusChange', 'operand_1': 'gte', 'value_1': str(date),
                  'col_2': 'StatusChange', 'operand_2': 'lt', 'value_2': str(date + np.timedelta64(1, 'D'))}

        try:
            response = requests.get(url=self.__url, headers=self.__headers, params=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise Exception(f'HTTP Error: {err}')
        except Exception as err:
            raise Exception(err) from err

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'{response.status_code}\n{response.json()}')

    @dask.delayed
    def __frame(self, response: dict) -> pd.DataFrame:
        """

        :param response:
        :return:
        """

        if 'items' in response:
            frame = pd.json_normalize(response, 'items')
            frame.rename(columns=self.__rename)
            return frame
        else:
            return pd.DataFrame()

    @dask.delayed
    def __write(self, blob: pd.DataFrame, path: str):

        self.__streams.write(blob=blob, path=path)

    def exc(self):
        """

        :return:
        """

        computation = []
        for date in self.__configurations.dates:

            response = self.__request(date=date)
            frame = self.__frame(response=response)




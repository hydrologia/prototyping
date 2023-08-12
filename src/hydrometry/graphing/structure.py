import pandas as pd
import glob
import os
import dask
import dask.dataframe

import config
import src.functions.objects


class Structure:

    def __init__(self, pathstr: str):
        """
        
        :param pathstr: 
        """
        
        self.__pathstr = pathstr
        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()
        
    def __write(self, data: pd.DataFrame, membership: list, trait: str, station: str) -> str:
        """
        
        :param data: 
        :param membership: 
        :param trait: 
        :param station: 
        :return: 
        """

        if sum(membership) > 0:
            fields = list(data.columns[membership])
            samples = data.copy()[fields]
            samples.reset_index(drop=False, inplace=True)
            nodes = samples.to_dict(orient='tight')
            message = self.__objects.write(nodes=nodes, path=os.path.join(self.__pathstr, trait, f'{station}.json'))
            return message
        else:
            return f'{station}: Unavailable {trait} traits.'

    @dask.delayed
    def __read(self, variables: list[str]) -> pd.DataFrame:
        """
        
        :param variables: 
        :return: 
        """

        # The variables data
        points = []
        for variable in variables:
            try:
                readings = dask.dataframe.read_csv(
                    urlpath=os.path.join(variable, '*.csv'), usecols=['epoch', os.path.basename(variable)])
                frame = readings.compute().set_index('epoch', drop=True)
            except IOError:
                frame = pd.DataFrame()
            points.append(frame)

        return pd.concat(points, axis=1, ignore_index=False)

    @dask.delayed
    def __physical(self, data: pd.DataFrame, station: str) -> str:
        """
        
        :param data: A station's data
        :param station: The station
        :return: 
        """

        membership = data.columns.isin(self.__configurations.physical_)

        return self.__write(data=data, membership=membership, trait='physical', station=station)

    @dask.delayed
    def __physicochemical(self, data: pd.DataFrame, station: str) -> str:
        """
        
        :param data: A station's data
        :param station: The station
        :return: 
        """

        membership = data.columns.isin(self.__configurations.physicochemical)

        return self.__write(data=data, membership=membership, trait='physicochemical', station=station)

    @dask.delayed
    def __variables(self, source: str, station: str) -> list:
        """
        
        :param source: The directory that hosts the stations directories 
        :param station: A station
        :return: 
        """

        return glob.glob(pathname=os.path.join(source, station, '*'))

    def exc(self, source: str, stations: list[str]) -> list[list[str]]:
        """
        
        :param source: The directory that hosts the stations directories 
        :param stations: The list of stations
        :return: 
        """

        # The variables per station
        computations = []
        for station in stations:

            # The variables; path string form.
            variables = self.__variables(source=source, station=station)

            # Read
            data = self.__read(variables=variables)

            # Write
            physical = self.__physical(data=data, station=station)
            physicochemical = self.__physicochemical(data=data, station=station)

            computations.append([physical, physicochemical])

        dask.visualize(computations, filename='dag', format='pdf')
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages

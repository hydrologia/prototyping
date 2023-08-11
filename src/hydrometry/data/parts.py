import pandas as pd
import numpy as np


class Parts:

    def __init__(self):
        """

        """

    @staticmethod
    def structuring(blob: pd.DataFrame, value: str) -> pd.DataFrame:
        """
        In addition to the re-naming of fields - read the <value> notes - an epoch field is appended.

        :param blob: The data set being structured.
        :param value: Each distinct data set details a single measurement type only, e.g., ammonia, dissolved
                      oxygen, etc.  However, the name of the column wherein the values are recorded is always
                      "value".  Herein the column's name is changed to a name that reflects what is being
                      measured.
        :return:
        """

        if blob.empty or blob.shape[0] == 0:
            return blob
        else:
            fields = {'dateTime': 'datetime', 'date': 'date', 'value': value}
            data = blob.copy()[fields.keys()]
            data.rename(columns=fields, inplace=True)

            data.loc[:, 'datetime'] = pd.to_datetime(data['datetime'])
            data.loc[:, 'epoch'] = (data['datetime'].to_numpy().astype(np.int64) / (10 ** 6)).astype(np.longlong)

            return data

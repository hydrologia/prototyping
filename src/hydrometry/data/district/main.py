"""
main.py
"""
import datetime
import logging
import os
import sys

import numpy as np


def main():
    """
    The entry point.

    :return:
    """

    # Setting-up
    definitions = Definitions(sources=sources, gazetteer=gazetteer, storage=storage,
                              starting=starting, ending=ending)
    logger.info(definitions)

    # Dates
    if restart:
        # The first day of January per year of interest: str
        values = np.arange(starting, ending, dtype='datetime64[Y]')
        cycles = np.array([f'{value}-01-01' for value in values])
    else:
        # Dates: datetime
        cycles = np.arange(starting, ending, dtype='datetime64[D]')
    logger.info(cycles)

    # Hence
    src.hydrometry.data.district.interface.Interface(definitions=definitions).\
        exc(restart=restart, district='thames', cycles=cycles)


if __name__ == '__main__':
    """
    Initially ...
    """

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Threads
    os.environ['NUMEXPR_MAX_THREADS'] = '8'

    # Logging
    logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # Classes
    import src.hydrometry.data.district.interface
    import src.hydrometry.data.datatype

    # Instances
    Definitions = src.hydrometry.data.datatype.DataType().Definitions

    # Arguments
    sources = 'https://raw.githubusercontent.com/thirdreading/references/master/warehouse/hydrometry/sources.csv'
    gazetteer = 'https://raw.githubusercontent.com/thirdreading/geocomputations/master/warehouse/hydrometry/gazetteer.csv'
    storage = os.path.join(os.getcwd(), 'warehouse', 'hydrometry', 'measures', 'district')

    restart = True
    today = datetime.date.today()
    starting = '1900-01-01' if restart else ''
    ending = f'{today.year}-01-01' if restart else (today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    main()

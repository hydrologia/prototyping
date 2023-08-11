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

    # Data Types
    definitions = Definitions(sources=sources, gazetteer=gazetteer, storage=storage,
                              starting=starting, ending=ending)
    logger.info(definitions)

    # Dates
    if restart:
        # The first day of January per year of interest: str
        values = np.arange(starting, ending, step, dtype='datetime64[Y]')
        cycles = np.array([f'{value}-01-01' for value in values])
    else:
        # Dates: datetime
        cycles = np.arange(starting, ending, dtype='datetime64[D]')
    logger.info(cycles)

    # Hence
    src.hydrometry.data.river.interface.Interface(definitions=definitions, step=step). \
        exc(restart=restart, river='river thames', river_='thames', cycles=cycles)


if __name__ == '__main__':
    """
    Initially ...
    """

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Threads
    os.environ['NUMEXPR_MAX_THREADS'] = '12'

    # Logging
    logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # Classes
    import config
    import src.hydrometry.data.river.interface
    import src.hydrometry.data.datatype

    # Instances
    Definitions = src.hydrometry.data.datatype.DataType().Definitions

    # Arguments
    sources = 'https://raw.githubusercontent.com/thirdreading/references/master/warehouse/hydrometry/sources.csv'
    gazetteer = config.Config().gazetteer
    storage = os.path.join(os.getcwd(), 'warehouse', 'hydrometry', 'measures', 'river')

    restart = True
    step = 10
    today = datetime.date.today()
    starting = '1960-01-01' if restart else ''
    ending = f'{today.year}-01-01' if restart else (today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    main()

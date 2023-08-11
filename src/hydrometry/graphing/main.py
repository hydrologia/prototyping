import os
import sys
import logging
import glob


def main():

    logger.info('temporary')

    # The river in focus
    river_ = 'thames'

    # Repositories
    source = os.path.join(os.getcwd(), 'warehouse', 'hydrometry', 'measures', 'river', river_)
    storage = os.path.join(os.getcwd(), 'warehouse', 'hydrometry', 'graphing', 'river', river_)
    pathstr = os.path.join(storage, 'data')

    # The stations ...
    stations = glob.glob(pathname=os.path.join(source, '*'))
    stations = [os.path.basename(station) for station in stations]
    logger.info(f'N: {len(stations)}')

    # Setting-up
    directories.cleanup(storage)
    directories.create(path=os.path.join(pathstr, 'physical'))
    directories.create(path=os.path.join(pathstr, 'physicochemical'))
    directories.create(path=os.path.join(storage, 'menu'))

    # Creating the graphing data for the river in focus ...
    messages = src.hydrometry.graphing.structure.Structure(pathstr=pathstr).exc(
        source=source, stations=stations)
    logger.info(messages)

    for trait in ['physical', 'physicochemical']:
        src.hydrometry.graphing.drops.Drops().exc(pathstr=pathstr, trait=trait)


if __name__ == '__main__':
    """
    Initially
    """

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # Classes
    import config
    import src.functions.directories
    import src.hydrometry.graphing.structure
    import src.hydrometry.graphing.drops

    # Instances
    configurations = config.Config()
    directories = src.functions.directories.Directories()

    main()

"""
config.py
"""


class Config:
    """
    The project's global configurations

    """

    def __init__(self):
        """

        """

        # The physical variables, properties
        self.physical = ['rainfall-t-900-mm-qualified', 'rainfall-t-86400-mm-qualified', 'level-min-86400-m-qualified',
                         'level-max-86400-m-qualified', 'level-i-900-m-qualified',
                         'gw-logged-i-subdaily-mAOD-qualified', 'gw-dipped-i-mAOD-qualified',
                         'flow-min-86400-m3s-qualified', 'flow-max-86400-m3s-qualified', 'flow-m-86400-m3s-qualified',
                         'flow-i-900-m3s-qualified']

        self.physical_ = ['flow-i-900-m3s-qualified', 'level-i-900-m-qualified']

        # The physicochemical properties
        self.physicochemical = ['turb-i-subdaily-ntu', 'temp-i-subdaily-C', 'sal-i-subdaily-psu', 'ph-i-subdaily',
                                'nitrate-i-subdaily-mgL', 'fdom-i-subdaily-rfu', 'do-i-subdaily-pct',
                                'do-i-subdaily-mgL', 'cphyll-i-subdaily-ugpL', 'cond-i-subdaily-uS',
                                'cond-i-subdaily-mS', 'bga-i-subdaily-rfu', 'amm-i-subdaily-mgL']

        # The mix in focus
        self.mixture = self.physical_ + self.physicochemical

        # Gazetteer
        self.gazetteer = 'https://raw.githubusercontent.com/thirdreading/geocomputations/master/warehouse/' \
                         'hydrometry/gazetteer.csv'

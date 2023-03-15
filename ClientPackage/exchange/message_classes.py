class Order:
    pass

class PortfolioUpdate:
    '''
    Specificies how a teams portfolio should change
    '''

    def __init__(self, team_name, asset_delta_dict) -> None:
        self.team_name = team_name
        self.asset_delta_dict = asset_delta_dict

    def apply_deltas(self, portfolio):
        assets = portfolio.assets
        for key in self.asset_delta_dict:
            if key not in assets:
                assets[key] = self.asset_delta_dict[key]
            else:
                assets[key] += self.asset_delta_dict[key]
    


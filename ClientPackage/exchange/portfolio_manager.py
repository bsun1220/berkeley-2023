from .exchange import Order
from .portfolio import Portfolio

class PortfolioManager:

    def __init__(self, team_names, standard_portfolio: Portfolio) -> None:
        self.teams = {}
        self.assets = set(standard_portfolio.assets.copy().keys())
        buying_power = standard_portfolio.buying_power
        for name in team_names:
            self.teams[name] = Portfolio(name, standard_portfolio.assets, buying_power)

    def queryPortfolio(self, team_name, with_history=False) -> str:
        """ Return the serialized portfolio of the given team name. """
        return self.teams[team_name].serialize() if team_name in self.teams else None

    def canExecute(self, order:Order) -> bool: #removed asset_name from params because it is already in Order
        # How to check if there are order.size amount of assets available for buying
        portfolio = self.teams[order.team_name]
        if portfolio is None:
            print("Team does not have a portfolio")
            return False
        if order.price <= 0 or order.size <= 0 or order.assetname not in self.assets:
            return False
        if order.is_bid:
            total_cost = order.price * order.size
            return total_cost <= portfolio.buying_power
        return True
        # SHORTS
        # else:
        #     asset_name = order.assetname
        #     assets = portfolio.assets
        #     if asset_name in assets:
        #         # this will depend on if negative positions are allowed
        #         return order.size <= assets[asset_name]
        #     return False
    
    def update(self, order_list: "list[Order]"):
        """ Given a list of orders, process them and update portfolios accordingly."""
        for order in order_list:
            portfolio = self.teams[order.team_name]
            portfolio.update(order)


    def updateBuyingPower(self, teamid, amount):
        portfolio = self.teams[teamid]
        portfolio.updateBuyingPower(amount)

    def updateAssetQuantity(self, teamid, assetname, amount):
        portfolio = self.teams[teamid]
        portfolio.updateAssetQuantity(assetname, amount)

    def finalRankings(self, final_asset_values):
        final_values = {}
        for team in self.teams:
            final_values[team] = self.teams[team].portfolioValue(final_asset_values)
        sorted_teams_by_value = sorted(final_values.items(), key=lambda x: -x[1])

        output = ""
        for i in range(len(sorted_teams_by_value)):
            output += str(i + 1) + ". " + str(sorted_teams_by_value[i]) + '\n'

        return output

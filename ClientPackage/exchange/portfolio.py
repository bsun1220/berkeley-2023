from .exchange import Order

from .message_classes import PortfolioUpdate

class Portfolio:
    """
    Each team should have a portfolio:
        - excess liquidity
        - buying power
        - positions

    Update portfolio when order is placed/filled
    """

    def __init__(self, owner_name: str, initial_asset_dictionary: dict, buying_power: float) -> None:
        self.assets = initial_asset_dictionary.copy()
        self.owner_name = owner_name
        #self.order_history = list()
        self.buying_power = buying_power


    def update(self, order:Order):
        """ Takes in a single order and then applies the changes based on it to the current portfolio"""
        if order.is_bid:
            if order.assetname not in self.assets:
                self.assets[order.assetname] = 0
            self.buying_power -= order.size * order.price

    def updateBuyingPower(self, amount):
        self.buying_power += amount

    def updateAssetQuantity(self, assetname, amount):
        self.assets[assetname] += amount

    def portfolioValue(self, final_asset_values):
        total = self.buying_power
        for asset in self.assets:
            total += final_asset_values[asset] * self.assets[asset]
        return total


    def serialize(self) -> str:
        """ Return the serialized portfolio. """
        to_ret = "Owner: " + str(self.owner_name) + "\nbuying_power: " + str(self.buying_power) + "\nAssets: " + str(self.assets)
        #if with_history:
        #    to_ret += "\nOrder History: " + str(self.order_history)
        return to_ret

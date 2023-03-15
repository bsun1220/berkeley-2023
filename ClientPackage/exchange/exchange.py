import time


class Order:
    """ Data that needs to be sent from the exchange
    """

    def __init__(self, assetname, uid, is_bid, size, price, team_name, root=None,
                 timestamp=None, next_item=None, previous_item=None, password=None):
        # Data Values
        self.assetname = assetname
        self.uid = uid
        self.is_bid = is_bid
        self.price = price
        self.size = size
        self.team_name = team_name
        self.timestamp = timestamp if timestamp else time.time()
        self.password = password


class ViewRequest:
    def __init__(self, team_id, pswd) -> None:
        self.team_id = team_id
        self.pswd = pswd


class cancelOrder:
    def __init__(self, team_id, order_id: int, password=None) -> None:
        self.team_id = team_id
        self.order_id = order_id
        self.password = password


class sittingOrder:
    def __init__(self, team_id, password=None) -> None:
        self.team_id = team_id
        self.password = password

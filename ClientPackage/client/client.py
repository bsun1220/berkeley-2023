import socket
import pickle
from exchange.exchange import Order as OrderExchange
from exchange.exchange import ViewRequest
from exchange.exchange import cancelOrder
from exchange.exchange import sittingOrder

ASSETS = ['SUM10', '10MAX10', 'PRODT3', 'ETF' ]# TODO: is there a master list of assets? And if so, should they reside on the client side??

class Client:
    def __init__(self, team_id, HOST, PORT, pswd="dummy"):
        self.team_id = team_id
        self.sock_addr = (HOST, PORT)
        self.orders = []
        self.pswd = pswd
        self.cancelled_orders = []

    def send_order(self):
        order_string = input("Input order in the exact format, delineated by spaces: stock symbol, 'B' or 'S', quantity, price\nEx. \"AAPL S 5 90\"\n\n").upper()
        try:
            inputs = order_string.split()
            # TODO: uid is just set to 0, idk what uid is for here
            order = OrderExchange(inputs[0], 0, inputs[1]=='B', int(inputs[2]), float(inputs[3]), self.team_id, password=self.pswd)
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect(self.sock_addr)
                    sock.sendall(pickle.dumps(order))
                    received = sock.recv(4000)
                    print(pickle.loads(received))
                self.orders.append(order)
            except:
                print("Socket error")
        except:
            print("Invalid format")
        
    def change_order(self, order_id):
        pass

    def cancel_order(self):
        order_string = input("Input order in the exact format, delineated by spaces (no commas): order_id\nEx. \"4e430368-9e43-443b-90bf-9e844ee36c18\"\n\n")
        try:
            order = cancelOrder(self.team_id, order_string, password=self.pswd)
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect(self.sock_addr)
                    sock.sendall(pickle.dumps(order))
                    received = sock.recv(4000)
                    print(pickle.loads(received))
                self.cancelled_orders.append(order)
            except:
                print("Socket error")
        except:
            print("Invalid format")

    def view_portfolio(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                v = ViewRequest(self.team_id, self.pswd)
                sock.connect(self.sock_addr)
                sock.sendall(pickle.dumps(v))
                received = sock.recv(4000)
                print("PORTFOLIO\n")
                print(pickle.loads(received))
        except:
            print("Socket error")

    def view_sitting_order(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                order = sittingOrder(self.team_id, password=self.pswd)
                sock.connect(self.sock_addr)
                sock.sendall(pickle.dumps(order))
                received = sock.recv(4000)
                print("Sitting Orders\n")
                print(pickle.loads(received))
        except:
            print("Socket Error")

            
    def price_of(self):
        #check current bid/ask for something
        pass
            
    def is_valid(self, order):
        elems = order.split()
        return (len(elems) == 4) and (elems[0] in ASSETS) and (elems[1] == "B" or elems[1] == "S") \
            and (elems[2].isnumeric()) and (type(elems[3]) == int or type(elems[3]) == float)
    
import heapq
import sys


class Exchange:
    def __init__(self):
        self.stop_buys = []
        self.stop_sells = []
        self.buys = []
        self.sells = []
        self.triggered_stops = []
        self.time = 1

    def parse(self, line):
        line = line.split()
        incoming_order = [float(line[3]), self.time, False, int(line[2]), line[0]]

        if line[1] == "buy":
            incoming_order[2] = True
            incoming_order[0] *= -1

        if incoming_order[4] == "market":
            incoming_order[0] = -float("inf")

        self.time += 1

        if incoming_order[4] != "stop":
            self.match(incoming_order)
        else:
            self.insert(incoming_order)

    def insert(self, order):
        if order[4] == "market":
            return

        if order[2]:
            if order[4] == "stop":
                orderbook = self.stop_buys
            elif order[4] == "limit":
                orderbook = self.buys
        else:
            if order[4] == "stop":
                orderbook = self.stop_sells
            elif order[4] == "limit":
                orderbook = self.sells

        heapq.heappush(orderbook, tuple(order))

    def stop_trigger(self, min_ex, max_ex):
        # print(min_ex, max_ex)
        while len(self.stop_buys) > 0 and max_ex >= -self.stop_buys[0][0]:
            order = list(heapq.heappop(self.stop_buys))
            order[0] = order[1]
            heapq.heappush(self.triggered_stops, tuple(order))

        while len(self.stop_sells) > 0 and min_ex <= self.stop_sells[0][0]:
            order = list(heapq.heappop(self.stop_sells))
            order[0] = order[1]
            heapq.heappush(self.triggered_stops, tuple(order))

        while len(self.triggered_stops) > 0:
            order = list(heapq.heappop(self.triggered_stops))
            order[0] = -float("inf")
            order[4] = "market"
            self.match(order)

    def match(self, order):
        # print(order)
        # print(self.buys, self.sells)
        min_ex = float("inf")
        max_ex = 0

        if order[2]:
            orderbook = self.sells
        else:
            orderbook = self.buys

        while len(orderbook) > 0 and orderbook[0][0] <= -order[0] and order[3] > 0:
            matched = heapq.heappop(orderbook)
            vol = min(matched[3], order[3])
            price = abs(matched[0])

            min_ex = min(min_ex, price)
            max_ex = max(max_ex, price)

            print(f"match {order[1]} {matched[1]} {vol} {price:.2f}")

            if matched[3] > vol:
                matched = list(matched)
                matched[3] -= vol
                self.insert(matched)
            order[3] -= vol

        if order[3] > 0:
            self.insert(order)

        self.stop_trigger(min_ex, max_ex)


def main():
    Ex = exchange()
    for line in sys.stdin:
        Ex.parse(line)


if __name__ == "__main__":
    main()




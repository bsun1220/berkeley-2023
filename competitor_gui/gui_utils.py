
import numpy as np
import matplotlib.pyplot as plt
import time
import math

data = {}
def parse_input(inp):
    inp_arr = inp.split("\n")
    for i in range(len(inp_arr)):
        inp_arr[i] = inp_arr[i].strip()
    rnd = int(inp_arr[0].split()[-1])
    
    teams = set([])
    team_name = None
    buy_position = None
    sell_position = None
    average_buy_price = None
    average_sell_price = None
    for i in range(1, len(inp_arr)):
        if "Team" in inp_arr[i]:
            colon = inp_arr[i].find(":")
            team_name = inp_arr[i][5:colon-1]
        if "buy_position" in inp_arr[i]:
            colon = inp_arr[i].find(":")
            buy_position = int(inp_arr[i][colon+2:])
        if "sell_position" in inp_arr[i]:
            colon = inp_arr[i].find(":")
            sell_position = int(inp_arr[i][colon+2:])
        if "average_buy_price" in inp_arr[i]:
            colon = inp_arr[i].find(":")
            average_buy_price = float(inp_arr[i][colon+2:])
        if "average_sell_price" in inp_arr[i]:
            colon = inp_arr[i].find(":")
            average_sell_price = float(inp_arr[i][colon+2:])
        if team_name not in data:
            data[team_name] = {}
        data[team_name][rnd] = {"buy_position": buy_position, "sell_position": sell_position, "average_buy_price": average_buy_price, "average_sell_price": average_sell_price}
    
def position_and_cash(ax_pos, ax_cash, inp, colors=['b', 'r', 'g', 'y']):
    parse_input(inp)
    for i in range(len(data)):
        team = list(data.keys())[i]
        color = colors[i]
        x = data[team].keys()
        y_pos = []
        y_cash = []
        for rnd in x:
            y_pos.append(data[team][rnd]["buy_position"] - data[team][rnd]["sell_position"])
            y_cash.append(data[team][rnd]["sell_position"] * data[team][rnd]["average_sell_price"] - data[team][rnd]["buy_position"] * data[team][rnd]["average_buy_price"])
        ax_pos.plot(x, y_pos, color, label=team, marker='o')
        ax_cash.plot(x, y_cash, color, label=team, marker='o')
    ax_pos.set_title("Team Positions")
    ax_pos.set_xlabel("Rounds")
    ax_pos.set_ylabel("Positions")
    ax_cash.set_title("Team Cash")
    ax_cash.set_xlabel("Rounds")
    ax_cash.set_ylabel("Cash")
    
    ax_pos.legend(list(data.keys()))
    ax_cash.legend(list(data.keys()))
    
    new_list = range(math.floor(min(x)), math.ceil(max(x))+1)
    ax_pos.set_xticks(new_list)
    ax_cash.set_xticks(new_list)
    
    # fig.canvas.draw()
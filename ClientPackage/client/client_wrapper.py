import sys
import os
sys.path.append(os.getcwd())
from client import Client
import re
import socket
import pickle
from login import LoginRequest, RegisterRequest



class ClientWrapper:
    def __init__(self, host, port):
        self.sock_addr = (host, port)

    def attempt_login(self, tid, pwd):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                login_req = LoginRequest(tid, pwd)
                sock.connect(self.sock_addr)
                sock.sendall(pickle.dumps(login_req))
                received = sock.recv(4000)
                return pickle.loads(received) == "Y"
        except:
            print("Socket error")
    
    def register_client(self, client, tid, pwd):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                reg_req = RegisterRequest(client, tid, pwd)
                sock.connect(self.sock_addr)
                sock.sendall(pickle.dumps(reg_req))
                received = sock.recv(4000)
                return pickle.loads(received)
        except:
            print("Socket error")



if __name__ == "__main__":
    ## Setup
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    wrapper = ClientWrapper(HOST, PORT)

    team_id = ""
    while not team_id:
        team_id = input("Enter your team ID: ")
        password = input("Enter your team password: ")
        active_client = Client(team_id, HOST, PORT, password)
        # logged_in = wrapper.attempt_login(team_id, password)
        # if logged_in:
        #     active_client = wrapper.register_client(team_id, password)
        # else:
        #     print("Incorrect team ID or password")
        #     team_id = ""
    
    ## Allow for sending commands
    while True:
        print("Type SEND for new order, CANCEL to cancel existing, PORT to see current portfolio, or EXIST to see sitting orders\n")
        cmd = input().upper()
        if cmd == "SEND": # send a new order
            active_client.send_order()
        elif cmd == "CANCEL": # cancel an existing order
            active_client.cancel_order()
        elif cmd == "PORT": # see portfolio and past orders
            active_client.view_portfolio()
        elif cmd == "EXIST":
            active_client.view_sitting_order()
        else:
            print("Invalid input. Input must be either SEND, EXIST, CANCEL, or PORT.")
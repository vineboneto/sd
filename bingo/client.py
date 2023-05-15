import grpc
import time
import threading
import signal
import numpy as np

import proto.bingo_pb2 as bingo_pb2
import proto.bingo_pb2_grpc as bingo_pb2_grpc

URL = "localhost:50051"


def authenticate(username):
    global auth
    channel = grpc.insecure_channel(URL)

    stub = bingo_pb2_grpc.BingoStub(channel)
    responses = stub.Login(bingo_pb2.LoginRequest(username=username))

    try:
        for response in responses:
            auth = {"username": username, "token": response.token}
            print(f"\nToken: {response.token}")
            print(f"Players loggedIn: {', '.join(list(response.playersLoggedIn))}")
            print(f"Players Ready: {', '.join(list(response.playersReady))}")
            print(f"message: {response.message}")
            print(f"status: {response.status}")
            print("\nwaiting for other players... press Ctrl+C to exit")
    except KeyboardInterrupt:
        print("Ctrl+C pressed...")
    finally:
        channel.close()


def ready():
    global auth

    with grpc.insecure_channel(URL) as channel:
        stub = bingo_pb2_grpc.BingoStub(channel)
        response = stub.Ready(bingo_pb2.ReadyRequest(username=auth["username"], token=auth["token"]))
    return response


if __name__ == "__main__":
    auth = {}

    try:
        execute = True
        card = np.array([])
        while execute:
            if auth.get("username"):
                print(f"\n{auth.get('username')} - {auth.get('token')}")
            if card.any():
                print(card)
            print("1. Login")
            print("2. Ready")
            print(":q. Exit")
            option = input("Enter option: ")
            if option == "1":
                username = input("Enter username: ")
                authenticate(username)
            elif option == "2":
                if not auth.get("token"):
                    print("You must login first")
                else:
                    response = ready()
                    card = np.reshape(list(response.card), (5, 5))
            elif option == ":q":
                execute = False
            else:
                print("Invalid option")
            # response = ready()
            # print(response)
    except KeyboardInterrupt:
        print("\nCtrl+C pressed...")

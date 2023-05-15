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
        response = stub.Ready(bingo_pb2.ReadyRequest(username=auth.get("username"), token=auth.get("token")))
    return response


def play():
    global auth

    channel = grpc.insecure_channel(URL)

    stub = bingo_pb2_grpc.BingoStub(channel)
    responses = stub.Play(bingo_pb2.PlayRequest(username=auth.get("username"), token=auth.get("token")))

    try:
        for response in responses:
            print(response)
            print("\nwaiting for new number... press Ctrl+C to exit")
    except KeyboardInterrupt:
        print("Ctrl+C pressed...")
    finally:
        channel.close()


def check_win():
    global auth

    with grpc.insecure_channel(URL) as channel:
        stub = bingo_pb2_grpc.BingoStub(channel)
        response = stub.CheckWin(bingo_pb2.WinCheckRequest(username=auth.get("username"), token=auth.get("token")))
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
            print("3. Play")
            print("4. Check Win")
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
            elif option == "3":
                if not auth.get("token"):
                    print("You must login first")
                else:
                    play()
            elif option == "4":
                if not auth.get("token"):
                    print("You must login first")
                else:
                    response = check_win()
                    print(response)
                    if response.status == 200:
                        card = np.array([])
            elif option == ":q":
                execute = False
            else:
                print("Invalid option")
    except KeyboardInterrupt:
        print("\nCtrl+C pressed...")

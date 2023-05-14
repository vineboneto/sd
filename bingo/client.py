import grpc
import time
import threading
import proto.bingo_pb2 as bingo_pb2
import proto.bingo_pb2_grpc as bingo_pb2_grpc

URL = "localhost:50051"

auth = {}

channel = grpc.insecure_channel(URL)


def listen_authenticate(responses):
    global auth

    for response in responses:
        auth = {"username": username, "token": response.token}


def authenticate(username):
    stub = bingo_pb2_grpc.BingoStub(channel)
    responses = stub.Login(bingo_pb2.LoginRequest(username=username))

    auth_thread = threading.Thread(target=listen_authenticate, args=(responses,))
    auth_thread.start()


def ready():
    global auth

    stub = bingo_pb2_grpc.BingoStub(channel)
    response = stub.Ready(bingo_pb2.ReadyRequest(username=auth["username"], token=auth["token"]))
    return response


if __name__ == "__main__":
    try:
        while True:
            username = input("Enter username: ")
            authenticate(username)
            # response = ready()
            # print(response)
    except KeyboardInterrupt:
        print("\nCtrl+C pressed... Closing channel.")
    finally:
        channel.close()

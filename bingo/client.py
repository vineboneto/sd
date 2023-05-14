import grpc
import bingo_pb2
import bingo_pb2_grpc

URL = "localhost:50051"

def authenticate(username):
    with grpc.insecure_channel(URL) as channel:
        stub = bingo_pb2_grpc.BingoStub(channel)
        responses = stub.Login(bingo_pb2.LoginRequest(username=username))
        for response in responses:
            print(response)


if __name__ == "__main__":
    while True:
        username = input("Enter username: ")

        response = authenticate(username)


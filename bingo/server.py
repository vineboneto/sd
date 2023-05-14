import grpc
import threading
import bingo_pb2
import bingo_pb2_grpc
from concurrent import futures
import queue
import uuid
import time

authenticated_users = {}
authenticated_users_queue = queue.Queue()

def listen_login_response(args):
    print("Iniciado thread")
    while True:
        username = authenticated_users_queue.get()
        if username in authenticated_users:
            token = authenticated_users[username]["token"]
            yield bingo_pb2.LoginResponse(
                token=token,
                playersLoggedIn=list(authenticated_users.keys()),
                playersReady=[],
                status=200,
                message="Logged in successfully",
            )
        time.sleep(1)

class BingoService(bingo_pb2_grpc.BingoServicer):
    def __init__(self) -> None:
        super().__init__()

    def Login(self, request, context):
        try:
            username = request.username
            if not username:
                yield bingo_pb2.LoginResponse(token="", playersLoggedIn=[], playersReady=[], status=400, message="Username cannot be empty")
            if not username in authenticated_users:
                token = uuid.uuid4().hex
                authenticated_users[username] = {"token": token, "authenticated": True, "ready": False}
                print(username)
                authenticated_users_queue.put(username)
            else:
                yield bingo_pb2.LoginResponse(token="", playersLoggedIn=[], playersReady=[], status=400, message="Username already exists")
        except Exception as e:
            yield bingo_pb2.LoginResponse(token="", playersLoggedIn=[], playersReady=[], status=500, message=str(e))
    
    def Ready(self, request, context):
        return super().Ready(request, context)
    def Play(self, request, context):
    
        return super().Play(request, context)
    
    def CheckWin(self, request, context):
        return super().CheckWin(request, context)



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=30))
    bingo_pb2_grpc.add_BingoServicer_to_server(BingoService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    try:

        login_thread = threading.Thread(target=listen_login_response, args=(1,))
        login_thread.start()
        serve()
    except Exception as e:
        print(e)

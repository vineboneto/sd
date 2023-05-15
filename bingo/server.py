import grpc
import uuid
import queue
import numpy as np
import concurrent.futures as futures

import proto.bingo_pb2 as bingo_pb2
import proto.bingo_pb2_grpc as bingo_pb2_grpc


class BingoService(bingo_pb2_grpc.BingoServicer):
    def __init__(self) -> None:
        super().__init__()
        self.active_streaming = True
        self.authenticated_users = {}

    def get_ready_players(self):
        read_players = [user for user, details in self.authenticated_users.items() if details["ready"]]
        return read_players

    def get_auth_players(self):
        return list(self.authenticated_users.keys())

    def notify_all(self, message):
        for _, client in self.authenticated_users.items():
            client["queue"].put(message)

    def notify(self, message, username):
        self.authenticated_users[username]["queue"].put(message)

    def queue_login(self, username):
        try:
            message = self.authenticated_users[username]["queue"].get(timeout=1)

            if message:
                yield bingo_pb2.LoginResponse(
                    token=self.authenticated_users[username]["token"],
                    playersLoggedIn=self.get_auth_players(),
                    playersReady=self.get_ready_players(),
                    status=200,
                    message=message,
                )
        except queue.Empty:
            pass

    def create_new_user(self, username):
        token = uuid.uuid4().hex
        self.authenticated_users[username] = {
            "token": token,
            "authenticated": True,
            "ready": False,
            "queue": queue.Queue(),
            "card": [],
        }

    def Login(self, request, context):
        try:
            username = request.username

            if not username:
                yield bingo_pb2.LoginResponse(
                    token="", playersLoggedIn=[], playersReady=[], status=400, message="Username cannot be empty"
                )
                return

            if not username in self.authenticated_users:
                self.create_new_user(username)

                self.notify_all(message=f"{username} has joined the game")

                while self.active_streaming:
                    for response in self.queue_login(username):
                        yield response
            else:
                self.notify(message="Already logged in", username=username)

                while self.active_streaming:
                    for response in self.queue_login(username):
                        yield response
        except Exception as e:
            yield bingo_pb2.LoginResponse(token="", playersLoggedIn=[], playersReady=[], status=500, message=str(e))

    def Ready(self, request, context):
        try:
            username = request.username
            token = request.token

            if username in self.authenticated_users.keys():
                current_user = self.authenticated_users[username]
                if current_user["ready"] == True:
                    return bingo_pb2.ReadyResponse(
                        card=current_user["card"],
                        status=200,
                        message="Ready successful",
                    )

                if current_user["token"] == token:
                    card = np.random.choice(100, size=25, replace=False)
                    card[12] = -1
                    self.authenticated_users[username]["ready"] = True
                    self.authenticated_users[username]["card"] = card
                    self.notify_all(message=f"{username} is ready")

                    return bingo_pb2.ReadyResponse(
                        card=current_user["card"],
                        status=200,
                        message="Ready successful",
                    )

            return bingo_pb2.ReadyResponse(
                card=[],
                status=400,
                message="Invalid username or token",
            )
        except Exception as e:
            print(str(e))
            return bingo_pb2.ReadyResponse(
                card=[],
                status=500,
                message=str(e),
            )

    def Play(self, request, context):
        return super().Play(request, context)

    def CheckWin(self, request, context):
        return super().CheckWin(request, context)


def serve():
    import signal
    import sys

    service = BingoService()

    s = grpc.server(futures.ThreadPoolExecutor(max_workers=30))
    bingo_pb2_grpc.add_BingoServicer_to_server(service, s)
    s.add_insecure_port("[::]:50051")
    s.start()

    def stop_server(sig, frame):
        print("Stopping server...")
        service.active_streaming = False
        s.stop(grace=0)

    signal.signal(signal.SIGINT, stop_server)

    try:
        print("Waiting connections at 50051")
        s.wait_for_termination()
    except KeyboardInterrupt:
        print("Ctrl+C pressed...")
        s.stop(0)


if __name__ == "__main__":
    serve()

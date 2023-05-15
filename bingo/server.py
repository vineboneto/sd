import grpc
import uuid
import time
import queue
import numpy as np
import threading
import concurrent.futures as futures

import proto.bingo_pb2 as bingo_pb2
import proto.bingo_pb2_grpc as bingo_pb2_grpc


class BingoService(bingo_pb2_grpc.BingoServicer):
    def __init__(self) -> None:
        super().__init__()
        self.is_streaming_game = True
        self.is_play_game = True
        self.authenticated_users = {}
        self.numbers_played = []
        self.is_number_generated = False
        self.interval_number = 15
        self.thread_number = threading.Thread(target=self.number_generation_thread)

    def get_ready_players(self):
        read_players = [user for user, details in self.authenticated_users.items() if details["ready"]]
        return read_players

    def get_auth_players(self):
        return list(self.authenticated_users.keys())

    def notify_all(self, message, queue):
        for _, client in self.authenticated_users.items():
            client[queue].put(message)

    def notify(self, message, username, queue: str):
        self.authenticated_users[username][queue].put(message)

    def generate_random_number(self):
        if len(self.numbers_played) == 100:
            self.is_number_generated = False
            return -1
        available_numbers = np.setdiff1d(np.arange(1, 100), self.numbers_played)
        random_number = np.random.choice(available_numbers)

        self.numbers_played.append(str(random_number))

        return random_number

    def queue_login(self, username):
        try:
            message = self.authenticated_users[username]["queue_login"].get(timeout=1)

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

    def check_users_ready(self):
        for user in self.authenticated_users.values():
            if not user["ready"]:
                return False
        return True

    def get_not_found_number(self, username):
        card = self.authenticated_users[username]["card"]

        played_numbers = np.array(self.numbers_played)
        card_without_minus_one = card[card != -1]

        missing_numbers = np.setdiff1d(card_without_minus_one, played_numbers)
        missing_numbers = missing_numbers.astype(str).tolist()

        return missing_numbers

    def is_auth(self, username, token):
        return username in self.authenticated_users.keys() and self.authenticated_users[username]["token"] == token

    def number_generation_thread(self):
        self.is_number_generated = True
        while self.is_number_generated:
            random_number = self.generate_random_number()

            print(f"Number generated: {random_number}")

            self.notify_all(message=("", random_number), queue="queue_play")

            time.sleep(self.interval_number)

    def create_new_user(self, username):
        token = uuid.uuid4().hex
        self.authenticated_users[username] = {
            "token": token,
            "authenticated": True,
            "ready": False,
            "queue_login": queue.Queue(),
            "queue_play": queue.Queue(),
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

                self.notify_all(message=f"{username} has joined the game", queue="queue_login")

                while self.is_streaming_game:
                    for response in self.queue_login(username):
                        yield response
            else:
                self.notify(message="Already logged in", username=username, queue="queue_login")

                while self.is_streaming_game:
                    for response in self.queue_login(username):
                        yield response
        except Exception as e:
            yield bingo_pb2.LoginResponse(token="", playersLoggedIn=[], playersReady=[], status=500, message=str(e))

    def Ready(self, request, context):
        try:
            username = request.username
            token = request.token

            if self.is_auth(username, token):
                current_user = self.authenticated_users[username]
                if current_user["ready"] == True:
                    return bingo_pb2.ReadyResponse(
                        card=current_user["card"],
                        status=200,
                        message="Ready successful",
                    )

                card = np.random.choice(100, size=25, replace=False)
                card[12] = -1
                self.authenticated_users[username]["ready"] = True
                self.authenticated_users[username]["card"] = card
                self.notify_all(message=f"{username} is ready", queue="queue_login")

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
            return bingo_pb2.ReadyResponse(
                card=[],
                status=500,
                message=str(e),
            )

    def Play(self, request, context):
        username = request.username
        token = request.token

        try:
            if not self.check_users_ready():
                yield bingo_pb2.GameStatusResponse(
                    number=-1,
                    winner="",
                    status=400,
                    message="Not all users are ready",
                )
                return

            if self.is_auth(username, token):
                if not self.is_number_generated:
                    self.thread_number.start()

                current_user = self.authenticated_users[username]
                while self.is_streaming_game and self.is_play_game:
                    try:
                        winner, random_number = self.authenticated_users[username]["queue_play"].get(timeout=1)

                        if winner:
                            self.is_play_game = False
                            self.is_number_generated = False
                            self.numbers_played = []
                            for user in self.authenticated_users.values():
                                user["ready"] = False
                                user["card"] = []
                            self.thread_number.join()
                            yield bingo_pb2.GameStatusResponse(
                                number=-1,
                                winner=winner,
                                status=200,
                                message=f"the game is over, {winner} won",
                            )
                        elif random_number:
                            yield bingo_pb2.GameStatusResponse(
                                number=random_number,
                                winner="Unknown",
                                status=200,
                                message=f"Numbers played: {', '.join(list(self.numbers_played))}",
                            )

                    except queue.Empty:
                        pass
            else:
                yield bingo_pb2.GameStatusResponse(
                    number=-1,
                    winner="",
                    status=400,
                    message="Invalid username or token",
                )
        except Exception as e:
            yield bingo_pb2.GameStatusResponse(
                number=-1,
                winner="",
                status=500,
                message=str(e),
            )
        finally:
            self.is_play_game = True

    def CheckWin(self, request, context):
        username = request.username
        token = request.token

        try:
            if self.is_auth(username, token):
                not_found_number = self.get_not_found_number(username)

                if not_found_number:
                    return bingo_pb2.WinCheckResponse(
                        status=200,
                        message=f"Not found: {', '.join(not_found_number)}",
                    )
                else:
                    self.notify_all(message=(username, None), queue="queue_play")
                    return bingo_pb2.WinCheckResponse(
                        status=200,
                        message=f"Congratulations {username}! You won!",
                    )

            else:
                return bingo_pb2.WinCheckResponse(
                    status=400,
                    message="Invalid username or token",
                )

        except Exception as e:
            return bingo_pb2.WinCheckResponse(
                status=500,
                message=str(e),
            )


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
        service.is_streaming_game = False
        service.is_play_game = False
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

from concurrent import futures
import grpc
import proto.sync_pb2 as sync_pb2
import proto.sync_pb2_grpc as sync_pb2_grpc
import time
import threading
from random import randint

time_difference = [0, 0, 0, 0]


def run(client_id):
    time.sleep(randint(1, 5))  # Simular um atraso
    channel = grpc.insecure_channel("localhost:50051")
    stub = sync_pb2_grpc.TimeSyncStub(channel)

    while True:
        print(client_id)
        response = stub.SendTime(
            sync_pb2.TimeRequest(client_id=client_id, client_time=time.time() + time_difference[client_id])
        )
        time_difference[client_id] = response.average_difference
        print(time_difference)
        time.sleep(5)


for i in range(4):
    client_thread = threading.Thread(target=run, args=(i,))
    client_thread.start()

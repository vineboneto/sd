from concurrent import futures
import grpc
import proto.sync_pb2 as sync_pb2
import proto.sync_pb2_grpc as sync_pb2_grpc
import time


class TimeSyncServicer(sync_pb2_grpc.TimeSyncServicer):
    def __init__(self):
        self.time_difference = [0.0, 0.0, 0.0, 0.0]

    def SendTime(self, request, context):
        client_time = request.client_time
        server_time = time.time()
        difference = server_time - client_time
        self.time_difference[request.client_id] = difference
        average_difference = sum(self.time_difference) / len(self.time_difference)
        print(self.time_difference)
        return sync_pb2.TimeReply(average_difference=average_difference)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sync_pb2_grpc.add_TimeSyncServicer_to_server(TimeSyncServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    print("server started at port 50051")
    serve()

import grpc
from concurrent import futures
import auth_service_pb2
import auth_service_pb2_grpc


class AuthService(auth_service_pb2_grpc.AuthServiceServicer):
    def Authenticate(self, request, context):
        username = request.username
        password = request.password

        if username == "user" and password == "pass":
            return auth_service_pb2.AuthResponse(success=True, message="Autenticação bem-sucedida.")
        else:
            return auth_service_pb2.AuthResponse(success=False, message="Credenciais inválidas.")

    def Quiz(self, request, context):
        # Pode ser modificado para verificar o token de autenticação, se necessário
        
        if request.token == "dummy_token":
            correct_answers = [2, 0, 1]
            user_answers = request.answers
            score = sum([1 if user_answers[i] == correct_answers[i] else 0 for i in range(len(user_answers))])

            questions = [
                "Qual é a capital do Brasil?",
                "Qual é a moeda oficial do Japão?",
                "Em que continente fica a Austrália?",
            ]
            options = [
                "A) Rio de Janeiro; B) São Paulo; C) Brasília",
                "A) Iene; B) Euro; C) Dólar",
                "A) Oceania; B) Ásia; C) Europa",
            ]

            return auth_service_pb2.QuizResponse(questions=questions, options=options, correct_answers=score)
        else:
            return auth_service_pb2.QuizResponse(questions=[], options=[], correct_answers=0)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_service_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
    
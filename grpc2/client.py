import grpc
import auth_service_pb2
import auth_service_pb2_grpc


def authenticate(username, password):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = auth_service_pb2_grpc.AuthServiceStub(channel)
        response = stub.Authenticate(auth_service_pb2.AuthRequest(username=username, password=password))
    return response


def request_quiz(answers):
    # O token pode ser substituído por um token de autenticação gerado após a autenticação bem-sucedida
    token = "dummy_token"
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = auth_service_pb2_grpc.AuthServiceStub(channel)
        response = stub.Quiz(auth_service_pb2.QuizRequest(token=token, answers=answers))
    return response


def display_question(question, options, index):
    print(f"\nPergunta {index + 1}: {question}")
    print(options)
    answer = int(input("Escolha a opção correta (0, 1 ou 2): "))
    return answer


if __name__ == "__main__":
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha: ")

    result = authenticate(username, password)

    if result.success:
        print("Autenticação bem-sucedida.")
        answers = []

        quiz_response = request_quiz(answers)
        questions = quiz_response.questions
        options_list = quiz_response.options

        for index, (question, options) in enumerate(zip(questions, options_list)):
            user_answer = display_question(question, options, index)
            answers.append(user_answer)

        quiz_result = request_quiz(answers)

        print(f"\nVocê acertou {quiz_result.correct_answers} de {len(questions)} perguntas.")
    else:
        print("Erro na autenticação: ", result.message)

package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net"
	"strings"
)

type SocketMessage struct {
	Channel string `json:"channel"`
	Message any    `json:"message"`
}

var questions = []string{
	"1. Qual é o principal objetivo da linguagem Assembly?\n" +
		"a) Criar aplicativos Web\n" +
		"b) Criar jogos para consoles de videogame\n" +
		"c) Criar aplicativos para desktops\n" +
		"d) Controlar a arquitetura do computador e os dispositivos de hardware.\n",

	"2. Qual das seguintes opções é uma linguagem de programação orientada a objetos?\n" +
		"a) C\n" +
		"b) Python\n" +
		"c) Assembly\n" +
		"d) HTML\n",

	"3. Qual é a principal diferença entre uma pilha (stack) e uma fila (queue)?\n" +
		"a) Uma pilha é uma estrutura de dados baseada em LIFO, enquanto uma fila é baseada em FIFO.\n" +
		"b) Uma pilha é uma estrutura de dados baseada em FIFO, enquanto uma fila é baseada em LIFO.\n" +
		"c) Uma pilha é usada para armazenar objetos com acesso rápido em suas extremidades, enquanto uma fila é usada para armazenar objetos com acesso rápido no meio.\n" +
		"d) Não há diferença entre uma pilha e uma fila.\n",
}

var answers = []string{"d", "b", "a"}

var students = []map[string]any{{
	"name":          "João",
	"senha":         "123",
	"isAuth":        false,
	"questao-atual": 0,
	"acertos":       0,
}}

func decodeMessage(buffer []byte) SocketMessage {
	message := string(buffer)

	message = strings.Trim(message, "\x00")

	socketMessage := SocketMessage{}

	json.Unmarshal([]byte(message), &socketMessage)

	return socketMessage
}

func encodeMessage(channel string, message any) []byte {

	socketMessage := &SocketMessage{
		Channel: channel,
		Message: message,
	}

	jsonMessage, err := json.Marshal(socketMessage)

	if err != nil {
		fmt.Println(err)
	}

	return jsonMessage
}

func emit(conn net.Conn, response []byte) {
	_, err := conn.Write(response)
	if err != nil {
		fmt.Printf("Error writing data: %v\n", err)
	}
}

func onNewConnection(conn net.Conn) {
	defer conn.Close()

	for {
		buf := make([]byte, 1024)
		_, err := conn.Read(buf)

		if err != nil {
			fmt.Printf("Error reading data: %v\n", err)
			break
		}

		message := decodeMessage(buf)

		if message.Channel == "ping" {
			log.Println("Ping received")
			emit(conn, encodeMessage("auth", false))
		}

		if message.Channel == "question-next" {
			fmt.Println("Questão...")
			message := message.Message.(map[string]any)

			name := message["name"].(string)

			for i, student := range students {

				if student["name"] == name && student["isAuth"] == true {
					questaoAtual := student["questao-atual"].(int)
					finish := questaoAtual == len(questions)

					if !finish {
						response := map[string]any{
							"questao":   questions[questaoAtual],
							"questaoId": questaoAtual,
						}
						emit(conn, encodeMessage("question", response))
						students[i]["questao-atual"] = questaoAtual + 1
					} else {
						response := map[string]any{
							"acertos":        student["acertos"],
							"total questões": len(questions),
						}
						emit(conn, encodeMessage("question-finish", response))
						break
					}
					break
				}
			}
		}

		if message.Channel == "answer-question" {
			fmt.Println("Resposta...")
			message := message.Message.(map[string]any)

			name := message["name"].(string)
			question := int(message["question"].(float64))
			answer := message["answer"].(string)

			for i, student := range students {
				if student["name"] == name && student["isAuth"] == true {
					if answers[question] == answer {
						emit(conn, encodeMessage("answer", "true"))
						students[i]["acertos"] = student["acertos"].(int) + 1
					} else {
						emit(conn, encodeMessage("answer", "false"))
					}
					break
				}
			}
		}

		if message.Channel == "auth" {
			fmt.Println("Login...")
			message := message.Message.(map[string]any)
			name := message["name"].(string)
			pass := message["pass"].(string)

			isAuth := false

			for i, student := range students {

				if student["name"] == name && student["senha"] == pass {
					students[i]["isAuth"] = true
					isAuth = true
					if err != nil {
						fmt.Printf("Error writing data: %v\n", err)
						break
					}
					break
				}
			}

			if isAuth {
				emit(conn, encodeMessage("auth", true))
			} else {
				emit(conn, encodeMessage("auth", false))

			}
		}
	}
}

func main() {
	listener, err := net.Listen("tcp", ":5000")
	if err != nil {
		fmt.Printf("Error listening on port 5000: %v\n", err)
		return
	}
	defer listener.Close()

	fmt.Println("Server is listening on port 5000...")

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Printf("Error accepting connection: %v\n", err)
			continue
		}

		go onNewConnection(conn)
	}
}

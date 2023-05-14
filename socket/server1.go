package main

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net"
	"strings"
)

type SocketMessage struct {
	Channel string `json:"channel"`
	Message any    `json:"message"`
}

func decodeMessage(buffer []byte) SocketMessage {
	message := string(buffer)

	message = strings.Trim(message, "\x00")

	socketMessage := SocketMessage{}

	json.Unmarshal([]byte(message), &socketMessage)

	return socketMessage
}

func encodeMessage(channel, message string) []byte {

	socketMessage := SocketMessage{
		Channel: channel,
		Message: message,
	}

	jsonMessage, err := json.Marshal(socketMessage)

	if err != nil {
		fmt.Println(err)
	}

	return jsonMessage
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
			response := encodeMessage("pong", "pong")
			_, err = conn.Write(response)
			if err != nil {
				fmt.Printf("Error writing data: %v\n", err)
				break
			}
		}

		if message.Channel == "arquivo-transfer" {
			fmt.Println("Recebendo arquivo...")
			message := message.Message.(map[string]any)
			content, err := base64.StdEncoding.DecodeString(message["base64"].(string))

			if err != nil {
				panic(err)
			}

			filename := message["name"].(string)

			if err != nil {
				panic(err)
			}

			err = ioutil.WriteFile("/tmp/socket/"+filename, content, 0644)

			if err != nil {
				panic(err)
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

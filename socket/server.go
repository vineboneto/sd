package main

import (
	"fmt"
	"net"
	"strings"
)

func onNewConnection(conn net.Conn) {
	defer conn.Close()

	for {
		buf := make([]byte, 1024)
		_, err := conn.Read(buf)

		if err != nil {
			fmt.Printf("Error reading data: %v\n", err)
			break
		}

		message := string(buf)

		message = strings.Trim(message, " \t\n\r\x00")

		if message == "ping" {
			response := "pong"
			_, err = conn.Write([]byte(response))
			if err != nil {
				fmt.Printf("Error writing data: %v\n", err)
				break
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

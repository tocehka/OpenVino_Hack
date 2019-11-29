package main

import (
	"fmt"
	"log"
	"net/http"

	socket "github.com/gorilla/websocket"
)

var upgrader = socket.Upgrader{}

func audioSocConn(w http.ResponseWriter, r *http.Request) {
	ws, err := upgrader.Upgrade(w, r, nil)
	defer ws.Close()
	if err != nil {
		log.Println(err)
	}
	reader(ws)
}

func reader(conn *socket.Conn) {
	for {
		// read in a message
		messageType, p, err := conn.ReadMessage()
		if err != nil {
			log.Println(err)
			return
		}

		fmt.Println(messageType)
		fmt.Println(len(p))

	}
}

func dataSocConn(w http.ResponseWriter, r *http.Request) {
	ws, err := upgrader.Upgrade(w, r, nil)
	defer ws.Close()
	if err != nil {
		log.Println(err)
	}
	dataReader(ws)
}

func dataReader(conn *socket.Conn) {
	for {
		// read in a message
		messageType, p, err := conn.ReadMessage()
		if err != nil {
			log.Println(err)
			return
		}

		fmt.Println(messageType)
		fmt.Println(string(p))

	}
}

func main() {
	fmt.Println("Server started...")
	http.HandleFunc("/audio", audioSocConn)
	http.HandleFunc("/data", dataSocConn)
	log.Fatal(http.ListenAndServe(":8081", nil))
}

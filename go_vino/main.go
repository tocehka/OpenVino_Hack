package main

import (
	"log"
	"net/http"
)

func main() {
	hub := newHub()
	go hub.run()
	http.HandleFunc("/audio", func(w http.ResponseWriter, r *http.Request) {
		serveWs(hub, w, r)
	})
	err := http.ListenAndServe(":8081", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}

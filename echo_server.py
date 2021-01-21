#!/usr/bin/env python3
import socket
from multiprocessing import Process

#Global vars
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

# Use to test echo "abcd" | nc localhost 8001 -q 1

def handle_request_echo(addr, conn):
    print("Connected by", addr)
    #Recieve data
    full_data = conn.recv(BUFFER_SIZE)
    #Send the data back
    conn.sendall(full_data)
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Starting multi echo server #Q8 Mod")
        #QUESTION 3 - Reuse same bind port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #Bind socket to address
        s.bind((HOST, PORT))

        #Start listening at the specified port
        s.listen(2)
        
        #Continue to listen for connections from client
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            # Proxy server fork so multiple programs can use
            # Referenced: https://stackoverflow.com/questions/24041935/difference-in-behavior-between-os-fork-and-multiprocessing-process
            # How to use Process 
            # Part #8 of lab
            p = Process(target=handle_request_echo, args=(addr, conn))
            p.daemon = True
            p.start()
            print("Child process started", p)
            
            
            
            

if __name__ == "__main__":
    main()


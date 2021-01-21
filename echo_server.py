#!/usr/bin/env python3
import socket
import time

#Global vars
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

# Use to test echo "abcd" | nc localhost 8001 -q 1

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
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
            
            #Recieve data
            full_data = conn.recv(BUFFER_SIZE)
            #Wait a bit 
            time.sleep(0.5)
            #Send the data back
            conn.sendall(full_data)
            conn.close()

if __name__ == "__main__":
    main()


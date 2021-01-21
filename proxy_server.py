#!/usr/bin/env python3
import socket, sys
from multiprocessing import Process

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Host name could not be resolved. Exiting.')
        sys.exit()

    print (f'IP address of {host} is {remote_ip}')
    return remote_ip


# For child processes when forking.
# Forward whatever is recv to www.google.com
# Send back recv to client that is connected
def handle_proxy_server(addr, conn, proxy_end):
    # Send data to google
    print("Connected by", addr)
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending received data {send_full_data} to google")
    conn.sendall(send_full_data)
    conn.shutdown(socket.SHUT_RDWR)

    #Send data back to client
    data = proxy_end.recv(BUFFER_SIZE)
    print(f"Sending received data {data} to client")
    conn.send(data)
    conn.close()

def main():
    #Connect to google.
    host = 'www.google.com'
    port = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Starting multi proxy server #Q8 Mod")
        # Listen locally at port
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(2)

        #continuously listen for connections
        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                # Connect proxy to google
                print("Connecting to Google")
                remote_ip = get_remote_ip(host)
                proxy_end.connect((remote_ip, port))

                # Proxy server fork so multiple programs can use
                # Referenced: https://stackoverflow.com/questions/24041935/difference-in-behavior-between-os-fork-and-multiprocessing-process
                # How to use Process 
                # Part #8 of lab
                p = Process(target=handle_proxy_server, args=(addr, conn, proxy_end))
                p.daemon = True
                p.start()
                print("Child process started", p)
            conn.close()

if __name__ == "__main__":
    main()
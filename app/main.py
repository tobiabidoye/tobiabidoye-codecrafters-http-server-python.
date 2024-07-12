import socket

MAXBYTES = 1024
def handle_connection(conn):
    conn.recv(MAXBYTES) #specifying max amount of bytes
    response = "HTTP/1.1 200 OK\r\n\r\n"
    conn.send(response.encode()) #.encode converts string into bytes



def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.accept() # wait for client
    # .accept() is a method that waits for clients
    while True:
        # while loop which waits for a connection
        print("Waiting for a connection...")
        conn, addr = server_socket.accept() #this gives us the client details
        print(f"connection from: {addr} has been established")
        handle_connection(conn)
        conn.close()





if __name__ == "__main__":
    main()

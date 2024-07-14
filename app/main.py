import socket

MAXBYTES = 1024
def handle_connection(conn):
    data = conn.recv(MAXBYTES)  # specifying max amount of bytes

    response = "HTTP/1.1 200 OK\r\n\r\n"
    if "http://localhost:4221" not in data:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"

    conn.send(response.encode())  # .encode converts string into bytes
    conn.close()


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    print("Server is listening for connections...")
    while True:
        # while loop which waits for a connection
        print("Waiting for a connection...")
        conn, addr = server_socket.accept()  # this gives us the client details
        print(f"connection from:{addr} has been established")
        handle_connection(conn)






if __name__ == "__main__":
    main()

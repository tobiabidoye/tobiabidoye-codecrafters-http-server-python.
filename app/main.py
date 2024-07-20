import socket

MAXBYTES = 1024
def handle_connection(conn):
    data = conn.recv(MAXBYTES)  # specifying max amount of bytes

    request_line, headers = data.decode().split("\r\n", 1)  # decoding data as it comes in bytes
    method, path, http_version = request_line.split()
    headers_list = headers.split("\r\n")
    response = "HTTP/1.1 200 OK\r\n\r\n"
    if "echo" in path:
        toSend = path[6:]
        contentType = "text/plain\r\n"
        contentLen = len(toSend)
        response = response + contentType + str(toSend) + contentLen + "\r\n"
    else:
        if path is not "/":
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

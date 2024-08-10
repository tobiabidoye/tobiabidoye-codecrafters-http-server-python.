import socket
import threading
import argparse
import os

MAXBYTES = 1024


def handle_connection(conn):
    data = conn.recv(MAXBYTES)  # specifying max amount of bytes

    request_line, headers = data.decode().split("\r\n", 1)  # decoding data as it comes in bytes
    method, path, http_version = request_line.split()
    headers_list = headers.split("\r\n")
    response = "HTTP/1.1 200 OK\r\n\r\n"

    if "echo" in path:

        response = "HTTP/1.1 200 OK\r\n"
        toSend = path[6:]
        contentType = "Content-Type: text/plain\r\n"
        contentLen = len(toSend)
        response = response + contentType + "Content-Length: " + str(contentLen) + "\r\n\r\n" + toSend

    elif "user-agent" in path:

        response = "HTTP/1.1 200 OK\r\n"
        agent, agentname = headers_list[1].split()
        contentType = "Content-Type: text/plain\r\n"
        contentLen = len(agentname)
        response = response + contentType + "Content-Length: " + str(contentLen) + "\r\n\r\n" + agentname

    elif path.startswith("/files"):

        filename = path[7:] #this is where filename is contained
        filepath = os.path.join(dirpath, filename)
        if os.path.exists(filepath) and os.path.isfile(filepath):
            
            with open(filepath, 'rb') as file: 
                #open file in binary mode and read it
                content = file.read()
            
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: application/octet-stream\r\n"
            response += f"Content-Length: {len(content)}\r\n\r\n"
            conn.send(response.encode() + content)
            
        else: 
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            conn.send(response.encode())
        return

    else:

        if path != "/":

            response = "HTTP/1.1 404 Not Found\r\n\r\n"

    conn.send(response.encode())  # .encode converts string into bytes
    conn.close()


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    parser = argparse.ArgumentParser() #parser initialization
    parser.add_argument('--directory',required= True, help= 'parsing command line argument for directory flag') #parsing for directory flag
    args = parser.parse_args()
    global dirpath
    dirpath = args.directory
    
    print("Server is listening for connections...")
    while True:
        # while loop which waits for a connection
        print("Waiting for a connection...")
        conn, addr = server_socket.accept()  # this gives us the client details
        print(f"connection from:{addr} has been established")
        thread = threading.Thread(target=handle_connection, args=(conn,))  # to support multithreading
        thread.start()






if __name__ == "__main__":
    main()

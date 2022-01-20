import socket 
from multiprocessing import Process

HOST = ''
PORT = 8001
BUFFER_SIZE = 1024

def handle_echo(conn, addr):
    '''
        Echo connections back to the client 

    '''
    print('Connected by:', addr)

    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_WR)
    conn.close()


def main():
    # Create socket, bind and start listening for connections 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.bind((HOST, PORT))
        s.listen(2)

        while True:
            # Accept connections and start a Process daemon to handle multiple connections 
            conn, addr = s.accept()
            p = Process(target=handle_echo, args=(conn, addr))
            p.daemon = True 
            p.start()
            print('Started process',  p)


main()
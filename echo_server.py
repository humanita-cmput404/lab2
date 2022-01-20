import socket, time

from example_code.echo_server import BUFFER_SIZE

HOST = ''
PORT = 8001
BUFFER_SIZE = 1024

def main():
        
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            #recieve data, wait a bit, then send it back
            full_data = conn.recv(BUFFER_SIZE)
            print('Fulldata:', full_data)
            time.sleep(0.5)
            conn.sendall(full_data)
            conn.close()


    return

main()
import socket, sys
from multiprocessing import Process

HOST = ''
PORT = 8001 
BUFFER_SIZE = 1024

def get_remote_ip(host):
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting program.')
        sys.exit()
    
    print(f'IP of {host}: {ip}')
    return ip


def handle_send_process_data(conn, addr, proxy_end):
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f'Sending received data {send_full_data} to google')
    proxy_end.sendall(send_full_data)

    proxy_end.shutdown(socket.SHUT_WR)

    # get data from google and send back to client 
    data = proxy_end.recv(BUFFER_SIZE)
    print(f'Sending data {data} from google back to client')
    conn.send(data)
    


def main():
    host = 'www.google.com'
    port = 80 
    
    # Create socket, bind and start listening for connections 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        proxy_start.bind((HOST, PORT))
        proxy_start.listen(2)

        while True:
            # Accept connections and start a Process daemon to handle multiple connections 
            conn, addr = proxy_start.accept()
            print('Connected by:', addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                remote_ip = get_remote_ip(host)

                proxy_end.connect((remote_ip,  port))
                print(f'Connected to {host}')
                

                p = Process(target=handle_send_process_data, args=(conn, addr, proxy_end))
                p.daemon = True 
                p.start()
                print('Started process',  p)

            conn.close()

main()
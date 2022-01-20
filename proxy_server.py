import socket, time, sys


def get_remote_ip(host):
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting program.')
        sys.exit()
    
    print(f'IP of {host}: {ip}')
    return ip

def main():
    host = 'www.google.com'
    port = 54236
    buffer_size = 1024

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print('Starting proxy server')
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        proxy_start.bind(('', port))
        #set to listening mode
        proxy_start.listen(2)
        
        #continuously listen for connections
        while True:
            print("Waiting to accept...")
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            # create another proxy server that acts as the client
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                ip = get_remote_ip(host)

                proxy_end.connect((ip, 80)) #FIXME
                print('Connected')
                # send_full data is already a byte string
                send_full_data = conn.recv(buffer_size)
                print(f'Sending received data {send_full_data} to google')
                proxy_end.sendall(send_full_data)

                proxy_end.shutdown(socket.SHUT_WR)

                # get data from google and send back to client 
                data = proxy_end.recv(buffer_size)
                print(f'Sending data {data} from google back to client')
                conn.send(data)
            
            conn.close()

    return 

main()
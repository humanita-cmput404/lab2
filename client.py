import socket, sys

def create_socket():

    # AF_INET is an address family that accepts (host, port)
    # where host is an IP address and port is an integer 
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as e:
        print('[ERROR] Creating Socket:', e)
        sys.exit()
    return s

def get_ip(host):

    try:
        ip = socket.gethostbyname(host)
    except Exception as e:
        print('[ERROR] Getting IP:', e)
        sys.exit()

    return ip


def main():

    try:
        HOST = 'www.google.com'
        PORT = 8000

        # Make the socket 
        s = create_socket()
        # Get the IP address to form the (HOST, PORT) connection
        ip = get_ip(HOST)
        print(f'IP of {HOST}: {ip}')
        
        # Connect the ip address to the port 
        s.connect((ip, PORT))
        print(f'Connected to {HOST} on {ip}')

        # Send the data 
        payload = f'GET / HTTP/1.0\r\nHost: {HOST}\r\n\r\n'
        s.sendall(payload.encode()) # convert to a bytes-like object
        s.shutdown(socket.SHUT_WR)
        print('Sent payload and shutdown the connection')

        received_data = b'' # byte literals
        buffer_size = 4096 # specified in the docs, a relatively small power of 2
        while True:
            data = s.recv(buffer_size)
            if not data:
                break
            received_data += data
        print(received_data)

    except Exception as e:
        print(f'[ERROR]:', e)

    finally:
        s.close()

    
    

main()
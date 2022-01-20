import socket 

def main():
    host = 'localhost'
    port = 8001
    buffer_size = 1024 

    payload = f'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'

    try:
        # create a socket 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', port))
        s.sendall(payload.encode())
        print('Sent payload to server')
        s.shutdown(socket.SHUT_WR)

        full_data = s.recv(buffer_size)
        print(full_data)
    
    except Exception as e:
        print(f'[ERROR]:', e)
    
    finally:
        s.close()


main()
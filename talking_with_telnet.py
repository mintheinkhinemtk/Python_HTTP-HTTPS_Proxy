import socket

HOST = '0.0.0.0'

port = 1246

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Socket successfully created')
    s.bind((HOST,port)) # binding IP Address and port for the server
    s.listen() # listening with OS default backlog queued number specified
    conn,addr = s.accept()  # socket.accept returns a new connection object and the address
    with conn:
        print(f'Connected by {addr}')
        buffer = ''
        while True:
            data = conn.recv(4096).decode('utf-8',errors='replace')
            if not data:
                break # breaking from the loop
            buffer += data
            while data and not data.endswith('\n'):
                if not data:
                    break
                data = conn.recv(4096).decode('utf-8',errors='replace')
                buffer += data
            conn.send(buffer.encode('utf-8'))
            print(buffer.rstrip('\r\n'))
            buffer = ''
        s.close()


except socket.error as error:
    print(f'Socket creation failed with error {error}')


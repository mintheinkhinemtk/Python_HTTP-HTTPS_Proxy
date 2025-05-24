import socket, sys, threading, ipaddress

def valid_ip_format(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
    except KeyboardInterrupt:
        print('User requested an interrupt')
        print('Application existing....')
        sys.exit()

def relay(source, destination):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                print('No more data received. Closing relay')
                break
            print(f'Forwarding {len(data)} bytes of data')
            destination.sendall(data)
    except socket.timeout:
        print('Relay timed out waiting for data ')

    except Exception as e:
        print(f" No Data Forwarded, {e}")



def forward_https(hostname,target_port,conn):
    try:
        https_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        https_server.settimeout(
            15)  # setting timeout for avoiding the proxy hanging forever when trying to connect to a website that doesn't respond
        https_server.connect((hostname, target_port))
        conn.sendall(b'HTTP/1.1 200 Connection Established\r\n\r\n')  # forward the requests to the desired hostname
        t1 = threading.Thread(target=relay, args=(conn, https_server), daemon=True)
        t2 = threading.Thread(target=relay, args=(https_server, conn), daemon=True)
        t1.start()
        t2.start()
        # Wait for both threads to finish before exiting main thread
        t1.join()
        t2.join()
        https_server.close()
        conn.close()

    except socket.error as error:
        print(f'Connection to the desired domain failed with error {error}')
        conn.close()
        sys.exit()


def forward_data_http(hostname,target_port,conn,req_data):
    try:
        s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_server.settimeout(
            15)  # setting timeout for avoiding the proxy hanging forever when trying to connect to a website that doesn't respond
        s_server.connect((hostname, target_port))
        s_server.sendall(req_data)  # forward the requests to the desired hostname
        while True:
            resp_data = s_server.recv(4096)
            if not resp_data:
                break
            conn.sendall(resp_data)
        s_server.close()
        conn.close()
    except socket.error as error:
        print(f'Connection to the desired domain failed with error {error}')
        conn.close()
        sys.exit()


def connect_(conn,addr,req_data):
    try:
        print(f'Connected by {addr}')
        req_data_str = req_data.decode('utf-8',
                                       errors='replace')  # replacing bytes that aren't string with the desired ones
        first_line = req_data_str.split('\r\n')[0] #url parsing
        method = first_line.split(' ')[0]
        url = first_line.split(' ')[1]
        print("URL = " + url)
        http_pos = url.find("://")  # find protocol format position
        if http_pos == -1:  # if '://' is not contained in the request
            tmp_url = url  # authority and path
        else:
            tmp_url = url[http_pos + 3:]  # authority+path

        # find port number position
        port_pos = tmp_url.find(":")

        # find the endpoint of the domain in url
        endpoint_pos = tmp_url.find('/')
        if endpoint_pos == -1:
            endpoint_pos = len(tmp_url)

        if (port_pos == -1) or (endpoint_pos < port_pos):
            target_port = 80
            hostname = tmp_url[:endpoint_pos]

        else:
            target_port = int((tmp_url[port_pos + 1:])[: endpoint_pos - port_pos - 1])  # getting port number exactly
            hostname = tmp_url[:port_pos]
        resolved_ip = socket.gethostbyname(hostname)
        print(f"HostName = {hostname}")
        print(f"Target Port = {target_port}")
        print(f"Resolved ip = {resolved_ip}")
        print(f"method = {method}")
        if method == 'CONNECT':
            forward_https(hostname,target_port, conn)
        elif method in ['GET', 'POST', 'HEAD', 'PUT', 'DELETE']:
            forward_data_http(hostname,target_port, conn, req_data)
    except Exception as e:
        print(e)

def main():
    host = input('Enter an IPv4 Address: ').strip()

    while not valid_ip_format(host):
        print('Invalid IPv4 Format.......')
        host = input('Enter an IPv4 Address: ')

    try:
        port = int(input('Enter a port number for listening: '))
    except KeyboardInterrupt:
        print('User requested an Interrupt')
        print('Application exiting.........')
        sys.exit()
    except ValueError:
        print('Entered wrong input. The port number must be integer number.')
        print('Application exiting.........')
        sys.exit()

    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        s.bind((host,port)) # binding IP Address and port for the listening server
        s.listen() # listening with OS default backlog queued number specified
        print('Socket successfully created')
        print(f'Listening Server successfully created with the port {port}')

    except socket.error as error:
        print(f'Listening Server creation failed with error {error}')
        print('Server shutting down...........')
        sys.exit(2)

    while True:
        try:
            #Client Browser connects to the listening server
            conn,addr = s.accept()  # socket.accept returns a new connection object and the address that connects to the server
            conn.settimeout(15)
            req_data = conn.recv(4096)
            if not req_data:
                print(f'Empty data requested from {addr}')
                conn.close()
                continue

            th = threading.Thread(target=connect_,args=(conn, addr,req_data))
            th.daemon=True
            th.start()

        except KeyboardInterrupt:
            print('Listening Server Shutting down...')
            s.close()
            sys.exit()
    s.close()
    sys.exit()

if __name__=="__main__":
    main()
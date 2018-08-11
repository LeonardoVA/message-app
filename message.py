import Crypto
import socket
import argparse
import time
import threading


def check_ip_addr_valid(ip_string):
    """returns binary format of address if valid"""
    try:
        addr = socket.inet_aton(ip_string)
        return addr
    except socket.error:
        print("Please enter a valid ip address for connecting to.")
        exit(1)

def setup_socket_listen(listen_port=55555):
    print("Acting as server in conversation.")
    listen_host = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
        listen_socket.bind((listen_host, listen_port))
        listen_socket.listen(1)
        conn, addr = listen_socket.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                decoded_data = data.decode("UTF-8")
                if data != '':
                    print('Received', decoded_data)
                    if data == 'exit':
                        break
                # if not data:
                #     continue
                data = data.decode("UTF-8")
                reply_str = 'receipt for message :{}'.format(data)
                conn.sendall(reply_str.encode('UTF-8'))

def setup_send_socket(port=55555):
    print("Acting as client in conversation.")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", port))
        x = ''
        while x != "exit":
            x = input("message to send:\n")
            #print ("x is '{}'".format(x))
            s.sendall(x.encode("UTF-8"))
            data = s.recv(1024)
            print('Received', repr(data))


# ip_string = input("enter address to connect to:\n")
# print(type(ip_string))
# #print(ip_string)
# check_ip_addr_valid(ip_string)
#
# listen_port = input("enter port to listen on:\n")
# print(type(listen_port))

# send_port = input("enter port to send on:\n")
# print(type(send_port))

#setup_socket_listen()
#setup_send_socket()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', '-c', help='client', action='store_true')
    parser.add_argument('--server', '-s', help='server', action='store_true')
    args = parser.parse_args()
    if args.client:
        setup_send_socket()
    elif args.server:
        setup_socket_listen()
    else:
        print("Normal mode chosen, will attempt to connect to host, if it fails will act as server")
        try:
            setup_send_socket()
        except ConnectionRefusedError:
            print("Connection to server failed, becoming the server!")
            setup_socket_listen()



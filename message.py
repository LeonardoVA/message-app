import Crypto
import socket
import argparse
import time
import threading
import binascii


def check_ip_addr_valid(ip_string):
    """returns binary format of address if valid"""
    try:
        addr = socket.inet_aton(ip_string)
        return addr
    except socket.error:
        print("Please enter a valid ip address for connecting to.")
        exit(1)

def send_message(conn):
     with conn:
        while True:
            #print("running send thread")
            message = input("")
            conn.sendall(message.encode('UTF-8'))

def receive_message(conn):
    with conn:
        while True:
            #print("Running rec thread")
            data = conn.recv(1024)
            decoded_data = data.decode("UTF-8")
            if decoded_data != '':
                print("Other: {}".format(decoded_data))
                if decoded_data == 'exit':
                    break


def setup_socket_listen(listen_port=55555):
    print("Acting as server in conversation.")
    listen_host = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
        listen_socket.bind((listen_host, listen_port))
        listen_socket.listen(1)
        conn, addr = listen_socket.accept()
        send = threading.Thread(target=send_message, args=(conn,))
        rec = threading.Thread(target=receive_message, args=(conn,))
        send.start()
        rec.start()
        send.join()
        rec.join()

def setup_send_socket(port=55555):
    print("Acting as client in conversation.")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", port))
        send = threading.Thread(target=send_message, args=(s,))
        rec = threading.Thread(target=receive_message, args=(s,))
        send.start()
        rec.start()
        send.join()
        rec.join()


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



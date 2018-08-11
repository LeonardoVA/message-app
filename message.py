"""This code sets up sockets and using the cosole as a messaging app"""
import socket
import argparse
import threading

import Crypto

def check_ip_addr_valid(ip_string):
    """returns binary format of address if valid"""
    try:
        addr = socket.inet_aton(ip_string)
        return addr
    except socket.error:
        print("Please enter a valid ip address for connecting to.")
        exit(1)

def send_message(conn):
    """Sets up sending a message from user input into shell"""
    with conn:
        while True:
            message = input("")
            # requires byte format
            conn.sendall(message.encode('UTF-8'))

def receive_message(conn):
    """Sets up reciving a message and displaying it"""
    with conn:
        while True:
            data = conn.recv(1024)
            decoded_data = data.decode("UTF-8")

            # if the incoming bytes are not empty show on screen
            if decoded_data != '':
                print("Other: {}".format(decoded_data))
                if decoded_data == 'exit':
                    break


def setup_socket_listen(listen_port=55555):
    """Sets up process as server, having to setup the
    socket for initial connection"""
    print("Acting as server in conversation.")
    listen_host = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
        listen_socket.bind((listen_host, listen_port))
        listen_socket.listen(1)
        conn, _ = listen_socket.accept()
        setup_send_rec_threads(conn)

def setup_send_socket(port=55555):
    """Sets up process as client"""
    print("Acting as client in conversation.")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect(("127.0.0.1", port))
        setup_send_rec_threads(conn)

def setup_send_rec_threads(conn):
    """"Set up threads to deal with sending and receiving messages"""
    send = threading.Thread(target=send_message, args=(conn,))
    rec = threading.Thread(target=receive_message, args=(conn,))
    send.start()
    rec.start()
    send.join()
    rec.join()


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--client', '-c', help='client', action='store_true')
    PARSER.add_argument('--server', '-s', help='server', action='store_true')
    ARGS = PARSER.parse_args()
    if ARGS.client:
        setup_send_socket()
    elif ARGS.server:
        setup_socket_listen()
    else:
        print("Normal mode chosen, will attempt to connect to host, if it fails will act as server")
        try:
            setup_send_socket()
        except ConnectionRefusedError:
            print("Connection to server failed, becoming the server!")
            setup_socket_listen()

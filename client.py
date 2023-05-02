import socket


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = input("请输入服务器IP地址：")
    client_socket.connect((ip, 3389))
    passwd = input(client_socket.recv(4096).decode())
    client_socket.send(passwd.encode())
    status = client_socket.recv(4096).decode()

    if status.startswith('连接成功'):
        print(status)
    else:
        print(status)
        client_socket.close()
        return

    try:
        while True:
            
            data = input()
            client_socket.send(data.encode())

            result = client_socket.recv(40960).decode()
            if data == "quit" or data == "exit":
                break
            print(result)

            print(client_socket.recv(4096).decode())
        client_socket.send("quit".encode())
    except:
        client_socket.send("quit".encode())

    client_socket.close()


if __name__ == '__main__':
    main()

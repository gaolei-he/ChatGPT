import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = input("请输入服务器IP地址：")
client_socket.connect((ip, 3389))
print("连接成功，开始聊天！(输入exit或quit来退出程序)")

try:
    while True:
        data = input('请输入你的问题：')
        client_socket.send(data.encode())

        result = client_socket.recv(40960).decode()
        if data == "quit" or data == "exit":
            break
        print(f'ChatGPT的回答：\n{result}\n')
    client_socket.send("quit".encode())
except:
    client_socket.send("quit".encode())

client_socket.close()
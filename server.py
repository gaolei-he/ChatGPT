#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''使用ChatGPT的API以及socket编程实现的聊天程序'''

import openai
import os
import socket
import threading
import time


def Chat(ask: str, message_history: list[dict]) -> str:
    '''处理当前问题
    
    返回值：
        ChatGPT的回答
    '''

    message = MakeMessages(ask, message_history)
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = message
    )
    response_content = response.choices[0].message.content
    message_history.append((ask, response_content))
    return response_content


def MakeMessages(ask, message_history):
    '''从聊天记录中生成ChatGPT的输入'''

    total_length = 0
    reverse_message = [
        {
            "role": "user",
            "content": ask
        }
    ]
    for question, answer in reversed(message_history):
        total_length += len(question) +len(answer)
        if total_length > 2048:
            break
        reverse_message.append({
            "role": "assistant",
            "content": answer
        })
        reverse_message.append({
            "role": "assistant",
            "content": question
        })
    return list(reversed(reverse_message))


def handle_client(client_socket, addr, passwd):
    '''处理客户端连接'''

    message_history = []

    print(f'客户端 {addr} 已连接，时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')


    

    try:
        user_input_passwd = client_socket.recv(4096).decode()

        if user_input_passwd.strip() != passwd:
            client_socket.send('密码错误，连接关闭'.encode())
            raise ValueError('密码错误')
        
        client_socket.send('连接成功'.encode())
        while True:
            data = client_socket.recv(4096).decode()

            result = Chat(data, message_history)

            client_socket.send(result.encode())

            if data.strip() == "quit" or data.strip() == "exit":
                raise ValueError('客户端主动断开连接')
    except ValueError as e:
        print(f'客户端 {addr} {e}，时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
    except Exception as e:
        print(f'客户端 {addr} {e}，时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

    print(f"客户端 {addr} 已断开连接，时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n")
    client_socket.close()


def main():

    openai.api_key = os.getenv("OPENAI_API_KEY")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((socket.gethostbyname(socket.gethostname()), 3389))

    server_socket.listen()

    passwd = input("请设置客户端连接密码：")

    print('服务器已启动，等待客户端连接...')

    while True:
        client_socket, addr = server_socket.accept()

        thread = threading.Thread(target=handle_client, args=(client_socket, addr, passwd))
        thread.start()


if __name__ == '__main__':
    main()

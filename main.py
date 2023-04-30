import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

message_history = []

def MakeMessages(ask):
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

while True:
    ask = input("请输入问题：")

    message = MakeMessages(ask)

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = message
    )
    response_content = response.choices[0].message.content
    print(response_content)
    message_history.append((ask, response_content))
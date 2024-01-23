import requests

# использование кастомного chatgpt через кастомный api
payload = {"event":"На какой минимальный срок можно оформить КАСКО?", "data":{"test":"asdfasdfasd"}}
response = requests.post("http://127.0.0.1:8000/webhook/dfcc1e78-aebd-43b2-97a8-f626420b0aa6", json=payload)
print(response.text)


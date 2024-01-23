# Алгоритм работы 
ловим запросы к OpenAI и перебрасываем на их сайт

https://api.openai.com


curl https://api.openai.com/v1/embeddings \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "The food was delicious and the waiter...",
    "model": "text-embedding-ada-002",
    "encoding_format": "float"
  }'

curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-3.5-turbo-1106",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Hello!"
      }
    ],
    "stream": true
  }'


curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-3.5-turbo-1106",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
  }'

# vsegpt

https://vsegpt.ru/Docs/API#h84-4



endpoint ="http://163.5.207.104:8000/v1"
import openai
openai.api_key = OPENAI_API_KEY
openai.api_base = endpoint
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY, base_url= openai.api_base)
response = client.chat.completions.create(**)




import requests
from dotenv import load_dotenv
import os
load_dotenv()
url_c ="/v1/chat/completions"
url_embeddings = "/v1/embeddings"
localhost ="http://127.0.0.1:8000"
openai = "https://api.openai.com"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
headers = {
"Authorization": f"Bearer {OPENAI_API_KEY}",
"Content-Type": "application/json"
}

headers2 = {
"authorization": f"Bearer {OPENAI_API_KEY}",
"content-type": "application/json"
}

d_c = {
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
}

d_c2 = {
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
    "stream": False
  }

def completions():
    response = requests.post(localhost+url_c, headers = headers2, json=d_c2)
    return response

def completions2():
    response = requests.post(openai+url_c, headers = headers2, json=d_c2)
    return response


def completions3():
    import openai
    openai.api_key = OPENAI_API_KEY
    openai.api_base = localhost+"/v1"

    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY, base_url= openai.api_base)
    response = client.chat.completions.create(**d_c2)
    return response


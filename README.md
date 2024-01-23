# py_web

# webhook
cd webhook
uvicorn server:app --reload
uvicorn server:app --host 0.0.0.0 --port 8000 --reload

# openai

cd openai
uvicorn openai_server:app --reload

http://127.0.0.1:8000 

import os
os.chdir("openai")
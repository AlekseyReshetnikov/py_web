from fastapi import FastAPI, HTTPException, Header, Request
from starlette.responses import StreamingResponse

from typing import Dict, List
import json
import requests
import httpx
from datetime import datetime
class Const:
    openai = "https://api.openai.com"
    completions = "/v1/chat/completions"
    completions1 = "/v1/completions"
    embeddings = "/v1/embeddings"
    headers = ["authorization", "content-type"]
    generations = "/v1/images/generations"
c = Const()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/v1/chat/completions")
async def completions(request: Request):
    # try:
    #     with open("test.txt","w",encoding="utf-8") as f:
    #         json.dump( request.headers.items(),f)
        headers = {k: v for k, v in filter(lambda x:x[0] in c.headers, request.headers.items())}
        body = await request.body()
        data = json.loads(body.decode("utf-8"))
        print(datetime.now(), " completions ", data)
        # response = requests.post(c.openai + c.completions, headers=headers, json = data)
        # Use the async version of requests (httpx) for better performance
        print(datetime.now())
        async with httpx.AsyncClient() as client:
            response = await client.post(c.openai + c.completions, headers=headers, json=data)
        print(datetime.now())
        if "stream" in data and data["stream"]:
            # Create a generator function to stream the content
            async def generate():
                async for it in response.aiter_bytes():
                    yield it
            # Return the streaming response
            return StreamingResponse(content=generate(), media_type="application/json", status_code = response.status_code)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        print(datetime.now())
        print("###@@@@  ",response.status_code)
        return response.json()

    # except json.JSONDecodeError:
    #     raise HTTPException(status_code=400, detail="Invalid JSON format in the request body")
    # except requests.RequestException as e:
    #     raise HTTPException(status_code=500, detail=f"Error connecting to OpenAI API: {str(e)}")

async def my_request(request: Request, path:str):
    headers = {k: v for k, v in filter(lambda x: x[0] in c.headers, request.headers.items())}
    body = await request.body()
    data = json.loads(body.decode("utf-8"))
    print(datetime.now(), " path ", data)
    # response = requests.post(c.openai + c.completions, headers=headers, json = data)
    # Use the async version of requests (httpx) for better performance
    print(datetime.now())
    async with httpx.AsyncClient() as client:
        response = await client.post(c.openai + path, headers=headers, json=data)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    print(datetime.now(), " ###@@@@  ", response.status_code)
    return response.json()

@app.post("/v1/images/generations")
async def generations(request: Request):
    return await my_request(request, c.generations)

@app.post("/v1/completions")
async def completions1(request: Request):
    return await my_request(request, c.completions1)

@app.post("/v1/embeddings")
async def embeddings(request: Request):
    headers = {k: v for k, v in filter(lambda x: x[0] in c.headers, request.headers.items())}
    body = await request.body()
    data = json.loads(body.decode("utf-8"))
    print(datetime.now(), " embeddings ", data)
    # response = requests.post(c.openai + c.completions, headers=headers, json = data)
    # Use the async version of requests (httpx) for better performance
    print(datetime.now())
    async with httpx.AsyncClient() as client:
        response = await client.post(c.openai + c.completions, headers=headers, json=data)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    print(datetime.now(), " ###@@@@  ", response.status_code)
    return response.json()
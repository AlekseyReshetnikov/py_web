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
    audio_transcriptions ="/v1/audio/transcriptions"
    headers = ["authorization", "content-type"]
    generations = "/v1/images/generations"
    v1 = "/v1"
c = Const()

app = FastAPI()

@app.get("/")
async def root():
    return {"message":
        """It is proxy server to https://api.openai.com/v1
# usage:
 
api_key = os.environ.get("OPENAI_API_KEY")
api_base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")


endpoint ="http://163.5.207.104:8000/v1"
import openai
openai.api_key = OPENAI_API_KEY
openai.api_base = endpoint
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY, base_url= openai.api_base)
embeddings =OpenAIEmbeddings(openai_api_base=config.OPENAI_END_POINT)
"""}

def get_headers(request:Request):
    return {k: v for k, v in filter(lambda x:x[0].lower() in c.headers, request.headers.items())}
@app.post("/v1/chat/completions")
async def completions(request: Request):
    try:
    #     with open("test.txt","w",encoding="utf-8") as f:
    #         json.dump( request.headers.items(),f)
        s:str=""
        headers = get_headers(request)
        body = await request.body()
        data = json.loads(body.decode("utf-8"))
        print(headers)
        print(datetime.now(), " completions ", data)
        # response = requests.post(c.openai + c.completions, headers=headers, json = data)
        # Use the async version of requests (httpx) for better performance
        print(datetime.now())
        async with httpx.AsyncClient() as client:
            response = await client.post(c.openai + c.completions, headers=headers, json=data, timeout= 120)
        print(datetime.now())
        async def generate():
            async for it in response.aiter_bytes():
                yield it
        if "stream" in data and data["stream"]:
            # Create a generator function to stream the content
            # Return the streaming response
            return StreamingResponse(content=generate(), media_type="application/json", status_code = response.status_code)
        return StreamingResponse(content=generate(), media_type="application/json", status_code = response.status_code)
        # response.raise_for_status()  # Raise an HTTPError for bad responses
        # print(datetime.now())
        # print("###@@@@  ",response.status_code)
        # return response.json()

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in the request body")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to OpenAI API: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


async def my_request(request: Request, path:str):
    try:
        headers = get_headers(request)
        body = await request.body()
        data = json.loads(body.decode("utf-8"))
        print(datetime.now(), " path ", data)
        # response = requests.post(c.openai + c.completions, headers=headers, json = data)
        # Use the async version of requests (httpx) for better performance
        print(datetime.now())
        
        async with httpx.AsyncClient() as client:
            response = await client.post(c.openai + path, headers=headers, json=data, timeout= 120)
        async def generate():
            async for it in response.aiter_bytes():
                yield it
        return StreamingResponse(content=generate(), media_type="application/json", status_code = response.status_code)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in the request body")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to OpenAI API: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@app.post("/v1/images/generations")
async def generations(request: Request):
    return await my_request(request, c.generations)

@app.post("/v1/completions")
async def completions1(request: Request):
    return await my_request(request, c.completions1)

@app.post("/v1/embeddings")
async def embeddings(request: Request):
    return await my_request(request, c.embeddings)

@app.post("/v1/audio/transcriptions")
async def audio_transcriptions(request: Request):
    return await my_request(request, c.audio_transcriptions)

@app.post("/v1/{p1}")
async def v1_p1(p1:str, request: Request):
    return await my_request(request, f"{c.v1}/{p1}")

@app.post("/v1/{p1}/{p2}")
async def v1_p1_p2(p1:str, p2:str, request: Request):
    return await my_request(request, f"{c.v1}/{p1}/{p2}")

@app.post("/v1/{p1}/{p2}/{p3}")
async def v1_p1_p2(p1:str, p2:str, p3:str, request: Request):
    return await my_request(request, f"{c.v1}/{p1}/{p2}/{p3}")


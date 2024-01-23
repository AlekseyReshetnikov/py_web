from fastapi import FastAPI, HTTPException, Header, Request
from typing import Dict, List
import json

app = FastAPI()
app_data = {}
app_data_ix = 10

@app.post("/webhook/{webhook_id}")
async def handle_webhook(webhook_id:str, request: Request):
    headers = {k:v for k,v in request.headers.items()}
    body = await request.body()
    data = json.loads( body.decode("utf-8"))
    # print(data)
    d = {}
    global app_data_ix
    app_data_ix +=1
    d["uuid"] = str(app_data_ix)
    # print( headers)
    for i in ["user-agent"]:
        d[i] = headers[i]
    d["user_agent"] = headers["user-agent"]
    is_list = False
    if "messages" in data:
        if type(data["messages"])==list:
            is_list = True
    if is_list:
        d["content"] = json.dumps(data,ensure_ascii=False)
        if not webhook_id in app_data:
            app_data[webhook_id]= {}
        w_data = app_data[webhook_id]
        w_data[str(app_data_ix)] = d
    # Добавьте вашу логику обработки вебхука здесь
    # Например, вы можете сохранять данные в базу данных или выполнять другие действия в зависимости от события
    # return {"message": f"Webhook '{webhook_id}' received for event '{data}' \n {headers}" }
    return ""

@app.get("/token/{token_id}/requests")
async def requests_list(token_id:str, sorting:str):
    if token_id in app_data:
        w_data = app_data[token_id]
        d = {"data":list(w_data.values())}
    else:
        d = {"data":[]}
    return d

# requests.delete(f'https://webhook.site/token/{token_id}/request/{req_id}', headers=headers)

@app.delete("/token/{token_id}/request/{req_id}")
async def requests_delete(token_id:str, req_id:str):
    if token_id in app_data:
        w_data = app_data[token_id]
        if req_id in w_data:
            w_data.pop(req_id)

    # print(f"{req_id} : {app_data}")
    # return {"message": f"Webhook '{token_id}' delete for event '{req_id}'"}

#  delete_webhook(token_id, request['uuid'], headers)
# for request in data['data']:
# request['user_agent'] == 'WappiWH':
# content = json.loads(request['content'])
# user-agent	WappiWH
# https://fastapi.tiangolo.com/tutorial/
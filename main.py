from fastapi import FastAPI, BackgroundTasks
from routes import router
from datetime import datetime
import asyncio
import logging

logging.basicConfig(filename='requests.log', level=logging.INFO)

app = FastAPI()
app.include_router(router)

async def time_now():
    while True:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Текущее время: {time}')
        await asyncio.sleep(10)

@app.get("/get_time")
async def get_time(background_tasks: BackgroundTasks):
    await time_now()
    return {"time": datetime.now()}

@app.middleware("http")
async def logs(request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    process_time = datetime.now() - start_time
    logging.info(f'{request.method} {request.url} - {response.status_code}')
    return response
#  .\venv\Scripts\activate 

import subprocess
from fastapi import FastAPI
from model import Task, UpdateTask
import test_calender
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def add_to_mongo(event, event_id):
    # mongo connection
    client = MongoClient("mongodb+srv://chronoappdev:cyNhAeyqy4Ax4kOH@chrono.h7plkti.mongodb.net/?retryWrites=true&w=majority&appName=Chrono")
    db = client['calender_events']
    collection = db['events']
    
    data_to_insert = {
        'id': event_id,
        'summary': event[0],
        'start': event[1],
        'end':event[2],
        'tag': event[3]
    }
    result = collection.insert_one(data_to_insert)
    client.close()
    


@app.get("/trial")
async def root():
    return {"message": "HELLOOOOO"}

@app.get("/get_tasks")
async def get_tasks():
    tasks_list = test_calender.get_latest_events()
    print(tasks_list)
    return {"message": tasks_list}

@app.post("/enter_new_task")
async def create_task(task: Task):
    print(Task.get_list(task))
    new_event_id = test_calender.add_event(Task.get_list(task))
    add_to_mongo(Task.get_list(task), new_event_id)
    return {"message": new_event_id}

@app.post("/update_task")
async def create_task(task: UpdateTask):
    print(Task.get_list(task))
    test_calender.update_event(Task.get_list(task))
    return {"message": task}

if __name__ == "__main__":
    command = "uvicorn fast_server:app --host 0.0.0.0 --port 8000 "

    # Run the command
    subprocess.run(command, shell=True)





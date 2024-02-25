
"""
We will create a todo applicaton for learning with basic functionalities

task title
date from
due date
tag
"""

from fastapi import FastAPI
from pydantic import BaseModel

class TodoItem(BaseModel):
    id: int
    todo: str

# app name
#uvicorn 'filename':'varname of fastapi' --reload
app = FastAPI()

#get and post is mode
#the thing in bracket is route.
# that is the url the frontend will use to post data here
# also will be used to sput data in mongodb
@app.get("/")
async def root():
    return {"message": "Hello World"}

todos = []


# get all todo
@app.get("/todos")
async def get_all_todos():
    return {"todos": todos}

# get a single todo
@app.get("/todos/single/{todo_id}")
async def get_first_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return {"firstTodo": todo}

# create to do
@app.post("/todos/create")
async def create_todo(task: TodoItem):
    todos.append(task)
    return {"message" : "todo created"}

# update to do

# delete to do
@app.get("/todos/delete/{todo_id}")
async def delete_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return {"message" : "todo deleted"}
    return {"message" : "todo not found"}
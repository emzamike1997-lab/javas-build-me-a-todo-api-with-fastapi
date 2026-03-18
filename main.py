from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Enable CORS for all origins
from fastapi.middleware.cors import CORSMiddleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory dict storage
todos = {}

class Todo(BaseModel):
    id: int
    title: str
    completed: bool

class TodoCreate(BaseModel):
    title: str
    completed: bool

class TodoUpdate(BaseModel):
    title: str | None
    completed: bool | None

# GET /health endpoint
@app.get("/health")
def get_health():
    return {"status": "healthy"}

# GET / endpoint
@app.get("/")
def get_api_info():
    return {"api": "Todo API", "version": "1.0"}

# GET /todos endpoint
@app.get("/todos", response_model=List[Todo])
def get_todos():
    return list(todos.values())

# GET /todos/{id} endpoint
@app.get("/todos/{id}", response_model=Todo)
def get_todo(id: int):
    if id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[id]

# POST /todos endpoint
@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    new_id = max(todos.keys(), default=0) + 1
    todos[new_id] = Todo(id=new_id, title=todo.title, completed=todo.completed)
    return todos[new_id]

# PUT /todos/{id} endpoint
@app.put("/todos/{id}", response_model=Todo)
def update_todo(id: int, todo: TodoUpdate):
    if id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.title:
        todos[id].title = todo.title
    if todo.completed is not None:
        todos[id].completed = todo.completed
    return todos[id]

# DELETE /todos/{id} endpoint
@app.delete("/todos/{id}")
def delete_todo(id: int):
    if id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[id]
    return {"message": "Todo deleted"}
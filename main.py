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

# GET / endpoint returning API info
@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

# GET /health endpoint returning {"status": "healthy"}
@app.get("/health")
def read_health():
    return {"status": "healthy"}

# GET /todos endpoint returning all todos
@app.get("/todos", response_model=List[Todo])
def read_todos():
    return list(todos.values())

# GET /todos/{todo_id} endpoint returning a single todo
@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]

# POST /todos endpoint creating a new todo
@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    new_id = max(todos.keys(), default=0) + 1
    todos[new_id] = Todo(id=new_id, title=todo.title, completed=todo.completed)
    return todos[new_id]

# PUT /todos/{todo_id} endpoint updating a single todo
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoUpdate):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.title is not None:
        todos[todo_id].title = todo.title
    if todo.completed is not None:
        todos[todo_id].completed = todo.completed
    return todos[todo_id]

# DELETE /todos/{todo_id} endpoint deleting a single todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
    return {"message": "Todo deleted"}
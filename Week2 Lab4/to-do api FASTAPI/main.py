from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# In-memory storage
todos = []
next_id = 1

# Model for creating a task
class TaskCreate(BaseModel):
    title: str

# Model for a full task (used in responses)
class Task(BaseModel):
    id: int
    title: str
    completed: bool

# Model for updating a task (both fields optional)
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


@app.post("/todos", response_model=Task)
def create_task(task: TaskCreate):
    global next_id
    new_task = {
        "id": next_id,
        "title": task.title,
        "completed": False
    }
    todos.append(new_task)
    next_id += 1
    return new_task


@app.get("/todos")
def get_all_tasks():
    return todos


@app.get("/todos/{id}")
def get_task(id: int):
    for task in todos:
        if task["id"] == id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/todos/{id}")
def update_task(id: int, updated: TaskUpdate):
    for task in todos:
        if task["id"] == id:
            if updated.title is not None:
                task["title"] = updated.title
            if updated.completed is not None:
                task["completed"] = updated.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/todos/{id}")
def delete_task(id: int):
    for task in todos:
        if task["id"] == id:
            todos.remove(task)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
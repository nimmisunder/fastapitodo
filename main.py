from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
app = FastAPI()
class Task(BaseModel):
    id:int
    name:str
    desc:str
    is_completed:bool

@app.get("/")
def get_tasks():
    return {"Hello":"World"}
tasklist=[]

@app.post("/add_item")
def create_item(task: Task):
    
    tasklist.append(task)
    return task

@app.get("/alltask")
def get_all_taskks():
    return tasklist

@app.put("/updatetask/{taskid}")
def update_task(taskid:int,task:Task):
    for i,j in enumerate(tasklist):
        if taskid==j.id:
            tasklist[i]=task
            return task
    raise HTTPException(status_code=404,detail="tasl not found")

@app.delete("/delete_task/{taskid}")
def del_task(taskid:int):
    for i,j in enumerate(tasklist):
        if taskid==j.id:
            tasklist.pop(i)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404,detail="Task not found")





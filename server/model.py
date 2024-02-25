from pydantic import BaseModel

class Task(BaseModel):
    summary: str
    start: str
    end: str
    tag: str

    def get_list(task: 'Task'):
        return [task.summary, task.start, task.end, task.tag]


class UpdateTask(BaseModel):
    summary: str
    start: str
    end: str
    tag: str
    task_update_id: str

    def get_list(task: 'Task'):
        return [task.summary, task.start, task.end, task.tag]
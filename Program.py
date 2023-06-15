from typing import List, Any
from datetime import datetime, timedelta

class Descriptor:
    def __init__(self, key: Any) -> None:
        self.key: str = key

    def __get__(self, instance: object, owner: Any) -> Any:
        if not instance:
            return
        return instance.__dict__[self.key]
    
    def __set__(self, instance: object, value: Any) -> None:
        instance.__dict__[self.key] = value

class Task:
    states: tuple = ("InProgress", "Done", "Failed")

    title: str = Descriptor('title')
    description: str = Descriptor('description')
    deadline: str = Descriptor('deadline')

    def __init__(self) -> None:
        self.title: str = ""
        self.description: str = ""
        self.deadline: str = ""
        self.state: str = Task.states[0]

class Program:
    tasks: List[Task] = Descriptor('tasks')

    def __init__(self) -> None:
        self.tasks: List[Task] = list()
    
    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
    
    def check_deadline(self, task: Task) -> None:
        current_time = datetime.now()
        target_time = datetime.strptime(task.deadline, "%Y-%m-%d %H:%M")
        time_difference = target_time - current_time

        if current_time > target_time and task.state == Task.states[0]:
            task.state = Task.states[2]
            return (f"Task {task.title} - failed!", (255, 0, 0))
        
        elif time_difference < timedelta(minutes=60) and task.state == Task.states[0]:
            return (f"Task {task.title} - less than one hour remaining!", (200, 200, 0))



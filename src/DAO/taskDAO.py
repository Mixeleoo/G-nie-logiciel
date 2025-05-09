
from src.dataclass.task import Task
from src.dataclass.color import Color
from src.dbcom import DBCom, dbcom
from src.dataclass.user import User

class TaskDAO:
    def __init__(self, s: DBCom):
        self.dbcom = s

    def insert(self, user: User, task: Task):
        """
        création d'un task
        """
        self.dbcom.sendall({
            "data":{
                "user_id": user.id,
                "name": task.name,
                "details": task.details,
                "done": task.done,
                "date": task.date,
                "color": (task.color.r << 16) | (task.color.g << 8) | task.color.b,
            },
            "requestType": "createTask",
            "op": 3
        })
        return self.dbcom.recv()

    def update(self, task: Task):
        """
        update l'task
        """
        self.dbcom.sendall({
            "data":{
                "name": task.name,
                "details": task.details,
                "done": task.done,
                "date": task.date,
                "color": (task.color.r << 16) | (task.color.g << 8) | task.color.b,
                "task_id": task.id
            },
            "requestType": "updateTask",
            "op": 3
        })
        return self.dbcom.recv()

    def delete(self, task: Task):
        """
        supprimer un task
        """
        self.dbcom.sendall({
            "data":{
                "event_id": task.id
            },
            "requestType": "deleteTask",
            "op": 3
        })
        return self.dbcom.recv()

    def get_task_list(self, user: User):
        """
        supprimer un task
        """
        self.dbcom.sendall({
            "data": {
                "user_id": user.id
            },
            "requestType": "getTaskList",
            "op": 3
        })
        r: list[Task] = []
        data: dict = self.dbcom.recv()
        for task in data["data"]["taskList"]:
            r.append(
                Task(
                    task["id"],
                    task["name"],
                    task["desc"],
                    bool(task["done"]),
                    task["deadline"],
                    Color(
                        r=(task["color"] >> 16) & 0xFF,
                        g=(task["color"] >> 8) & 0xFF,
                        b=task["color"] & 0xFF
                    )
                )
            )

        return r

taskdao = TaskDAO(dbcom)
tasklist: list[Task] = []

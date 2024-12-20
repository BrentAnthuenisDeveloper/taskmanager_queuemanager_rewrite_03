from Infrastructure.SQLServer_QueueDB.Interfaces.IConnectionProvider import IConnectionProvider
from .Model.Task import Task
import json
from GlobalSettings import statuses


class TaskService:
    def __init__(self, connectionprovider: IConnectionProvider) -> None:
        self.connection = connectionprovider
        self.statuses: dict[str, str] = statuses

    def getNextQueueItem(self) -> Task | None:
        """geef de eerste task in de queue et de hoogste prioriteit en de laagste aantal retries en minder dan settings.maxretries"""

        query = """
        SELECT top 1 q.ID, q.task_type, q.payload, q.status, q.statuslog, q.retries, q.priority, q.created_at, q.updated_at, q.processed_at
        FROM dbo.tasks_queue AS q LEFT OUTER JOIN
             dbo.task_type AS tt ON q.task_type = tt.task_type
        WHERE status IN (?, ?) 
              AND DATEDIFF(MINUTE, updated_at, GETDATE()) > (POWER(2,q.retries)*tt.retryinterval)-61 
              And q.retries < tt.maxretries
        ORDER BY q.priority, q.ID
        """
        values = (self.statuses["in_queue"], self.statuses["failed"])
        # print("-executing: ",query, " -with values: ",values)
        tasks = []
        rows = self.connection.fetch_query(query, values)
        for row in rows:
            # print("payload", row.payload)
            firstTask = Task(
                id=row.ID,
                task_type=row.task_type,
                payload=json.loads(row.payload),
                status=row.status,
                statuslog=row.statuslog,
                retries=row.retries,
                priority=row.priority,
                created_at=row.created_at,
                updated_at=row.updated_at,
                processed_at=row.processed_at,
            )
            tasks.append(firstTask)
        if tasks.__len__() == 0:
            return None
        else:
            if tasks.__len__() > 1:
                raise ValueError("er werden meerdere tasks gevonden")
            firstTask: Task = tasks[0]
            return firstTask

    def updateTask(self, task: Task) -> None:
        """update de gegeven task in de queue"""

        query = """
            UPDATE tasks_queue
            SET 
                status = ?, 
                statuslog = ?, 
                retries = ?, 
                created_at = ?, 
                updated_at = ?, 
                processed_at = ?
            WHERE ID = ?
            """
        # Values to update in the database (use the task values)
        values = (
            task.status,
            task.statuslog,
            task.retries,
            task.created_at,
            task.updated_at,
            task.processed_at,
            task.id,
        )
        cursor = self.connection.execute_query(query, values)

    def getTasks(self, offset=0, limit=1000) -> list[Task]:
        """geef alle tasks uit de queue"""

        query = f"""
            SELECT id, task_type, payload, status, statuslog, retries, priority, created_at, updated_at, processed_at 
            FROM tasks_queue
            order by id
            OFFSET {offset} ROWS FETCH NEXT {limit} ROWS ONLY;
            """
        data = self.connection.fetch_query(query)
        tasks = []
        for row in data:
            # print("payload", row.payload)
            firstTask = Task(
                id=row.id,
                task_type=row.task_type,
                payload=json.loads(
                    row.payload
                ),  # Assuming payload is a JSON string or dict
                status=row.status,
                statuslog=row.statuslog,
                retries=row.retries,
                priority=row.priority,
                created_at=row.created_at,
                updated_at=row.updated_at,
                processed_at=row.processed_at,
            )
            tasks.append(firstTask)
        data.close()
        return tasks

    def insertTask(self, newTask: Task):
        """maak een nieuwe task aan in de queue"""

        query = """
        INSERT INTO tasks_queue (
            task_type, payload, status, statuslog, retries,
            priority, created_at, updated_at, processed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        payload = json.dumps(newTask.payload)
        values = (
            newTask.task_type,
            payload,
            newTask.status,
            newTask.statuslog,
            newTask.retries,
            newTask.priority,
            newTask.created_at,
            newTask.updated_at,
            newTask.processed_at,
        )
        return self.connection.execute_query()(query, values)

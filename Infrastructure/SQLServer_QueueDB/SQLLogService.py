
from Infrastructure.SQLServer_QueueDB.Interfaces.IConnectionProvider import IConnectionProvider
from Infrastructure.SQLServer_QueueDB.Model.Log import Log


class LogService:
    def __init__(self, connectionprovider: IConnectionProvider) -> None:
        self.connection = connectionprovider
    
    def insertLog(self,log : Log)->None:
        query = """
        INSERT INTO logs (
            timestamp, level, message,extra_info
        ) VALUES (?, ?, ?,?)
        """
        values=(log.timestamp,log.level,log.message,log.extra_info)

        self.connection.execute_query(query,values)
    

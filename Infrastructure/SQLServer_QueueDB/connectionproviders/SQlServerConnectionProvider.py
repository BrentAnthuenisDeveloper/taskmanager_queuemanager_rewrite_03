from typing import Any
import pyodbc

from Infrastructure.SQLServer_QueueDB.Interfaces.IConnectionProvider import (
    IConnectionProvider,
)


class SQLServerConnectionProvider(IConnectionProvider):
    def __init__(self, server, database, username, password, driver="{SQL Server}"):
        self._connection = pyodbc.connect(
            f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        )

    def execute_query(self, query, params={}) -> None:
        cursor=self._connection.cursor()
        cursor.execute(query, params)
        self._connection.commit()
        cursor.close()

    def fetch_query(self,query,params={}) -> Any:
        cursor=self._connection.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        self._connection.commit()
        cursor.close()
        return data
    
    def __del__(self):
        self._connection.close()

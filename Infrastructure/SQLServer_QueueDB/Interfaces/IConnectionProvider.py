import abc
from typing import Any


class IConnectionProvider(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "execute_query") and callable(subclass.execute_query)

    @abc.abstractmethod
    def execute_query(self, query, params={})->None:
        """execute a query with optional params and that doesn't expect a response body"""
        raise NotImplementedError
    def fetch_query(self,query,params={})->Any:
        """execute a query with optional params and a response body"""
        raise NotImplementedError
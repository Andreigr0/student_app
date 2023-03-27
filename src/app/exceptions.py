from typing import Type

from app.database import Base


class NotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ModelNotFoundException(NotFoundException):
    def __init__(self, model: Type[Base]):
        message = f'{model.__name__} not found'.replace('Model', '')
        super().__init__(message)

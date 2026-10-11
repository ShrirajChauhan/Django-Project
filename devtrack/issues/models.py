from django.db import models
from abc import ABC, abstractmethod

# Create your models here.

class BaseEntity(ABC):

    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}

class Reporter(BaseEntity):
    def __init__(self, id,name, email,team):
        self.id = id
        self.name = name
        self.email = email
        self.team = team

    def validate(self):
        if not self.name:
            raise ValueError("Name cannot be empty.")
        if '@' not in self.email:
            raise ValueError("Invalid email")

class Issue(BaseEntity):
    def __init__(self, id, title, description, status, priority, reporter_id):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.reporter_id = reporter_id

    def validate(self):
        if not self.title:
            raise ValueError("Title cannot be empty.")
        if not isinstance(self.reporter_id, int):
            raise ValueError("Reporter ID must be an integer.")

class CriticalIssue(Issue):
    def __init__(self, id, title, description, status, priority, reporter_id, severity):
        super().__init__(id, title, description, status, priority, reporter_id)
        self.severity = severity

    def describe(self):
        return f"[URGENT] {self.title} - needs immediate attention!"

class LowPriorityIssue(Issue):
    def __init__(self, id, title, description, status, priority, reporter_id, estimated_time):
        super().__init__(id, title, description, status, priority, reporter_id)
        self.estimated_time = estimated_time

    def describe(self):
        return f"{self.title} - low priority, handle when free"
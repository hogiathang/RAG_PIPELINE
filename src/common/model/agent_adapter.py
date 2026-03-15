from abc import ABC, abstractmethod

class AgentAdapter:
    def __init__(self, model):
        self.model = model

    @abstractmethod
    def execute_task(self, prompt, task_type):
        pass
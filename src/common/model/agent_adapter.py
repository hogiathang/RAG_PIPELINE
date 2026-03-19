from abc import ABC, abstractmethod

class AgentAdapter:

    @abstractmethod
    def execute_task(self, prompt, task_type):
        pass
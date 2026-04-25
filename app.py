from executor import Executor
from parser import Parser
from storage import Storage
from transformations import Transformations


class App:
    def __init__(self):
        self.parser = Parser()
        self.executor = Executor(Transformations())
        self.storage = Storage()

    def execute_script(self, script):
        program = self.parser.parse(script)
        execution_result = self.executor.execute(program)
        execution_id = self.storage.save_execution(execution_result.variables)

        return execution_id

    def view_items(self, execution_id, items):
        saved_items = self.storage.load_items(execution_id, items)
        return saved_items

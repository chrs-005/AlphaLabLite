import argparse
import json
import sys

from executor import Executor
from parser import Parser
from storage import Storage
from transformations import Transformations


def execute_command():
    script = sys.stdin.read()

    parser = Parser()
    executor = Executor(Transformations())
    storage = Storage()

    program = parser.parse(script)
    execution_result = executor.execute(program)
    execution_id = storage.save_execution(execution_result.variables)

    print(f"Script sucessfully executed: {execution_id}")


def view_command(execution_id, items):
    storage = Storage()
    saved_items = storage.load_items(execution_id, items)

    for name, series in saved_items.items():
        print(f"{name}:")
        print("      ",series)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("execute")
    view_parser = subparsers.add_parser("view")
    view_parser.add_argument("--id", required=True)
    view_parser.add_argument("items", nargs="+")

    
    args = parser.parse_args()

    if args.command == "execute":
        execute_command()
    elif args.command == "view":
        view_command(args.id, args.items)
    else:
        parser.print_help()


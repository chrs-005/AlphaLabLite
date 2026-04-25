import argparse
import sys

from app import App


def execute_command():
    script = sys.stdin.read()
    app = App()
    execution_id = app.execute_script(script)

    print(f"Script sucessfully executed: {execution_id}")


def view_command(execution_id, items):
    app = App()
    saved_items = app.view_items(execution_id, items)

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

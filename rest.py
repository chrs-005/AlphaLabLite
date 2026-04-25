import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from executor import Executor
from parser import Parser
from storage import Storage
from transformations import Transformations


class RestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read().decode("utf-8")
        try:
            data = json.loads(body)
            script = data["script"]

            parser = Parser()
            executor = Executor(Transformations())
            storage = Storage()

            program = parser.parse(script)
            execution_result = executor.execute(program)
            execution_id = storage.save_execution(execution_result.variables)

            self._send_json(
                200,
                {
                    "message": "Scripts successfully executed",
                    "result": execution_id,
                },
            )
        except Exception as error:
            self._send_json(400, {"message": str(error)})

    def do_GET(self):
        parsed_url = urlparse(self.path)
        execution_id = parsed_url.path.removeprefix("/view/")
        query = parse_qs(parsed_url.query)
        items = query.get("items", [])

        try:
            storage = Storage()
            saved_items = storage.load_items(execution_id, items)
            self._send_json(200, saved_items)
        except Exception as error:
            self._send_json(400, {"message": str(error)})




    def _send_json(self, code, data):
        response = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), RestHandler)
    print("Runnig on http://127.0.0.1:8000")
    server.serve_forever()

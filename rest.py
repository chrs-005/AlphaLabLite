import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from app import App


class RestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        parsed_url = urlparse(self.path)
        post_routes = {
            "execute": self.handle_execute,
        }#add later POST routes here
        
        #Assuming path format :"/ROUTENAME/..."
        path_parts = parsed_url.path.split("/")
        
        route_name = ""



        if len(path_parts) > 1:
            route_name = path_parts[1] 

        handler = post_routes.get(route_name)

        if handler is None:
            self._send_json(404, {"message": "Not found"})
            return

        handler()


    def do_GET(self):
        parsed_url = urlparse(self.path)
        get_routes = {
            "view": self.handle_view,
        } #add later GET routes here

        path_parts = parsed_url.path.split("/")
        route_name = ""

        if len(path_parts) > 1:
            route_name = path_parts[1]

        handler = get_routes.get(route_name)

        if handler is not None:
            handler(parsed_url)
            return

        self._send_json(404, {"message": "Not found"})


    def handle_execute(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            data = json.loads(body)
            script = data["script"]
            app = App()
            execution_id = app.execute_script(script)

            self._send_json(
                200,
                {
                    "message": "Scripts successfully executed",
                    "result": execution_id,
                },
            )
        except Exception as error:
            self._send_json(400, {"message": str(error)})

    def handle_view(self, parsed_url):
        execution_id = parsed_url.path.removeprefix("/view/")
        query = parse_qs(parsed_url.query)
        items = query.get("items", [])

        try:
            app = App()
            saved_items = app.view_items(execution_id, items)
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
    print("Running on http://127.0.0.1:8000")
    server.serve_forever()

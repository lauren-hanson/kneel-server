from urllib.parse import urlparse, parse_qs
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import *


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]
        id = None
        try:
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass
        return (resource, id)

    def do_GET(self):
        """Handles GET requests to the server """
        response = {}  # Default response
        # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)
        if resource == "metals":
            if id is not None:
                response = get_single_metal(id)
                # self._set_headers(200)
                if response is None:
                    self._set_headers(404)
                    response = "This metal is not in stock"
                else:
                    self._set_headers(200)
            else:
                self._set_headers(200)
                response = get_all_metals()
        if resource == "orders":
            if id is not None:
                self._set_headers(200)
                response = get_single_order(id)
            else:
                self._set_headers(200)
                response = get_all_orders()
        if resource == "sizes":
            if id is not None:
                # self._set_headers(200)
                response = get_single_size(id)
                if response is None:
                    self._set_headers(404)
                    response = "This size is not in stock"
                else:
                    self._set_headers(200)
            else:
                self._set_headers(200)
                response = get_all_sizes()
        if resource == "styles":
            if id is not None:
                # self._set_headers(200)
                response = get_single_style(id)
                if response is None:
                    self._set_headers(404)
                    response = "This style is not in stock"
                else:
                    self._set_headers(200)
            else:
                self._set_headers(200)
                response = get_all_styles()
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)
        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        # Initialize new response
        new_order = None
        # new_location = None
        # new_employee = None
        # Add a new order to the list. Don't worry about
        # the orange squiggle, you'll define the create_order
        # function next.
        if resource == "orders":
            new_order = create_order(post_body)
        # Encode the new order and send in order
        self.wfile.write(json.dumps(new_order).encode())

    def do_DELETE(self):
        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        # Delete a single order from the list
        if resource == "orders":
            # Set a 204 response code
            self._set_headers(204)
            delete_order(id)

        # Encode the new order and send in response
        self.wfile.write("".encode())

    # def do_PUT(self):
    #     """Handles PUT requests to the server """
    #     self.do_POST()

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "metals":
            success = update_metal(id, post_body)
    # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()

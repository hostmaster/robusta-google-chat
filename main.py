#!/usr/bin/env python
# pylint: disable=unused-argument, import-error, logging-fstring-interpolation, global-statement, fixme

from functools import partial
import signal
import sys
import os
from json import dumps
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests


class WebhookServer:
    """Webhook server"""

    def start_server(self):
        class GoogleChat:
            """Google Chat"""

            def __init__(self, webhook_url: str = None) -> None:
                self.webhook_url = webhook_url

            def send(self, message: str) -> requests.Response:
                """Send a message to a webhook"""
                msg = {"text": message}
                hdrs = {"Content-Type": "application/json; charset=UTF-8"}
                response = requests.post(
                    self.webhook_url, data=dumps(msg), headers=hdrs, timeout=5
                )
                return response

        class WebhookRequestHandler(BaseHTTPRequestHandler):
            """Webhook request handler"""

            protocol_version = "HTTP/1.0"

            def __init__(self, google_chat, *args, **kwargs):
                self.google_chat = google_chat
                super().__init__(*args, **kwargs)

            def _send_response(self, http_code, message=None, headers=None):
                """Sends HTTP response code, message and headers."""
                self.send_response(http_code, message)
                if headers:
                    for header in headers:
                        self.send_header(*header)
                    self.end_headers()

            def do_GET(self):  # pylint: disable=invalid-name
                """Handles HTTP GET requests."""
                self._send_response(
                    200, headers=(("Content-type", "%s; charset=utf-8" % "text/html"),)
                )

            def do_HEAD(self):  # pylint: disable=invalid-name
                """Handles HTTP HEAD requests."""
                self._send_response(
                    200, headers=(("Content-type", "%s; charset=utf-8" % "text/html"),)
                )

            def do_POST(self):  # pylint: disable=invalid-name
                """Handles HTTP POST requests."""
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                data = post_data.decode("utf-8")

                self.google_chat.send(data)

                self._send_response(
                    200, headers=(("Content-type", "%s; charset=utf-8" % "text/html"),)
                )

        port = int(os.getenv("PORT", "8001"))
        webhook_url = os.getenv("WEBHOOK_URL", "undefined")

        server_address = ("", port)
        google_chat = GoogleChat(webhook_url)
        handler = partial(WebhookRequestHandler, google_chat)

        self.httpd = HTTPServer(server_address, handler)
        print(f"Webhook server is running on {port} ...")
        self.httpd.serve_forever()


def exit_now(signum, frame):
    sys.exit(0)


if __name__ == "__main__":
    try:
        forwarder = WebhookServer()
        signal.signal(signal.SIGTERM, exit_now)
        forwarder.start_server()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

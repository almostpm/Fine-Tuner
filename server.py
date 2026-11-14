"""
HTTP Server for Fine Tuner Application.

Provides a local web interface for the Fine Tuner CLI. Uses Python's
standard http.server to serve the UI and handle POST requests for
prompt processing. No external dependencies.
"""

import json
import socketserver
from http.server import SimpleHTTPRequestHandler
from linter import grade_prompt
from optimizer import optimize_prompt

PORT = 8000

class FineTunerHandler(SimpleHTTPRequestHandler):
    """
    Custom request handler that serves the static HTML file
    and handles API POST requests for processing prompts.
    """

    def do_GET(self):
        # Serve index.html by default when hitting the root
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        # Handle API requests
        if self.path == "/api/process":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse incoming JSON
                data = json.loads(post_data.decode("utf-8"))
                prompt = data.get("prompt", "")

                # Run the core engine
                lint_result = grade_prompt(prompt)
                opt_result = optimize_prompt(prompt)

                # Build response
                response_data = {
                    "grade": lint_result["grade"],
                    "feedback": lint_result["feedback"],
                    "optimized": opt_result["optimized"]
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))
                
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    # Allow port reuse to prevent "address already in use" on quick restarts
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), FineTunerHandler) as httpd:
        print(f"🚀 Fine Tuner server running at http://localhost:{PORT}")
        print("Press Ctrl+C to stop.")
        httpd.serve_forever()
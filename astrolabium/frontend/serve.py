#!/usr/bin/env python
"""
Simple HTTP server for the Astrolabium frontend

Serves the frontend on port 3000 with proper CORS headers
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 3000
DIRECTORY = Path(__file__).parent

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def log_message(self, format, *args):
        # Suppress request logs for cleaner output
        if '/favicon.ico' not in args[0]:
            super().log_message(format, *args)

def serve():
    """Start the frontend server"""
    os.chdir(DIRECTORY)

    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        print("=" * 60)
        print("ASTROLABIUM FRONTEND SERVER")
        print("=" * 60)
        print(f"Serving at: http://localhost:{PORT}")
        print("\nMake sure the API server is also running:")
        print("  python api_server_optimized.py")
        print("\nPress Ctrl+C to stop")
        print("-" * 60)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()

if __name__ == "__main__":
    serve()
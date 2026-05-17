import os
import json
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 8000

class CMSHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/save':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                payload = json.loads(post_data.decode('utf-8'))
                
                filename = payload.get('filename')
                html_content = payload.get('html')
                
                # Basic security validation
                if not filename or '/' in filename or '\\' in filename or not filename.endswith('.html'):
                    self.send_error(400, "Invalid Filename")
                    return
                
                # Write to the file in the current working directory
                file_path = os.path.join(os.getcwd(), filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                # Respond success
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "message": f"{filename} saved successfully"}).encode('utf-8'))
                print(f"🟢 Saved {filename} to local disk successfully.")
            except Exception as e:
                self.send_error(500, f"Error saving file: {str(e)}")
        else:
            self.send_error(404, "API Endpoint Not Found")

    def end_headers(self):
        # Enable CORS for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, CMSHandler)
    print(f"🚀 Shaurya Portfolio Local CMS Server is running at http://localhost:{PORT}")
    print(f"📂 Serving local files from: {os.getcwd()}")
    print("👉 Direct edits will be saved directly to your local HTML files.")
    print("⌨️ Press Ctrl+C to stop the server.")
    
    # Auto-open browser in new tab
    webbrowser.open_new_tab(f"http://localhost:{PORT}/admin.html")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped successfully.")

if __name__ == '__main__':
    run_server()

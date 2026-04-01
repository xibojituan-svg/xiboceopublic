import http.server
import socketserver
import urllib.request
import json
import os

PORT = 8888
API_BASE = "https://ops.xibojiaoyu.com/xmkp-backend-middle/ops/qwChat"

class ProxyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 加上通用跨域头，防止前端本地开发时拦截
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path.startswith('/api/qwChat/'):
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            endpoint = self.path.replace('/api/qwChat/', '/')
            target_url = API_BASE + endpoint
            
            req = urllib.request.Request(target_url, data=post_data, method='POST')
            req.add_header('Content-Type', 'application/json')
            req.add_header('Accept', 'application/json')
            
            try:
                with urllib.request.urlopen(req) as response:
                    res_body = response.read()
                    self.send_response(response.status)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(res_body)
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(e.read())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"code": 500, "message": str(e)}).encode('utf-8'))
        elif self.path == '/api/save_report':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                uid = str(data.get('uid', 'unknown'))
                name = str(data.get('name', 'unknown'))
                report = data.get('report', '')
                
                target_dir = os.path.join(os.getcwd(), '用户画像数据')
                os.makedirs(target_dir, exist_ok=True)
                
                file_name = f"{uid}_{name}.md"
                file_path = os.path.join(target_dir, file_name)
                
                if os.path.exists(file_path):
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"code": 200, "status": "exists"}).encode('utf-8'))
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(report)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"code": 200, "status": "saved"}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"code": 500, "message": str(e)}).encode('utf-8'))
        else:
            super().do_POST()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == '__main__':
    # 强制切换到当前脚本所在目录，确保可以访问 html 文件
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("=" * 50)
    print(f"🚀 解码器本地代理服务启动成功！")
    print(f"👉 请在浏览器访问：http://localhost:{PORT}/用户需求解码器.html")
    print("=" * 50)
    
    with ThreadedTCPServer(("", PORT), ProxyHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n关闭服务.")

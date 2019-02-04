from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import settings


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        if self.path.startswith('/set'):
            self.wfile.write(b'Test')
        else:
            viss = settings.get("core", "vis_list")
            print(viss)
            print(parse_qs(urlparse(self.path).query))
            out = '<html>'
            for v in viss:
                custom = settings.get("custom", v)
                print (custom)
                out += '<div>'
                out += v
                out += ' - '
                for s in custom:
                    out += s['name'] + ":" + s['type'] + "<br/>"
                out += '</div><hr/>'
            out += '</html>'
            self.wfile.write(bytes(out, 'utf-8'))


HTTPServer(('localhost', 8000), Handler).serve_forever()

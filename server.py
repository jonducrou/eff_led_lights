from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import settings
from pystalkd.Beanstalkd import Connection
import json

#BS = Connection()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        out = '<html>'
        if self.path.startswith('/set'):
            qs = parse_qs(urlparse(self.path).query)
            print(qs)
            vis = qs['vis'][0]
            cust = settings.get("custom", vis)
            for q in qs:
                if not "vis" == q:
                    print(vis)
                    print(q)
                    print(qs[q][0])
                    print(cust)
                    for c in cust:
                        if c['name'] == q:
                            if "number" == c['type']:
                                settings.set(vis, q, int(qs[q][0]))
                            elif "rgb" == c['type']:
                                rgb = json.loads(qs[q][0])
                                if len(rgb) == 3:
                                    settings.set(vis, q, rgb)
#            BS.put('{"action":"update","params":"'+ vis + '"}')
        viss = settings.get("core", "vis_list")
        print(viss)

        for v in viss:
            custom = settings.get("custom", v)
            print(custom)
            out += '<div><form action="/set" method="GET"/><input type="hidden" name="vis" value="' + v + '"/>'
            out += v
            out += '<br/>'
            for s in custom:
                out += s['name']
                if s['type'] == 'number':
                    x = settings.get(v, s['name'])
                    print(x)
                    out += '<input type="text" name="' + s['name']
                    out += '" value="' + str(x) + '"/>'
                elif s['type'] == 'rgb':
                    x = settings.get(v, s['name'])
                    print(x)
                    out += '<input type="text" name="' + s['name']
                    out += '" value="' + str(x) + '"/>'
                else:
                    out += s['name'] + ":" + s['type'] + "<br/>"
                out += '<br/>'
            out += '<input type="submit"/></form></div><hr/>'
        out += '</html>'
        self.wfile.write(bytes(out, 'utf-8'))


HTTPServer(('localhost', 8000), Handler).serve_forever()

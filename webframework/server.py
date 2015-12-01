#!/usr/bin/python
import importlib
import asyncio
import url
import json
from aiohttp import web

host = "0.0.0.0"
port = 9011
origin = "*"
verbose_errors = True
verbose_logging = True

@asyncio.coroutine
def handle(request):
  s = "api."
  if 'project' in request.match_info:
    s += request.match_info['project'] + "."
  if 'module' in request.match_info:
    s += request.match_info['module'] + "." 
  if 'action' in request.match_info:
    s += request.match_info['action']
  if verbose_logging:
    print("Incoming request - " + str(request.raw_path))
  try:
    module = importlib.import_module(s)
    arguments = url.parse(request.GET, module.arguments)
    response = yield from module.process(arguments)
    if 'json' in response:
      # Dump to json if the module wants to return json
      return respond(headers=response.get('headedrs', {}),
                    status=response.get('status', 200),
                    text=json.dumps(response.get("json", "")),
                    content_type="application/json")
    else:
      return respond(headers=response.get('headedrs', {}),
                    status=response.get('status', 200),
                    text=response.get("text", ""))
  except ImportError:
    return respond(status=404, text="Page does not exist")
  except Exception as e:
    s = str(e.args) if verbose_errors else "No verbose errors."
    return respond(status=500, text="Error while querying data.\n" + s)

def respond(headers={}, status=200, text="", content_type="text/plain"):
  headers['Access-Control-Allow-Origin'] = origin
  if verbose_logging:
    print("Response - Headers:",headers, "Status:", status, "Content-type:",content_type)
    print("Text:", text)
  return web.Response(headers=headers, status=status, text=text, content_type=content_type)

@asyncio.coroutine
def init(loop, host='localhost', port=9011):
  app = web.Application(loop=loop)
  app.router.add_route('GET', '/{action}', handle)
  app.router.add_route('GET', '/{module}/{action}', handle)
  app.router.add_route('GET', '/{project}/{module}/{action}', handle)

  srv = yield from loop.create_server(app.make_handler(), host, port)
  print("Server started at http://" + host + ":" + str(port))
  return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop, host=host, port=port))
loop.run_forever()

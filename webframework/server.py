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

@asyncio.coroutine
def handle(request):
  s = "api."
  if 'project' in request.match_info:
    s += request.match_info['project'] + "."
  if 'module' in request.match_info:
    s += request.match_info['module'] + "." 
  if 'action' in request.match_info:
    s += request.match_info['action']
  try:
    module = importlib.import_module(s)
    arguments = url.parse(request.GET, module.arguments)
    response = yield from module.process(arguments)

    # Build response
    final_response = {}
    final_headers = response.get('headers', {})
    final_headers["Access-Control-Allow-Origin"] = origin 
    final_response['headers'] = final_headers
    final_response['status'] = response.get('status', 200)
    if 'json' in response:
      # Dump to json if the module wants to return json
      final_response["text"] = json.dumps(response['json'])
      final_content = "application/json"
    else:
      # Else, return as raw output
      final_response["text"] = response.get("text", "")
      final_content = "text/plain"
    # And send it
    return web.Response(headers=final_response['headers'], status=final_response['status'], text=final_response['text'], content_type = final_content)
  except ImportError:
    return web.Response(headers={"Access-Control-Allow-Origin":origin}, status=404, text="Page does not exist.")
  except Exception as e:
    s = str(e.args) if verbose_errors else "No verbose errors."
    return web.Response(headers={"Access-Control-Allow-Origin":origin}, status=500, text="Error while querying data.\n" + s)

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

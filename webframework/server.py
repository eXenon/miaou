#!/usr/bin/python
"""
  A aiohttp based webserver with a few extended functionalities :
  - automatic dispatch of a URL to an imported python file, using default
    routes referring to the corresponding python module.
  - url.py handles argument parsing with requirement given by the modules.
  - session.py handles basic sessions using Redis as a server-side storage.
"""

import importlib
import asyncio
import json
import url
import re
import sessions
from aiohttp import web

host = "0.0.0.0"
port = 9011
origin = "*"
verbose_errors = True
verbose_logging = True

@asyncio.coroutine
def handle(request):

  # URL Parsing
  s = "api."
  if 'project' in request.match_info:
    p = re.sub('[^0-9a-zA-Z]+', '', request.match_info['project'])
    s += p + "."
  if 'module' in request.match_info:
    p = re.sub('[^0-9a-zA-Z]+', '', request.match_info['module'])
    s += p + "." 
  if 'action' in request.match_info:
    p = re.sub('[^0-9a-zA-Z]+', '', request.match_info['action'])
    s += p
  if verbose_logging:
    print("Incoming request - " + str(request.raw_path))

  # Session loading
  if "cookie" in request.headers and  "AIOHTTP_SESSION" in request.headers["cookie"]:
    cookies = request.headers.getall("cookie")[0]
    aiocookie = re.search("AIOHTTP_SESSION=([0-9a-z]{32})", cookies)
    if aiocookie:
      session = sessions.Session(aiocookie.group(1))
      if verbose_logging:
        print("Session ID - " + session.id)
    else:
      session = sessions.Session() 
      if verbose_logging:
        print("New Session with ID - " + session.id)
  else: 
    session = sessions.Session() 
    if verbose_logging:
      print("New Session with ID - " + session.id)

  # Response building
  try:
    module = importlib.import_module(s)
    arguments = url.parse(request.GET, module.arguments)
    response = yield from module.process(session, arguments)
    headers = response.get('headers', {})
    if session.is_new_session:
      headers.update({"Set-Cookie": "AIOHTTP_SESSION=" + session.id})
    if 'json' in response:
      # Dump to json if the module wants to return json
      return respond(headers=headers,
                    status=response.get('status', 200),
                    text=json.dumps(response.get("json", "")),
                    content_type="application/json")
    else:
      return respond(headers=headers,
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

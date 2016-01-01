import asyncio

arguments = { 'hello': { 'required': True },
              'integer': { 'required': False, 'default': 0, 'parser': lambda x:int(x) },
              'optional': { 'required': False },
            }

@asyncio.coroutine
def process(session, args):
  return { 'json': args }

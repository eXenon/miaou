import asyncio

arguments = { 'hello': { 'required': True },
              'integer': { 'required': False, 'default': 0, 'parser': lambda x:int(x) },
              'optional': { 'required': False },
            }

@asyncio.coroutine
def process(args):
  print(args)
  return { 'json': args }

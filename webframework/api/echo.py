import asyncio


@asyncio.coroutine
def process(args):
  print(args)
  return { 'body': str(args).encode() }

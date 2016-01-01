import asyncio

arguments = { 'save': { 'required': False, 'default': False },
            }

@asyncio.coroutine
def process(session, args):
  if args["save"]:
    session['save'] = str(args["save"])
    return {"text": "Saved."}
  else:
    return { 'text': "From memory : " + session["save"] }

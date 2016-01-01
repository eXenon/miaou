"""
  Rudimentary argument parser to ensure that the called modules have expected arguments
  at their disposal.

  Modules should expose the 'arguments' dictionnary with following structure :
  { <argument name> : { "required": <bool>,      -- is this argument optional ?
                        "parser": <function>     -- a function that will be applied to the argument [optional]
                        "default": <any>         -- default value of the argument [optional]
                      }
  }
"""

def parse(urlargs, requirements):
  acc = {}
  for arg in requirements:
    if arg in urlargs:
      if 'parser' in requirements[arg]:
        acc[arg] = requirements[arg]['parser'](urlargs[arg])
      else:
        acc[arg] = urlargs[arg]
    elif not 'required' in requirements[arg]:
      raise ValueError("the 'required' value is not optional when declaring args")
    elif not requirements[arg]['required']:
      if 'default' in requirements[arg]:
        acc[arg] = requirements[arg]['default']
    elif requirements[arg]['required']:
      raise ValueError("required argument %s is not present in the request" % arg)
  return acc

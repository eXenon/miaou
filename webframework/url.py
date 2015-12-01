"""
  Rudimentary argument parser to ensure that the called modules have expected arguments
  at their disposal
"""

def parser(urlargs, requirements):
  acc = {}
  for arg in requirements:
    if arg in urlargs:
      if 'parser' in requirements[arg]
        acc[arg] = requirements[arg]['parser'](urlargs[arg])
      else:
        acc[arg] = urlargs[arg]
    elif not 'required' in requirements[arg]:
      raise ValueError("the 'required' value is not optional when declaring args")
    elif not requirements[arg]['required']:
      if 'default' in requirements[arg]:
        acc[arg] = requirements['default']
      else:
        raise ValueError("expected default for optional argument %s" % arg)
    elif requirements[arg]['required']:
      raise ValueError("required argument %s is not present in the request" % arg)
  return acc

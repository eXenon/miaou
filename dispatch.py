#!/usr/bin/python3

# An extension for Monica that allows to repeat commands
# and execute several iterations of the loop in parallel threads.


from multiprocessing import Pool
import helper
import itertools
import re
import os


def execute(cmd):
  print("Executing",cmd)
  os.system(cmd)

def dispatch(cmd):
  # This is the command called from MONICA, with the
  # exact command typed in by the user after "monica-dispatch"
  
  # Command Queue building :
  #  monica-dispatch echo {{<builder>:<argument>}}
  #   -> will execute "echo" with the successive values returned bt the builder
  #      as argument. By default, 50 threads will be created.
  # Builders :
  #  {{file: <filename>}}
  #   -> will return successively every line of the file
  #   -> Example : echo {{file: /path}} will print the file /path
  #  {{range:<start>:<stop>:<step>}}
  #   -> will return every integer from start to stop with interval step
  # If there are several builders :
  #  Every combination of values will be called ! This can make a lot of 
  #  combinations really quickly ! AVOID !

  # Extract builders :
  builders = []
  if re.search("\{\{.*?\}\}", cmd):
    for builder in re.finditer("\{\{(.*?)\}\}", cmd):
      builders.append(builder.group(1))

  # Build an iterable object for every builder :
  builder_iterators = []
  for builder in builders:
    typ = builder.split(":")[0]
    args = builder.split(":")[1:]
    if typ == "range":
      builder_iterators.append(build_range(args))
    elif typ == "file":
      builder_iterators.append(build_file_iterator(args[0]))

  # Build the product of the builder iterators
  builder_product = itertools.product(*tuple(builder_iterators))
 
  # Split the string and rebuild it with arguments :
  splitted_cmd = re.split("\{\{.*?\}\}", cmd)
  finalecmds = []
  for i in builder_product:
    # This ugly one-liner allows to concatenate every part of the command
    # together. The idea is to interlace the spliited_cmd elements with
    # the arguments and concatenate everytihng into a string, giving the
    # final command.:
    cmd = "".join( [a+b for a,b in zip(splitted_cmd, i)])
    if len(splitted_cmd) > len(i):
      cmd += splitted_cmd[-1]
    finalecmds.append(cmd)

  # Give the user the possibility to abort and printout the first few commands
  print("First few commands :")
  for i in range(min(5, len(finalecmds))):
    print(finalecmds[i])
  if not helper.query_yes_no("Launch it ?"):
    print("Aborted.")
    return False

  # Launch it all for good :
  pool = Pool(processes=1)
  pool.map(execute, finalecmds)

  # Close all file handlers
  for b in builder_iterators:
    if "close" in dir(b):
      print("Closing file")
      b.close() 


def build_range(args):
  if len(args) == 2:
    return range(int(args[0]), int(args[1]))
  elif len(args) == 3:
    return range(int(args[0]), int(args[1]), int(args[2]))

def build_file_iterator(path):
  with open(path, "r") as f:
    return f.read().splitlines()

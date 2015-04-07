
# PowerZip

# A little utility that creates a self-extracting powershell file.
# It takes a folder and converts every file into base64. Then prints out
# a powershell script extracting the same directory structure and files.

import sys
import base64
from itertools import chain
from glob import glob
import os

def powerzip(outfile, *to_zip):
  # to_zip contains a list of files and directories to zip, paths are all relative
  pref = "$Base64=\""
  suff = "\";$Content = [System.Convert]::FromBase64String($Base64);Set-Content -Path $env:temp\FILENAME -Value $Content -Encoding Byte;"
  addir = "New-Item -ItemType directory -Path $env:temp\DIRNAME;"
  acc = ""
  matches = []
  for folder in to_zip:
    for root, dirnames, filenames in os.walk(folder):
      for filename in filenames:
        matches.append(os.path.join(root, filename))

  for f in matches:
    if os.path.isdir(f):
      # Create directories before writing files to them
      diracc = f.split("/")[0]
      for sdir in f.split("/")[1:-1]:
        acc +=  addir.replace("DIRNAME", diracc)
        diracc += sdir + "\\"
    
    with open(f, "rb") as bf:
      s = base64.b64encode(bf.read()).decode()
      acc += pref + s + suff.replace("FILENAME", f.replace("/","\\")) + "\n"
  
  with open(outfile, "w") as o:
    print(acc, file=o)

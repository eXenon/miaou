
# PowerZip

# A little utility that creates a self-extracting powershell file.
# It takes a folder and converts every file into base64. Then prints out
# a powershell script extracting the same directory structure and files.

import sys
import base64
from itertools import chain
from glob import glob
import os

pref = "$Base64=\""
suff = "\";$Content = [System.Convert]::FromBase64String($Base64);Set-Content -Path $env:temp\FILENAME -Value $Content -Encoding Byte;"
addir = "New-Item -ItemType directory -Path $env:temp\DIRNAME;"
acc = ""
files = []

result = [y for x in os.walk(sys.argv[1]) for y in glob(os.path.join(x[0], '*.txt'))]
print(result)


for f in sys.argv[2:]:
	if f.find("/") >= 0:
		# Create directories before writing files to them
		diracc = f.split("/")[0]
		for sdir in f.split("/")[1:-1]:
			acc +=  addir.replace("DIRNAME", diracc)
			diracc += sdir + "\\"
	with open(f, "rb") as bf:
		s = base64.b64encode(bf.read())
		acc += pref + s + suff.replace("FILENAME", f.replace("/","\\"))

with open(sys.argv[1], "w") as o:
	o.write(acc)

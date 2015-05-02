# helpers/bin.py
# A few generic functions to manipulate binary/hex data

def hexdecode(s):
  # Convert HEX to ASCII
  buff = s.replace(" ", "")
  acc = ""
  while len(buff) > 1:
    acc += chr(int(buff[0:2], 16))
    buff = buff[2:]
  return acc

def memdumpdecode(s):
  # Convert a memory dump into ASCII
  byte = s.split(" ")
  acc2 = ""
  for b in byte:
    acc = ""
    for i in range(0,8,2):
      acc = chr(int(b[i:i+2], 16)) + acc
    acc2 += acc
  return acc2

def bytes_from_file(path, f):
  # Load a byte string from file and give
  # it to f as argument
  with open(path, "rb") as file:
    s = file.read()
  return f(s)


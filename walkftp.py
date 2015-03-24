#!/usr/bin/python3

# An extension for Monica allowing to recursively list FTPs

import ftplib
import socket
import sys

def ftp_walk_recursive(ftp, root):
  elts = ftp.nlst(root)
  if elts == None:
    return None
  for l in elts:
    try:
      # Going deep !
      ftp.cwd(l)
      print("Path :", root + l.split(" ")[-1])
      ftp_walk_recursive(ftp, root=root + l.split(" ")[-1])
      ftp.cwd("..")
    except:
      # usual file
      print("File :", l)


def ftp_walk(ip, user="anonymous", pwd="", port=21):
  try:
    print("Connecting to",ip,"as", user)
    ftp = ftplib.FTP(ip)
    ftp.login(user, pwd)
    ftp.cwd("/")
    ftp_walk_recursive(ftp, "/")
  except ftplib.error_perm:
    print("Access denied.")
    return False
  except socket.error:
    print("FTP seems down.")
    return False
  return True
 

if __name__ == "__main__":
  ftp_walk(sys.argv[1]) 

#
#  Crypto utilities
#

import random
import string

FRENCH = [" ", "e","s","a","i","t","n","r","u","l","o","d","c","p","m","é","v","q","f","b","g","h","j","à","x","y","è","ê","z","w","ç","ù","k","î","œ","ï","ë"]

def bruteforce_Factory(length=5):
  # Returns functions that will simply return consecutive strings
  def bf(i):
    return chr(i) + (length - 1) * "A"
  return bf

def bruteforce_Cesarcode(s):
  # Simply print out the 5 first caracters
  # for every possible shift value
  for i in range(255):
    print("For shift " + str(i) + " " + "".join([chr((ord(c) + i) % 255) for c in s[:5]]))

def decrypt_Cesarcode(s, shift):
  # Shift'n some bytes back
  return "".join([chr((ord(c) + shift) % 255) for c in s])

def fuzzing_Factory(length=5):
  # Returns functions that will spew random strings
  def ff(i):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
  return ff

def char_freq(s, file=False):
  # Print out the frequencies of every
  # alphabet caracter in a string or file
  st = s
  if file:
      with open(s, "r") as f:
        st = f.read()
  occurences = {}
  for c in st:
    if c in occurences.keys():
      occurences[c] += 1
    else:
      occurences[c] = 1
  occurences_array = [[occurences[k], k] for k in occurences.keys()]
  occurences_array.sort(reverse=True)
  for freq, c in occurences_array:
    print(c + " appears " + str(freq/len(st)*100) + "%")
  return occurences_array

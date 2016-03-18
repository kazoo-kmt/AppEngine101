from google.appengine.ext import ndb


def sha256(string):
  from hashlib import sha256
  return sha256(string).hexdigest()


class FailedAuthorizationException(Exception):
  pass

class UsernameInUseException(Exception):
  pass

class EmailInUseException(Exception):
  pass


class User(ndb.Model):
  email    = ndb.StringProperty(indexed=True)
  password = ndb.StringProperty(indexed=True)
  username = ndb.StringProperty(indexed=True)
  
  def toPublicDict(self):
    return {
      'email': self.email,
      'username': self.username
    }
  
  def toPrivateDict(self):
    return {
      'email': self.email,
      'username': self.username,
      'auth': self.getAuth()
    }
  
  def delete(self):
    self.key.delete()
  
  def getAuth(self):
    return 'auth_{}'.format(self.email)
  
  @classmethod
  def getByAuth(cls, authtoken):
    email = authtoken[5:]
    user = cls.getByEmail(email)
    return user
  
  @classmethod
  def getByEmail(cls, email):
    return cls.query(cls.email == email).get()
  
  @classmethod
  def hasByEmail(cls, email):
    return cls.query(cls.email == email).count() != 0
  
  @classmethod
  def getByUsername(cls, username):
    return cls.query(cls.username == username).get()
  
  @classmethod
  def hasByUsername(cls, username):
    return cls.query(cls.username == username).count() != 0
  
  @classmethod
  def queryAll(cls):
    return cls.query()
  
  @classmethod
  def signup(cls, email, password, username):
    if cls.hasByEmail(email): raise EmailInUseException()
    if cls.hasByUsername(username): raise UsernameInUseException()
    
    user = cls()
    
    user.email = email
    user.password = sha256(password)
    user.username = username
    
    user.put()
    return user



def RequireAuth(funct):
  def helper(self, *args, **kwargs):
    auth = self.request.headers['X-Authorization']
    user = User.getByAuth(auth)
    if not user: raise FailedAuthorizationException()
    kwargs['user'] = user
    return funct(self, *args, **kwargs)
  return helper
  
  
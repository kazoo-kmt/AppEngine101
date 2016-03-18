from google.appengine.ext import ndb


class InvalidPermissionsException(Exception):
  pass


class Todo(ndb.Model):
  title     = ndb.StringProperty  (indexed=True)
  userkey   = ndb.KeyProperty     (indexed=True)
  completed = ndb.BooleanProperty (indexed=True, default=False)
  
  def toPrivateDict(self):
    return {
      'title'    : self.title,
      'user'     : self.userkey.get().toPublicDict(),
      'completed': self.completed,
      'todoid'   : self.key.id()
    }
  
  @classmethod
  def queryByUser(cls, user):
    return cls.query(cls.userkey == user.key)
  
  def requireOwner(self, user):
    if not user.key == self.userkey:
      raise InvalidPermissionsException()
  
  def delete(self, user):
    self.requireOwner(user)
    self.key.delete()
  
  def complete(self, user):
    self.requireOwner(user)
    self.completed = True
    self.put()
  
  @classmethod
  def create(cls, title, author):
    todo = cls()
    
    todo.title = title
    todo.userkey = author.key
    
    todo.put()
    return todo
  

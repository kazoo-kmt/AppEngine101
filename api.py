import webapp2
import json
import logging
import traceback

from lib.models.User import *
from lib.models.Todo import *


class MissingParameterException(Exception):
  pass


errormap = {
  MissingParameterException: (102, 'Missing parameter'),
  FailedAuthorizationException: (103, 'Auth failed'),
  EmailInUseException: (104, 'email in use'),
  UsernameInUseException: (105, 'username in use'),
  InvalidPermissionsException: (106, 'Invalid todo permissions')
}


class APIRequestHandler(webapp2.RequestHandler):
  def dispatch(self):
    try:
      if not self.request.method.lower() in ['get', 'delete']:
        self.request.json = json.loads(self.request.body)
      response = super(APIRequestHandler, self).dispatch()
      if not response:
        response = {}
      response['success'] = True
    except Exception as error:
      error_cls = error.__class__
      if error_cls in errormap:
        code, message = errormap[error_cls]
      else:
        code, message = (-1, 'Unknown error')
        logging.error(error)
        traceback.print_exc()
      
      self.error(500)
      response = {
        'success': False,
        'message': message,
        'code'   : code
      }
    
    text_response = json.dumps(response)
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(text_response)


class UsersHandler(APIRequestHandler):
  def post(self):
    try:
      email    = self.request.json['email']
      password = self.request.json['password']
      username = self.request.json['username']
    except:
      raise MissingParameterException()
    
    user = User.signup(email, password, username)
    return user.toPrivateDict()
  
  @RequireAuth
  def delete(self, user=None):
    user.delete()
    return {}
  
  @RequireAuth
  def get(self, user=None):
    users = User.queryAll()
    return {
      'users': [user.toPublicDict() for user in users]
    }
    
    
class TodoHandler(APIRequestHandler):
  @RequireAuth
  def post(self, user=None):
    try:
      title = self.request.json['title']
    except:
      raise MissingParameterException()
    
    todo = Todo.create(title, user)
    return { 'todo': todo.toPrivateDict() }
  
  @RequireAuth
  def get(self, user=None):
    todos = Todo.queryByUser(user)
    return {
      'todos': [todo.toPrivateDict() for todo in todos]
    }


class TodoByIdHandler(APIRequestHandler):
  @RequireAuth
  def put(self, todoid, user=None):
    todo = Todo.get_by_id(int(todoid))
    todo.complete(user)
    return {}
  
  @RequireAuth
  def delete(self, todoid, user=None):
    todo = Todo.get_by_id(int(todoid))
    todo.delete(user)
    return {}


app = webapp2.WSGIApplication([
  ('/api/v1/users', UsersHandler),
  ('/api/v1/todo', TodoHandler),
  ('/api/v1/todo/(\d+)', TodoByIdHandler)
], debug=True)
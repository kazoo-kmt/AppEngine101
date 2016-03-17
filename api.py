import webapp2
import json

from User import User


class MissingParameterException(Exception):
  pass


errormap = {
  MissingParameterException: (102, 'Missing parameter')
}


class APIRequestHandler(webapp2.RequestHandler):
  def dispatch(self):
    try:
      if self.request.method.lower() != 'get':
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
    return user.toDict()
    
  def get(self):
    users = User.queryAll()
    return {
      'users': [user.toDict() for user in users]
    }
    
    


class DefaultHandler(APIRequestHandler):
  def get(self):
    self.response.write('Hello World!')


app = webapp2.WSGIApplication([
  ('/api/v1/users', UsersHandler),
  ('.*', DefaultHandler)
], debug=True)
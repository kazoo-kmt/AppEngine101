import webapp2
import json

from User import User

class UsersHandler(webapp2.RequestHandler):
    def get(self):
        json_body = json.loads(self.request.body)
        email = json_body[]
        email = json_body[]
        email = json_body[]
        user =  User.signup(email, password, username)

    def post(self):
        pass

class DefaultHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello World!')

app = webapp2.WSGIApplication([
    ('/api/v1/users', UsersHandler),
    ('.*', DefaultHandler)
], debug=True)

from google.appengine.ext import ndb

class User(ndb.Model):
    email    = ndb.StringProperty(indexed=True)
    password = ndb.StringProperty(indexed=True)
    username = ndb.StringProperty(indexed=True)

    @classmethod
    def signup(cls, email, password, username):
        user = cls()

        user.email = email
        user.password = password
        user.username = username

        user.put()
        return user

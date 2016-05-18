from google.appengine.ext import ndb


class Vseofilmu(ndb.Model):
    naslov = (ndb.StringProperty()
    ocena = ndb.IntegerProperty()
    ocenjevalec = ndb.StringProperty()
    mnenje = ndb.StringProperty()
    slika = ndb.TextProperty()
    ustvarjeno = ndb.DateTimeProperty(auto_now_add=True)
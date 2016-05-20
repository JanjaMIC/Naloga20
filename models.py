from google.appengine.ext import ndb


class Vseofilmu(ndb.Model):
    naslov = ndb.StringProperty()
    ocena = ndb.IntegerProperty()
    ocenjevalec = ndb.StringProperty()
    mnenje = ndb.StringProperty()
    slika = ndb.StringProperty()
    ustvarjeno = ndb.DateTimeProperty(auto_now_add=True)
              
              

class Uporabnik(ndb.Model):
    ime = ndb.StringProperty()
    priimek = ndb.StringProperty()
    email = ndb.StringProperty()
    sifrirano_geslo = ndb.StringProperty()
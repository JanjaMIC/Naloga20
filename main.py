#!/usr/bin/env python
import os
import jinja2
import webapp2
import cgi
from models import Vseofilmu


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")


class PosljiSporociloHandler(BaseHandler):
    def popravi_input(self, spremenljivka):
        return cgi.escape(spremenljivka)


    def post(self):
        naslov = self.request.get("naslov")
        ocena = int(self.request.get("ocena"))
        ocenjevalec = self.request.get("ocenjevalec")
        mnenje = self.request.get("mnenje")
        slika = self.request.get("slika")

        naslov = self.popravi_input(naslov)
        ocena = self.popravi_input(ocena)
        ocenjevalec = self.popravi_input(ocenjevalec)
        mnenje = self.popravi_input(mnenje)
        slika = self.popravi(slika)


        sporocilo = Vseofilmu(naslov=naslov, ocena=ocena, slika=slika, ocenjevalec=ocenjevalec, mnenje=mnenje)
        sporocilo.put()

        view_vars = {"naslov": naslov, "ocena": ocena, "slika": slika}

        return self.render_template("poslano.html", view_vars)


class PrikaziSporocilaHandler(BaseHandler):
    def get(self):
        vsa_sporocila = Vseofilmu.query().order(Vseofilmu.ustvarjeno).fetch()

        view_vars = {
            "vsa_sporocila": vsa_sporocila
        }

        return self.render_template("prikazi_vnose.html", view_vars)


class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Vseofilmu.get_by_id(int(sporocilo_id))

        view_vars = {
            "sporocilo": sporocilo
        }

        return self.render_template("posamezen_vnos.html", view_vars)


class UrediSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Vseofilmu.get_by_id(int(sporocilo_id))

        view_vars = {
            "sporocilo": sporocilo
        }

        return self.render_template("uredi_sporocilo.html", view_vars)

    def post(self, sporocilo_id):
        sporocilo = Vseofilmu.get_by_id(int(sporocilo_id))
        sporocilo.naslov = self.request.get("naslov")
        sporocilo.ocena = int(self.request.get("ocena"))
        sporocilo.ocenjevalec = self.request.get("ocenjevalec")
        sporocilo.slika = self.request.get("slika")
        sporocilo.put()

        self.redirect("/sporocilo/" + sporocilo_id)


    def post(self, sporocilo_id):
        sporocilo = Vseofilmu.get_by_id(int(sporocilo_id))
        sporocilo.naslov = self.request.get("naslov")
        sporocilo.ocena = int(self.request.get("ocena"))
        sporocilo.ocenjevalec = self.request.get("ocenjevalec")
        sporocilo.mnenje = self.request.get("mnenje")
        sporocilo.slika = self.request.get("slika")
        sporocilo.put()

        self.redirect("/sporocilo/" + int(sporocilo_id))

class IzbrisiSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Vseofilmu.get_by_id(int(sporocilo_id))

        view_vars = {
            "sporocilo": sporocilo
        }

        return self.render_template("izbrisi_sporocilo.html", view_vars)

    def post(self, sporocilo_id):
        sporocilo = Vseofilmu.get_by_id(int(sporocilo_id))
        sporocilo.key.delete()

        self.redirect("/prikazi_vnose")



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/poslano', PosljiSporociloHandler),
    webapp2.Route('/prikazi_vnose', PrikaziSporocilaHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/uredi', UrediSporociloHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/izbrisi', IzbrisiSporociloHandler),
], debug=True)

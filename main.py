#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Sporocilo

from datetime import datetime

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
        return self.render_template("hello.html")

class BlogHandler(BaseHandler):
    def get(self):
        # iz baze fiktivno dobim podatke
        params = {
            "sporocilo": "To je moje sporocilo",
            "drugo_sporocilo": "Nekaj je na nebyu"
        }

        return self.render_template("blog.html", params=params)

class SporociloHandler(BaseHandler):
    def get(self):
        # iz baze fiktivno dobim podatke
        params = {}
        return self.render_template("vpisi-sporocilo.html", params=params)

    def post(self):
        vnos = self.request.get('vnos')
        avtor = self.request.get('avtor')
        nastanek = self.request.get('nastanek')

        # nastanek = datetime.strptime('2011-11-11 12:12', '%Y-%m-%d %H:%M')

        # s tem smo dobili iz htmlja iz
        # input boxa, ki mu je bilo ime "vnos", tisto sporocilo

        # shrani podatke v bazo
        sporocilo = Sporocilo(vnos=vnos, avtor=avtor)# , nastanek=nastanek) # to se ustvari objekt
        sporocilo.put() # s tem shranimo ta objekt v bazo

        return self.write("Uspesno si vnesel sporocilo.")

class MojHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template("base.html", params=params)

class SporocilaHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template("sporocila.html", params=params)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))

        params = {
            "sporocilo": sporocilo
        }

        return self.render_template("posamezno-sporocilo.html", params=params)

class SeznamSporocilHandler(BaseHandler):
    def get(self):
        seznam = Sporocilo.query().fetch()

        params = {
            "seznam": seznam
        }

        return self.render_template("seznam-sporocil.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/blog/', BlogHandler),
    webapp2.Route('/vnos-sporocila/', SporociloHandler),
    webapp2.Route('/base/', MojHandler),
    webapp2.Route('/sporocila/', SporocilaHandler),
    webapp2.Route('/seznam-sporocil/', SeznamSporocilHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/', PosameznoSporociloHandler)
    # webapp2.Route('/vpisi-sporocilo/', SporociloHandler)
], debug=True)

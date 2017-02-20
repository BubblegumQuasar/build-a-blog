#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import jinja2
import os

from google.appengine.ext import db


# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


# class to set up blog posts:

class Blogpost(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class Handler(webapp2.RequestHandler):
    blog = db.GqlQuery("SELECT * FROM Blogpost ORDER BY created DESC LIMIT 5")
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(**params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


    

class MainPage(Handler):
    def render_posts(self, title="", content="", error=""):
       self.render("main-page.html" title=title, content=content, error=error, blog=blog)

class NewPost(Handler):
    def get(self):
        self.render("submit.html" title=title, content=content, error=error)

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

        if title and content:
            a = Blogpost(title=title, content=content)
            a.put()

            self.redirect("/blog")
        else:
            error = "We need both a title and some content!"
            self.render(title, content, error)



app = webapp2.WSGIApplication([
    ('/blog', MainPage),
    ('/', NewPost)
], debug=True)


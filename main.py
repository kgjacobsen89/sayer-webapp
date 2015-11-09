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
import os
import webapp2
# from jinja2 import Environment, PackageLoader
import jinja2
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
import json
from google.appengine.api import urlfetch
url = "http://sayerapp-oauth.cloudapp.net/api/v1/sooth/4677"
headers = {"Accept": "application/json",
               "Content-Type": "application/json",
               "Authorization": "Basic _authcode_"}

options = {"method": "GET",
               "headers": headers
               }
response = urlfetch.fetch(url, options)
result = urlfetch.fetch(url)
the_dict = {}
if result.status_code == 200:
    the_dict = json.loads(response.content)
    print the_dict['result']['status']

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # self.response.write('Hello world!')
        template = jinja_env.get_template('index.html')

        self.response.write(template.render(the_dict))

        value = str(self.request.get('clientID'))
        self.response.set_cookie(key='clientID', value=value)

    def post(self):


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

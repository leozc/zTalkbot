import sys
sys.path.insert(0, "packages.zip")
import cgi
import datetime
import urllib
import wsgiref.handlers
import json
import os
import logging
import string
import hmac, hashlib, base64

from google.appengine.api import urlfetch

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import taskqueue
from google.appengine.api.taskqueue import UnknownQueueError
from google.appengine.api import app_identity
from google.appengine.api import capabilities
from utils import compute_signature
import webapp2
from logconstant import *
import prodeagle.counter
class Hello(webapp2.RequestHandler):

  def get(self):
        acct_name = app_identity.get_service_account_name()
        self.response.write('accountname: ' + acct_name)



### MAIN HANDLER
application = webapp2.WSGIApplication([
  ('/hello', Hello),
], debug=True)



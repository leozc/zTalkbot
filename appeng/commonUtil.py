
from __future__ import with_statement
import sys
sys.path.insert(0, "packages.zip")

#import PIL
from google.appengine.api import memcache

# Globals
memcacheClient = memcache.Client()
DEFAULT_RESIZE_FILTER = PIL.Image.ANTIALIAS



#a context per user

import zconfig
from commonUtil import *
import searchresultclient
import urllib2
# this object is dump in memcache.

class zRobotContext:
    PROPERTYVALUATION="propertysearch"
    PROPERTYINFO="propertyinfo"
    MORTGAGE="mortgage"
    def __init__(self,clientId):
        self.setClientId(clientId)
        self.addressContext =None
        self.resultsCache = {}
        self.zpid=None

    def __str__ (self):
        return "Client Id " + self.clientId  + " Address:" +str(self.getAddressContext())+" zpid="+str(self.zpid)+ " resultCache:"+ str(self.resultsCache)

## client Id
    def setClientId(self,clientid):
        self.clientId = clientid
    def getClientId(self):
        return self.clientId
## Address context
    def setAddressContext(self, addressContext,zpid=None):
        self.addressContext = addressContext
        self.zpid = zpid
        # clean memory
        self.resultsCache = {}
    def getZpid(self):
        return self.zpid

    def getAddressContext(self):
        return self.addressContext
    def hasAddressContext(self):
        return self.zpid!=None


### object management
### blank out object caching
    def setResult(self,key, searchResult):
        #self.resultsCache[key]=searchResult
        pass
    def getResult(self,key):
        #if self.resultsCache.has_key(key):
        #    return self.resultsCache[key]
        #else:
        return None

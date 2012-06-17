import re
import logging
import zconfig
import urllib
import urllib2
import logging
import xml
from xml.dom.minidom import parse, parseString
import xml.etree.cElementTree as ET
from utils import *
class GetUpdatedPropertyDetailsClient:
    def search (self,zpid):
        logging.info("GETUPDATEDPropertyDetails for zpid:"+str(zpid))
        request = urllib.urlencode({"zws-id":zconfig.ZWSID,
            "zpid":str(zpid)
            }
            )
        url = zconfig.GETUPDATEDPROPERTYDETAILS_EP+"?"+request

        logging.info("GETUPDATEDPropertyDetails openurl "+url)
        result = urllib2.urlopen(url)
        content = result.read()
        return GetUpdatedPropertyDetailsResult(content)

class GetUpdatedPropertyDetailsResult:
    def __init__(self,xml):
        self.xml = xml
        self.doc = ET.fromstring(xml)
    def getPayload(self):
        return self.xml
    def getMessageCode(self):
        return long(self.doc.find("message/code").text)
    def isValid(self):
        return int(self.getMessageCode())==0

    def getZipd(self):
        return long(self.doc.find("response/zpid").text)

    def getHDPUrl(self):
        return self.doc.find("response/links/homedetails").text

    def getHomeInfo(self):
        return self.doc.find("response/links/homeInfo").text

    def getPhotoGallery(self):
        return self.doc.find("response/links/photoGallery").text

    def getLayoutDescription(self):

        hometype = self.doc.find("response/editedFacts/useCode").text
        bedrooms = self.doc.find("response/editedFacts/bedrooms").text
        bathrooms = self.doc.find("response/editedFacts/bathrooms").text

        lotsize = self.doc.find("response/editedFacts/lotSizeSqFt").text

        finishedSqft = self.doc.find("response/editedFacts/finishedSqFt").text
        yearBuilt = self.doc.find("response/editedFacts/yearBuilt").text

        result = "This "+bedrooms +" beds "+bathrooms +" baths property built in "+yearBuilt +" living space "+ finishedSqft+"sqft on a "+lotsize+"sqft lot"
        return result



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
class SearchResultClient:
    def search (self,addressDict):
        logging.info("SearchResultClient for zpid:"+str(addressDict))

        request = urllib.urlencode({"zws-id":zconfig.ZWSID,
            "address":addressDict["addressline"],
            "citystatezip":addressDict["citystatezip"],
            "rentzestimate":"true"
            }
            )
        url = zconfig.SEARCHRESULT_EP+"?"+request
        logging.info("SearchResultClient for openurl "+url)

        result = urllib2.urlopen(url)
        content = result.read()
        return SearchResult(content)

class SearchResult:
    def __init__(self,xml):
        self.xml = xml
        self.doc = ET.fromstring(xml)

    def getMessageCode(self):
        return long(self.doc.find("message/code").text)

    def getMessageErrorText(self):
        return self.doc.find("message/text").text

    def isValid(self):
        if(int(self.getMessageCode())!=0):
            raise Exception(self.getMessageErrorText())
        return True;

    def getZpid(self):
        return long(self.doc.find("response/results/result/zpid").text)

    def getHDPUrl(self):
        return self.doc.find("response/results/result/links/homedetails").text

    def getComparables(self):
        return self.doc.find("response/results/result/links/comparables").text

    def getZestimateLastUpdate(self):
        lastUpdate = self.doc.find("response/results/result/zestimate/last-updated").text
        return lastUpdate

    def getZestimate(self):
        amount = moneyfmt(self.doc.find("response/results/result/zestimate/amount").text)
        return amount

    def getZestimateRange(self):
        low = moneyfmt(self.doc.find("response/results/result/zestimate/valuationRange/low").text)
        high =moneyfmt(self.doc.find("response/results/result/zestimate/valuationRange/high").text)
        return (low,high)

    def getRentZestimateLastUpdate(self):
        return self.doc.find("response/results/result/rentzestimate/last-updated").text

    def getRentZestimate(self):
        return moneyfmt(self.doc.find("response/results/result/rentzestimate/amount").text)

    def getRentZestimateRange(self):
        low = moneyfmt(self.doc.find("response/results/result/rentzestimate/valuationRange/low").text)
        high =moneyfmt(self.doc.find("response/results/result/rentzestimate/valuationRange/high").text)
        return (low,high)

    def getLayoutDescription(self):

        hometype = self.doc.find("response/results/result/useCode").text
        bedrooms = self.doc.find("response/results/result/bedrooms").text
        bathrooms = self.doc.find("response/results/result/bathrooms").text

        lotsize = self.doc.find("response/results/result/lotSizeSqFt").text

        finishedSqft = self.doc.find("response/results/result/finishedSqFt").text
        yearBuilt = self.doc.find("response/results/result/yearBuilt").text

        result = "This "+bedrooms +" beds "+bathrooms +" baths "+hometype+" built in "+yearBuilt +", livable space: "+ finishedSqft+"sqft on a "+lotsize+"sqft lot."
        return result


    def getLastSold(self):
        lastSolddate = self.doc.find("response/results/result/lastSoldDate").text
        lastPrice = moneyfmt(self.doc.find("response/results/result/lastSoldPrice").text)
        return "Last sold was for "+lastPrice + " in "+lastSolddate

    def getLastTax(self):
        ta = moneyfmt(self.doc.find("response/results/result/taxAssessment").text)
        tay = self.doc.find("response/results/result/taxAssessmentYear").text
        tam = moneyfmt(float(self.doc.find("response/results/result/taxAssessment").text)/12 )
        tay = self.doc.find("response/results/result/taxAssessmentYear").text
        return "The latest assessment value we have on file is "+ta +" for "+tay+" tax year. Around "+tam +" per month."

    def getLocalRealEstateOverview(self):
        pass

    def getForSaleByOwner(self):
        pass

    def getForSale(self):
        pass



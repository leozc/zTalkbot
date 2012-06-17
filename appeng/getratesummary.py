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
class GetRateSummaryClient:
    def search (self,zpid):
        logging.info("GETRateSummaryClien for zpid:"+str(zpid))
        request = urllib.urlencode({"zws-id":zconfig.ZWSID,
            "zpid":str(zpid)
            }
            )
        url = zconfig.GETRATESUMMARY_EP+"?"+request

        logging.info("GetRateSummaryClient openurl "+url)
        result = urllib2.urlopen(url)
        content = result.read()
        return GetRateSummaryResult(content)

class GetRateSummaryResult:
    def __init__(self,xml):
        self.xml = xml
        self.doc = ET.fromstring(xml)
    def getPayload(self):
        return self.xml
    def getMessageCode(self):
        return self.doc.find("message/code").text
    def isValid(self):
        return int(self.getMessageCode())==0

    def getTodayRate(self):
         thirtyyearfixed  = self.doc.find("response/today/rate[@loanType='thirtyYearFixed']").text
         fifteenyearfixed = self.doc.find("response/today/rate[@loanType='fifteenYearFixed']").text
         fiveonearm       = self.doc.find("response/today/rate[@loanType='fiveOneARM']").text
         return {"30":thirtyyearfixed,"15":fifteenyearfixed,"1/5":fiveonearm}

    def getLastWeekRate(self):
         thirtyyearfixed  = self.doc.find("response/lastWeek/rate[@loanType='thirtyYearFixed']").text
         fifteenyearfixed = self.doc.find("response/lastWeek/rate[@loanType='fifteenYearFixed']").text
         fiveonearm       = self.doc.find("response/lastWeek/rate[@loanType='fiveOneARM']").text
         return {"30":thirtyyearfixed,"15":fifteenyearfixed,"1/5":fiveonearm}



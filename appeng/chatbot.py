from __future__ import with_statement
import sys
sys.path.insert(0, "packages.zip")

from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import re
import logging
from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors
from google.appengine.api.urlfetch_errors import DownloadError
from google.appengine.api.urlfetch_errors import ResponseTooLargeError
from google.appengine.api.urlfetch_errors import InvalidURLError
from google.appengine.api.urlfetch_errors import Error

import zconfig
from commonUtil import *
import searchresultclient

import getupdatedpropertyDetails
import getratesummary
import urllib2

from chatbot_context import zRobotContext
import json
class XMPPHandler(webapp.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        self.processMsg(message)
    def shortenUrl(self,url):
        req = "http://tinyurl.com/api-create.php?url="+url
        tiny = urllib2.urlopen(req).read()
        return tiny

    def get_data(self,clientId):
        data = memcacheClient.get(clientId,namespace="ztalkbot")
        if data is not None:
            return data
        else:
            logging.info("creating cache object for " +clientId)
            data = zRobotContext(clientId)
            memcacheClient.add(clientId, data, 600,namespace="ztalkbot")
        return data

    def set_data(self,data):
        logging.info("updated cache object for " +str(data))
        memcacheClient.set(data.getClientId(), data, time=600,namespace="ztalkbot")


    def addressRule(self,message):
        message.reply("Address must be double quoted, and in full form that contains City State and ZIP.")
        message.reply('e.g. "80 Vine ST Seattle WA 98121" ' )

    def processMsg(self,message):
        try:

            session = self.get_data(message.sender)
            body = " ".join(message.body.splitlines())
            body = body.lower()
            body_a = body.split()
            inlineaddr = self.getAddress(body)
            logging.info("from:"+message.sender + "says: "+ body)
            if inlineaddr :

                # query and cache the zpid not the most clever stuff to do .
                searchResult = searchresultclient.SearchResultClient().search(inlineaddr)

                if(searchResult.isValid()):
                    zpid = searchResult.getZpid()
                    session.setAddressContext(inlineaddr,zpid)
                    message.reply("OK, let's start look at " + self.formatAddress(inlineaddr) + " from now.")
                else:
                    logging.debug(self.formatAddress(inlineaddr))
                    message.reply("Hmm the address " + self.formatAddress(inlineaddr) +" doesn't exists in Zillow database... try another one, please")



                self.set_data(session)
                session = self.get_data(message.sender)
######################## GREETING

            if 'hello' in body_a or 'greeting' in body_a or 'hi' in body_a:
                message.reply("Hello! "+message.sender.split('@')[0]+ " I am zRobot from Zillow!")

                if session.hasAddressContext()==False:
                    message.reply("Are you lookin' for info of a property, give me the address ;) ")
                    self.addressRule(message)
######################### HELP

            elif "bye" in body_a and len(body)<10:
                memcacheClient.delete(session.getClientId(),namespace="ztalkbot")
                message.reply("Bye bye!")
            elif body == "help":
                if session.getAddressContext()!=None:
                    message.reply("We are talking about address " + self.formatAddress(session.getAddressContext()) )
                    message.reply('See how much your home worth? e.g. how much is my home (address optional) ')
                    message.reply('Ask for rent e.g. how much to rent it ')
                    message.reply('See tax info? e.g. property tax.')
                    message.reply('See property info? e.g. property info')
                    message.reply('Check out mortgage? say I need a loan')
                    message.reply('Check comparisons? say comps or comparibles ')
                else:
                    self.addressRule(message)

################ ADDRESS ASSIGNMENT
            elif session.hasAddressContext() == False:
                message.reply('May I have the address of the property? e.g. "80 Vine st Seattle WA 98121"')
                message.reply('Address needs to be double quoted and with city state and ZIP')
                message.reply('Please give me an address to start :).')
############### DEBUG INTERNAL

            elif body == ":info": #debug
                message.reply('Erh, back door!')
                message.reply(str(session))

            elif body == ":washbrain": #debug
                message.reply('Erh, back door! washbrain')
                memcacheClient.delete(session.getClientId(),namespace="ztalkbot")
                message.reply('I lost all memony, I love you but I have to forget you...')

############### Rent
            elif ("comps" in body_a) or ( "comparible" in body_a) or ("similar" in body_a):
                # set address
                address = session.getAddressContext()
                self.doReplyPropertyComp(message,address,session)
############### Rent
            elif ("rental" in body_a) or ( "rent" in body_a):
                # set address
                address = session.getAddressContext()
                self.doReplyPropertyRent(message,address,session)
############### VALUATION SERVICE
            elif ("worth" in body_a) or (("much" in body_a) and ("how" in body_a)):
                # set address
                address = session.getAddressContext()
                self.doReplyPropertyWorth(message,address,session)

################# Property Details
            elif (("detail" in body_a) or ("info" in body_a)) and  ("property" in body_a):
                zpid = session.getZpid()
                self.doReplyPropertyDetails(message,zpid,session)

################# Property Tax
            elif (("property" in body_a) or ("info"in body_a)) and  ("tax" in body_a):
                zpid = session.getZpid()
                self.doReplyPropertyTaxDetails(message,zpid,session)

################# mortgage
            elif ("mortgage" in body_a) or ("loan" in body_a) or  ("quote" in body_a):
                zpid = session.getZpid()
                self.doReplyMortgageQuote(message,zpid,session)

############## INFORMATION
            elif (body == "info"):
                # set address
                address = session.getAddressContext()
                message.reply("We are talking about the property in "+self.formatAddress(address));
                message.reply("If not tell me anouther address");

################# DEFAULT

            else: #DEFAULT HANDLER
                message.reply("Nice try! Say 'help' to see what I can do.")
        except Exception as inst:
            logging.error(type(inst) )    # the exception instance
            logging.error(inst.args)      # arguments stored in .args
            logging.error(inst)           # __str__ allows args to printed directly
            logging.error(self.request.get('url'))
            logging.exception(inst)
            message.reply("I am screwed " + str(inst) +" :(")
            raise
##################
# RESPONSE HANDLERS
##################
    def getSearchResult(self,message,address,session):
        searchResult = None
        if session.getResult(zRobotContext.PROPERTYVALUATION):
            searchResult =session.getResult(zRobotContext.PROPERTYVALUATION)
            message.reply("Arh, I have that on my file..")
        else:
            searchResult = searchresultclient.SearchResultClient().search(address)
            session.setResult(zRobotContext.PROPERTYVALUATION,searchResult)
            self.set_data(session)# update session
        return searchResult


    def doReplyPropertyComp(self,message,address,session):
        message.reply("Checking the comps .. ")
        searchResult = self.getSearchResult(message,address,session)

        if(searchResult.isValid()):
            t = searchResult.getComparables()
            t = self.shortenUrl(t)
            message.reply("Here is a bunch... pls see "+t+".")
        else:
            message.reply("I cannot find the address. Address I was looking for is: "+self.formatAddress(address) +"  :(");
            message.reply("try again with another address?");

    def doReplyPropertyRent(self,message,address,session):
        message.reply("Checking the rent .. ")
        searchResult = self.getSearchResult(message,address,session)

        if(searchResult.isValid()):
            message.reply("You probaly can rent it for:" +searchResult.getRentZestimate() + ", the reasonable range is within "+str(searchResult.getRentZestimateRange()))
        else:
            message.reply("I cannot find the address. Address I was looking for is: "+self.formatAddress(address) +"  :(");
            message.reply("try again with another address?");



    def doReplyPropertyWorth(self,message,address,session):
        message.reply("Getting this from Zillow, for "+self.formatAddress(address) + ", one sec pls")
        searchResult = self.getSearchResult(message,address,session)

        if(searchResult.isValid()):
            message.reply("Zestimate is :" +searchResult.getZestimate() + " within HI/LOW range of "+str(searchResult.getZestimateRange()))
            t = self.shortenUrl(searchResult.getHDPUrl())

            message.reply("ALSO:")
            message.reply("Don't forget to check out more from here Zillow:"+ t)
        else:
            message.reply("I cannot find the address. Address I was looking for is: "+self.formatAddress(address) +"  :(");
            message.reply("try again with another address?");

    def doReplyPropertyDetails(self,message,zpid,session):
        address = session.getAddressContext()
        result = searchresultclient.SearchResultClient().search(address)
        message.reply(result.getLayoutDescription()  );
        t = self.shortenUrl(result.getHDPUrl())
        message.reply("Details on Zillow " + t);



    def doReplyPropertyTaxDetails(self,message,zpid,session):
        address = session.getAddressContext()
        result = searchresultclient.SearchResultClient().search(address)
        message.reply(result.getLastTax()  );

    def doReplyMortgageQuote(self,message,zpid,session):
        z = session.getZpid()
        result = getratesummary.GetRateSummaryClient().search(z)
        today = result.getTodayRate()
        lastweek = result.getLastWeekRate()


        message.reply("30 Years Fixed : " + today["30"] + "- Last week" + lastweek["30"])
        message.reply("15 Years Fixed : " + today["15"] + "- Last week" + lastweek["15"])
        message.reply("1/5 ARM : " + today["1/5"] + "- Last week" + lastweek["1/5"])
        message.reply("Pls check out Zillow Mortgage for more details: http://zillow.com/mortgage")


##############
# HELPER FUNCTIONS
##############
    def getAddress(self,body):
        try:
            addrpattern='".*"'; # within a quote, doggy but it works now
            if re.search(addrpattern,body):
                address = re.search(addrpattern,body).group(0)
                address = re.sub("[,:'\"]","",address)
                address= address.split()
                return {"addressline":" ".join(address[0:-3]),"state":address[-2], "zip":address[-1],"city":address[-3]}
            else:
                return None
        except Exception as ee:
            raise Exception ("Cannot parse your address, are you using full address? "+str(ee))

    def formatAddress(self,address):
        return "'"+address["addressline"]+"'" + ", city is " + address["city"].capitalize() + " in " +address["state"].upper() + " state, ZIP code is "+ address['zip']

application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                                     debug=True)

########################
######## MAINS
########################
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

import re
##  a simple address parsing class.
## Accept missing state or zip.
class AddressParser:
    states = {
            "AL":{"count":"0","name":"Alabama","abbr":"AL"},
            "AK":{"count":"1","name":"Alaska","abbr":"AK"},
            "AZ":{"count":"2","name":"Arizona ","abbr":"AZ"},
            "AR":{"count":"3","name":"Arkansas","abbr":"AR"},
            "CA":{"count":"4","name":"California ","abbr":"CA"},
            "CO":{"count":"5","name":"Colorado ","abbr":"CO"},
            "CT":{"count":"6","name":"Connecticut","abbr":"CT"},
            "DE":{"count":"7","name":"Delaware","abbr":"DE"},
            "DC":{"count":"8","name":"District Of Columbia","abbr":"DC"},
            "FL":{"count":"9","name":"Florida","abbr":"FL"},
            "GA":{"count":"10","name":"Georgia","abbr":"GA"},
            "HI":{"count":"11","name":"Hawaii","abbr":"HI"},
            "ID":{"count":"12","name":"Idaho","abbr":"ID"},
            "IL":{"count":"13","name":"Illinois","abbr":"IL"},
            "IN":{"count":"14","name":"Indiana","abbr":"IN"},
            "IA":{"count":"15","name":"Iowa","abbr":"IA"},
            "KS":{"count":"16","name":"Kansas","abbr":"KS"},
            "KY":{"count":"17","name":"Kentucky","abbr":"KY"},
            "LA":{"count":"18","name":"Louisiana","abbr":"LA"},
            "ME":{"count":"19","name":"Maine","abbr":"ME"},
            "MD":{"count":"20","name":"Maryland","abbr":"MD"},
            "MA":{"count":"21","name":"Massachusetts","abbr":"MA"},
            "MI":{"count":"22","name":"Michigan","abbr":"MI"},
            "MN":{"count":"23","name":"Minnesota","abbr":"MN"},
            "MS":{"count":"24","name":"Mississippi","abbr":"MS"},
            "MO":{"count":"25","name":"Missouri","abbr":"MO"},
            "MT":{"count":"26","name":"Montana","abbr":"MT"},
            "NE":{"count":"27","name":"Nebraska","abbr":"NE"},
            "NV":{"count":"28","name":"Nevada","abbr":"NV"},
            "NH":{"count":"29","name":"New Hampshire","abbr":"NH"},
            "NJ":{"count":"30","name":"New Jersey","abbr":"NJ"},
            "NM":{"count":"31","name":"New Mexico","abbr":"NM"},
            "NY":{"count":"32","name":"New York","abbr":"NY"},
            "NC":{"count":"33","name":"North Carolina","abbr":"NC"},
            "ND":{"count":"34","name":"North Dakota","abbr":"ND"},
            "OH":{"count":"35","name":"Ohio","abbr":"OH"},
            "OK":{"count":"36","name":"Oklahoma","abbr":"OK"},
            "OR":{"count":"37","name":"Oregon","abbr":"OR"},
            "PA":{"count":"38","name":"Pennsylvania","abbr":"PA"},
            "RI":{"count":"39","name":"Rhode Island","abbr":"RI"},
            "SC":{"count":"40","name":"South Carolina","abbr":"SC"},
            "SD":{"count":"41","name":"South Dakota","abbr":"SD"},
            "TN":{"count":"42","name":"Tennessee","abbr":"TN"},
            "TX":{"count":"43","name":"Texas","abbr":"TX"},
            "UT":{"count":"44","name":"Utah","abbr":"UT"},
            "VT":{"count":"45","name":"Vermont","abbr":"VT"},
            "VA":{"count":"46","name":"Virginia ","abbr":"VA"},
            "WA":{"count":"47","name":"Washington","abbr":"WA"},
            "WV":{"count":"48","name":"West Virginia","abbr":"WV"},
            "WI":{"count":"49","name":"Wisconsin","abbr":"WI"},
            "WY":{"count":"50","name":"Wyoming","abbr":"WY"}
    };
    def __init__(self, address):
        self.address = address

## a quick address parsing
    def parse(self):
        addr_a = self.address.strip().split()[::-1]
        if (len(addr_a) > 4):
            zAddress(None,None,None,None)

        a = zAddress(None,None,None,None)
        addressLine=[]
        reverseCounter = 0
        for s in addr_a:
            if   reverseCounter < 4 and a.city == None and re.search("^\d\d\d\d\d",s) !=None :
                a.zipCode =s
            elif (a.state == None and a.city == None and s.upper() in  AddressParser.states.keys()):
                a.state = s
            elif (a.zipCode != None or a.state != None) and a.city==None:
                a.city = s
            else:
                addressLine.append(s)
            reverseCounter= reverseCounter + 1
        a.addressLine = " ".join(addressLine[::-1])
        return a

class zAddress:
    def __init__(self, addressLine, city, state, zipCode):
        self.addressLine = addressLine
        self.city = city
        self.state = state
        self.zipCode = zipCode

    def cityStateZip(self):
        r = []
        if self.city != None:
            r.append(self.city)
        if self.state!=None:
            r.append(self.state)
        if self.zipCode != None:
            r.append(self.zipCode)
        return " ".join(r)


    def isCompleteAddress(self):
        return self.city != None and self.state != None and self.zipCode != None and self.addressLine != None

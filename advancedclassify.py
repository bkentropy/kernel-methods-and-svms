from pylab import *
from urllib import urlopen,quote_plus
from json import loads, dumps

class matchrow:
    def __init__(self, row, allnum=False):
        if allnum:
            self.data = [float(row[i]) for i in range(len(row) -1)]
        else:
            self.data=row[0:len(row)-1]
        self.match=int(row[len(row)-1])

def loadmatch(f, allnum=False):
    rows=[]
    for line in file(f):
        rows.append(matchrow(line.split(','),allnum))
    return rows

def plotagematches(rows):
     xdm,ydm=[r.data[0] for r in rows if r.match==1],[r.data[1] for r in rows if r.match==1]
     xdn,ydn=[r.data[0] for r in rows if r.match==0],[r.data[1] for r in rows if r.match==0]
     plot(xdm,ydm,'go')
     plot(xdn,ydn,'ro')
     show()

agesonly = loadmatch('data/agesonly.csv', allnum=True) ## you only want to do this if there
## really are only numbers involved
matchmaker = loadmatch('data/matchmaker.csv')

def lineartrain(rows):
    averages={}
    counts={}

    for row in rows:
        # Get the class of this point
        c1=row.match
        averages.setdefault(c1,[0.0]*(len(row.data)))
        counts.setdefault(c1,0)

        # Add this point to the averages
        for i in range(len(row.data)):
            averages[c1][i]+=float(row.data[i])

        # Keep track of many points in each class
        counts[c1]+=1

    # Divide sums by counts to get the averages 
    for c1,avg in averages.items(): # for key and value, so setting the value - mutably sets the value
        for i in range(len(avg)):
            avg[i]/=counts[c1]

    return averages

def dotproduct(v1,v2):
    return sum([v1[i]*v2[i] for i in range(0, len(v1))])

def dpclaissify(point,avgs):
    b = (dotproduct(avgs[1],avgs[1])-dotproduct(avgs[0],avgs[0]))/2
    y = dotproduct(point, args[0])-dotproduct(point, avgs[1]) + b
    if y>0: return 0
    else: return 1

def yesno(v):
    if v == 'yes': return 1
    elif v == 'no': return 0
    return 0

def matchcount(interest1, interest2):
    l1 = interest1.split(':')
    l2 = interest2.split(':')
    x = 0
    for v in l1:
        if v in l2: x+=1
    return x

apikey = "AIzaSyDW2PtzeTBQXorByFxgEUSxmazgZOQkJjw"
address = "E+47th+St+,New+York,+NY&"

def makeurl(addr):
    return "https://maps.googleapis.com/maps/api/geocode/json?address=" +\
            addr.replace(' ', '+') +\
            "key=AIzaSyDW2PtzeTBQXorByFxgEUSxmazgZOQkJjw"


def milesdistance(a1, a2):
    return 0

loc_cache={}
def getlocation(address):
    if address in loc_cache: return loc_cache[address]
    data = urlopen(url)
    str = data.read()
    loc = loads(str)
    addr = loc['results'][0]['geometry']['location']
    with open('dump.json', 'a') as f:
        json.dump(addr, f)
    return addr

addresses = [row.data[4] for row in matchmaker]
#getlocation("")

from csv import reader
from json import loads
from io import StringIO
from os.path import dirname
from re import findall
from xml.etree import ElementTree
from bs4 import BeautifulSoup
from requests import Session

def fixorders(orders):

    if len(orders) < 18:

        orderslen = 18 - len(orders)
        for i in range(orderslen):

            orders.append("0")

        for order in orders:

            if not order.strip():

                orders.remove(order)
                orders.append("0")

        return orders

    else:

        return orders

path = dirname(__file__)
with open(path+r"\cache\freefloat.json") as file: 

    freefloats = loads(file.read())

session = Session()

class Share:

    def __init__(self, inscode):

        url = "http://tsetmc.com/Loader.aspx"
        payload = {"partree": "15131M", "i": inscode}

        htmlfile = session.get(url, params=payload)
        htmlfile = htmlfile.text

        soup = BeautifulSoup(htmlfile, "html.parser")
        tds = soup.find_all("td")

        self.inscode = inscode
        self.instrumentid = tds[1].string
        self.cvalmne = tds[3].string
        self.companylatinname = tds[5].string # self naming
        self.csoccsac = tds[7].string
        self.companyname = tds[9].string # self naming
        self.sharename = tds[11].string.strip() # self naming
        self.lval30 = tds[13].string
        self.cisin = tds[15].string
        self.market = tds[17].string # self naming
        self.ccomval = tds[19].string
        self.csecval = tds[21].string
        self.lsecval = tds[23].string
        self.csosecval = tds[25].string
        self.lsosecval = tds[27].string

    def getinst(self):

        url = "http://tsetmc.com/tsev2/data/instinfodata.aspx"
        payload = {"i": self.inscode, "c": self.csecval}

        csvfile = session.get(url, params=payload)
        csvfile = csvfile.text.replace(";", "\n").replace("@", ",")
        csvfile = list(reader(StringIO(csvfile)))

        csvfile[2] = fixorders(csvfile[2])

        inst = {
            "heven": csvfile[0][0],
            "cetaval": csvfile[0][1].strip(), # not sure about name maybe it is "cgdsval"
            "pl": int(csvfile[0][2]),
            "pc": int(csvfile[0][3]),
            "po": int(csvfile[0][4]),
            "py": int(csvfile[0][5]),
            "pd": int(csvfile[0][6]),
            "pf": int(csvfile[0][7]),
            "tno": int(csvfile[0][8]),
            "tvol": int(csvfile[0][9]),
            "tval": int(csvfile[0][10]),
            #"unknown": csvfile[0][11],
            "deven": int(csvfile[0][12]),
            "ltt": int(csvfile[0][13]), # self naming
            "plp": round(((int(csvfile[0][2]) - int(csvfile[0][5])) * 100) / int(csvfile[0][5]), 2),
            "pcp": round(((int(csvfile[0][3]) - int(csvfile[0][5])) * 100) / int(csvfile[0][5]), 2),
            "orders": [
                {
                    "zd": int(csvfile[2][0]),
                    "qd": int(csvfile[2][1]),
                    "pd": int(csvfile[2][2]),
                    "po": int(csvfile[2][3]),
                    "qo": int(csvfile[2][4]),
                    "zo": int(csvfile[2][5]),
                },
                {
                    "zd": int(csvfile[2][6]),
                    "qd": int(csvfile[2][7]),
                    "pd": int(csvfile[2][8]),
                    "po": int(csvfile[2][9]),
                    "qo": int(csvfile[2][10]),
                    "zo": int(csvfile[2][11]),
                },
                {
                    "zd": int(csvfile[2][12]),
                    "qd": int(csvfile[2][13]),
                    "pd": int(csvfile[2][14]),
                    "po": int(csvfile[2][15]),
                    "qo": int(csvfile[2][16]),
                    "zo": int(csvfile[2][17]),
                }
            ],
        }

        if csvfile[4]:

            inst.update({
                "buyivolume": int(csvfile[4][0]),
                "buynvolume": int(csvfile[4][1]),
                "sellnvolume": int(csvfile[4][2]),
                "sellivolume": int(csvfile[4][3]),
                #"unknown": csvfile[4][4],
                "buycounti": int(csvfile[4][5]),
                "buycountn": int(csvfile[4][6]),
                "sellcountn": int(csvfile[4][7]),
                "sellcounti": int(csvfile[4][8]),
                #"unknown": csvfile[4][9],
            })

        url = "http://tsetmc.com/Loader.aspx"
        payload = {"ParTree": "151311", "i": self.inscode}

        htmlfile = session.get(url, params=payload)
        htmlfile = htmlfile.text

        if self.inscode in freefloats:
            freefloat = freefloats[self.inscode]
        else:
            freefloat = findall(r"KAjCapValCpsIdx='(.*?)',", htmlfile)[0].strip()
        eps = findall(r"EstimatedEPS='(.*?)',", htmlfile)[0].strip()
        sectorpe = findall(r"SectorPE='(.*?)',", htmlfile)[0].strip()

        inst.update({
            "bvol": int(findall(r"BaseVol=(.*?),", htmlfile)[0]),
            "eps": float(eps) if eps else 0,
            "z": int(findall(r"ZTitad=(.*?),", htmlfile)[0]),
            "psgelstamax": float(findall(r"PSGelStaMax='(.*?)',", htmlfile)[0]),
            "psgelstamin": float(findall(r"PSGelStaMin='(.*?)',", htmlfile)[0]),
            "minweek": float(findall(r"MinWeek='(.*?)',", htmlfile)[0]),
            "maxweek": float(findall(r"MaxWeek='(.*?)',", htmlfile)[0]),
            "minyear": float(findall(r"MinYear='(.*?)',", htmlfile)[0]),
            "maxyear": float(findall(r"MaxYear='(.*?)',", htmlfile)[0]),
            "sectorpe": float(sectorpe) if sectorpe else 0,
            "freefloat": float(freefloat) if freefloat else 0, # self naming
        })

        return inst

    def getclientes(self, day=0, many=1):
        
        url = "http://www.tsetmc.com/tsev2/data/clienttype.aspx"
        payload = {"i": self.inscode}

        csvfile = session.get(url, params=payload)
        csvfile = csvfile.text.replace(";", "\n")
        csvfile = list(reader(StringIO(csvfile)))

        clientes = {}
        for row in csvfile[day:day+many]:

            clientes.update({
                row[0]: {
                    "buycounti": int(row[1]),
                    "buycountn": int(row[2]),
                    "sellcounti": int(row[3]),
                    "sellcountn": int(row[4]),
                    "buyivolume": int(row[5]),
                    "buynvolume": int(row[6]),
                    "sellivolume": int(row[7]),
                    "sellnvolume": int(row[8]),
                    "buyival": int(row[9]),
                    "buynval": int(row[10]),
                    "sellival": int(row[11]),
                    "sellnval": int(row[12]),
                }
            })

        return clientes
    
    def getshareholders(self):

        url = "http://www.tsetmc.com/Loader.aspx"
        payload = {"partree": "15131T", "c": self.cisin}

        htmlfile = session.get(url, params=payload)
        htmlfile = htmlfile.text

        soup = BeautifulSoup(htmlfile, "html.parser")
        trs = soup.find_all("tr")
        
        shareholders = {}
        holdernumber = 1
        for tr in trs[1:]:

            tds = tr.find_all("td")
            shareholderid = findall(r"'(.+?)'", tr.get("onclick"))[0]

            url = "http://www.tsetmc.com/tsev2/data/ShareHolder.aspx"
            payload = {"i": shareholderid}

            csvfile = session.get(url, params=payload).text
            csvfile = csvfile[:csvfile.index("#")].replace(";", "\n")
            csvfile = list(reader(StringIO(csvfile)))

            duration = len(csvfile)
            percent = float(tds[2].string)

            div = tds[1].find('div')
            if div:
                sharevalue = int(div.get("title").replace(",", ""))
            else:
                sharevalue = int(tds[1].string.replace(",", ""))

            div = tds[3].find('div')
            if div:
                change = int(div.get("title").replace(",", ""))
            else:
                change = int(tds[3].string.replace(",", ""))

            shareholders.update({
                tds[0].string+str(holdernumber): {
                    "shareholderid": shareholderid,
                    "sharevalue": sharevalue,
                    "percent": percent,
                    "change": change,
                    "duration": duration,
                }
            })

            holdernumber += 1

        return shareholders

    def getpricehistory(self, day=0, many=1):

        url = "http://tsetmc.com/tsev2/data/InstTradeHistory.aspx"
        payload = { "i": self.inscode, "Top": many, "A": 0}

        csvfile = session.get(url, params=payload)
        csvfile = csvfile.text.replace("@", ",").replace(";", "\n")
        csvfile = list(reader(StringIO(csvfile)))

        tradehistory = {}
        for line in csvfile[day:day+many]:

            tradehistory.update({
                line[0]: {
                    "high": float(line[1]),
                    "low": float(line[2]),
                    "close": float(line[3]),
                    "last": float(line[4]),
                    "first": float(line[5]),
                    "open": float(line[6]),
                    "value": float(line[7]),
                    "volumn": int(line[8]),
                    "openint": int(line[9]),
                }
            })

        return tradehistory
    
    def gettransactions(self):

        url = "http://tsetmc.com/tsev2/data/TradeDetail.aspx"
        payload = {"i": self.inscode}

        xmlfile = session.get(url, params=payload)
        xmlfile = xmlfile.text
        xmlfile = ElementTree.fromstring(xmlfile)

        lasttime = None
        lastvolume = None
        lastprice = None
        tradedetail = {}
        for row in xmlfile:
            
            time = row[1].text
            volume = int(row[2].text)
            price = float(row[3].text)

            if lasttime == time:
                
                lastvolume += volume
                closeprice = price

                tradedetail.update({
                    time: {
                        "volume": lastvolume,
                        "open": openprice,
                        "close": closeprice,
                    }
                })

            else:

                lasttime = time
                lastvolume = volume
                openprice = price
                closeprice = price

                tradedetail.update({
                    time: {
                        "volume": lastvolume,
                        "open": openprice,
                        "close": closeprice,
                    }
                })

        return tradedetail

class TradeHistory:

    def __init__(self, inscode, date=None):

        self.inscode = inscode

        if not date:

            url = 'http://cdn.tsetmc.com/Loader.aspx'
            payload = {'partree': '151321', 'i': self.inscode}

            self.cdn = session.get(url, params=payload).text

        else:

            url = "http://cdn.tsetmc.com/Loader.aspx"
            payload = {"partree": "15131P", "i": self.inscode, "d": date}

            self.cdn = session.get(url, params=payload).text

    def finder(self, find):

        databox = loads(findall(rf"{find}=(.+?);", self.cdn)[0].replace("'", '"'))

        return databox

if __name__ == "__main__":

    pass
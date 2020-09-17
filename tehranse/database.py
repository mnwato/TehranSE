def update():

    from csv import reader
    from io import StringIO
    from json import loads, dumps
    from os.path import dirname 
    from requests import get

    url = "http://tsetmc.com/tsev2/data/MarketWatchInit.aspx"
    payload = {"h": 0, "r": 0} # these queries are not necessary, with only url we can get same result but i want to be like exact same request that tsetmc send 

    csvfile = get(url, params=payload)
    csvfile = csvfile.text.replace("@", "\n").replace(";", "\n")
    csvfile = reader(StringIO(csvfile))

    market = {}
    for row in csvfile:

        if len(row) == 23:

            market.update({
                row[0]: {
                    "sharename": row[2],
                    "flow": int(row[17]),
                    "csecval": int(row[18]),
                    "yval": int(row[22]),
                }
            })

    path = dirname(__file__)

    with open(path+r"\cache\shares.json") as file: 

        shares = loads(file.read())

    shares.update(market)

    with open(path+r"\cache\shares.json", "w") as file:

        file.write(dumps(shares))

    url = "https://sinamobasheri.me/resources/freefloat.json"

    jsonfile = get(url, params=payload)
    jsonfile = jsonfile.json()

    with open(path+r"\cache\freefloat.json") as file: 

        freefloats = loads(file.read())

    freefloats.update(jsonfile)

    with open(path+r"\cache\freefloat.json", "w") as file:

        file.write(dumps(freefloats))

def modify(share, method):

    from json import loads, dumps
    from os.path import dirname

    path = dirname(__file__)

    with open(path+r"\cache\shares.json") as file:

        shares = loads(file.read())

    if method == "delete":

        shares.pop(share)

    elif method == "add":

        shares.update(share)

    with open(path+r"\cache\shares.json", "w") as file:

        file.write(dumps(shares))

def report():

    from json import loads, dumps
    from os.path import dirname

    path = dirname(__file__)

    with open(path+r"\cache\shares.json") as file:

        shares = loads(file.read())

    return shares

if __name__ == "__main__":

    pass
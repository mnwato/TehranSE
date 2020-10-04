def search(sharename):

    from csv import reader
    from io import StringIO
    from requests import get

    url = "http://tsetmc.com/tsev2/data/search.aspx"
    payload = {"skey": sharename}

    csvfile = get(url, payload)
    csvfile = csvfile.text.replace(";", "\n")
    csvfile = list(reader(StringIO(csvfile)))

    if not csvfile:

        return None

    else:

        inscode = csvfile[0][2]
        return inscode

def csvwriter(filename, dictionary):

    from csv import writer

    headers = [header for header in list(dictionary.values())[0]]
    headers.insert(0, "")

    with open(f"{filename}.csv", "w", newline="", encoding="UTF-8") as file:

        write = writer(file, headers)

        write.writerow(headers)
        for key in dictionary:

            write.writerow([key] + [value for value in dictionary[key].values()])

def impactindex(many, flow):

    from re import findall
    from bs4 import BeautifulSoup
    from requests import get

    url = "http://tsetmc.com/Loader.aspx"
    payload = {"Partree": "151316", "Flow": flow}

    htmlfile = get(url, params=payload)
    htmlfile = htmlfile.text

    soup = BeautifulSoup(htmlfile, "html.parser")
    tbody = soup.find("tbody")
    trs = tbody.find_all("tr")

    pack = {}
    for tr in trs[:many]:

        tds = tr.find_all("td")

        inscode = findall(r"i=(.+)", tr.find("a").get("href"))[0]
        sharename = tds[0].string
        companyname = tds[1].string
        pc = int(tds[2].string.replace(",", ""))
        impact = -1*float(tds[3].string.replace("(", "").replace(")", "")) if "(" in tds[3].string else float(tds[3].string)

        pack.update({
            inscode: {
                "sharename": sharename,
                "companyname": companyname,
                "pc": pc,
                "impact": impact
            }
        })

    return pack

if __name__ == "__main__":

    pass
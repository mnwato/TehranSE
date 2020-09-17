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

def holdertracer(shareholderid):

    from .share import Share
    from .database import report

    inscodes = report().keys()
    length = len(list(inscodes))
    for place, inscode in enumerate(inscodes):

        share = Share(inscode)
        shareholders = share.getshareholders()

        for holder in shareholders:

            if shareholders[holder]["shareholderid"] == shareholderid:

                print(holder)

        print(f"\r{place+1}/{length}", end="")

if __name__ == "__main__":

    pass
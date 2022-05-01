def parseCookieFile(cookiefile):
    """Parse a cookies.txt file and return a dictionary of key value pairs
    compatible with requests.
    Cf. https://stackoverflow.com/a/54659484/9654083"""

    cookies = {}
    with open (cookiefile, 'r') as fp:
        for line in fp:
            if line.strip() == "":
                continue
            if not line.startswith("#") or line.startswith("#HttpOnly"):
                lineFields = line.strip().split('\t')
                try:
                    lineFields[6]
                except IndexError:
                    lineFields.append("")
                cookies[lineFields[5]] = lineFields[6]
    return cookies

cookies = parseCookieFile('cookies.txt')

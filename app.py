from html.parser import HTMLParser
import cookie_parser, sys, requests

try:
    cookies = cookie_parser.parseCookieFile("cookies.txt")
except FileNotFoundError:
    sys.exit("Missing cookies.txt.")

class DeviantArtParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "data-hook" and attr[1] == "download_button":
                    for attr in attrs: # this is extremely fucking inefficient but idc
                        if attr[0] == "href":
                            print(attr[1])
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        pass

parser = DeviantArtParser()
parser.feed(requests.get("https://www.deviantart.com/duncecapart/art/Hello-World-903668022", cookies=cookies).text)

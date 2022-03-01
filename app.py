from html.parser import HTMLParser
import cookie_parser, sys, requests

user = input("What user do you want to scrape?\nEnter the full profile-page URL please: ")

try:
    cookies = cookie_parser.parseCookieFile("cookies.txt")
except FileNotFoundError:
    sys.exit("Missing cookies.txt.")

class DeviantArtParser(HTMLParser):
    @staticmethod
    def get(url, cookies):
        return requests.get(url, cookies=cookies)
    islist = False
    links = []
    _feed = HTMLParser.feed
    def feed(self, *args, **kwargs):
        self._feed(*args, **kwargs)
        if self.islist:
            self.run(None, None)
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr == self.checkattr:
                    for attr in attrs: # this is extremely fucking inefficient but idc
                        if attr[0] == "href":
                            if self.islist:
                                self.links.append(attr)
                            else:
                                self.run(tag, attrs, attr)
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        pass

class DeviantArtPostParser(DeviantArtParser):
    checkattr = ("data-hook", "download_button")
    def run(self, tag, attrs, link):
        print(link[1])

class DeviantArtUserParser(DeviantArtParser):
    checkattr = ("data-hook", "deviation_link")
    islist = True
    def run(self, tag, attrs):
        for i in self.links:
            parser = DeviantArtPostParser()
            parser.feed(self.get(i[1], cookies).text)

parser = DeviantArtUserParser()
parser.feed(parser.get(user, cookies).text)

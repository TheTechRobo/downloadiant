from html.parser import HTMLParser
import cookie_parser, sys, requests

class input_:
    def __init__(*args):
        return

t = input_("What do you want to scrape for links today?:\n\
        (G)allery\n\
        (U)ser\n\
        (I)ndividual post\n\
        ")
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

class DeviantArtGalleryParser(DeviantArtParser):
    checkattr = ("data-hook", "deviation_link")
    islist = True
    def run(self, tag, attrs):
        for i in self.links:
            parser = DeviantArtPostParser()
            parser.feed(self.get(i[1], cookies).text)

def pagination_get(user):
    offset = 0
    total = 0
    limit = 60
    more = True
    posts = []
    while more:
        json = requests.get(f"https://www.deviantart.com/_napi/da-user-profile/api/gallery/contents?username={user}&offset={offset}&limit={limit}&all_folder=true").json()
        more = json["hasMore"]
        print(f"Scraping, {offset} results so far", file=sys.stderr)
        offset = json["nextOffset"]
        posts += json["results"]
    parser = DeviantArtPostParser()
    for itemm in posts:
        item = itemm["deviation"]["url"]
        parser.feed(requests.get(item, cookies=cookies).text)
if __name__ == "__main__":
    user = input("What user do you want to scrape?: ")
    pagination_get(user)

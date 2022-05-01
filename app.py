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
    FinishedYes = False

    @staticmethod
    def get(url, cookies, **kwargs):
        return requests.get(url, cookies=cookies, **kwargs)
    islist = False
    links = []
    _feed = HTMLParser.feed
    def feed(self, *args, **kwargs):
        self.lowquality = ""
        self._feed(*args, **kwargs)
        if self.islist:
            self.run(None, None)
        if not self.FinishedYes:
            print("\033[31;42m Warning: Submission does not have a download button. Outputting low-quality version instead...\033[0;0m", file=sys.stderr)
            assert self.lowquality != "", "No low-quality image found."
            print(self.lowquality)
        #assert self.FinishedYes, "Could not find download link."
        self.FinishedYes = False
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
                            self.FinishedYes = True
        elif tag == "img" and (not self.islist):
            for attr in attrs:
                if attr == self.lowquality_checkattr:
                    for attr in attrs:
                        if attr[0] == "src":
                            self.lowquality = attr[1]
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        pass

class DeviantArtPostParser(DeviantArtParser):
    checkattr = ("data-hook", "download_button")
    lowquality_checkattr = ("aria-hidden", "true")
    def run(self, tag, attrs, link):
        print(link[1])

class DeviantArtGalleryParser(DeviantArtParser):
    checkattr = ("data-hook", "deviation_link")
    #lowquality_checkattr = ("aria-hidden", "true")
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
    print(f"Finished, {len(posts)} results",file=sys.stderr)
    parser = DeviantArtPostParser()
    for itemm in posts:
        item = itemm["deviation"]["url"]
        #print(item)
        data = parser.get(item, cookies, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36"}).text
        parser.feed(data)
if __name__ == "__main__":
    print("What user do you want to scrape?: ", end="", file=sys.stderr, flush=True)
    user = input()
    pagination_get(user)

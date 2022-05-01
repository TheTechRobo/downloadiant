# DeviantArt scraper
This scraper logs into DeviantArt with a Netscape-style cookies.txt, fetches a user's profile page, and displays the links so you can `wget -i` them.

Please note: If a post doesn't have a download link (owners can disable downloading), a low-quality image will be
shown instead. Additionally, a failure to log in will not raise an error. Instead, only low-quality images will be
downloadable.

It is currently possible to use this as a module, but I need to overhaul the code before I document that.

## So how do I use this?

0. Get your cookies.txt. Make sure it's Netscape-style or wget-compatible. There are usually browser extensions to do this, or you can make your own. (It's a plain-text format.)

1. Clone the repo.

2. Put your cookies.txt in the same folder as where you're running the script from. Make sure it's named cookies.txt.  
  **NB:** With the advent of [`3acc837e3`](https://github.com/TheTechRobo/downloadiant/commit/3acc837e3af17be943bc1a55aa9880d754c641d5), you no longer need to be authenticated.
  However, the URLs outputted will have a DeviantArt watermark.
3. Run the script.

4. Enter a username.

- There is currently code for scraping an individual post, but this is not yet accessible to the public
- There is also currently code for scraping a gallery, but this needs to be rewritten before it's made accessible to the public

5. Use the list of URLs in a bulk downloader!

## I am not responsible if you are banned.
Scraping is usually against a service's ToS. I am not responsible for your getting banned.

## Licence
This program is licenced under the Apache-2.0 licence - copyright (c) 2022 TheTechRobo.

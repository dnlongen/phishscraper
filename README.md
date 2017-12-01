phishscraper
=============
OpenDNS Labs launched a Twitter bot that posts verified phishing links. This is a proof of concept project to scrape phishing links and domains from any Twitter alias. Sure you could do the same thing with the PhishTank API, faster, with more complete results, but hey maybe someone will find this useful.

If given the name of a CSV file using -f or --file, phishcraper will search that file (ideally a web proxy log that records URLs, since that's what we're looking for...) for any fields containing any links or domains retrieved from the aforementioned Twitter account. It's slow, but it works. What do you expect from a PoC :-)

Other possible uses include automatically adding the phishing links to a block list.

Requirements:
=============
* Requires tweepy, the Twitter API module for Python, available from https://github.com/tweepy/tweepy
* Requires an application token for the Twitter API. Refer to documentation at https://dev.twitter.com/oauth/overview/application-owner-access-tokens, and set up your own app-specific tokens at https://apps.twitter.com
 
Note that the search API typically serves up only tweets from the last week or so, and that it is "tuned" toward most relevant results rather than most complete results. YMMV.

At least one parameter of -d, -l, or -f is required; otherwise phishscraper won't know what to do with the scraped phishing links.

Usage:
=============

```
usage: phishscraper.py [-h] -a TWITTER_ALIAS [-n NUMTWEETS] [-p PROXY] [-d]
                       [-l] [-f LOGFILE]

Grab phishing links from a Twitter account. PoC for grabbing links posted by
@PhishTank_Bot

optional arguments:
  -h, --help            show this help message and exit
  -a TWITTER_ALIAS, --alias TWITTER_ALIAS
                        Twitter alias whose tweets to analyze
  -n NUMTWEETS, --numtweets NUMTWEETS
                        Maximum number of tweets to analyze for specified
                        Twitter user; default 10
  -p PROXY, --proxy PROXY
                        HTTPS proxy to use, if necessary, in the form of
                        https://proxy.com:port
  -d, --domains         Output phishing domains
  -l, --links           Output phishing links
  -f LOGFILE, --file LOGFILE
                        Search for matching URLs in the specified log file.
                        File must be CSV
  ```

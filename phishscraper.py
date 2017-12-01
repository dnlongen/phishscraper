'''
PhishScraper v0.1
Source: https://github.com/dnlongen/phishscraper
Author: David Longenecker
Author email: david@securityforrealpeople.com 
Author Twitter: @dnlongen
Requires tweepy, the Twitter API module for Python, available from https://github.com/tweepy/tweepy
Requires an application token for the Twitter API. See https://dev.twitter.com/oauth/overview/application-owner-access-tokens for documentation, and https://apps.twitter.com to generate your tokens

Note that the search results at twitter.com may return historical results while the Search API usually only serves tweets from the past week. See https://dev.twitter.com/rest/public/search
'''

import argparse, tweepy, sys, codecs, time, re, csv

#########################################################################
# Replace the below values with your own, from https://apps.twitter.com #
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
#########################################################################

# Define supported parameters and default values
debug=0 # set to 1 to print debug output
parser = argparse.ArgumentParser(description='Grab phishing links from a Twitter account. PoC for grabbing links posted by @PhishTank_Bot')
parser.add_argument('-a', '--alias', dest='twitter_alias', required=True, help='Twitter alias whose tweets to analyze')
parser.add_argument('-n', '--numtweets', default=10, type=int, help='Maximum number of tweets to analyze for specified Twitter user; default 10')
parser.add_argument('-p', '--proxy', default='', required=False, help='HTTPS proxy to use, if necessary, in the form of https://proxy.com:port')
parser.add_argument('-d', '--domains', dest='domains', action='store_true', help='Output phishing domains')
parser.add_argument('-l', '--links', dest='links', action='store_true', help='Output phishing links')
parser.add_argument('-f', '--file', dest='logfile', required=False, help='Search for matching URLs in the specified log file. File must be CSV')
parser.set_defaults(debug=False)
args=parser.parse_args()
twitter_load=args.numtweets
twitter_list=[args.twitter_alias]
https_proxy=args.proxy
show_domains=args.domains
show_links=args.links
if args.logfile: 
    logfile = args.logfile
else:
    logfile = False

if not (show_domains or show_links or logfile): print("Nothing to output. You must select at least one of domains or links to output, or a logfile to scan for matching links.")

def parse_twitter(twitter_user, phishlinks):
    status     = ""
    try:
        for status in api.user_timeline(twitter_user,count=twitter_load, tweet_mode='extended'):
            if debug: print("Original message: " + status.full_text);
            if status.full_text.startswith('hxxp'):
                if show_links:
                    print("Link: ", re.match(r'hxxps?://(.*)',status.full_text).group(0))
                if show_domains: 
                    print("Domain: ", re.match(r'hxxps?://([^/\s]+)/?',status.full_text).group(1)) 
                phishlinks.append(re.match(r'hxxps?://(.*)',status.full_text).group(0))
                phishlinks.append(re.match(r'hxxps?://([^/\s]+)/?',status.full_text).group(1))

    except tweepy.TweepError as e:
        # Error format is like tweepy.error.TweepError: [{'code': 215, 'message': 'Bad Authentication data.'}]
        # 215 means bad authentication
        # 429 means rate-limited
        # Other error types from the Twitter API: https://developer.twitter.com/en/docs/basics/response-codes
        #if str(e).find("code = 429"): 
        #    print("Twitter API rate-limited; try again in a few minutes.")
        #    print("The Twitter API rate-limits requests within a 15-minute window.")
        #    print("Refer to https://dev.twitter.com/rest/public/rate-limiting for more information.")
        print("Twitter API error. Message:")
        print(str(e))


#################################################################################################
# Main body
#################################################################################################

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,proxy=https_proxy)
phishlinks = []
for twitter_user in twitter_list:
    # With each Twitter handle, run through the parser routine
    # Current cmdline parameters allow for only one Twitter handle; this is to enable future enhancement
    parse_twitter(twitter_user, phishlinks)

if logfile:
    #Search for matches in the log file
    if debug: print("Phishlinks: ", phishlinks)
    csvfile = open(logfile, "r")
    csvhandle = csv.reader(csvfile)
    for row in csvhandle:
        for phishlink in phishlinks:
            if any(phishlink in x for x in row):
                print(row)
    csvfile.close()
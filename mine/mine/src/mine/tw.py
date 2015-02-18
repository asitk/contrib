#!/usr/bin/env python
# encoding: utf-8
'''
mine.tw -- shortdesc

mine.tw is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2014 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os
import json
import threading
import twitter
import networkx as nx
import cPickle as Pickle
import nltk
import re
import unicodedata
import subprocess
import getopt
from optparse import OptionParser
from pygraphviz import *

__all__ = []
__version__ = 0.1
__date__ = '2014-10-01'
__updated__ = '2014-10-01'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class MineTwitter(threading.Thread):
  consumer_key        = "ykKi3K2ziYxMiIISczYJuEn5z"
  consumer_secret     = "MlcCDbrMhWvhiKuxLweIcpfyAMorwijwY4KiCGZiFK7Q3si2fq"
  access_token        = "36694403-ZnKq9NdVhhiJhVlnGiqt7VWEu9UU8MjvxzjCPsW4N"
  access_token_secret = "0Q9VbcwzgwJgGMer7eOiDrS5oxxqTR0wLVWPJbNFvKjRB"
  api = None

  def __init__(self, consumer_key=None, consumer_secret=None, access_token=None, access_token_secret=None):
    if consumer_key is not None:
      if len(consumer_key) > 0:
        self.consumer_key = consumer_key
    if consumer_secret is not None:
      if len(consumer_secret) > 0:
        self.consumer_secret = consumer_secret
    if access_token is not None:
      if len(access_token) > 0:
        self.access_token = access_token
    if access_token_secret is not None:
      if len(access_token_secret) > 0:
        self.access_token_secret = access_token_secret
    self.api = twitter.Api(self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret)

  def SaveObj(self, fname, obj):
    try:
      wf = open(fname, 'wb')
      wf.seek(0,0)
      Pickle.dump(obj, wf, protocol = Pickle.HIGHEST_PROTOCOL)
      wf.close
    except IOError as e:
      print "I/O error({0}): {1}".format(e.errno, e.strerror)

  def LoadObj(self, fname):
    try:
      rf = open(fname, 'rb')
      rf.seek(0,0)
      robj = Pickle.load(rf)
      rf.close
      return robj
    except (IOError) as e:
      print "I/O error({0})".format(e.strerror)

  def GetMentions(self, tweet):
    rt_patterns = re.compile(r"(@\w*\b)", re.IGNORECASE)
    lmatches = []
    for m in rt_patterns.finditer(tweet):
      lmatches.append(unicode(m.group(0)))
    return lmatches

  def GetReTweetSources(self, tweet):
    rt_patterns = re.compile(r"(RT|via)(\b\W*@\w+)", re.IGNORECASE)
    m = rt_patterns.search(tweet) # return tuple
    if m:
      return unicode(m.group(2)).strip()
    else:
      return ""

  def GetReTweetTags(self, tweet):
    rt_patterns = re.compile(r"#[a-z0-9A-Z]*", re.IGNORECASE)
    lmatches = []
    for m in rt_patterns.finditer(tweet):
      lmatches.append(unicode(m.group(0)))
    return lmatches

  def GetFriends(self):
    users =self.api.GetFriends()
    for u in users:
      print u.name;

  def GetPublicTweets(self):
    public_tweets =self.api.GetHomeTimeline();
    for tweet in public_tweets:
      print tweet.text

  def ProcessTrends(self, bPersistLocal=True):
    #id_delhi = 20070458
    id_india = 23424848
    id_bangalore = 2295420

    trends = self.api.GetTrendsWoeid(id_bangalore)
    print "=== Bangalore trends ==="
    jtrends = json.dumps(trends, default=lambda o: o.__dict__, indent=2);
    print jtrends
    self.SaveObj("/mnt/data/src/exp/python/bangalore_trends_obj", trends)
    print "========================"

    tlist = []
    for trend in trends:
      tlist.append(trend.name)
    bangalore_set = set(tlist)

    trends =self.api.GetTrendsWoeid(id_india)
    print "=== India trends ==="
    jtrends = json.dumps(trends, default=lambda o: o.__dict__, indent=2)
    print jtrends
    self.SaveObj("india_trends_obj", trends)
    print "===================="

    tlist = []
    for trend in trends:
      tlist.append(trend.name)
    india_set = set(tlist)

    union_set = india_set.union(bangalore_set)
    intersection_set = india_set.intersection(bangalore_set)

    print "== common trends =="
    print union_set
    print "== intersection =="
    print intersection_set

  # Searching
  def ProcessSearch(self):

    #tag = "#ISRO";
    tag = "#HikeUpYourLife"

    count = 10000;
    search_results =self.api.GetSearch(term=tag, count=count);
    print "=== Search Results ==="
    print json.dumps(search_results, default=lambda o: o.__dict__, indent=1);
    self.SaveObj("searchresults_obj", search_results)
    print "======================"

    tlist=[]

    #g = nx.DiGraph()
    g = AGraph();
    for result in search_results:
      print "=== Parse Result ==="

      asctweet = unicodedata.normalize("NFC", result._text).encode('ascii', 'ignore')
      ascscreenname = unicodedata.normalize("NFC", result._user.screen_name).encode('ascii', 'ignore')
      ascloc = unicodedata.normalize("NFC", result._user.location).encode('ascii', 'ignore')

      print "Tweet:     " + asctweet
      print "Location:  " + ascloc
      print "Name:      " + ascscreenname

      lrt_tags = self.GetReTweetTags(asctweet)
      print "Tags:      " + str(lrt_tags)
      lrt_mentions = self.GetMentions(asctweet)
      print "Mentions:  " + str(lrt_mentions)
      for l in lrt_mentions:
        g.add_edge(str(l), ascscreenname, {"location" : ascloc, "tags" : "test"})
        
      tlist.append(asctweet)
      rt_source = self.GetReTweetSources(asctweet)
      if not rt_source: continue
      ascsource = str(rt_source)
      print "Source:    " + ascsource

      g.add_edge(ascsource, ascscreenname, {"location" : ascloc, "tags" : "test"})

    count = 0
    words = ""
    for t in tlist:
      for w in t.split():
        words += " " + w
        count += 1

    f = open("words", "wb")
    Pickle.dump(words, f)
    f.close

    #print "=== Words ==="
    #print words
    #print "============="

    print "# :" + str(count)                  # words
    print "Unique: " + str(len(set(words)))   # uniques

    if count > 0:
      print "Diversity: " + str (1.0 * len(set(words))/count)
    else:
      print "Diversity: 0"

    # average words per tweet
    print "Word Count: " + str(count) + " Tlist # elements: " + str(len(tlist))
    print "Avg words per tweet :" + str(1.0*count/len(tlist))

    print "No of nodes: " + str(g.number_of_nodes())
    print "No of edges: " + str(g.number_of_edges())

    outfile = "/mnt/data/src/exp/python/search_results.dot"
    nx.write_dot(g, outfile)
    #args = ("circo", "-Gcharset=latin1", "-Tjpg", "-ooutfile.jpg", "/mnt/data/src/exp/python/search_results.dot")
    args = ("circo", "-v", "-Tjpeg", "-O", "/mnt/data/src/exp/python/search_results.dot")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print output
    
    # frequency analysis
    # K/V Pairs corresponding to values and frequency
    

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"
    program_build_date = "%s" % __updated__

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    #program_usage = '''usage: spam two eggs''' # optional - will be autogenerated by optparse
    program_longdesc = '''''' # optional - give further explanation about what the program does
    program_license = "Copyright 2014 asitk                                             \
            Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"

    if argv is None:
        argv = sys.argv[1:]
    
    try:
        # setup option parser
        # parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        # parser.add_option("-i", "--in", dest="infile", help="set input path [default: %default]", metavar="FILE")
        # parser.add_option("-o", "--out", dest="outfile", help="set output path [default: %default]", metavar="FILE")
        # parser.add_option("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %default]")

        # set defaults
        # parser.set_defaults(outfile="./out.txt", infile="./in.txt")

        # process options
        # (opts, args) = parser.parse_args(argv)

        #if opts.verbose > 0:
        #    print("verbosity level = %d" % opts.verbose)
        #if opts.infile:
        #    print("infile = %s" % opts.infile)
        #if opts.outfile:
        #    print("outfile = %s" % opts.outfile)

        # MAIN BODY #
        mTwitter = MineTwitter()
        mTwitter.ProcessTrends()
        mTwitter.ProcessSearch()

    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'mine.twitter_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
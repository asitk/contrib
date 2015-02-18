#! /usr/bin/python

import MySQLdb
import time
import requests
import json
import phone
import threading
import twitter
import networkx as nx
import cPickle
import nltk
import re
import unicodedata
import subprocess

exitFlag = 0
threadLock = threading.Lock()

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        threadLock.acquire();
        print_time(self.name, self.counter, 5)
        threadLock.release();
        print "Exiting " + self.name

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            thread.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1

class Parent:        # define parent class
   parentAttr = 100
   def __init__(self, attr):
      print "Calling parent constructor"
      Parent.parentAttr = attr;

   def parentMethod(self):
      print 'Calling parent method'

   def setAttr(self, attr):
      Parent.parentAttr = attr

   def getAttr(self):
      print "Parent attribute :", Parent.parentAttr

class Child(Parent): # define child class
   def __init__(self, attr):
      print "Calling child constructor"
      Parent.parentAttr = attr

   def childMethod(self):
      print 'Calling child method'


def testdb ():

  db = MySQLdb.connect("localhost","root","","dtm");

  # prepare a cursor object using cursor() method
  cursor = db.cursor();

  # execute SQL query using execute() method.
  cursor.execute("SHOW TABLES");

  # Fetch a single row using fetchone() method.
  try:
      data = cursor.fetchall();

      for row in data:
        print " %s " % row

  except:
    print "Unable to get data"

  # disconnect from server
  db.close();
  return

def test2 ():
  tinydict = {"name" : "asit", "lname" : "kharshikar", "mname" : "pramod"}
  for k,v in tinydict.items():
    print 'key is ' + k + " " + tinydict[k];

  localtime = time.asctime(time.localtime(time.time()));
  print "Local current time :", localtime;

  return;

def test3 ():
  r = requests.get('http://httpbin.org/ip');
  print r.text;

  print json.dumps(r.text, sort_keys=False, indent=2, separators=(',','\n  '));

  data = [ { 'a' : 'A', 'b' : (2,4), 'c' : 3.0 } ];
  print 'Data ' + repr(data);

  json_string = json.dumps (data, sort_keys=True, indent=1);
  print 'JSON: ', json_string;

  print phone.pots();
  c = Child(10)           # instance of child
  #c.childMethod()        # child calls its method
  #c.parentMethod()       # calls parent's method
  #c.setAttr(200)         # again call parent's method
  #c.getAttr()            # again call parent's method

  threads = []

  # Create new threads
  thread1 = myThread(1, "Thread-1", 1)
  thread2 = myThread(2, "Thread-2", 2)

  # Start new Threads
  thread1.start()
  thread2.start()

  # Add threads to thread list
  threads.append(thread1)
  threads.append(thread2)

  # Wait for all threads to complete
  for t in threads:
    t.join()

  return;

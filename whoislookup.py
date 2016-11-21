#!/usr/bin/python

from urllib2 import HTTPSHandler, build_opener
import pprint
from json import loads
from threading import Thread

# restendpoint="https://whois.arin.net/rest/ip/192.149.252.75"
# request = urllib2.Request(restendpoint,headers={"Accept":"application/json"})
# response=urllib2.urlopen(request)
# pprint.pprint(loads(response.read()))

contextFactory = optionsForClientTLS(restendpoint)
agent = Agent(reactor, contextFactory)
d = agent.request("GET", restendpoint)
d.addCallbacks(display, err)
d.addCallback(lambda ignored: reactor.stop())
reactor.run()
#!/usr/bin/python
# coding:utf8

#! /usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import Controller, RemoteController, Switch, Node
import os



class POXBridge(Controller):
	"Custom Controller class to invoke POX forwarding.l3_learning"
	def start(self):
	    "Start POX learning switch"
            print "starting controller",os.getcwd()
	    self.pox = '%s/pox/pox.py' % os.getcwd()
	    self.cmd( self.pox, 'log --file=output.log,w log.level --DEBUG forwarding.l3_learning_enhanced &' )

	def stop( self ):
	    "Stop POX"
	    self.cmd( 'kill %' + self.pox )

class QuaggaRouter( Node ):
    "Quagga Router running zebra and bgp daemons."
    def __init__(self,*args,**kwargs):
		super(QuaggaRouter,self).__init__(*args,**kwargs)

    def start(self,*args,**kwargs):
		self.cmd("/usr/lib/quagga/zebra -f conf/zebra-%s.conf -d -i /tmp/zebra-%s.pid > logs/%s-zebra-stdout 2>&1" % (self.name,self.name,self.name))
		self.waitOutput()
		self.cmd("/usr/lib/quagga/bgpd -f conf/bgpd-%s.conf -d -i /tmp/bgp-%s.pid > logs/%s-bgpd-stdout 2>&1" % (self.name,self.name,self.name), shell=True)
		self.router.waitOutput()
		log("Starting zebra and bgpd on %s" % self.name)

    def stop(self):
		pass

sn = Mininet()

#bgpNodeExternal = sn.addHost("eebgppeer")
bgpNodeExternal = sn.addSwitch(name="eebgppeer",cls=QuaggaRouter)
#bgpNode = sn.addHost("ebgppeer")
bgpNode = sn.addSwitch(name="ebgppeer",cls=QuaggaRouter)
#lookupserviceNode = sn.addHost("lookservice", ip="0.0.0.0")

bs = sn.addSwitch("s1")

c = sn.addController("firewallapplication", controller=RemoteController, ip='127.0.0.1', port=6633 )

sn.addLink(bgpNodeExternal, bs)
sn.addLink(bs,bgpNode)
#sn.addLink(c,lookupServiceNode)
#lookupserviceNode.popen("export APP= ;flask run --host=0.0.0.0", shell=True)
sn.start()

CLI( sn )

sn.stop()
os.system("killall -9 zebra bgpd")

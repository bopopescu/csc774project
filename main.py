#!/usr/bin/python
# coding:utf8

#! /usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import Controller, RemoteController
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

sn = Mininet()

bgpNodeExternal = sn.addHost("eebgppeer")
bgpNode = sn.addHost("ebgppeer")
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

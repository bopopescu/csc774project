#!/usr/bin/python
# coding:utf8

#! /usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import Controller



class POXBridge(Controller):
	"Custom Controller class to invoke POX forwarding.l3_learning"
	def start(self):
	    "Start POX learning switch"                                                                    
	    self.pox = '%s/pox/pox.py' % os.environ[ 'HOME' ]                                              
	    self.cmd( self.pox, 'log.level --DEBUG forwarding.l3_learning_enhanced &' )                                               
	
	def stop( self ):                                                                                  
	    "Stop POX"                                                                                     
	    self.cmd( 'kill %' + self.pox ) 

sn = Mininet()

bgpNodeExternal = sn.addHost("ebgppeer_external")
bgpNode = sn.addHost("ebgppeer")

bs = sn.addswitch("borderswitch")

c = sn.addController("firewallapplication", controller=POXBridge)

sn.addLink(bgpNodeExternal, bgpNode)

sn.start()

CLI( sn )

sn.stop()
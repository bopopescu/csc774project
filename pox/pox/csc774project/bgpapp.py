from pox.core import core
import pox
log = core.getLogger()

from pox.lib.packet.ethernet import ethernet, ETHER_BROADCAST
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.arp import arp
from pox.lib.packet.tcp import tcp
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.util import str_to_bool, dpid_to_str
from pox.lib.recoco import Timer

import pox.openflow.libopenflow_01 as of

from pox.lib.revent import *

import time

class bgpapp(EventMixin):

  def __init__(self):
      core.openflow.addListeners(self)

  def _handle_PacketIn (self, event):
    dpid = event.connection.dpid
    inport = event.port
    packet = event.parsed
    if not packet.parsed:
      log.warning("%i %i ignoring unparsed packet", dpid, inport)
      return

    log.debug(packet)

    if packet.type == ethernet.IP_TYPE and packet.next.dstip is "10.0.0.2" and packet.next.protocol == ipv4.TCP_PROTOCOL:
      log.debug("%i %i IP %s => %s,%s", dpid,inport,packet.next.srcip,packet.next.dstip,packet.next.next.dstport)

  def _handle_ConnectionUp (self, event):
      log.debug("Edge Switch is up..")
      self.connection=event.connection
      log.debug("Installing Flow for BGP ..")
      self.connection.send(
        of.ofp_flow_mod(
          command=of.OFPFC_ADD,
          action=of.ofp_action_output( port=of.OFPP_CONTROLLER ), # SEND_TO_CONTROLLER
          priority=42,
          match=of.ofp_match( dl_type=0x800, nw_dst="10.0.0.2" )
          ))

  def _handle_ConnectionDown(self,event):
      log.debug("Switch Down")

def launch() :
  core.registerNew(bgpapp)
  log.debug("bgpapp running")

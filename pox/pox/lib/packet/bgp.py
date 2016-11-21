import struct
import string
from packet_utils import *

from packet_base import packet_base
import pox.lib.util as util
from pox.lib.util import is_subclass
from pox.lib.addresses import *

_dhcp_option_unpackers = {}


class bgp(packet_base):
    "BGP Packet struct"

    def __init__(self, raw=None, prev=None, **kw):
        packet_base.__init__(self)
        self.prev = prev

        if raw is not None:
            self.parse(raw)

         self._init(kw)

    def feed(self,packet):
      pass

    def isReady(self):
      return False

class BGPHeader(object):
    MARKER = chr(0xff)*16
    TYPE_OPEN = 1
    TYPE_UPDATE = 2
    TYPE_NOTIFICATION = 3
    TYPE_KEEPALIVE = 4
    def __init__(self):
      pass
       

    def _to_str(self):
        s  = '[BGP op:'+str(self.op)
        s += ' htype:'+str(self.htype)
        s += ' hlen:'+str(self.hlen)
        s += ' hops:'+str(self.hops)
        s += ' xid:'+str(self.xid)
        s += ' secs:'+str(self.secs)
        s += ' flags:'+str(self.flags)
        s += ' ciaddr:'+str(self.ciaddr)
        s += ' yiaddr:'+str(self.yiaddr)
        s += ' siaddr:'+str(self.siaddr)
        s += ' giaddr:'+str(self.giaddr)
        s += ' chaddr:'
        if isinstance(self.chaddr, EthAddr):
            s += str(self.chaddr)
        elif self.chaddr is not None:
            s += ' '.join(["{0:02x}".format(x) for x in self.chaddr])
        s += ' magic:'+' '.join(
            ["{0:02x}".format(ord(x)) for x in self.magic])
        #s += ' options:'+' '.join(["{0:02x}".format(ord(x)) for x in
        #                          self._raw_options])
        if len(self.options):
          s += ' options:'
          s += ','.join(repr(x) for x in self.options.values())
        s += ']'
        return s

    def parse(self, raw):
        assert isinstance(raw, bytes)
        self.raw = raw
        dlen = len(raw)


class BGPOpen(object):
  
  def __init__(self):
    self.version = 0
    self.autonomoussystem = 0
    self.holdtime = 0
    self.bgpidentifier = 0
    self.optionalparameterslength = 0
    self.optionalparameters = 0

  @classmethod
  def unpack (cls, data, code = None):
    pass

  def pack (self):
    return b''

class BGPUpdate(object):
  
  def __init__(self):
    self.unfeasiblerouteslength = 0
    self.withdrawnroutes = 0
    self.totalpathattributelength = 0
    self.pathattributes = 0
    self.networklayerreachability = 0

  @classmethod
  def unpack (cls, data, code = None):
    pass

  def pack (self):
    return b''

class BGPNotification(object):
    def __init__(self):
    self.errorcode = 0
    self.errorsubcode = 0
    self.errordata = 0

  @classmethod
  def unpack (cls, data, code = None):
    pass

  def pack (self):
    return b''

"""
MIT License

Copyright (c) 2016 Neela Krishna Teja Tadikonda

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
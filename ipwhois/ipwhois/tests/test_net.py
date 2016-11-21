import sys
import logging
from ipwhois.tests import TestCommon
from ipwhois.exceptions import (IPDefinedError, ASNLookupError,
                                ASNRegistryError, WhoisLookupError,
                                HTTPLookupError, HostLookupError)
from ipwhois.net import Net

LOG_FORMAT = ('[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s] '
              '[%(funcName)s()] %(message)s')
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


class TestNet(TestCommon):

    def test_ip_invalid(self):
        self.assertRaises(ValueError, Net, '192.168.0.256')
        self.assertRaises(ValueError, Net, 'fe::80::')

    def test_ip_defined(self):
        if sys.version_info >= (3, 3):
            from ipaddress import (IPv4Address, IPv6Address)
        else:
            from ipaddr import (IPv4Address, IPv6Address)

        self.assertRaises(IPDefinedError, Net, '192.168.0.1')
        self.assertRaises(IPDefinedError, Net, 'fe80::')
        self.assertRaises(IPDefinedError, Net, IPv4Address('192.168.0.1'))
        self.assertRaises(IPDefinedError, Net, IPv6Address('fe80::'))

    def test_ip_version(self):
        result = Net('74.125.225.229')
        self.assertEqual(result.version, 4)
        result = Net('2001:4860:4860::8888')
        self.assertEqual(result.version, 6)

    def test_timeout(self):
        result = Net('74.125.225.229')
        self.assertIsInstance(result.timeout, int)

    def test_proxy_opener(self):
        try:
            from urllib.request import (OpenerDirector,
                                        ProxyHandler,
                                        build_opener)
        except ImportError:
            from urllib2 import (OpenerDirector,
                                 ProxyHandler,
                                 build_opener)

        result = Net('74.125.225.229')
        self.assertIsInstance(result.opener, OpenerDirector)

        handler = ProxyHandler()
        opener = build_opener(handler)
        result = Net(address='74.125.225.229', proxy_opener=opener)
        self.assertIsInstance(result.opener, OpenerDirector)

    def test_get_asn_dns(self):
        data = ['"15169 ', ' 74.125.225.0/24 ', ' US ', ' arin ',
                ' 2007-03-13"']
        result = Net('74.125.225.229')
        try:
            self.assertIsInstance(result.get_asn_dns(result=data), dict)
        except AssertionError as e:
            raise e
        except Exception as e:
            self.fail('Unexpected exception raised: {0}'.format(e))

        data = ['"15169 ', ' 74.125.225.0/24 ', ' US ', ' random ',
                ' 2007-03-13"']
        result = Net('74.125.225.229')
        self.assertRaises(ASNRegistryError, result.get_asn_dns, data)

        data = []
        result = Net('74.125.225.229')
        self.assertRaises(ASNLookupError, result.get_asn_dns, data)

    def test_get_asn_whois(self):
        data = ('15169   | 74.125.225.229   | 74.125.225.0/24     | US | arin'
                '     | 2007-03-13')
        result = Net('74.125.225.229')
        try:
            self.assertIsInstance(result.get_asn_whois(result=data), dict)
        except AssertionError as e:
            raise e
        except Exception as e:
            self.fail('Unexpected exception raised: {0}'.format(e))

        data = ('15169   | 74.125.225.229   | 74.125.225.0/24     | US | rdm'
                '     | 2007-03-13')
        result = Net('74.125.225.229')
        self.assertRaises(ASNRegistryError, result.get_asn_whois, 3, data)

    def test_get_asn_http(self):
        data = {
            'nets': {
                'net': {
                    'orgRef': {
                        '@handle': 'APNIC'
                    }
                }
            }
        }
        result = Net('1.2.3.4')
        try:
            self.assertIsInstance(result.get_asn_http(result=data), dict)
        except AssertionError as e:
            raise e
        except Exception as e:
            self.fail('Unexpected exception raised: {0}'.format(e))

        data['nets']['net']['orgRef']['@handle'] = 'RIPE'
        try:
            self.assertIsInstance(result.get_asn_http(result=data), dict)
        except AssertionError as e:
            raise e
        except Exception as e:
            self.fail('Unexpected exception raised: {0}'.format(e))

        data['nets']['net']['orgRef']['@handle'] = 'DNIC'
        try:
            self.assertIsInstance(result.get_asn_http(result=data), dict)
        except AssertionError as e:
            raise e
        except Exception as e:
            self.fail('Unexpected exception raised: {0}'.format(e))

        data['nets']['net']['orgRef']['@handle'] = 'INVALID'
        try:
            self.assertRaises(ASNRegistryError, result.get_asn_http,
                              result=data)
        except AssertionError as e:
            raise e
        except Exception as e:
            self.fail('Unexpected exception raised: {0}'.format(e))

        data = ''
        try:
            self.assertIsInstance(result.get_asn_http(result=data), dict)
        except AssertionError as e:
            raise e
        except Exception as e:
            self.fail('Unexpected exception raised: {0}'.format(e))

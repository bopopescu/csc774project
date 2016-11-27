#!/usr/bin/python
# coding:utf8

__author__ = "ntadiko"

from csv import reader
from pickle import dump, load
from time import clock, time
from signal import signal
from time import time
from logging import basicConfig, debug, info, warning, critical, DEBUG


from ipaddress import ip_address,ip_network
from patricia import trie


binrep=lambda ipaddr,mask: bin(sum([ 256**(3-i)*v for i,v in enumerate(map(int,ipaddr.split('.')))]))[2:].zfill(32)[:int(mask)]

T=trie()
with open("db/db.txt", 'r') as f:
    db=reader(f, delimiter='|')
    for row in db:
        if len(row[0]) < 19:
            T[binrep(*row[0].split(':'))]={"prefix":row[0],"asn":int(row[1].lstrip("AS")),"lastUpdated":time()}

with open("db.pickle","wb") as f:
    dump(T, f)
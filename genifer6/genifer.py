#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys

from rete.common import Has, Rule, WME
from rete.network import Network

def init_network():
    net = Network()
    c1 = Has('□', '$x', '$x')
    c2 = Has('X', '$y', '$y')
    net.add_production(Rule(c1, c2))
    return net

def add_wmes():
    net = init_network()
    wmes = [
		WME('X', '0', '2'),
		WME('X', '1', '1'),
		WME('X', '2', '1'),
        WME('O', '0', '0'),
        WME('O', '1', '0'),
        WME('O', '1', '2'),
        WME('O', '2', '2'),
        WME('□', '0', '1'),
        WME('□', '2', '0'),
    ]
    for wme in wmes:
        net.add_wme(wme)
    print(net.dump())

print(u"\n\u001b[32m——`—,—{\u001b[31;1m@\u001b[0m\n".encode("utf-8"))   # Genifer logo ——`—,—{@

init_network()
add_wmes()

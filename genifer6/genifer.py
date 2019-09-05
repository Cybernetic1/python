#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys

from rete.common import Has, Rule, WME
from rete.network import Network

def init_network():
    net = Network()
    c1 = Has('_', '$x', '$y')
    c2 = Has('X', '$u', '$v')
    c3 = Has('+1', '$u', '$x')
    net.add_production(Rule(c1, c2))
    return net

def add_wmes():
    net = init_network()
    wmes = [
        WME('O', '0', '0'),
        WME('X', '0', '1'),
        WME('O', '1', '0'),
        WME('_', '1', '1')
    ]
    for wme in wmes:
        net.add_wme(wme)
    print(net.dump())

print(u"\n\u001b[32m——`—,—{\u001b[31;1m@\u001b[0m\n".encode("utf-8"))   # Genifer logo ——`—,—{@

init_network()
add_wmes()

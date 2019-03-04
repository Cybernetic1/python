# -*- coding: utf-8 -*-
from rete.common import Has, Rule, WME
from rete.network import Network

def init_network():
    net = Network()
    c0 = Has('$x', 'loves', '$y')
    # c1 = Has('$z', 'loves', 'Mary')
    net.add_production(Rule(c0))
    return net

def add_wmes():
    net = init_network()
    wmes = [
        #WME('John', 'loves', 'Mary'),
        #WME('Mary', 'loves', 'Pete'),
        #WME('Mary', 'loves', 'John')
    ]
    for wme in wmes:
        net.add_wme(wme)
    print(net.dump())

print(u"\n\u001b[32m——`—,—{\u001b[31;1m@\u001b[0m\n")
init_network()
add_wmes()

#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os

from rete.common import Has, Rule, WME, Neg, Ncc, Token
from rete.network import Network

net = Network()

c1 = Has('female', '$a', '_')
c2 = Has('love', '$a', '$b')
c3 = Neg('female', '$b', '_')
# net.add_production(Rule(Ncc(c1, Ncc(c2, c3))))
# net.add_production(Rule(Ncc(c2, Ncc(c3))))
p0 = net.add_production(Rule(c3, c1, Ncc(c2)))
# net.add_production(Rule(c1, Ncc(c2)))
# net.add_production(Rule(c1, Ncc(c2, c3)))
# net.add_production(Rule(c2, c3))

wmes = [
	WME('female', 'Mary', '_'),
	WME('female', 'Ann', '_'),
	WME('love', 'John', 'Pete'),		# 基
	WME('love', 'John', 'John'),		# 自恋
	WME('love', 'Pete', 'Mary'),		# 所谓正常
	WME('love', 'Pete', 'John'),		# 互基
	WME('love', 'Mary', 'Ann'),			# Lesbian
	WME('male', 'John', '_'),
	WME('male', 'Pete', '_'),
]
for wme in wmes:
	net.add_wme(wme)

print("# of results = ", len(p0.items))
print("Results:")
for result in p0.items:
	print(result)

print("\n\x1b[32m——`—,—{\x1b[31;1m@\x1b[0m\n")   # Genifer logo ——`—,—{@

f = open("rete.dot", "w+")
f.write(net.dump())
f.close()
os.system("dot -Tpng rete.dot -orete.png")
print("Rete graph saved as rete.png\n")

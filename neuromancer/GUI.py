# -*- coding: utf8 -*-

import sys
import os
import pygame
import math
import pickle
import chart_studio.plotly as py	# communicate with external plotly server
import plotly.graph_objs as go

cache = []							# dunno what's the use of this??
best = {}

quitting = False
pausing = False

import tkinter as tk
root = tk.Tk()
root.title("Fit Formulas by Genetic Programming  (C)YKY 2020")

# ****** Create embed frame for pygame window ******
embed = tk.Frame(root,width=1000,height=500,takefocus=True)
embed.grid(row=15,column=0,columnspan=3,padx=10,pady=10)
root.update()
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())

pygame.init()
screen = pygame.display.set_mode((1000, 500))

def plot_population(pop):
	global pausing
	screen.fill((0xff,0xff,0xff))
	H = 500
	h = float(H) - 3.0
	x = 1.0
	dx = 999.0 / len(pop)
	# dn = int(math.ceil(dx))
	dn = int(dx)
	# ymax = max(pop, key = lambda x: x['fitness'])['fitness']
	# print("ymax =", ymax)
	ymax = 20.0
	for child in pop:
		z = child['fitness']
		x += dx
		if z < 0.0:
			pygame.draw.line(screen, (0xFF,0x77,0x77), [int(x),H], [int(x),H+int(z*1.0)], dn)
		elif math.isnan(z):
			pygame.draw.line(screen, (0xFF,0x00,0x00), [int(x),H], [int(x),3], dn)
		elif math.isinf(z):
			pygame.draw.line(screen, (0x00,0xFF,0x00), [int(x),H], [int(x),3], dn)
		else:
			# y = h / (1.0 + math.exp(-0.001*z))
			try:
				y = int(z * h / ymax)
			except:
				y = H - 3
			if y > H - 3:
				y = H - 3
			pygame.draw.line(screen, (0x00,0x00,0xFF), [int(x),H], [int(x),H-y], dn)

	embed.update()
	while pausing:
		embed.update()

	pygame.display.flip()

# **** old function ****
def plot_OHLC():
	N = 100     # Number of boxes

	# Each box is represented by a dict that contains the data, the type, and the colour.
	# Use list comprehension to describe N boxes
	data = [{
		'y': [opens[i], highs[i], lows[i], closes[i]],
		'type':'box',
		'marker':{'color': 'green'}
		} for i in range(int(N))]

	# format the layout
	layout = {'xaxis': {'showgrid':False,'zeroline':False, 'tickangle':60,'showticklabels':False},
			  'yaxis': {'zeroline':False,'gridcolor':'white'},
			  'paper_bgcolor': 'rgb(233,233,233)',
			  'plot_bgcolor': 'rgb(233,233,233)',
			  'showlegend':False}

	url = py.plot(data,layout=layout,filename='Box plot')

# **** old function ****
def plot_EMAs():
	# from numpy import * 		# used in plotting
	import plotly.plotly as py	# communicate with external plotly server
	import plotly.graph_objs as go

	N = 100     # Number of boxes

	# Each box is represented by a dict that contains the data, the type, and the colour.
	# Use list comprehension to describe N boxes
	data = [{
		'y': [opens[i], highs[i], lows[i], closes[i]],
		'type':'box',
		'marker':{'color': 'green'}
		} for i in range(int(N))]

	# format the layout
	layout = {'xaxis': {'showgrid':False,'zeroline':False, 'tickangle':60,'showticklabels':False},
			  'yaxis': {'zeroline':False,'gridcolor':'white'},
			  'paper_bgcolor': 'rgb(233,233,233)',
			  'plot_bgcolor': 'rgb(233,233,233)',
			  'showlegend':False}

	url = py.plot(data,layout=layout,filename='Box plot')

"""
	print("Generating population...")
	for c in cache:
		population.append({
			'prog' : c['prog'],
			'fitness' : fitness(c['prog'])
		})
	print("Adding from cache:", len(cache))
	for i in range(0, pop_size - len(cache)):
		print(i, ' ', end=' ')
		sys.stdout.flush()
		# print "\tGenerating formula..."
		prog = generate_random_formula(max_depth, arith_ops, terms)
		# print "\tGenerating condition..."
		# cond = generate_random_condition(max_depth, arith_ops, terms)
		population.append({
			'prog' : prog, \
			# 'cond' : cond, \
			'fitness' : fitness(prog)})

		print("best in pop =", round(population[0]['fitness'],2), "\tprevious best =", round(best['fitness'],2))
"""

def butt_train_pop():
	global best
	max_gens  = int(text1.get("1.0", tk.END)[:-1])
	pop_size  = int(text1c.get("1.0", tk.END)[:-1])
	max_depth = int(text1b.get("1.0", tk.END)[:-1])
	bouts     = int(text1a.get("1.0", tk.END)[:-1])
	p_repro   = float(text0c.get("1.0", tk.END)[:-1])
	p_cross   = float(text0b.get("1.0", tk.END)[:-1])
	p_mut     = float(text0a.get("1.0", tk.END)[:-1])

	# execute the algorithm
	best = search()
	print("Done!")
	print("best fitness = ", round(best['fitness'],8))
	print("\tformula =", end='')
	print(print_program(best['prog']))
	import os
	os.system("beep -f 4000 -l 1000")

def butt_train_again():
	global best
	max_gens  = int(text1.get("1.0", tk.END)[:-1])
	pop_size  = int(text1c.get("1.0", tk.END)[:-1])
	max_depth = int(text1b.get("1.0", tk.END)[:-1])
	bouts     = int(text1a.get("1.0", tk.END)[:-1])
	p_repro   = float(text0c.get("1.0", tk.END)[:-1])
	p_cross   = float(text0b.get("1.0", tk.END)[:-1])
	p_mut     = float(text0a.get("1.0", tk.END)[:-1])

	# execute the algorithm
	best = search(again=True)
	print("Done!")
	print("best fitness = ", round(best['fitness'],8))
	print("\tformula =", end='')
	print(print_program(best['prog']))
	import os
	os.system("beep -f 4000 -l 1000")

def butt_stop_train():
	print("(Function not implemented yet)")
	return

def butt_export_graph():
	s = text2.get("1.0", tk.END)
	if s == "\n":
		fname = "formula.dot"
	else:
		fname = s[:-1]
	print("Exporting best formula as graph....")
	export_tree_as_graph(best['prog'], fname)
	from subprocess import call
	call(["dot", "-Tpng", "-O", fname])
	call(["eog", fname + ".png"])

def butt_print_best():
	print("formula =")
	print(print_program(best['prog']))

def butt_reinsert_best():
	reinsert_best()

def butt_save_population():
	fname = text6.get("1.0", tk.END)[:-1]
	if fname == "":
		fname = "population.pkl"
	save_population(fname)

def butt_load_population():
	fname = text6.get("1.0", tk.END)[:-1]
	if fname == "":
		fname = "population.pkl"
	load_population(fname)

def butt_export_Excel():
	print("Saving to Excel....")
	s = textC.get("1.0", tk.END)
	if s == "\n":
		f = open("results.csv", 'w')
	else:
		f = open(s[:-1], 'w')
	N = float(datasize - 110) / 100.0
	for i in range(0, datasize - 110):
		print(round(i / N, 0), "%\r", end=' ')
		sys.stdout.flush()
		time = i + 100
		prog = eval_tree(best['prog'], time)
		profit = fitness(best['prog'])
		f.write(str(round(prog,2)) + ",")
		f.write(str(round(profit,2)) + "\n")
	print()
	# f.write("\n")
	f.close()

def butt_save_best():
	s = text8.get("1.0", tk.END)
	if s == "\n":
		f = open("formula", 'wb')
	else:
		f = open(s[:-1], 'wb')
	import pickle
	pickle.dump(best, f, pickle.HIGHEST_PROTOCOL)
	f.close()
	print("Formula saved")

def butt_load_best():
	s = text7.get("1.0", tk.END)
	if s == "\n":
		f = open("formula", 'rb')
	else:
		f = open(s[:-1], 'rb')
	import pickle
	best = pickle.load(f)
	f.close()
	cache.append(best)
	print("Formula loaded into cache")

def butt_input_best():
	s = text9.get("1.0", tk.END)
	s2 = s[:-1]
	s = s2.replace("+", "operator.add")
	s2 = s.replace("-", "operator.sub")
	s = s2.replace("*", "operator.mul")
	s2 = s.replace("/", "operator.div")
	prog = eval(s2)
	print(prog)
	best = {
		'prog' : prog,
		'fitness' : fitness(prog, None, 500)
		}
	cache.append(best)
	print("Formula read into cache, current cache size =", len(cache))
	msgA.config(text = "cache size = " + str(len(cache)))

def butt_write_best():
	s = text8.get("1.0", tk.END)
	if s == "\n":
		import glob #, os
		# os.chdir("~/fintech")
		maxnum = 0
		suffix = ""
		for fname in glob.glob("f[0-9]*"):
			s = fname.split('.')
			num = int(s[0][1:])
			if num > maxnum:
				maxnum = num
				if len(s) == 2: suffix = s[1]
		fname = "f" + str(maxnum + 1)
	else:
		fname = s[:-1]
	f = open(fname, 'w')
	print(best['prog'], file=f)
	f.close()
	print("Formula written to:", fname)

def butt_read_best():
	s = text7.get("1.0", tk.END)
	if s == "\n":
		import glob #, os
		# os.chdir("~/fintech")
		maxnum = 0
		suffix = ""
		for fname in glob.glob("f[0-9]*"):
			s = fname.split('.')
			print(s)
			num = int(s[0][1:])
			if num > maxnum:
				maxnum = num
				if len(s) == 2: suffix = s[1]
		fname = "f" + str(maxnum) + ('' if suffix == "" else '.' + suffix)
	else:
		import glob
		matches = glob.glob(s[:-1] + "*")
		if matches == []:
			fname = s[:-1]
		else:
			fname = matches[0]
	f = open(fname, 'r')
	s = f.read()
	f.close()
	s2 = s.replace("<built-in function add>", "operator.add")
	s = s2.replace("<built-in function sub>", "operator.sub")
	s2 = s.replace("<built-in function mul>", "operator.mul")
	s = s2.replace("<built-in function div>", "operator.div")
	prog = eval(s)
	# print prog
	global best
	best = {
		'prog' : prog,
		'fitness' : fitness(prog, None, 500)
		}
	cache.append(best)
	print("Formula read into cache, current cache size =", len(cache))
	msgA.config(text = "cache size = " + str(len(cache)))

def butt_clear_cache():
	cache = []
	print("Cache cleared")
	msgA.config(text = "cache size = " + str(len(cache)))

def show_formula(str):
	text10.delete(1.0, tk.END)
	text10.insert(tk.END, str)

# **** Parameters

tk.Label(root, text="P(mutate)").grid(row=0, column=2, sticky=tk.W)
text0a = tk.Text(root, height=1, width=10)
text0a.grid(row=0,column=2,sticky=tk.E)

tk.Label(root, text="P(cross)").grid(row=1, column=2, sticky=tk.W)
text0b = tk.Text(root, height=1, width=10, wrap=tk.NONE)
text0b.grid(row=1,column=2,sticky=tk.E)

tk.Label(root, text="P(repro)").grid(row=2, column=2, sticky=tk.W)
text0c = tk.Text(root, height=1, width=10)
text0c.grid(row=2,column=2,sticky=tk.E)

tk.Label(root, text="#Gens").grid(row=3, column=2, sticky=tk.W)
text1 = tk.Text(root, height=1, width=10)
text1.grid(row=3,column=2,sticky=tk.E)

tk.Label(root, text="bouts").grid(row=4, column=2, sticky=tk.W)
text1a = tk.Text(root, height=1, width=10)
text1a.grid(row=4,column=2,sticky=tk.E)

tk.Label(root, text="depth").grid(row=5, column=2, sticky=tk.W)
text1b = tk.Text(root, height=1, width=10)
text1b.grid(row=5,column=2,sticky=tk.E)

tk.Label(root, text="pop size").grid(row=6, column=2, sticky=tk.W)
text1c = tk.Text(root, height=1, width=10)
text1c.grid(row=6,column=2,sticky=tk.E)

# Training buttons

button2 = tk.Button(root, text="Train population", command=butt_train_pop)
button2.grid(row=0,column=0,sticky=tk.W)

button2b = tk.Button(root, text="Continue training", command=butt_train_again)
button2b.grid(row=0,column=0,sticky=tk.E)

button2c = tk.Button(root, text="stop", command=butt_stop_train)
button2c.grid(row=0,column=1)

button3 = tk.Button(root, text="export formula graph", command=butt_export_graph)
button3.grid(row=1,column=0)
text3 = tk.Text(root, height=1, width=30)
text3.grid(row=1,column=1)
text3.insert(tk.END, "formula.dot")

button6 = tk.Button(root, text="save population", command=butt_save_population)
button6.grid(row=2,column=0,sticky=tk.W)
button6b = tk.Button(root, text="load population", command=butt_load_population)
button6b.grid(row=2,column=0,sticky=tk.E)
text6 = tk.Text(root, height=1, width=30)
text6.grid(row=2,column=1)
text6.insert(tk.END, "population.pkl")

button7 = tk.Button(root, text="load formula", command=butt_read_best)
button7.grid(row=3,column=0,sticky=tk.W)
text7 = tk.Text(root, height=1, width=25)
text7.grid(row=3,column=0,sticky=tk.E)
# text7.insert(tk.END, "f1")
button8 = tk.Button(root, text="save formula", command=butt_write_best)
button8.grid(row=4,column=0,sticky=tk.W)
text8 = tk.Text(root, height=1, width=25)
text8.grid(row=4,column=0,sticky=tk.E)
# text8.insert(tk.END, "f1")

button4 = tk.Button(root, text="print best formula", command=butt_print_best)
button4.grid(row=3,column=1)
button5 = tk.Button(root, text="re-insert best into pop", command=butt_reinsert_best)
button5.grid(row=4,column=1)

buttonA = tk.Button(root, text="clear cache", command=butt_clear_cache)
buttonA.grid(row=5,column=0)
msgA = tk.Message(root, width=70, text="cache size = " + str(len(cache)))
msgA.grid(row=5,column=1)

# buttonD = tk.Button(root, text="quit", command=exit)
# buttonD.grid(row=1,column=0)

buttonC = tk.Button(root, text="save as Excel", command=butt_export_Excel)
buttonC.grid(row=6,column=0)
textC = tk.Text(root, height=1, width=30)
textC.grid(row=6,column=1)
textC.insert(tk.END, "results.csv")

button9 = tk.Button(root, text="insert formula", command=butt_input_best)
button9.grid(row=7,column=0)
text9 = tk.Text(root, height=1, width=70)
text9.grid(row=7,column=1,columnspan=2)
text9.insert(tk.END, "(1 + 1)")

text10 = tk.Text(root, height=1, width=120)
text10.grid(row=8,column=0,columnspan=3)

def key_pressed(event):
	c = repr(event.char)
	print ("pressed", c)
	if (c == 'p'):
		pausing = True
	elif (c == 's'):
		pausing = False

def mouse_clicked(event):
	global pausing
	embed.focus_set()
	pygame.display.flip()
	pausing = not pausing
	print("clicked at", event.x, event.y)
	print("Paused" if pausing else "Resumed")

embed.bind("<Key>", key_pressed)
embed.bind("<Button-1>", mouse_clicked)
embed.focus_set()

screen.fill((0xff,0xff,0xff))
root.update()
pygame.display.flip()

def start_GUI():
	# [s] save best formula\n\
	# [l] load best formula\n\
	text0b.insert(tk.END, str(p_cross))
	text0a.insert(tk.END, str(p_mut))
	text0c.insert(tk.END, str(p_repro))

	text1.insert(tk.END, str(max_gens))
	text1a.insert(tk.END, str(bouts))
	text1b.insert(tk.END, str(max_depth))
	text1c.insert(tk.END, str(pop_size))

	root.mainloop()
	exit(0)

# -*- coding: utf-8 -*-

import time
import random
import shelve		# for object persistence
import pdb			# for debugging

# import qlearn_mod_random as qlearn # to use the alternative exploration method
import alice # to use standard exploration method
# reload(alice)

# 打井游戏大约有 N = 9 × 8 × 7 × ... × 2 × 1 = 9! = 362880 个状态。
# 可以选择的 actions 数目是 9×8 + 9×8×7×6 + 9×8×7×6×5×4 + 9×8×7×6×5×4×3×2 = 72 + 3024 + 60480 + 362880 = 426456。
state = 0


ai = alice.QLearn(学习速度=0.1, 折扣=0.9, 随机行为=0.1)
lastState = None
lastAction = None

def update():
	state = calcState()
	reward = -1

	if cell == cat:
		eaten += 1
		reward = -100
		if lastState is not None:
			ai.learn(lastState, lastAction, reward, state)
		lastState = None

		cell = pickRandomLocation()
		return

	if cell == cheese:
		fed += 1
		reward = 50
		cheese.cell = pickRandomLocation()

	if lastState is not None:
		ai.learn(lastState, lastAction, reward, state)

	state = calcState()
	action = ai.chooseAction(state)
	lastState = state
	lastAction = action

	goInDirection(action)

def calcState():
	def cellvalue(cell):
		if cat.cell is not None and (cell.x == cat.cell.x and
									 cell.y == cat.cell.y):
			return 3
		elif cheese.cell is not None and (cell.x == cheese.cell.x and
										  cell.y == cheese.cell.y):
			return 2
		else:
			return 1 if cell.wall else 0

	return tuple([cellvalue(world.getWrappedCell(cell.x + j, cell.y + i))
				  for i,j in lookcells])

age = 0
endAge = age + 860000

print("e = 随机行为, W = fed, L = eaten\n")

while age < endAge:
	# world.update()

	if age % 10000 == 0:
		print("age {:d}, e: {:0.2f}, W: {:d}, L: {:d}"\
			.format(age, ai.随机行为, fed, eaten))
		eaten = 0
		fed = 0

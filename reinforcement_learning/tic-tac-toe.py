# -*- coding: utf-8 -*-

import time
import random
import shelve		# for object persistence
import pdb			# for debugging
from array import array

# import qlearn_mod_random as qlearn # to use the alternative exploration method
import Qlearn # to use standard exploration method
# reload(alice)

# 打井游戏大约有 N = 9 × 8 × 7 × ... × 2 × 1 = 9! = 362880 个状态。
# 但这个计算方法会把很多相同的状态重复计算（因为下井的次序是不影响状态的）。
# 另一种计算方法似乎表示 3^9 = 19683 个状态。
# 可以选择的 actions 数目是 9×8 + 9×8×7×6 + 9×8×7×6×5×4 + 9×8×7×6×5×4×3×2 = 72 + 3024 + 60480 + 362880 = 426456。
state = (0,0,0,  0,0,0,  0,0,0)		# a tuple of 9 components

ai = Qlearn.QLearn(学习速度=0.1, 折扣=0.9, 随机行为=0.1)
lastState = None
lastAction = None
step = 0

def next_state(a, who):
	global state
	if state[a] != 0:
		print("illegal move\n")
		exit()
	s1 = list(state)
	s1[a] = who
	state = tuple(s1)

def update():
	global state
	reward = 0

	# Alice move
	action = ai.chooseAction(state)
	lastState = state
	lastAction = action
	state = next_state(action, who=1)

	# Bob move
	# determine which positions are empty
	spaces = []
	for i, c in enumerate(list(state)):
		if c == 0:
			spaces.append(i)
	bob_action = random.choice(spaces)
	state = next_state(bob_action, who=2)

	if won(1):				# Alice (= 1) has won
		reward = +100
		# restart
		lastState = None
		# cell = pickRandomLocation()
		return

	if won(2):				# Bob (= 2) has won
		reward = -100
		# restart
		lastState = None
		# cell = pickRandomLocation()
		return

	if lastState is not None:
		ai.learn(lastState, lastAction, reward, state)


def won(who):				# check if player has won
	# total of 8 cases:
	# 0 1 2
	# 3 4 5
	# 6 7 8

	if (state[0] == who and state[1] == who and state[2] == who):
		return True
	if (state[3] == who and state[4] == who and state[5] == who):
		return True
	if (state[6] == who and state[7] == who and state[8] == who):
		return True

	if (state[0] == who and state[3] == who and state[6] == who):
		return True
	if (state[1] == who and state[4] == who and state[7] == who):
		return True
	if (state[2] == who and state[5] == who and state[8] == who):
		return True

	if (state[0] == who and state[4] == who and state[8] == who):
		return True
	if (state[2] == who and state[4] == who and state[6] == who):
		return True

	return False

age = 0
endAge = age + 860000

print("e = 随机行为, W = fed, L = eaten\n")

while age < endAge:
	update()

	if age % 10000 == 0:
		print("age {:d}, e: {:0.2f}, L: {:d}"\
			.format(age, ai.随机行为, step))
		step = 0

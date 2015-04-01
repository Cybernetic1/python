import random

''' The aim of Q-learning is to learn Q values.

Each Q value Q(S,A) is the utility of doing action A in state S.

The update rule is:
	Q(S,A) += alpha [ R(S) + gamma max Q(S',A') - Q(S,A) ].
									A'
where:
	alpha = learning rate
	gamma = discount factor of rewards
	R(S) = reward gotten at state S
	S' = any state gotten from state S after action A
	the max value = U(S') = utility of S'.

The idea of Q-learning comes from TD (temporal-difference) learning,
where the update formula is:
	U(S) += alpha [ R(S) + gamma U(S') - U(S) ].
From this we can see the 'desired' value of U(S) is:
	R(S) + gamma U(S').
This update occurs whenever state S transits to S'.

In passive learning (that is, when the policy is fixed and we just want
to find the utilities of every state), the utility U(S) is equal to its
reward plus the expected utility of all its subsequent states S':
	U(S) = R(S) + gamma ∑ P(S' | S, pi(S)) U(S')
						S'
where pi is the fixed policy.  This is the Bellman optimality condition
and is also the 'equilibrium' we want to achieve in TD learning.

The TD update rule works without needing the transition probabilities
because rarely-occurring transitions are automatically accounted for.

In active learning the policy itself has to be learned.
[To be continued...]

'''

class QLearn:
	def __init__(self, actions, epsilon=0.1, alpha=0.2, gamma=0.9):
		self.q = {}

		self.epsilon = epsilon
		self.alpha = alpha
		self.gamma = gamma
		self.actions = actions

	def getQ(self, state, action):
		return self.q.get((state, action), 0.0)
		# return self.q.get((state, action), 1.0)

	def learnQ(self, state, action, reward, value):
		oldv = self.q.get((state, action), None)
		if oldv is None:
			self.q[(state, action)] = reward
		else:
			self.q[(state, action)] = oldv + self.alpha * (value - oldv)

	def chooseAction(self, state):
		if random.random() < self.epsilon:
			action = random.choice(self.actions)
		else:
			q = [self.getQ(state, a) for a in self.actions]
			maxQ = max(q)
			count = q.count(maxQ)
			if count > 1:
				best = [i for i in range(len(self.actions)) if q[i] == maxQ]
				i = random.choice(best)
			else:
				i = q.index(maxQ)

			action = self.actions[i]
		return action

	def learn(self, state1, action1, reward, state2):
		maxqnew = max([self.getQ(state2, a) for a in self.actions])
		self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)

	def printQ(self):
		keys = self.q.keys()
		states = list(set([a for a,b in keys]))
		actions = list(set([b for a,b in keys]))

		dstates = ["".join([str(int(t)) for t in list(tup)]) for tup in states]
		print (" "*4) + " ".join(["%8s" % ("("+s+")") for s in dstates])
		for a in actions:
			print ("%3d " % (a)) + \
				" ".join(["%8.2f" % (self.getQ(s,a)) for s in states])

	def printV(self):
		keys = self.q.keys()
		states = [a for a,b in keys]
		statesX = list(set([x for x,y in states]))
		statesY = list(set([y for x,y in states]))

		print (" "*4) + " ".join(["%4d" % (s) for s in statesX])
		for y in statesY:
			maxQ = [max([self.getQ((x,y),a) for a in self.actions])
					for x in statesX]
			print ("%3d " % (y)) + " ".join([ff(q,4) for q in maxQ])

import math
def ff(f,n):
	fs = "{:f}".format(f)
	if len(fs) < n:
		return ("{:"+n+"s}").format(fs)
	else:
		return fs[:n]
	# s = -1 if f < 0 else 1
	# ss = "-" if s < 0 else ""
	# b = math.floor(math.log10(s*f)) + 1
	# if b >= n:
	#     return ("{:" + n + "d}").format(math.round(f))
	# elif b <= 0:
	#     return (ss + ".{:" + (n-1) + "d}").format(math.round(f * 10**(n-1)))
	# else:
	#     return ("{:"+b+"d}.{:"+(n-b-1)+"

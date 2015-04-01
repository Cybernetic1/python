import random

''' Notes from the book "AI - a modern approach" (3rd edition).

Ch 21 talks about reinforcement learning.  The aim of Q-learning is to
learn Q values.  Each Q value Q(S,A) is the utility of doing action A in
state S.

The update rule is:
	Q(S,A) += 𝞪 [ R(S) + 𝞬 max Q(S',A') - Q(S,A) ].
						   A'
where:
	𝞪 = learning rate
	𝞬 = discount factor of rewards
	R(S) = reward gotten at state S
	S' = any state gotten from state S after action A
	the max value = U(S') = utility of S'.

The idea of Q-learning comes from TD (temporal-difference) learning,
where the update formula is:
	U(S) += 𝞪 [ R(S) + 𝞬 U(S') - U(S) ].
From this we can see the 'desired' value of U(S) is:
	R(S) + 𝞬 U(S').
This update occurs whenever a state transition S -> S' occurs.

In passive learning (that is, when the policy is fixed and we just want
to find the utilities of every state), the utility U(S) is equal to its
reward plus the expected utility of all its subsequent states S':
	U(S) = R(S) + 𝞬 ∑ P(S' | S, 𝝿(S)) U(S')
					S'
where 𝝿 is the fixed policy.  This is the famous Bellman optimality
condition and is also the 'equilibrium' we want to achieve in TD learning.

The TD update rule works without needing the transition probabilities
because rarely-occurring transitions are automatically accounted for.

Another method for passive learning is ADP (adaptive dynamic programming).
This involves learning the transition model P(S'|S,𝝿(S)) and substituting
it into the Bellman condition to obtain U(S).  It simply records the
frequencies of transitions of each action, using them to estimate P(S'|S,𝝿(S)).
It's called dynamic programming because it exploits the Bellman condition.
It uses maximum likelihood to estimate the transition model P(), and then
assumes that this is the correct model.  Choosing actions according to
such a model is not always a good idea, as we should consider the distribution
over all possible / probable models.

In active learning the policy itself has to be learned.  That brings in the
question of exploration vs exploitation, and greedy algorithms often converge
to rather bad policies because of the lack of exploration to learn models of
the world.

For active learning, an "optimistic" utility U₊ is used which includes the
"exploration function" f(utility, n):
	U₊(S) = R(S) + 𝞬 max f( ∑ P(S'|S,A) U₊(S') , N(S,A) )
where N(S,A) is the number of times action A has been tried in state S.
The function f() detemines the balance of preference between utility and
novelty (represented by the number n).  f() is monotonously increasing for
utility, and monotonously decreasing for n.  A simple possible definition
of f(u,n) is:
	f(u,n)	= R		if n < N0
			= u		otherwise
which ensures that each state-action pair is tried at least N0 times.
R is a constant reward assigned to novel territories.

SARSA (state-action-reward-state-action) is a subtle variant of Q-learning
with update formula:
	Q(S,A) += 𝞪 [ R(S) + 𝞬 Q(S',A') - Q(S,A) ].

Q-Learning is a model-free learning method because it does not attempt to
learn the (transition) model P(S'|S,𝝿(S)).

Ch 17 talks about Value Iteration and Policy Iteration, and POMDP.

Ch 15 talks about filtering, HMM, Kalman filtering, dynamic Bayes nets.

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

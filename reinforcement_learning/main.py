# -*- coding: utf-8 -*-

import time
import random
import shelve

import pdb

import cellular
# reload(cellular)
# import qlearn_mod_random as qlearn # to use the alternative exploration method
import qlearn # to use standard exploration method
# reload(qlearn)

directions = 8			# Can move up, down, left, right, and diagonally x 4

# Seems to be the cells that are visible to the mouse
lookdist = 2
lookcells = []
for i in range(-lookdist,lookdist+1):
    for j in range(-lookdist,lookdist+1):
        if (abs(i) + abs(j) <= lookdist) and (i != 0 or j != 0):
            lookcells.append((i,j))

def pickRandomLocation():
    while 1:
        x = random.randrange(world.width)
        y = random.randrange(world.height)
        cell = world.getCell(x, y)
        if not (cell.wall or len(cell.agents) > 0):
            return cell

# Defines a cell in the world
class Cell(cellular.Cell):
    wall = False

    def colour(self):
        if self.wall:
            return 'black'
        else:
            return 'white'

    def load(self, data):
        if data == 'X':
            self.wall = True
        else:
            self.wall = False

# Defines behavior of cat
class Cat(cellular.Agent):
    cell = None
    score = 0
    colour = 'red'

    def update(self):
        cell = self.cell
        if cell != mouse.cell:
            self.goTowards(mouse.cell)
            while cell == self.cell:
                self.goInDirection(random.randrange(directions))

# Defines behavior of cheese
class Cheese(cellular.Agent):
    colour = 'yellow'

    def update(self):
        pass

# Defines behavior of mouse
class Mouse(cellular.Agent):
    colour = 'blue'

    def __init__(self):
        self.ai = None
        self.ai = qlearn.QLearn(actions=range(directions),
                                alpha=0.1, gamma=0.9, epsilon=0.1)
        self.eaten = 0
        self.fed = 0
        self.lastState = None
        self.lastAction = None

    def update(self):
        state = self.calcState()
        reward = -1

        if self.cell == cat.cell:
            self.eaten += 1
            reward = -100
            if self.lastState is not None:
                self.ai.learn(self.lastState, self.lastAction, reward, state)
            self.lastState = None

            self.cell = pickRandomLocation()
            return

        if self.cell == cheese.cell:
            self.fed += 1
            reward = 50
            cheese.cell = pickRandomLocation()

        if self.lastState is not None:
            self.ai.learn(self.lastState, self.lastAction, reward, state)

        state = self.calcState()
        action = self.ai.chooseAction(state)
        self.lastState = state
        self.lastAction = action

        self.goInDirection(action)

    def calcState(self):
        def cellvalue(cell):
            if cat.cell is not None and (cell.x == cat.cell.x and
                                         cell.y == cat.cell.y):
                return 3
            elif cheese.cell is not None and (cell.x == cheese.cell.x and
                                              cell.y == cheese.cell.y):
                return 2
            else:
                return 1 if cell.wall else 0

        return tuple([cellvalue(self.world.getWrappedCell(self.cell.x + j, self.cell.y + i))
                      for i,j in lookcells])

mouse = Mouse()
cat = Cat()
cheese = Cheese()

world = cellular.World(Cell, directions=directions, filename='waco.maze.txt')
world.age = 0

world.addAgent(cheese, cell=pickRandomLocation())
world.addAgent(cat)
world.addAgent(mouse)

epsilonx = (0,100000)
epsilony = (0.1,0)
epsilonm = (epsilony[1] - epsilony[0]) / (epsilonx[1] - epsilonx[0])

endAge = world.age + 600000

print "e = epsilon, W = mouse.fed, L = mouse.eaten\n"

while world.age < endAge:
    world.update()

    '''if world.age % 100 == 0:
        mouse.ai.epsilon = (epsilony[0] if world.age < epsilonx[0] else
                            epsilony[1] if world.age > epsilonx[1] else
                            epsilonm*(world.age - epsilonx[0]) + epsilony[0])'''

    if world.age % 10000 == 0:
        print "age {:d}, e: {:0.2f}, W: {:d}, L: {:d}"\
            .format(world.age, mouse.ai.epsilon, mouse.fed, mouse.eaten)
        mouse.eaten = 0
        mouse.fed = 0


world.display.activate(size=30)
world.display.delay = 1
while 1:
    world.update()

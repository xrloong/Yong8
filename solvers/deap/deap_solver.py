import array
import random

import numpy

from itertools import chain

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

import sympy as sp

def mutDE(y, a, b, c, f):
	size = len(y)
	for i in range(len(y)):
		y[i] = a[i] + f*(b[i]-c[i])
	return y

def cxBinomial(x, y, cr):
	size = len(x)
	index = random.randrange(size)
	for i in range(size):
		if i == index or random.random() < cr:
			x[i] = y[i]
	return x

def cxExponential(x, y, cr):
	size = len(x)
	index = random.randrange(size)
	# Loop on the indices index -> end, then on 0 -> index
	for i in chain(range(index, size), range(0, index)):
		x[i] = y[i]
		if random.random() < cr:
			break
	return x

def deapSolve(symbols, constraints, objective, verbose=False):
	variableCount = len(symbols)

	penalties = []
	targetObjective = objective
	for c in constraints:
		if c.rel_op == '==':
			f=abs(c.lhs-c.rhs)
		elif c.rel_op in ['<=', '<']:
			f=-(c.rhs-c.lhs)
		elif c.rel_op in ['>=', '>']:
			f=-(c.lhs-c.rhs)
		penalty=(f+abs(f))/2
		penalties.append(penalty)

	penaltyWeight = -10
	targetObjective = objective + penaltyWeight * sum(penalties)

	lambdifiedObjective = sp.lambdify(symbols, targetObjective)
	evaluate = lambda params: (lambdifiedObjective(*params),)
	weights=tuple([1.0])


	creator.create("FitnessMax", base.Fitness, weights=weights)
	creator.create("Individual", array.array, typecode='f', fitness=creator.FitnessMax)

	toolbox = base.Toolbox()

	# Attribute generator
	toolbox.register("attr_bool", random.randint, 0, 1)
	toolbox.register("attr_int", random.randint, 0, 255)
	toolbox.register("attr_float", random.uniform, 0, 255)

	# Structure initializers
	toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, variableCount)
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)

	toolbox.register("evaluate", evaluate)
	toolbox.register("mate", cxBinomial, cr=0.8)
	toolbox.register("mutate", mutDE, f=0.8)
	toolbox.register("select", tools.selRandom, k=3)

	def main():
		random.seed(64)

		pop = toolbox.population(n=40)
		hof = tools.HallOfFame(1)
		stats = tools.Statistics(lambda ind: ind.fitness.values)
		stats.register("avg", numpy.mean)
		stats.register("std", numpy.std)
		stats.register("min", numpy.min)
		stats.register("max", numpy.max)

		logbook = tools.Logbook()
		logbook.header = "gen", "evals", "std", "min", "avg", "max"

		# Evaluate the individuals
		fitnesses = toolbox.map(toolbox.evaluate, pop)
		for ind, fit in zip(pop, fitnesses):
			ind.fitness.values = fit

		record = stats.compile(pop)
		logbook.record(gen=0, evals=len(pop), **record)
		if verbose:
			print(logbook.stream)

		NGEN = 4000
		for g in range(1, NGEN):
			children = []
			for agent in pop:
				# We must clone everything to ensure independance
				a, b, c = [toolbox.clone(ind) for ind in toolbox.select(pop)]
				x = toolbox.clone(agent)
				y = toolbox.clone(agent)
				y = toolbox.mutate(y, a, b, c)
				z = toolbox.mate(x, y)
				del z.fitness.values
				children.append(z)

			fitnesses = toolbox.map(toolbox.evaluate, children)
			for (i, ind), fit in zip(enumerate(children), fitnesses):
				ind.fitness.values = fit
				if ind.fitness > pop[i].fitness:
					pop[i] = ind

			hof.update(pop)
			record = stats.compile(pop)
			logbook.record(gen=g, evals=len(pop), **record)
			if verbose:
				print(logbook.stream)

		log = logbook
		return pop, log, hof
	pop, log, hof = main()

	individual = max(hof, key = lambda idv: idv.fitness)
	if verbose:
		print("Best individual is ", individual)
		print("with fitness", individual.fitness.values[0])

	del creator.FitnessMax
	del creator.Individual

	return individual.tolist()


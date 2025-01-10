import random

Genes = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'#List of possible genes (Characters in this case)
Target = 'In hopes of finding out the truth, he entered the one-room library.'#Target string

#Creates an inital population made up of randomly selected genes
def initalPopulation(popSize,genes,targetLen):
    population = []
    for x in range(popSize):
        chromosome = ''
        for _ in range(targetLen): #Underscore is used as either a generic variable or an ignore variable
            chromosome += random.choice(genes)
        population.append(chromosome)
    return population

#Mutates a given string(child) to add some variance (Chance should be lower than around 5% but higher than 1%)
def mutate(child,mutationRate,genes):
    mutatedChild = ''
    for x in child:
        if random.random()>1-mutationRate:
            mutatedChild+=random.choice(genes)
        else:
            mutatedChild+=x
    return mutatedChild

#Evaluates a given string by assigning a fitness value depending on how close it is to the target string (Higher is better, Max is length of target string)
def fitnessEvaluation(selectedChromosome,target):
    fitness = len(target)
    for x in range(len(target)):
        if selectedChromosome[x] != target[x]:
            fitness-=1
    return fitness

#Creates a child string that aims to be 50/50 from each parent but favours parent 2 if odd
def crossover(parent1,parent2):
    child = ''
    if len(parent1)>1:
        parent1Max = len(parent1)//2
    else:
        return 'Error Too Short'
    parent2Max = len(parent1) - parent1Max
    p1 = 0
    p2 = 0
    for x in range(len(parent1)):
        if p1==parent1Max:
            child += parent2[x]
            p2+=1
        elif p2==parent2Max:
            child += parent1[x]
            p1+=1
        else:
            choice = random.choice(['p1','p2'])
            if choice == 'p1':
                child += parent1[x]
                p1+=1
            else:
                child += parent2[x]
                p2+=1     
    return child

#Takes target string and starting from a random string gets closer to the target string using a genetic algorithm
def geneticAlgorithm(popSize,target,genes,mutationRate):
    maxFitness = 0#Max fitness of current population
    population = initalPopulation(popSize,genes,len(target))
    iteration = 0#Generation
    while maxFitness != len(target):
        iteration+=1
        population = sorted(population, key=lambda x:fitnessEvaluation(x,target),reverse=True) #lambda x in sorted is like saying for everything in population
        population = population[:popSize//2]
        children = []
        for x in range(len(population)):
            #Creates 2 children by picking a random parent that is not the current parent for each child
            children.append(crossover(population[x],random.choice(population[0:x]+population[x+1:])))
            children.append(crossover(population[x],random.choice(population[0:x]+population[x+1:])))
        #In case of an odd population size you need 1 more child so the strongest of the current population gets another child
        if len(children) != popSize:
            children.append(crossover(population[0],random.choice(population[1:])))
        print('Generation:'+str(iteration))
        print(population[0])
        print("Fitness Score:",fitnessEvaluation(population[0],target))
        print("--------------------------------------------------------")
        maxFitness = fitnessEvaluation(population[0],target)
        population = []
        #Mutate each child and add to the population
        for x in children:
            population.append(mutate(x,mutationRate,genes))#Mutation rate should be between 5% to 1% (Longer targets should have a lower rate to stop the likeily hood of bad mutations)
Target = str(input("Write a string for the program to find (No punctuation or special characters):"))
MutationRate = float(input("Enter a mutation rate (Should preferably be between 0.05 to 0.01 (Longer targets should have a lower rate):"))
geneticAlgorithm(500,Target,Genes,MutationRate)

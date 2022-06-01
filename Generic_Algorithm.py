import random
import copy
from objects import Bird
from settings import *

def next_generation(array,backup):

    calculate_fitness(backup)

    for i in range(TOTAL_POPULATION):
        array.append(pick_one(backup))
    backup.clear()



def pick_one(backup):
        index=0
        r=random.uniform(0,1)
        while r>0:
            r-=backup[index].fitness
            index+=1
        index-=1

        bird = copy.deepcopy(backup[index])
        child = Bird((WIDTH//8, HEIGHT//TOTAL_POPULATION*random.randint(0,TOTAL_POPULATION)),30,brain=bird.brain)
        child.mutate(0.1)
        return child


def calculate_fitness(array):
    score_sum = 0
    for b in array:
        score_sum += b.score

    for b in array:
        b.fitness = b.score/score_sum
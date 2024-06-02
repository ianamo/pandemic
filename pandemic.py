#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 14:27:12 2024

@author: ianamo
"""

import random

class Pandemic(object):
    def __init__(self, population=[], pathogens={}, infected={},encounters=5):
        self.t = 0
        self.pop_size = len(population)
        self.population = population
        self.pathogens = pathogens
        self.infected = 0
        self.infected_pop = []
        self.hospitalized = 0
        self.dead = 0
        self.encounters = encounters
        
        for k in infected:
            for i in range(infected[k]):
                p = random.choice(self.population)
                p.infect(pathogens[k])
    
    def turn(self):
        self.t += 1
        for p in self.infected_pop:
            encounter_group = []
            for i in range(self.encounters):
                encounter_group.append(random.choice(self.population))
            p.update(encounter_group)
        self.infected_pop = [p for p in self.population if p.infected]
        self.infected = len(self.infected_pop)
        self.hospitalized = len([p for p in self.population if p.hospitalized])
        for p in self.population:
            if p.dead:
                self.dead+=1
                self.population.remove(p)
                self.infected_pop.remove(p)
                self.infected-=1
                self.hospitalized -= 1
    
    def show(self):
        print(f"""
              t: {self.t}
              Population: {self.pop_size}
              Infected: {self.infected}
              Hospitalized: {self.hospitalized}
              Dead: {self.dead}
              """)
                
class Person(object):
    def __init__(self, clear_rate):
        self.infected = False
        self.hospitalized = False
        self.dead = False
        self.infected_days = 0
        self.clear_rate = clear_rate
        self.pathogens = []
        self.immune = []
    
    def infect(self,pathogen):
        self.pathogens.append(pathogen)
        self.infected = True
        self.immune.append(pathogen)
    
    def is_immune(self, v):
        return v in self.immune
    
    def update(self, encounter_group):
        
        if self.infected:
            self.infected_days+=1
        
        for v in self.pathogens:
            if random.random() < self.clear_rate:
                self.pathogens.remove(v)
            elif self.infected_days > v.serious:
                self.hospitalized = True
            elif self.infected_days > v.fatal:
                self.dead = True
                return 'dead'
        
        for p in encounter_group:
            for v in self.pathogens:
                if random.random() < v.infect_rate and not p.is_immune(v):
                    p.infect(v)

class Pathogen(object):
    def __init__(self, name, infect_rate, serious, fatal):
        self.name = name
        self.infect_rate = infect_rate
        self.serious = serious
        self.fatal = fatal
        
    def __str__(self):
        return self.name
    

def prepare_population(size, clear_rate):
    pop = []
    for i in range(size):
        pop.append(Person(clear_rate=clear_rate))
    return pop

my_pop = prepare_population(1000, 0.08)
covid = Pathogen("COVID-19",0.3,15,30)
pan = Pandemic(population=my_pop, pathogens={'COVID-19':covid},infected={'COVID-19':1})

for i in range(90):
    pan.turn()
    pan.show()

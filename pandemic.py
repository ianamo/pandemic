#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 14:27:12 2024

@author: ianamo
"""

import random
import pylab as plt

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
        self.pop_log = []
        self.infected_log = []
        self.hospitalized_log = []
        self.dead_log = []
        
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
                try:
                    self.infected_pop.remove(p)
                except ValueError:
                    pass
        self.dead = len([p for p in self.population if p.dead])
    
    def show(self):
        print(f"""
              t: {self.t}
              Population: {self.pop_size - self.dead}
              Infected: {self.infected}
              Hospitalized: {self.hospitalized}
              Dead: {self.dead}
              """)
    
    def log(self):
        self.pop_log.append(self.pop_size-self.dead)
        self.infected_log.append(self.infected)
        self.hospitalized_log.append(self.hospitalized)
        self.dead_log.append(self.dead)
    
    def plot(self,title=None):
        plt.figure()
        if not title:
            names = []
            for k in self.pathogens:
                names.append(str(self.pathogens[k]))
            str_names = ",".join(names)
            plt.title(f"Pandemic Curve of {str_names}")
        else:
            plt.title(title)
        plt.xlabel("t=")
        plt.ylabel("Amounts")
        x = list(range(1,self.t+1))
        plt.plot(x, self.pop_log, label="Population")
        plt.plot(x, self.infected_log, label="Infected")
        plt.plot(x, self.hospitalized_log, label="Hospitalized")
        plt.plot(x, self.dead_log, label="Deaths")
        plt.legend()
        plt.show()
    
    def model(self, t):
        for i in range(t):
            self.turn()
            self.log()
        self.plot()
                
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
                if len(self.pathogens)<1:
                    self.infected = False
                    self.hospitalized = False
            elif self.infected_days > v.serious and self.infected_days < v.fatal:
                self.hospitalized = True
            elif self.infected_days > v.fatal:
                self.dead = True
                self.infected = False
                self.hospitalized = False
        
        if not self.dead:
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
covid = Pathogen("COVID-19",0.1,15,30)
pan = Pandemic(population=my_pop, pathogens={'COVID-19':covid},infected={'COVID-19':1},encounters=15)
pan.model(90)
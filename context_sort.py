# -*- coding: utf-8 -*-

from abc       import ABCMeta, abstractmethod
from random    import shuffle
from time      import sleep
from sort      import Sort
from db        import DataSort
from threading import Thread, BoundedSemaphore, stack_size

import os
import matplotlib.pyplot as plt

#threadLimiter = BoundedSemaphore(38)

stack_size(134217728)   # for your needs


class ContextSort(object):
    """
        Author:  Aline Rodrigues
        Created: 20/10/2021
        Initialize and manage sort
    """
    
    def __init__(self):
        self.path_dir     = os.path.dirname(os.path.realpath(__file__))
        self.db           = DataSort(self.path_dir)
        self.sort         = Sort()
        self.mode_vector  = [['Vetores Ordenados (ASC)', SortedVector()], 
                            ['Vetores Desordenados',     NotSortedVector()], 
                            ['Vetores Ordenados (DESC)', ReverseSortedVector()],
                            ['Vetores Quase Ordenados',  AlmostSortedVector()]]

        self.threads            = []
        self.status_thread      = False
        self.status_thread_sort = [False for i in range(0, len(self.sort.types) * len(self.mode_vector))]
        self.len_vector         = [10, 100, 1000, 10000, 100000, 1000000]
        
    
    def init_sort(self):
        self.db.insert_environment()
        
        for mode in self.mode_vector:
            for type_sort in self.sort.types:  
                self.threads.append(Thread(target=self.init_threads, args=(type_sort, mode, len(self.threads), )))
                self.threads[len(self.threads)-1].start()
        
        while False in self.status_thread_sort:
            sleep(10) 
            print (self.status_thread_sort)
        self.status_thread = True
    
    def init_threads(self, type_sort, mode_sort, thread):
        
        db_thread = DataSort(self.path_dir)
        for i in range(0, len(self.len_vector)):
            vector = mode_sort[1].create_mode_vector(self.len_vector[i])
            sleep(5)
            self.sort.execute_sort(vector, type_sort, mode_sort[0], db_thread)
            sleep(5)
            
        self.status_thread_sort[thread] = True
                            
    def create_charts(self):
        environment   = self.db.select_environment()
        path_graphics = self.path_dir + '/graphics'
        
        try:
            os.makedirs(path_graphics)
        except OSError as error:
            print (f'Error: {error}')
        
        plt.figure(figsize=(12, 18))
        graphics = 1
        len_vector = list(self.len_vector)
        len_vector.remove(len_vector[0])
        for mode in self.mode_vector:
            legend = []
            plt.subplot(310 + graphics)
            
            for type_sort in self.sort.types:
                time_execute = []
                assortments = self.db.select_assortment(mode[0], type_sort[0])
                legend.append(type_sort[0])
                for i in range(1, len(self.len_vector)):
                    if i < len(assortments):
                        time_execute.append(assortments[i]['time_execute'])
                
                plt.plot(len_vector, time_execute, marker='o', linewidth=2)
            
            plt.xticks(len_vector)
            plt.title(u'' + mode[0])
            plt.xlabel(u'tamanho do vetor (n)') 
            plt.ylabel(u'tempo de execução (minutos)') 
            plt.legend(legend, loc='best')
            graphics +=  1
            
        plt.savefig(f"{path_graphics}/{environment['user_name']}.pdf", format='pdf')
            


class AbstractModeVector(object):
    """
        Author:  Aline Rodrigues
        Created: 14/03/2018
        Template Method to create mode vector
    """
    __metaclass__ = ABCMeta

    
    @abstractmethod
    def create_mode_vector(self, size):          
        return 
    
class SortedVector(AbstractModeVector):
    
    def create_mode_vector(self, size):
        return list(range(1, size + 1))


class NotSortedVector(AbstractModeVector):
    
    def create_mode_vector(self, size):
        vector = list(range(1, size + 1))
        shuffle(vector)
        return  vector
    
    
class ReverseSortedVector(AbstractModeVector):
    
    def create_mode_vector(self, size):
        return list(range(size, 0, -1))
    

class AlmostSortedVector(AbstractModeVector):
    
    def create_mode_vector(self, size):
        vector = list(range(1, size + 1))
        index = 5
        while (index + 5) <= size:
            aux = vector[index-1]
            vector[index-1] = vector[(index-1) + 5]
            vector[(index-1) + 5] = aux
            index = index + 5
        return vector
            
    
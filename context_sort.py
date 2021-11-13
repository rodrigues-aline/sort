# -*- coding: utf-8 -*-

from abc       import ABCMeta, abstractmethod
from random    import shuffle
from time      import sleep
from sort      import Sort
from db        import DataSort
from threading import Thread, stack_size

import os
import pandas as pd


stack_size(134217728)


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
        self.mode_vector  = [['Arranjos Ordenados (ASC)', SortedVector()], 
                             ['Arranjos Desordenados',     NotSortedVector()], 
                             ['Arranjos Ordenados (DESC)', ReverseSortedVector()],
                             ['Arranjos Quase Ordenados (1)',  AlmostSortedVector1(5)],
                             ['Arranjos Quase Ordenados (2)',  AlmostSortedVector2()],]

        self.threads            = []
        self.status_thread      = False
        self.status_thread_sort = [False for i in range(0, len(self.sort.types) * len(self.mode_vector) * 6)]
        self.len_vector         = [10, 100, 1000, 10000, 100000, 1000000]
        
    
    def init_sort(self):
        self.db.insert_environment()
        
        for mode in self.mode_vector:
            for type_sort in self.sort.types:  
                for i in range(0, len(self.len_vector)):
                    self.threads.append(Thread(target=self.init_thread, args=(type_sort, mode, len(self.threads), i, )))
                    self.threads[len(self.threads)-1].start()
        
        while False in self.status_thread_sort:
            sleep(60) 
            index = 0
            for mode in self.mode_vector:
                for type_sort in self.sort.types:
                    for i in range(0, len(self.len_vector)):
                        if self.status_thread_sort[index]  == False:
                            print (f'Runing: {type_sort[0]} ({self.len_vector[i]}) {mode[0]}')
                        index += 1

        self.status_thread = True
    
    def init_thread(self, type_sort, mode_sort, thread, v):
        db = DataSort(self.path_dir)
        vector = mode_sort[1].create_mode_vector(self.len_vector[v])
        self.sort.execute_sort(vector, type_sort, mode_sort[0], db)
        self.status_thread_sort[thread] = True
    
    def convert_data_to_csv(self):
        path_data = self.path_dir + '/dataset'
        
        try:
            os.makedirs(path_data)
        except OSError:
            print (f'Already exists path: {path_data}')
        
        data = self.db.select_all_assortment()
        df = pd.DataFrame(data, columns=data[0].keys())
        print(df.head())
        df.to_csv(path_data + '/assortments.csv')

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
    

class AlmostSortedVector1(AbstractModeVector):
    def __init__(self, steep):
        self.steep = steep
    
    def create_mode_vector(self, size):
        vector = list(range(1, size + 1))
        index = self.steep
        while (index + self.steep) <= size:
            aux = vector[index-1]
            vector[index-1] = vector[(index-1) + self.steep]
            vector[(index-1) + self.steep] = aux
            index = index + self.steep
        return vector

class AlmostSortedVector2(AbstractModeVector):
    
    def create_mode_vector(self, size):
        vector = list(range(1, size + 1))
        index = 5
        while (index + 5) <= size:
            aux = vector[index-1]
            vector[index-1] = vector[(index-1) + 5]
            vector[(index-1) + 5] = aux
            index = index + 5

        index = 4
        while (index + 4) <= size:
            aux = vector[index-1]
            vector[index-1] = vector[(index-1) + 4]
            vector[(index-1) + 4] = aux
            index = index + 4

        index = 3
        while (index + 3) <= size:
            aux = vector[index-1]
            vector[index-1] = vector[(index-1) + 3]
            vector[(index-1) + 3] = aux
            index = index + 3

        index = 2
        while (index + 2) <= size:
            aux = vector[index-1]
            vector[index-1] = vector[(index-1) + 2]
            vector[(index-1) + 2] = aux
            index = index + 2
        return vector
            
    
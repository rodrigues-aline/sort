# -*- coding: utf-8 -*-

from abc      import ABCMeta, abstractmethod
from datetime import datetime
from sys      import setrecursionlimit

setrecursionlimit(300000)

class Sort(object):
    """
        Author:  Aline Rodrigues
        Created: 20/10/2021
        Manage assortment execute
    """
    def __init__(self):
        self.types = [['InsertionSort', InsertionSort], ['SelectionSort', SelectionSort], ['BubbleSort', BubbleSort],
                      ['HeapSort', HeapSort],           ['MergeSort', MergeSort],         ['QuickSort', QuickSort],  
                      ['SmoothSort', SmoothSort]        
                      #['ShellSort', ShellSort], ['TimSort', TimSortPython]
                     ]
    
    def execute_sort(self, vector, type_sort, mode_sort, db):
        time_start = datetime.now()
        print (f'{time_start} init {type_sort[0]} vector: {len(vector)} {mode_sort}')
        
        sort = type_sort[1]()
        vector = sort.execute_sort(vector)
                
        time_end = datetime.now()
        print (f'{time_end} end {type_sort[0]} vector: {len(vector)} {mode_sort}')
        
        db.insert_assortment(len(vector), type_sort[0], mode_sort, sort.count_compare, sort.count_moves, time_start, (time_end - time_start).total_seconds() / 60)
        
        
class AbstractSort(object):
    """
        Author:  Aline Rodrigues
        Created: 20/10/2021
        Template Method to execute assortment
    """
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.count_compare = 0
        self.count_moves = 0

    @abstractmethod
    def execute_sort(self, vector):          
        return 
             

class SelectionSort(AbstractSort):
    
    def __init__(self):
        AbstractSort.__init__(self)
    
    def execute_sort(self, vector):
        for i in range(0, len(vector)-1):
            min = i
            for j in range(i + 1, len(vector)):
                if vector[j] < vector[min]:
                    min = j
                self.count_compare += 1
            aux = vector[min]
            vector[min] = vector[i]
            vector[i]   = aux
            self.count_moves += 3
  
        return vector


class InsertionSort(AbstractSort):
    
    def __init__(self):
        AbstractSort.__init__(self)
    
    def execute_sort(self, vector):
        for i in range(1, len(vector)):
            value = vector[i]
            self.count_moves += 1
            index = i
            while index > 0 and vector[index-1] > value:
                self.count_compare += 1
                vector[index] = vector[index-1]
                self.count_moves += 1
                index = index - 1
                
            vector[index] = value
            self.count_moves += 1
            
        return vector


class BubbleSort(AbstractSort):
    
    def __init__(self):
        AbstractSort.__init__(self)
    
    def execute_sort(self, vector):
        for i in range(0, len(vector)):
            status = True
            for j in range(1, len(vector)):
                if vector[j] < vector[j-1]:
                    aux          = vector[j]
                    vector[j]   = vector[j-1]
                    vector[j-1] = aux
                    self.count_moves += 3
                    status = False
                self.count_compare += 1
            
            if status: break
                       
        return vector

class MergeSort(AbstractSort):
    
    def __init__(self):
        AbstractSort.__init__(self)
    
    def execute_sort(self, vector):
        if len(vector) > 1:
            mid   = len(vector) // 2
            left  = vector[:mid]
            right = vector[mid:]

            self.execute_sort(left)
            self.execute_sort(right)

            i = 0
            j = 0
            k = 0
            
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    vector[k] = left[i]
                    self.count_moves += 1
                    i += 1
                else:
                    vector[k] = right[j]
                    self.count_moves += 1
                    j += 1
                self.count_compare += 1
                k += 1

            while i < len(left):
                vector[k] = left[i]
                self.count_moves += 1
                i += 1
                k += 1

            while j < len(right):
                vector[k] = right[j]
                self.count_moves += 1
                j += 1
                k += 1
                
        return vector


class ShellSort(AbstractSort):
    
    def __init__(self):
        AbstractSort.__init__(self)
    
    def execute_sort(self, vector):
        h = len(vector) // 2
        while h >= 1:
            for i in range(h, len(vector)):
                aux = vector[i]
                self.count_moves += 1
                index = i
                while index >= h:
                    if vector[index-h] > aux:
                        vector[index] = vector[index-h]
                        self.count_moves += 1
                        index = index - h
                    self.count_compare += 1
                vector[index] = aux
                self.count_moves += 1
            h = h // 2
        return vector
    
     
    
class QuickSort(AbstractSort):
    
    def __init__(self):
        AbstractSort.__init__(self)
    
    def execute_sort(self, vector):
        p = len(vector) // 2
        if vector:
            left  = []
            right = []
            for i in vector:
                self.count_compare += 1
                if i < vector[p]:
                    left.append(i)
                    self.count_moves += 1
                else:
                    self.count_compare += 1
                    if i > vector[p]:
                        right.append(i)
                        self.count_moves += 1
            if len(left) > 1:
                left = self.execute_sort(left)
            if len(right) > 1:
                right = self.execute_sort(right)
            return left + [vector[p]] + right

        return vector
    
class HeapSort(AbstractSort):
    
    def __init__(self):
        AbstractSort.__init__(self)
        self.v = []

    def swap(self, i, j):
        self.v[i], self.v[j] = self.v[j], self.v[i]
        self.count_moves += 3
        
    def heapify(self, end, i):
        left  = 2 * i + 1
        right = 2 * (i + 1)
        max   = i
        if left < end:
            if self.v[i] < self.v[left]:
                max = left
            self.count_compare += 1
        if right < end:
            if self.v[max] < self.v[right]:
                max = right
            self.count_compare += 1
        if max != i:
            self.swap(i, max)
            self.heapify(end, max)
        
            
    def execute_sort(self, vector):
        self.v = vector
        end = len(vector)
        start = end // 2 -1
        for i in range(start, -1, -1):
            self.heapify(end, i)
        for i in range(end - 1, 0, -1):
            self.swap(i, 0)
            self.heapify(i, 0)
        
        return vector

class SmoothSort(AbstractSort):
    
    def __init__(self):
        AbstractSort.__init__(self)
        self.leonardo_nums = [1, 1]

    # returns the k-th Leonardo number
    def L(self, k):
        if len(self.leonardo_nums) < k:
            return self.leonardo_nums[k]
        else:
            while len(self.leonardo_nums) <= k:
                self.leonardo_nums.append(self.leonardo_nums[-2] + self.leonardo_nums[-1] + 1)
            return self.leonardo_nums[k]

    
    # sorts the max heap in-place. requires the list of sizes of leonardo trees in
    # the forest
    def sort_heap(self, heap, size_list):
        for heap_size in reversed(range(len(heap))):
            self.dequeue_max(heap, size_list, heap_size)


    # removes the max value from the graph
    def dequeue_max(self, heap, size_list, heap_size):
        removed_size = size_list.pop()
        # case 1: rightmost tree has a single node
        if removed_size == 0 or removed_size == 1:
            pass  # already removed
        # case 2: rightmost tree has two children
        else:
            # add sizes back
            size_list.append(removed_size - 1)
            size_list.append(removed_size - 2)
            # calculate indices of left and right children
            left_idx = heap_size - self.L(size_list[-1]) - 1
            right_idx = heap_size - 1
            left_size_idx = len(size_list) - 2
            right_size_idx = len(size_list) - 1
            # fix left child
            idx, size_idx = self.fix_roots(heap, size_list, left_idx, left_size_idx)
            self.sift_down(heap, idx, size_list[size_idx])
            # fix right child
            idx, size_idx = self.fix_roots(heap, size_list, right_idx, right_size_idx)
            self.sift_down(heap, idx, size_list[size_idx])


    # modifies array in-place to make a heap. returns list of sizes of leonardo
    # trees in the forest
    def create_heap(self, arr):
        size_list = []
        for heap_end in range(len(arr)):
            # Update the sizes of the trees in the forest
            self.add_new_root(size_list)

            # Swap the root nodes of the trees. Return [heap index, size index]
            idx, size_idx = self.fix_roots(arr, size_list, heap_end, len(size_list) - 1)

            # Fix the tree that now has the new node
            self.sift_down(arr, idx, size_list[size_idx])

        return size_list
    

    # updates the list of sizes of leonardo trees in a forest after a new node is
    # added
    def add_new_root(self, size_list):
        # case 1: Empty forest. Add L_1 tree.
        if len(size_list) == 0:
            size_list.append(1)
        # case 2: Forest with two rightmost trees differing in size by 1.
        #         Replace the last two trees of size L_k-1 and L_k-2 by a single
        #         tree of size L_k.
        elif len(size_list) > 1 and size_list[-2] == size_list[-1] + 1:
            size_list[-2] = size_list[-2] + 1
            del size_list[-1]
        # case 3: Add a new tree, either L_1 or L_0
        else:
            # case 1: Rightmost tree is an L_1 tree. Add L_0 tree.
            if size_list[-1] == 1:
                size_list.append(0)
            # case 2: Rightmost tree is not an L_1 tree. Add L_1 tree.
            else:
                size_list.append(1)


    # modifies 'heap' in place, assuming an implicit Leonardo heap structure exists
    # with trees having sizes in the order given by 'sizes'
    def fix_roots(self, heap, sizes, start_heap_idx, start_size_idx):
        # variables in this function are referring to indexes
        cur = start_heap_idx
        size_cur = start_size_idx
        # keep fixing roots until we're at the leftmost root
        while size_cur > 0:
            next = cur - self.L(sizes[size_cur])
            # stop if the next root is not strictly greater than the current root
            self.count_compare += 1
            if heap[next] <= heap[cur]:
                break
           
            # stop if the next root is not greater than both children of the
            # current root, if those children exist, i.e. the size of the current
            # tree is not 0 or 1.
            if sizes[size_cur] > 1:
                right = cur - 1
                left = right - self.L(sizes[size_cur] - 2)
                self.count_compare += 1
                if heap[next] <= heap[right] or heap[next] <= heap[left]:
                    break

            # swap the current root with the next root
            temp = heap[cur]
            heap[cur] = heap[next]
            heap[next] = temp
            self.count_moves += 3
            # continue, starting with the next root as the current root
            size_cur = size_cur - 1
            cur = next
        return (cur, size_cur)


    # Fixes the tree of size tree_size rooted at root_idx in heap, where heap is otherwise a valid heap
    def sift_down(self, heap, root_idx, tree_size):
        cur = root_idx
        # continue iterating until there are no child nodes
        while tree_size > 1:
            right = cur - 1
            left = cur - 1 - self.L(tree_size - 2)
            # the root is at least as large as both children
            self.count_compare += 2
            if heap[cur] >= heap[left] and heap[cur] >= heap[right]:
                break
            # the right child is at least as large as the left child
            else:
                self.count_compare += 1
                if heap[right] >= heap[left]:
                    heap[cur], heap[right] = heap[right], heap[cur]
                    self.count_moves += 3
                    cur = right
                    tree_size = tree_size - 2
                # the left child is the greatest of the three
                else:
                    heap[cur], heap[left] = heap[left], heap[cur]
                    self.count_moves += 3
                    cur = left
                    tree_size = tree_size - 1
    
    def execute_sort(self, vector):
        size_list = self.create_heap(vector)
        self.sort_heap(vector, size_list)
        return vector
    
class TimSortPython(AbstractSort):
    
    def __init__(self):
        AbstractSort.__init__(self)
    
    def execute_sort(self, vector):
        return sorted(vector)

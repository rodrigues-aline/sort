# -*- coding: utf-8 -*-

from time        import sleep
from context_sort import ContextSort
    

if __name__=="__main__":
    """
        Author:  Aline Rodrigues
        Created: 20/10/2021
        Run the context sort
    """ 
    sort_processor = ContextSort()
    
    try:
        sort_processor.init_sort()
        # while not sort_processor.status_thread:
        #     sleep(30)
        #sort_processor.create_charts()
    except Exception as error:
        print (f'Error: {error}')

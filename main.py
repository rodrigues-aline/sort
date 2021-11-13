# -*- coding: utf-8 -*-

from time        import sleep
from context_sort import ContextSort
    

if __name__=="__main__":
    """
        Author:  Aline Rodrigues
        Created: 20/10/2021
        Run the context sort
    """ 
    sort = ContextSort()
    
    try:
        #sort.init_sort()
        # while not sort.status_thread:
        #     sleep(30))
        sort.convert_data_to_csv()
    except Exception as error:
        print (f'Error: {error}')

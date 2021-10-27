# -*- coding: utf-8 -*-

import sqlite3
import platform


class DataSort(object):
    """
        Author:  Aline Rodrigues
        Created: 20/10/2021
        Manage data sort (time process)
    """
    
    def __init__(self, path_dir):
        self.path_dir = path_dir
        self.db       = None
        self.cursor   = None
        self.connect()
        
    def connect(self):
        """
            Connect database sqlite 
        """
        if self.db is None:
            self.db     = sqlite3.connect(self.path_dir+'/data_sort.db')
            self.db.row_factory = sqlite3.Row
            self.cursor = self.db.cursor()
            
            # self.cursor.execute("DROP TABLE IF EXISTS environment;")
            # self.cursor.execute("DROP TABLE IF EXISTS assortment;")
                    
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS environment (
                                        user_name    TEXT,
                                        system       TEXT,
                                        platform     TEXT,
                                        processor    TEXT);""")
            
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS assortment (
                                        user_name     TEXT,
                                        type_sort     TEXT,
                                        mode_sort     TEXT,
                                        len_vector    INTEGER,
                                        time_execute  INTEGER,
                                        count_compare INTEGER,
                                        count_moves   INTEGER,
                                        date_execute  DATETIME);""")
            

    def insert_environment(self):
        self.cursor.execute(f"DELETE FROM environment WHERE user_name='{platform.uname()[1]}';")
        self.cursor.execute(f"DELETE FROM assortment  WHERE user_name='{platform.uname()[1]}';")
        self.db.commit()
        
        self.cursor.execute(f"""INSERT INTO environment (user_name, system, platform, processor)
                                VALUES ('{platform.uname()[1]}','{platform.system()}','{platform.platform()}','{platform.processor()}');""")
        self.db.commit()
        
        
    def insert_assortment(self, len_vector, type_sort, mode_sort, count_compare, count_moves, date_start, time_execute):
        self.cursor.execute(f"""INSERT INTO assortment (user_name,     len_vector,  type_sort,    mode_sort, 
                                                        count_compare, count_moves, time_execute, date_execute)
                                VALUES ('{platform.uname()[1]}', {len_vector}, '{type_sort}', '{mode_sort}', 
                                         {count_compare}, {count_moves}, {time_execute}, '{date_start}');""")
        self.db.commit()
        
        
    def select_environment(self):
        return self.cursor.execute(f"SELECT * FROM environment WHERE user_name='{platform.uname()[1]}';").fetchall()[0]
        
    
    def select_assortment(self, mode_sort, type_sort):
        return self.cursor.execute(f"""SELECT * FROM assortment 
                                             WHERE user_name='{platform.uname()[1]}' AND 
                                                   mode_sort='{mode_sort}' AND
                                                   type_sort='{type_sort}'
                                                   ORDER BY len_vector;""").fetchall()
    

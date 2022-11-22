#!/usr/bin/python3

from dataclasses import dataclass
import csv
import json
from operator import itemgetter

class BaselineFile:
    
    def __init__(self, filename, object_type='line', image_filename = "", has_header = False):
        
        header = has_header
        if len(image_filename) > 0:
            filter_image = True
        else:
            filter_image = False
            
        self.entries = 0
        self.object_type = object_type
            
        self.column_headings = []
        self.data_rows = []
        
        #55.0,58.0,57.0,1392.0,1401.0,1397.0
        #73.0,80.0,76.0,1169.0,1381.0,1266.0
        #148.0,152.0,150.0,90.0,115.0,103.0

        max_row_len = 0
        with open(filename, 'r') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if header:
                    column_headings = row
                    header = False
                    continue
                if filter_image:
                    if row[0] != image_filename:
                        continue
                max_row_len = max(max_row_len, len(row))
                self.entries += 1
                self.data_rows.append(Baseline(row, 2))
            f.close()
        if len(self.column_headings) == 0 and len(self.data_rows) > 0:
            self.column_headings = ['Col' + str(i) for i in range(max_row_len)]
            
    def get_headings(self):
        return self.column_headings
        
    def get_row(self, row_id):
        
        return self.data_rows[row_id]
            
            
class Baseline:
    
    def __init__(self, entry_row, x_value):
        
        self.y_pos = int(float(entry_row[x_value]))
        self.x_start = int(float(entry_row[3]))
        self.x_end = int(float(entry_row[4]))

    def __str__(self):
        
        return 'y:' + str(self.y_pos) + '; y:' + str(self.x_start) + ' --> ' + str(self.x_end)

if __name__ == '__main__':
    
    V = BaselineFile("./Data/out_cPAS-1211.jpg_baselines.txt")
    print(V.get_headings())
    
    sorting_list = []
    for i in range(V.entries):
        print(V.get_row(i))
        sorting_list.append([i, V.get_row(i).y_pos])
        
    sorting_list.sort(key=itemgetter(1))
    
    
    
        
    
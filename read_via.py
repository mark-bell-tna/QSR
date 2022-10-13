#!/usr/bin/python3

from dataclasses import dataclass
import csv
import json
from operator import itemgetter

class ViaFile:
    
    def __init__(self, filename, object_type, image_filename = "", has_header = True):
        
        header = has_header
        if len(image_filename) > 0:
            filter_image = True
        else:
            filter_image = False
            
        self.entries = 0
        self.object_type = object_type
            
        self.column_headings = []
        self.data_rows = []
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
                self.data_rows.append(ViaEntry(row, object_type, True))
            f.close()
        if len(self.column_headings) == 0 and len(self.data_rows) > 0:
            self.column_headings = ['Col' + str(i) for i in range(max_row_len)]
            
    def get_headings(self):
        return self.column_headings
        
    def get_row(self, row_id):
        
        return self.data_rows[row_id]
            
            
class ViaEntry:
    
    def __init__(self, entry_row, object_type, simplify=False):
        
        self.region_id = entry_row[4]
        self.shape_attributes = json.loads(entry_row[5])
        self.object_type = object_type
        if simplify:
            self.simplify_line()
        
    def get_shape(self):
        
        return self.shape_attributes
        
    def simplify_line(self):
        
        if self.shape_attributes["name"] == "polyline":
            this_x = self.shape_attributes["all_points_x"]
            this_y = self.shape_attributes["all_points_y"]
            new_x = [min(this_x), max(this_x)]
            new_y = [min(this_y), min(this_y)]
            self.shape_attributes["all_points_x"] = new_x
            self.shape_attributes["all_points_y"] = new_y
        

if __name__ == '__main__':
    
    V = ViaFile("../VIA/via_annotations_c54_18_10d_full - text lines.csv", "C 54-18 10d - tidy.jpg")
    print(V.get_headings())
    
    sorting_list = []
    for i in range(V.entries):
        print(V.get_row(i).shape_attributes)
        sorting_list.append([i, min(V.get_row(i).shape_attributes["all_points_y"])])
        
    sorting_list.sort(key=itemgetter(1))
    
    
    
        
    
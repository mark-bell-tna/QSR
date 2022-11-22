#!/usr/bin/python3

class AllenIntervals:
    
    description_lookup = {'XY': {1: 'before', 2: 'equals', 3: 'meets', 4: 'overlaps', 5: 'contains', 6: 'starts', 7: 'finishes'},
                   'YX': {1: 'after', 2: 'equals', 3: 'met by', 4: 'overlapped by', 5: 'during', 6: 'started by', 7: 'finished by'}}
                   
    def __init__(self, start_point, end_point, orientation):
        self.start_point = min(start_point, end_point)
        self.end_point = max(start_point, end_point)
        self.orientation = orientation

     
    def get_relationship(self, other):
        
        if self.orientation != other.orientation:
            return None
        
        X = self
        Y = other
        relationship = self._calc_relationship(other)
        desc_key = 'XY'
        if relationship is None:
            relationship = other._calc_relationship(self)
            desc_key = 'YX'
        #print("\t",X.start_point, X.end_point, Y.start_point, Y.end_point)
        print("\t", " " * X.start_point + "*" * (X.end_point-X.start_point))
        print("\t", " " * Y.start_point + "*" * (Y.end_point-Y.start_point))
        return " ".join(['X', str(self.description_lookup[desc_key][relationship]), 'Y'])
        
    def _calc_relationship(self, other):
        
        X = self
        Y = other
        if X.start_point < X.end_point < Y.start_point < Y.end_point:
            return 1
        if X.start_point == Y.start_point < X.end_point == Y.end_point:
            return 2
        if X.start_point < X.end_point == Y.start_point < Y.end_point:
            return 3
        if X.start_point < Y.start_point < X.end_point < Y.end_point:
            return 4
        if X.start_point < Y.start_point < Y.end_point < X.end_point:
            return 5
        if X.start_point == Y.start_point < X.end_point < Y.end_point:
            return 6
        if Y.start_point < X.start_point < X.end_point == Y.end_point:
            return 7
         
        return None  #self._calc_relationship(Y, X)   



if __name__ == '__main__':
    
    # Test rectangles
    # Rectangle coordinates = [top left, top right, bottom right, bottom left]
    # Descriptions are relative to rect1

    AI1 = AllenIntervals(10,20, 'H')
    
    for s in [3, 5, 7, 10, 12, 15, 18, 20, 25]:
        AI2 = AllenIntervals(s, s+5, 'H')
        #print(s, s+5)
        print("\t", AI1.get_relationship(AI2))
        #print("\t", AI1.get_relationship(AI2, True))
    
    for l in [[10,20], [10,25], [5,20], [8,22]]:
        AI2 = AllenIntervals(l[0],l[1],'H')
        print("\t", AI1.get_relationship(AI2))
    
    
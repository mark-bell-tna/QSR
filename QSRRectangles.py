#!/usr/bin/python3

class Rectangle:
    
    def __init__(self,coordinates):
        self.coordinates = coordinates
        self.set_rect_descriptor()
        
    def set_rect_descriptor(self):
        self.descriptor = {}
        self.descriptor['FL'] = min([k[0] for k in self.coordinates])
        self.descriptor['FR'] = max([k[0] for k in self.coordinates])
        self.descriptor['HP'] = min([k[1] for k in self.coordinates])
        self.descriptor['LP'] = max([k[1] for k in self.coordinates])
        
    def get_coordinates(self, original=False):
        if original:
            return self.coordinates
        D = self.descriptor
        box_coords = [[D['FL'], D['HP']],   # top left corner
                      [D['FR'], D['HP']],   # top right corner
                      [D['FL'], D['LP']],   # bottom left corner
                      [D['FR'], D['LP']]]   # bottomr right corner
        return box_coords
                      
    @property
    def left(self):
        return self.descriptor["FL"]
    
    @property
    def right(self):
        return self.descriptor["FR"]
    
    @property
    def top(self):
        return self.descriptor["HP"]
        
    @property
    def bottom(self):
        return self.descriptor["LP"]
    
    @property
    def height(self):
        return self.bottom-self.top
        
    @property
    def length(self):
        return self.right-self.left
        
    def get_descriptor(self):
        return(self.descriptor)
        
    def union(self, other):
        union_rect = Rectangle(self.get_coordinates() + other.get_coordinates())
        return union_rect
   
    def get_vertical_coords(self):
        return([self.descriptor['HP'], self.descriptor['LP']])
        
    def get_horizontal_coords(self):
        return([self.descriptor['FL'], self.descriptor['FR']])
        
    def is_above(self,rect2):
        if self.descriptor['HP']  < rect2.descriptor['HP']:
            return(True)
        return(False)
    
    def is_below(self,rect2):
        if self.descriptor['LP']  > rect2.descriptor['LP']:
            return(True)
        return(False)

    def is_leftof(self,rect2):
        if self.descriptor['FL']  < rect2.descriptor['FL']:
            return(True)
        return(False)

    def is_rightof(self,rect2):
        if self.descriptor['FR']  > rect2.descriptor['FR']:
            return(True)
        return(False)
    
    def is_equal(self, rect2):
        if self.descriptor['FL'] != rect2.get_descriptor()['FL']:
            return(False)
        if self.descriptor['FR'] != rect2.get_descriptor()['FR']:
            return(False)
        if self.descriptor['HP'] != rect2.get_descriptor()['HP']:
            return(False)
        if self.descriptor['LP'] != rect2.get_descriptor()['LP']:
            return(False)
        return(True)
    
    def has_horizontal_overlap(self, rect2):
        this_len = self.descriptor['FR'] - self.descriptor['FL']
        other_len = rect2.get_descriptor()['FR'] - rect2.get_descriptor()['FL']
        whole_len = max(self.descriptor['FR'], rect2.get_descriptor()['FR']) - \
                    min(self.descriptor['FL'], rect2.get_descriptor()['FL'])
        if whole_len < this_len + other_len:
            return(True)
        return(False)
    
    def has_vertical_overlap(self, rect2):
        this_len = self.descriptor['LP'] - self.descriptor['HP']
        other_len = rect2.get_descriptor()['LP'] - rect2.get_descriptor()['HP']
        whole_len = max(self.descriptor['LP'], rect2.get_descriptor()['LP']) - \
                    min(self.descriptor['HP'], rect2.get_descriptor()['HP'])
        if whole_len < this_len + other_len:
            return(True)
        return(False)
    
    def has_horizontal_abuttal(self, rect2):
        this_len = self.descriptor['LP'] - self.descriptor['HP']
        other_len = rect2.get_descriptor()['LP'] - rect2.get_descriptor()['HP']
        whole_len = max(self.descriptor['LP'], rect2.get_descriptor()['LP']) - \
                    min(self.descriptor['HP'], rect2.get_descriptor()['HP'])
        if whole_len == this_len + other_len:
            return(True)
        return(False)

    def has_vertical_abuttal(self, rect2):
        this_len = self.descriptor['LP'] - self.descriptor['HP']
        other_len = rect2.get_descriptor()['LP'] - rect2.get_descriptor()['HP']
        whole_len = max(self.descriptor['LP'], rect2.get_descriptor()['LP']) - \
                    min(self.descriptor['HP'], rect2.get_descriptor()['HP'])
        if whole_len == this_len + other_len:
            return(True)
        return(False)
    
    def has_overlap(self, rect2):
        if not self.has_horizontal_overlap(rect2):
            return(False)
        if not self.has_vertical_overlap(rect2):
            return(False)
        return(True)

    def is_disconnected(self, rect2):
        if not self.has_overlap(rect2):
            if not self.is_externally_connected(rect2):
                return(True)
        return(False)
    
    def is_externally_connected(self, rect2):
        if self.has_horizontal_abuttal(rect2):
            if self.has_vertical_abuttal(rect2) or self.has_vertical_overlap(rect2):
                return(True)
        if self.has_vertical_abuttal(rect2):
            if self.has_horizontal_abuttal(rect2) or self.has_horizontal_overlap(rect2):
                return(True)
        return(False)
    
    def is_proper_part(self, rect2):
        if not self.has_overlap(rect2):
            return(False)
        if self.is_above(rect2):
            return(False)
        if self.is_below(rect2):
            return(False)
        if self.is_leftof(rect2):
            return(False)
        if self.is_rightof(rect2):
            return(False)
        return(True)
    
    def is_tangential_proper_part(self, rect2):
        if self.is_equal(rect2):
            return(False)
        if not self.is_proper_part(rect2):
            return(False)
        other_descriptor = rect2.get_descriptor()
        for k, v in self.descriptor.items():
            if v == other_descriptor[k]:
                return(True)
        return(False)
    
    def is_inverse_proper_part(self, rect2):
        return(rect2.is_proper_part(self))
    
    def is_inverse_tangential_proper_part(self, rect2):
        return(rect2.is_tangential_proper_part(self))
    
    def get_euclid(self, rect2):
        a_x = (self.descriptor['FR'] - self.descriptor['FL']) / 2
        a_y = (self.descriptor['LP'] - self.descriptor['HP']) / 2
        b_x = (rect2.descriptor['FR'] - rect2.descriptor['FL']) / 2
        b_y = (rect2.descriptor['LP'] - rect2.descriptor['HP']) / 2

        return ((a_x-b_x)**2 + (a_y-b_y)**2) ** 0.5

    def get_rcc8_class(self, rect2):
        if self.is_disconnected(rect2):
            return("DC")
        if self.is_externally_connected(rect2):
            return("EC")
        if self.is_equal(rect2):
            return("EQ")
        if self.is_proper_part(rect2):
            if self.is_tangential_proper_part(rect2):
                return("TPP")
            else:
                return("NTPP")
        if self.is_inverse_proper_part(rect2):
            if self.is_inverse_tangential_proper_part(rect2):
                return("TPPi")
            else:
                return("NTPPi")
        return("PO")
        
    def get_direction_of_other(self, rect2):
        # 0 = Connected
        # 1 = North
        # 2 = North East
        # 3 = East
        # 4 = South East
        # 5 = South
        # 6 = South West
        # 7 = West
        # 8 = North West
        if not self.is_disconnected(rect2):
            return(0)
        if self.has_vertical_overlap(rect2):
            vertical_orientation = 0 # Same
        elif self.is_below(rect2):
            vertical_orientation = -1 # Northern
        else:
            vertical_orientation = 1 # Southern
        if self.has_horizontal_overlap(rect2):
            horizontal_orientation = 0
        elif self.is_leftof(rect2):
            horizontal_orientation = -1
        else:
            horizontal_orientation = 1

        if horizontal_orientation == 0:
            return(1 + ((vertical_orientation > 0) * 4))
        else:
            return((3 + (vertical_orientation*-horizontal_orientation)) + (horizontal_orientation > 0) * 4)

    def __str__(self):
        return ",".join([str(self.left), str(self.right), str(self.top), str(self.bottom)])
        
        
    def __repr__(self):
        
        return str(self)


if __name__ == '__main__':
    
    # Test rectangles
    # Rectangle coordinates = [top left, top right, bottom right, bottom left]
    # Descriptions are relative to rect1
    rect1 = Rectangle([(20,30),(60,30),(60,70),(20,70)])  # Box of interest - EQ
    rect2 = Rectangle([(0,0),(100,0),(100,100),(0,100)])  # Large outer box - NTPP
    rect3 = Rectangle([(20,20),(80,20),(80,80),(20,80)])  # Medium outer box, touching side - TPP
    rect4 = Rectangle([(25,10),(45,10),(45,30),(25,30)])  # Small box abut to outside - EC
    rect5 = Rectangle([(30,40),(40,40),(40,45),(30,45)])  # Small inner box, no touching - NTPPi
    rect6 = Rectangle([(40,50),(50,50),(50,70),(40,70)])  # Small inner box, touching - TPPi
    rect7 = Rectangle([(50,50),(80,50),(80,60),(50,60)])  # Small box, overlapping - PO
    rect8 = Rectangle([(90,0),(100,0),(100,10),(90,10)])  # Small box outside - DC"
    
    A = rect5
    B = rect8
    print(A.descriptor)
    print(B.descriptor)
    print(A.union(B).descriptor)
    #  EQ
    #  NTPP
    #  TPP
    #  EC
    #  NTPPi
    #  TPPi
    #  PO
    #  DC
    #print(rect1.get_rcc8_class(rect1))
    #print(rect1.get_rcc8_class(rect2))
    #print(rect1.get_rcc8_class(rect3))
    #print(rect1.get_rcc8_class(rect4))
    #print(rect1.get_rcc8_class(rect5))
    #print(rect1.get_rcc8_class(rect6))
    #print(rect1.get_rcc8_class(rect7))
    #print(rect1.get_rcc8_class(rect8))
    #print(rect1.get_direction_of_other(rect8)) # North east = 2
    #print(rect1.get_direction_of_other(rect2)) # Overlapping = 0"

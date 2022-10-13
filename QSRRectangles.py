#!/usr/bin/python3

class Rectangle:
    
    # FL = Furthest left
    # FR = Furthest right
    # HP = Highest point
    # LP = Lowest point

    def __init__(self,coordinates):
        if isinstance(coordinates, str):
            self.coordinates = self._coords_from_string(coordinates)
        elif isinstance(coordinates, Rectangle):  # This isn't great but will do for now
            c = coordinates
            self.coordinates = ((c.fl, c.hp), (c.fr, c.hp), (c.fr, c.lp), (c.fr, c.lp))
        elif isinstance(coordinates, dict):
            c = coordinates
            self.coordinates = ((int(c["fl"]), int(c["hp"])), (int(c["fr"]), int(c["hp"])), (int(c["fr"]), int(c["lp"])), (int(c["fr"]), int(c["lp"])))
        else:
            self.coordinates = coordinates
        self.set_rect_descriptor()
        
    def _coords_from_string(self, coords):
        return ([[int(x) for x in y.split(",")] for y in coords.split(" ")])

    def set_rect_descriptor(self):
        # Rationalise polygon coordinates [horizontal, vertical] to bounding box
        #self.descriptor = {}
        #self.descriptor['FL'] = min([k[0] for k in self.coordinates])
        #self.descriptor['FR'] = max([k[0] for k in self.coordinates])
        #self.hp = min([k[1] for k in self.coordinates])
        #self.lp = max([k[1] for k in self.coordinates])
        self.fl = min([k[0] for k in self.coordinates])
        self.fr = max([k[0] for k in self.coordinates])
        self.hp = min([k[1] for k in self.coordinates])
        self.lp = max([k[1] for k in self.coordinates])
        
    def get_descriptor(self):
        return(self.descriptor)
   
    def is_above(self,rect2):
        if self.hp  < rect2.hp:
            return(True)
        return(False)
    
    def is_below(self,rect2):
        if self.lp  > rect2.lp:
            return(True)
        return(False)

    def is_leftof(self,rect2):
        if self.fl  < rect2.fl:
            return(True)
        return(False)

    def is_rightof(self,rect2):
        if self.fr  > rect2.fr:
            return(True)
        return(False)
    
    def is_equal(self, rect2):
        if self.fl != rect2.fl:
            return(False)
        if self.fr != rect2.fr:
            return(False)
        if self.hp != rect2.hp:
            return(False)
        if self.lp != rect2.lp:
            return(False)
        return(True)
    
    def get_width(self):
        return self.fr-self.fl

    def get_height(self):
        return self.lp-self.hp

    def has_horizontal_overlap(self, rect2):
        this_len = self.fr - self.fl
        other_len = rect2.fr - rect2.fl
        whole_len = max(self.fr, rect2.fr) - \
                    min(self.fl, rect2.fl)
        if whole_len < this_len + other_len:
            return(True)
        return(False)
    
    def has_vertical_overlap(self, rect2):
        this_len = self.lp - self.hp
        other_len = rect2.lp - rect2.hp
        whole_len = max(self.lp, rect2.lp) - \
                    min(self.hp, rect2.hp)
        if whole_len < this_len + other_len:
            return(True)
        return(False)
    
    def has_horizontal_abuttal(self, rect2):
        this_len = self.lp - self.hp
        other_len = rect2.lp - rect2.hp
        whole_len = max(self.lp, rect2.lp) - \
                    min(self.hp, rect2.hp)
        if whole_len == this_len + other_len:
            return(True)
        return(False)

    def has_vertical_abuttal(self, rect2):
        this_len = self.lp - self.hp
        other_len = rect2.lp - rect2.hp
        whole_len = max(self.lp, rect2.lp) - \
                    min(self.hp, rect2.hp)
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
        if self.is_above(rect2):
            return(False)
        if self.is_below(rect2):
            return(False)
        if self.is_leftof(rect2):
            return(False)
        if self.is_rightof(rect2):
            return(False)
        if not self.has_overlap(rect2):
            return(False)
        return(True)
    
    def is_tangential_proper_part(self, rect2):
        if not self.is_proper_part(rect2):
            return(False)
        if self.is_equal(rect2):
            return(False)
        if self.has_vertical_abuttal(rect2) or self.has_horizontal_abuttal(rect2):
            return(True)
        return(False)
    
    def is_inverse_proper_part(self, rect2):
        return(rect2.is_proper_part(self))
    
    def is_inverse_tangential_proper_part(self, rect2):
        return(rect2.is_tangential_proper_part(self))
    
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
        # ...
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
        return(",".join([str(x) for x in [self.fl, self.hp, self.fr, self.lp]]))

    def __repr__(self):
        return (str(self))


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
    print(rect8._coords_from_string("1,2 3,4 5,6 6,7"))
    
    #  EQ
    #  NTPP
    #  TPP
    #  EC
    #  NTPPi
    #  TPPi
    #  PO
    #  DC
    print(rect1.get_rcc8_class(rect1))
    print(rect1.get_rcc8_class(rect2))
    print(rect1.get_rcc8_class(rect3))
    print(rect1.get_rcc8_class(rect4))
    print(rect1.get_rcc8_class(rect5))
    print(rect1.get_rcc8_class(rect6))
    print(rect1.get_rcc8_class(rect7))
    print(rect1.get_rcc8_class(rect8))
    print(rect1.get_direction_of_other(rect8)) # North east = 2
    print(rect1.get_direction_of_other(rect2)) # Overlapping = 0"

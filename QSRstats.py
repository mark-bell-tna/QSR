#!/usr/bin/python3

from QSRRectangles import Rectangle
from operator import itemgetter
from sklearn.cluster import KMeans
import numpy as np

class QSRstats:
    
    def __init__(self, rectangles, page_width, page_height):
        
        self.rectangles = rectangles
        self.sort_by()
        self.page_width = page_width
        self.page_height = page_height
        
    def sort_by(self, sort_key=None):
        to_be_sorted = []
        for i,r in enumerate(self.rectangles):
            if r.top < 0:
                print("*****************", r)
            if sort_key is None:
                v = i
            else:
                v = getattr(r, sort_key)
            to_be_sorted.append([i,v])
        to_be_sorted.sort(key=itemgetter(1))
        self.ordering = to_be_sorted
        
    
    def _get_distrib(self, attribute=None): # [ i.e. FL, FR, HP, LP ]
        
        distrib = {}
        for i, r in enumerate(self.rectangles):
            value = getattr(r, attribute)
            if value in distrib:
                distrib[value] += 1
            else:
                distrib[value] = 1
        return distrib
        
    def get_left_distrib(self):
        
        return self._get_distrib('left')
    
    def get_right_distrib(self):
        
        return self._get_distrib('right')
    
    def get_top_distrib(self):
        
        return self._get_distrib('top')
    
    def get_bottom_distrib(self):
        
        return self._get_distrib('bottom')
        
    def get_length_distrib(self):
        
        return self._get_distrib('length')

    def get_height_distrib(self):
        
        return self._get_distrib('height')
        
    def get_nearest_neighbours(self, overlap=None):
        
        neighbours = []
        
        for i in range(len(self.ordering)-1):
            this_r = self.ordering[i]
            found = False
            for j in range(i+1, len(self.ordering)):
                next_r = self.ordering[j]
                #print(self.rectangles[this_r[0]], self.rectangles[next_r[0]], self.rectangles[this_r[0]].has_horizontal_overlap(self.rectangles[next_r[0]]), next_r[1]-this_r[1])
                if overlap == 'horizontal':
                    if self.rectangles[this_r[0]].has_horizontal_overlap(self.rectangles[next_r[0]]):
                        neighbour = next_r[0]
                        found = True
                elif overlap == 'vertical':
                    if self.rectangles[this_r[0]].has_vertical_overlap(self.rectangles[next_r[0]]):
                        neighbour = next_r[0]
                        found = True
                else:
                    neighbour = next_r[0]
                    found = True
                if found:
                    break
            
            if not found:
                neighbours.append([this_r[0], None, self.rectangles[this_r[0]], None])
            else:
                neighbours.append([this_r[0], neighbour, self.rectangles[this_r[0]], self.rectangles[neighbour]])
            
        return neighbours
                
        
    def get_diff_distrib(self, direction='vertical', overlap='horizontal'):
        
        distrib = {}
        for nn in self.get_nearest_neighbours(overlap=overlap):
            if nn[1] is None:
                # TODO: test for horizontal ordered at some point
                if direction == 'vertical':
                    diff = self.page_height-nn[2].bottom  # TODO: this only works for vertically ordered rectangles - parameterise
                else:
                    diff = nn[2].left
            else:
                if direction == 'vertical':
                    diff = nn[3].bottom-nn[2].bottom
                else:
                    diff = nn[3].left-nn[2].right
            if diff in distrib:
                distrib[diff] += 1
            else:
                distrib[diff] = 1
        return distrib
        
    def get_distrib_KM(self, distrib, clusters=2):
        X = []
        W = []
        for k,v in distrib.items():
            X.append(k)
            W.append(v)
        X = np.array(X).reshape(-1,1)
        W = np.array(W)
            
        KM = KMeans(n_clusters=clusters).fit(X=X, sample_weight=W)
        return KM
    
    def get_KM_centres(self, KM):
        return KM.cluster_centers_
        
    def get_distrib_labels(self, distrib, KM):
        return dict((k,KM.labels_[i]) for i,k in enumerate(distrib.keys()))
        
    def __iter__(self):
        
        for x in self.ordering:
            yield self.rectangles[x[0]]
            

        
     
if __name__ == '__main__':
    
    R = [Rectangle([[0,1],[0,4],[1,4],[1,1]]),
         Rectangle([[0,3],[0,6],[1,6],[1,3]]),
         Rectangle([[0,3],[0,10],[1,10],[1,3]])]
    S = QSRstats(R,12,12)

    print(S.get_top_distrib())
    print(S.get_bottom_distrib())
    print(S.get_left_distrib())
    print(S.get_right_distrib())
    print(S.get_height_distrib())
    print(S.get_length_distrib())
    #print(S.get_distrib_labels(S.get_top_distrib()))
    
        
        
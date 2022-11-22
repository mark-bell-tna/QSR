#!/usr/bin/python3

from read_via import ViaEntry, ViaFile
from QSRRectangles import Rectangle
from QSRAllen import AllenIntervals
from QSRstats import QSRstats
from QSRExtendedAllen import ExtendedAllenIntervals
from operator import itemgetter
from sklearn.cluster import KMeans
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import sys
from read_baselines import BaselineFile

def add_to_dict_list(D,k,v):
    
    if k not in D:
        D[k] = []
    D[k].append(v)
    
if __name__ == '__main__':
    
    via_list = []
    example = int(sys.argv[1])
    mode = [1,1,0,0,0]   # Text segments, merged vertical, polygons, merged horizontal, load rectangles
    show_image = False
    
    if example == 0:
        image_name = "out_cPAS-1211.jpg-1.jpg"
        image_width = 1467 #4445
        image_height = 1866 #5654
        line_height = 10
        via_list.append(BaselineFile("./Data/out_cPAS-1211.jpg_baselines.txt"))

    y_sorting_list = []
    left_edges = []
    bottom_edges = []
    rectangles = []
    object_types = []
    v_index = 0
    polygons = []

    for V in via_list:
        print("Entries:", V.entries)
        for i in range(V.entries):
            entry = V.get_row(i)
            if entry.x_end > entry.x_start:
                this_rect = Rectangle([(entry.x_start,entry.y_pos-line_height), (entry.x_end, entry.y_pos-line_height),
                                        (entry.x_start, entry.y_pos), (entry.x_end, entry.y_pos)])
                if entry.y_pos >= line_height:
                    # [top left, top right, bottom right, bottom left]
                    rectangles.append(this_rect)
            
                v_index += 1
     
    XcolourLookup = ['firebrick','darkorange','darkgoldenrod','royalblue','midnightblue','skyblue','green','purple','black','yellow'] 
    YcolourLookup = ['firebrick','darkorange','darkgoldenrod','royalblue','midnightblue','skyblue','green','purple','black','yellow'] 
    
    QS = QSRstats(rectangles, image_width, image_height)
    x_distrib = QS.get_left_distrib()
    x_KM = QS.get_distrib_KM(x_distrib, 7)
    x_centres = QS.get_KM_centres(x_KM)
    x_labels = QS.get_distrib_labels(x_distrib, x_KM)
    print("Labels:", x_labels, "Centres:", x_centres)
    bar_colours = [XcolourLookup[v % len(XcolourLookup)] for v in x_labels.values()]
    plt.bar(list(x_distrib.keys()), list(x_distrib.values()), color=bar_colours, width=10)
    fig = plt.gcf()
    fig.set_size_inches(10.5, 2.5)
    plt.savefig(image_name + '_x_distrib.png')   
    plt.clf()
    
    QS.sort_by('bottom')
    #print(QS.ordering)
    y_diff_distrib = QS.get_diff_distrib()
    y_diff_KM = QS.get_distrib_KM(y_diff_distrib)
    y_diff_labels = QS.get_distrib_labels(y_diff_distrib, y_diff_KM)
    print(y_diff_labels)
    bar_colours = [YcolourLookup[v % len(YcolourLookup)] for v in y_diff_labels.values()]
    print(y_diff_distrib)
    print(y_diff_labels)
    print(y_diff_KM.cluster_centers_)
    ordered_clusters = [[i,c] for i,c in enumerate(y_diff_KM.cluster_centers_)]
    ordered_clusters.sort(key=itemgetter(1))
    plt.barh(list(y_diff_distrib.keys()), list(y_diff_distrib.values()), color=bar_colours, height=10)
    fig = plt.gcf()
    fig.set_size_inches(2.5, 10.5)
    plt.savefig(image_name + '_y_diff_distrib.png')
    plt.clf()
    
    
    print(ordered_clusters)
    merged_Rects = [[] for i in set(x_labels.values())]
    eai_relations = []
    left_align = True
    equal_is_null = True
    direction_matters = True
    
    for i, r in QS.ordering:
        #nn in QS.get_nearest_neighbours(overlap='horizontal'):
        this_r = QS.rectangles[i]
        label = x_labels[this_r.left]
        this_eai = ExtendedAllenIntervals( x_centres[label][0] if left_align else this_r.left, this_r.right, 'H')
        prev_eai = None
        for j, eai in enumerate(eai_relations):
            prev_eai = eai[-1]
            #print(prev_eai, this_eai)
            this_rel = this_eai.get_relationship_code(prev_eai)
            if this_rel['value'] in [1,3]:
                prev_eai = None
                continue
            eai.append(this_eai)
            break
            
        if prev_eai is None:
            eai_relations.append([this_eai])
            
        found = False
        
        for j, relat in enumerate(eai_relations):
            if len(relat) == 0:
                relat.append(this_eai)
        
        for j,mr in enumerate(merged_Rects[label]):
            this_diff = this_r.bottom-mr.bottom
            # Only merge if they are the smallest y diff cluster apart
            if abs(ordered_clusters[0][1]-this_diff) < abs(ordered_clusters[1][1]-this_diff):
                merged_Rects[label][j] = mr.union(this_r)
                found = True
                break
        if not found:
            merged_Rects[label].append(this_r)
    
    for mr in merged_Rects:
        print(mr)

    
    repeating_patterns = []
    rp_locations = []
    for i, interval_list in enumerate(eai_relations):
        print(i, len(interval_list), interval_list[0])
        prev = None
        repeating_patterns.append([])
        patterns = repeating_patterns[-1]
        rp_locations.append(interval_list[0])
        for I in interval_list:
            if prev is None:
                prev = I
                patterns.append(['*',1,'*'])
                continue
            R = prev.get_relationship_code(I)
            print("\t",R, I.start_point, I.end_point)
            if R['value'] == patterns[-1][0] or (equal_is_null and R['value'] == 2):
                patterns[-1][1] += 1
            else:
                patterns.append([R['value'], 1, R['direction'] if direction_matters else 'XY'])
            prev = I
            
        #TODO: for each r, find runs of relationships
        # e.g. [[6.1, 8], [7.2, 4], [6.1, 15]]
    
    #print(repeating_patterns)
    c = 0
    print(ExtendedAllenIntervals.extension_descriptions)
    for RP in repeating_patterns:
        c += 1
        print("Block:", c, rp_locations[c-1])
        for p in RP:
            
            print("\t", p, '*' if p[2] == '*' else ExtendedAllenIntervals.extension_descriptions[p[2]][p[0]])
    exit()
    

    im = Image.open("./Images/" + image_name) 
    
    # Create figure and axes
    fig, ax = plt.subplots()
    plt.yticks(np.arange(0, image_height+1, 100.0))
    plt.axis('off')
    # Display the image
    ax.imshow(im)
    if not show_image:
        background = patches.Rectangle((0,0), image_width, image_height, linewidth=1, edgecolor='grey', facecolor='white', fill=True)
        ax.add_patch(background)
    #ax.plot([0, .1],[0, .1])
    
    for i, r in enumerate(QS.rectangles):
        rect = patches.Rectangle((r.left, r.top), r.length, r.height, linewidth=0.5, edgecolor=YcolourLookup[i % 2], facecolor='none')
        if mode[0] == 1:
            ax.add_patch(rect)
        
    # Create a Rectangle patch
    #colours = ['red','blue','black','white','orange','yellow','green']
    for i, mr in enumerate(merged_Rects):
        for r in mr:
            rect = patches.Rectangle((r.left, r.top), r.length, r.height, linewidth=2, edgecolor=XcolourLookup[i], facecolor='none')
        
            # Add the patch to the Axes
            if mode[1] == 1:
                ax.add_patch(rect)


    for ply in polygons:
        xy = np.array([z for z in zip(ply["all_points_x"], ply["all_points_y"])])
        p = patches.Polygon(xy, facecolor = 'none', edgecolor = 'black', linewidth=0.3)
        if mode[2] == 1:
            ax.add_patch(p)

    relations = []
    QS.sort_by('bottom')
    for i,x in enumerate(QS.get_nearest_neighbours(overlap='vertical')):
        if x[1] is not None:
            mr = x[2].union(x[3])
            rect = patches.Rectangle((mr.left,mr.top), mr.length, mr.height, linewidth=0.5, edgecolor=YcolourLookup[(i % 2)],
            facecolor='chocolate', fill=False, alpha = 1.0)

            if mode[3] == 1:
                ax.add_patch(rect)
            
    plt.savefig('merged_rects_' + image_name + '_' + "-".join([str(m) for m in mode + [1*show_image]]) + '.png')   
    

            
    
    exit()
    

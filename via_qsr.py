#!/usr/bin/python3

from read_via import ViaEntry, ViaFile
from QSRRectangles import Rectangle
from QSRAllen import AllenIntervals
from QSRstats import QSRstats
from operator import itemgetter
from sklearn.cluster import KMeans
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import sys

def add_to_dict_list(D,k,v):
    
    if k not in D:
        D[k] = []
    D[k].append(v)
    
if __name__ == '__main__':
    
    via_list = []
    example = int(sys.argv[1])
    mode = [1,0,0,0,0]   # Text segments, merged vertical, polygons, merged horizontal, load rectangles
    show_image = False
    
    if example == 0:
        image_name = "C 54-18 10d - Crop long.jpg"
        image_width = 2592
        image_height = 1925
        line_height = 35
        via_list.append(ViaFile("../VIA/via_annotations_C 54-18 10d - text.csv", "text", image_name))
    if example == 1:
        image_name = "KB 9-210-39 (1417) - tidy.jpg"
        image_width = 2800
        image_height = 2700
        line_height = 26
        via_list.append(ViaFile("../VIA/via_annotations_KB_9-210-39_1417 - text.csv", "text", image_name))
        via_list.append(ViaFile("../VIA/via_annotations_KB_9-210-39_1417 - PP.csv", "PP", image_name))
        via_list.append(ViaFile("../VIA/via_annotations_KB_9-210-39_1417 - S.csv", "S", image_name))
    if example == 2:
        image_name = "mt_speech_draft_1_page_1 - crop.png"
        via_list.append(ViaFile("../VIA/via_annotations_mt_draft_1_pg_1 - hand text.csv", "hand", image_name))
        via_list.append(ViaFile("../VIA/via_annotations_mt_draft_1_pg_1 - typed text.csv", "typed", image_name))
    if example == 3:
        image_name = "Photo 08-09-2022 14 15 07 - straight.jpg"
        image_width = 3511
        image_height = 2634
        line_height = 60
        via_list.append(ViaFile("../VIA/via_annotations_141507 - text.csv", "text", image_name))
        via_list.append(ViaFile("../VIA/via_annotations_141507 - polygon.csv", "polygon", image_name))
        #via_list.append(ViaFile("../VIA/via_annotations_KB_9-210-39_1417 - S.csv", "S", image_name))
    if example == 4:
        image_name = "Photo 08-09-2022 14 44 52 - crop.jpg"
        image_width = 3511
        image_height = 2634
        line_height = 60
        via_list.append(ViaFile("../VIA/via_annotations - Photo 08-09-2022, 14 44 52 - text.csv", "text", image_name))
    if example == 5:
        image_name = "mt_speech_draft_1_page_1.PNG"
        image_width = 805
        image_height = 1116
        line_height = 60
        via_list.append(ViaFile("../VIA/via_project_21Sep2022_10h7m_csv - text.csv", "text", image_name))
    if example == 6:
        image_name = "mt_speech_draft_2_page_1.PNG"
        image_width = 793
        image_height = 1116
        line_height = 60
        via_list.append(ViaFile("../VIA/via_project_21Sep2022_10h7m_csv - text.csv", "text", image_name))
    if example == 7:
        image_name = "mt_speech_final_page_1.PNG"
        image_width = 798
        image_height = 1112
        line_height = 60
        via_list.append(ViaFile("../VIA/via_project_21Sep2022_10h7m_csv - text.csv", "text", image_name))
    if example == 8:
        image_name = "mt_speech_final_page_2.PNG"
        image_width = 790
        image_height = 1111
        line_height = 60
        via_list.append(ViaFile("../VIA/via_project_21Sep2022_10h7m_csv - text.csv", "text", image_name))
    if example == 9:
        image_name = "mt_speech_draft_1_page_1.PNG"
        image_width = 805
        image_height = 1116
        line_height = 60
        via_list.append(ViaFile("../VIA/via_project_21Sep2022_10h7m_csv - annotations.csv", "annotations", image_name))
    if example == 10:
        image_name = "mt_speech_draft_2_page_1.PNG"
        image_width = 793
        image_height = 1116
        line_height = 60
        via_list.append(ViaFile("../VIA/via_project_21Sep2022_10h7m_csv - annotations.csv", "text", image_name))
    
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
            this_shape = V.get_row(i).shape_attributes
            this_object = V.get_row(i).object_type
            shape_type = this_shape["name"]
            if this_object == 'polygon':
                if shape_type == 'polygon':
                    polygons.append(this_shape)
                    continue
            print("\t", this_shape, this_object, shape_type)
            # {""name"":""polyline"",""all_points_x"":[544,1729,2021,2608],""all_points_y"":[901,879,872,866]}
            if shape_type == "polyline":
                # {""name"":""rect"",""x"":62,""y"":167,""width"":38,""height"":45}
                this_y = this_shape["all_points_y"]
                this_x = this_shape["all_points_x"]
                min_x = min(this_x)
                max_x = max(this_x)
                max_y = np.mean(this_y)
                min_y = max_y-line_height  # Turn lines into rectangles
            elif shape_type == "rect":
                if mode[4] == 0:
                    continue
                min_x = this_shape["x"]
                max_x = min_x + this_shape["width"]
                min_y = this_shape["y"]
                max_y = min_y + this_shape["height"]
                #print("\tCreate rect:", min_x, max_x, min_y, max_y)
            this_rect = Rectangle([(min_x,min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)])
            #y_sorting_list.append([v_index, max_y])
            #left_edges.append(min_x)
            #bottom_edges.append(max_y)
            if min_y >= 0:
                object_types.append(this_object)
            
                # [top left, top right, bottom right, bottom left]
                rectangles.append(this_rect)
            
            v_index += 1
     
    colourLookup = ['firebrick','darkorange','darkgoldenrod','royalblue','midnightblue','skyblue','green'] 
    
    QS = QSRstats(rectangles, image_width, image_height)
    x_distrib = QS.get_left_distrib()
    x_KM = QS.get_distrib_KM(x_distrib, 3)
    x_labels = QS.get_distrib_labels(x_distrib, x_KM)
    print(x_labels)
    bar_colours = [colourLookup[v % len(colourLookup)] for v in x_labels.values()]
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
    bar_colours = [colourLookup[v % len(colourLookup)] for v in y_diff_labels.values()]
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
    for i, r in QS.ordering:
        #nn in QS.get_nearest_neighbours(overlap='horizontal'):
        this_r = QS.rectangles[i]
        label = x_labels[this_r.left]
        found = False
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

        
    

    im = Image.open("../Images/" + image_name) 
    
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
        rect = patches.Rectangle((r.left, r.top), r.length, r.height, linewidth=0.5, edgecolor=colourLookup[i % 2], facecolor='none')
        if mode[0] == 1:
            ax.add_patch(rect)
        
    # Create a Rectangle patch
    #colours = ['red','blue','black','white','orange','yellow','green']
    for i, mr in enumerate(merged_Rects):
        for r in mr:
            rect = patches.Rectangle((r.left, r.top), r.length, r.height, linewidth=2, edgecolor=colourLookup[i+3], facecolor='none')
        
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
            rect = patches.Rectangle((mr.left,mr.top), mr.length, mr.height, linewidth=0.5, edgecolor=colourLookup[(i % 2)],
            facecolor='chocolate', fill=False, alpha = 1.0)

            if mode[3] == 1:
                ax.add_patch(rect)
            
    plt.savefig('merged_rects_' + image_name + '_' + "-".join([str(m) for m in mode + [1*show_image]]) + '.png')   
    

            
    
    exit()
    

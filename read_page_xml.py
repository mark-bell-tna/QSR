#!/usr/bin/python3

import xmltodict
from QSRRectangles import Rectangle

def chartotype(text):
    outtext = []
    for t in text:
        c = ord(t)
        if 97 <= c <= 122:
            outtext.append("a")
        elif 65 <= c <= 90:
            outtext.append("A")
        elif 48 <= c <= 57:
            outtext.append("9")
        else:
            outtext.append(t)
    return "".join(outtext)

c = 0
formats = {}
textregions = []

import os
import sys

data_dir = "/home/dataowner/vn_share/Images/QFA_1_1_-_England_&_Wales_Ecclesiastical_A-L_duplicated/QFA_1_1_-_England_&_Wales_Ecclesiastical_A-L_duplicated/"
file_prefixes = ['690762_0014_26191180', '690762_0015_26191181', '690762_0016_26191182']
file_prefixes = ['690762_0012_26191178', '690762_0011_26191177', '690762_0010_26191176']
#file_prefixes = [x[:-4] for x in os.listdir(data_dir) if x[-4:] == ".jpg"]
file_id = int(sys.argv[1])
prefix = file_prefixes[file_id]

#Z:\Images\QFA_1_1_-_England_&_Wales_Ecclesiastical_A-L_duplicated\QFA_1_1_-_England_&_Wales_Ecclesiastical_A-L_duplicated\page

print(prefix + ".xml")
X = xmltodict.parse(open(data_dir + "page/" + prefix + ".xml", 'rb'))

#V = X['PcGts']['Page'].items()

for k,v in X['PcGts']['Page'].items():
    if k == 'TextRegion':
        if isinstance(v, list):
            v = v[0]
        lines = v['TextLine']
        for ln in lines:

            R = Rectangle(ln['Coords']['@points'])
            textregions.append(R)

from PIL import Image, ImageDraw

image = Image.open(data_dir + prefix + ".jpg")
draw = ImageDraw.Draw(image)

for i, R in enumerate(textregions):
    if i == 2:
        draw.rectangle(((R.fl, R.hp), (R.fr, R.lp)), outline = "red", fill = None, width = 3)
        print(R)
        break

image.save("/home/dataowner/vn_share/Images/qfa_textregions_" + prefix + ".jpg")

exit()

h_overlaps = {}
v_overlaps = {}
for i in range(len(textregions)-1):
    h_overlaps[i] = []
    v_overlaps[i] = []
    for j in range(len(textregions)):
        if i == j:
            continue
        if textregions[i].has_horizontal_overlap(textregions[j]):
            if textregions[i].is_above(textregions[j]):
                h_overlaps[i].append(j)
        if textregions[i].has_vertical_overlap(textregions[j]):
            if textregions[i].is_leftof(textregions[j]):
                v_overlaps[i].append(j)

for k in v_overlaps.keys():
    print("K",k)
    thisr = textregions[k]
    olrs = [textregions[x] for x in v_overlaps[k]]
    olrs.sort(key=lambda x: x.fl)
    if len(olrs) > 0:
        print("\tFR",thisr.fr, "FL", olrs[0].fl-1)
        thisr.fr = olrs[0].fl-1

exit()
print(h_overlaps)

from PIL import Image, ImageDraw

image = Image.open(data_dir + prefix + ".jpg")
draw = ImageDraw.Draw(image)

min_width = 300
blocks = True

for k in h_overlaps.keys():
    thisr = [textregions[k]]
    olrs = [textregions[x] for x in h_overlaps[k]]
    olrs.sort(key=lambda x: x.hp, reverse=False)
    new_thisr = []
    #print("Others:",olrs)
    #print("This:",thisr)
    for oth in olrs:
        #print("This:",thisr)
        for tr in thisr:
            #print("TR:",tr)
            if tr.has_horizontal_overlap(oth):
                ol_rec = Rectangle(tr)
                ol_rec.fl = max(ol_rec.fl, oth.fl)
                ol_rec.fr = min(ol_rec.fr, oth.fr)
                ol_coords = ((ol_rec.fl, ol_rec.lp), (ol_rec.fr, ol_rec.lp+5))
                #ol_coords = ((ol_rec.fl, ol_rec.hp), (ol_rec.fr, ol_rec.lp))
                #print("draw ol:",ol_coords,"rec:", ol_rec)
                if blocks:
                    draw.rectangle(((ol_rec.fl, ol_rec.hp), (ol_rec.fr, oth.hp)), outline = "red", fill = None, width = 3)
                else:
                    draw.rectangle(ol_coords, fill = "#ffff33", outline="#ffff33")
                    #print("draw ol:",((ol_rec.fl, oth.hp), (ol_rec.fr, oth.lp)),"rec:", ol_rec)
                    draw.rectangle(((ol_rec.fl, oth.hp-4), (ol_rec.fr, oth.hp)), fill = "red")
                    draw.rectangle(((int((ol_rec.fr-ol_rec.fl)/2)+ol_rec.fl-2, ol_rec.lp), (int((ol_rec.fr-ol_rec.fl)/2)+ol_rec.fl+2, oth.hp)), fill = "black")
                if tr.is_leftof(oth):
                    left_rec = Rectangle(tr)
                    left_rec.fr = min(left_rec.fr, oth.fl)
                    if left_rec.get_width() > min_width:
                        new_thisr.append(left_rec)
                        left_coords = ((left_rec.fl, left_rec.hp), (left_rec.fr, left_rec.lp))
                        #draw.rectangle(left_coords, fill = "red", outline="red")
                        print("\tAdded left:",left_coords,"Width",left_rec.get_width())
                if tr.is_rightof(oth):
                    right_rec = Rectangle(tr)
                    right_rec.fl = max(right_rec.fl, oth.fr)
                    if right_rec.get_width() > min_width:
                        new_thisr.append(right_rec)
                        right_coords = ((right_rec.fl, right_rec.hp), (right_rec.fr, right_rec.lp))
                        #draw.rectangle(right_coords, fill = "#ffff33", outline="#ffff33")
                        print("\tAdded right:",right_coords,"Width",right_rec.get_width())
            else:
                new_thisr.append(tr)
        thisr = new_thisr
        new_thisr = []
        #print("\tOther:",oth, "This:",thisr)
#image = image.convert("RGB")
if blocks:
    image.save("/home/dataowner/vn_share/Images/qfa_rectangles_" + prefix + ".jpg")
else:
    image.save("/home/dataowner/vn_share/Images/qfa_lines_" + prefix + ".jpg")
#print(v_overlaps)


        #if 'TextBlock' not in X['alto']['Layout']['Page']['PrintSpace']:
        #    continue
        #for k,v in enumerate(X['alto']['Layout']['Page']['PrintSpace']['TextBlock']):
        #    if isinstance(v, list):
        #        continue
        #    if isinstance(v, str):
        #        continue
        #    try:
        #        textline = v['TextLine']
        #    except:
        #        print(v, type(v))
        #        print("error")
        #        exit()
        #    if not isinstance(textline, list):
        #        textline = [textline]
        #    print("******* BLOCK",k,"**********")
        #    for i,line in enumerate(textline):
        #        #print(v['@HPOS'], line['@HPOS'])
        #        line = line['String']
        #        t = []
        #        #print(type(line),line)
        #        if not isinstance(line, list):
        #            line = [line]
        #        for e,entry in enumerate(line):
        #            #print(entry)
        #            content = entry['@CONTENT']
        #            if e == 0:
        #                form = chartotype(content)
        #                if form not in formats:
        #                    formats[form] = 1
        #                else:
        #                    formats[form] += 1
        #            t.append(entry['@CONTENT'])
        #        print(i," ".join(t))

from operator import itemgetter

print("**************numbers*****************")
numeric_forms = sorted([(k,v) for k,v in formats.items() if '9' in k], key=itemgetter(1), reverse=True)
for sf in numeric_forms[0:10]:
    print(sf)

print("**************text*****************")
text_forms = sorted([(k,v) for k,v in formats.items() if '9' not in k], key=itemgetter(1), reverse=True)
for sf in text_forms[0:10]:
    print(sf)

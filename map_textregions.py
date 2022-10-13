#!/usr/bin/python3

import xmltodict
from QSRRectangles import Rectangle
import os

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
file_prefixes = ['690762_0010_26191176', '690762_0011_26191177', '690762_0012_26191178']
file_prefixes += ['690762_0018_26191184', '690762_0015_26191181', '690762_0016_26191182']
file_prefixes += ['690762_0008_26191174']
#file_prefixes = [x[:-4] for x in os.listdir(data_dir) if x[-4:] == ".jpg"]
file_id = int(sys.argv[1])
prefix = file_prefixes[file_id]

#Z:\Images\QFA_1_1_-_England_&_Wales_Ecclesiastical_A-L_duplicated\QFA_1_1_-_England_&_Wales_Ecclesiastical_A-L_duplicated\page

print(prefix + ".xml")
X = xmltodict.parse(open(data_dir + "page/" + prefix + ".xml", 'rb'))

#V = X['PcGts']['Page'].items()

show_average = True
save = False

for k,v in X['PcGts']['Page'].items():
    if k == 'TextRegion':
        if isinstance(v, list):
            v = v[0]
        lines = v['TextLine']
        for ln in lines:
            line_id = ln["@id"]
            R = Rectangle(ln['Coords']['@points'])
            textregions.append([line_id,R])

from PIL import Image, ImageDraw

image = Image.open(data_dir + prefix + ".jpg")
draw = ImageDraw.Draw(image)

region_list = []
type_lookup = {}
if os.path.isfile("region_labels.txt"):
    region_file = open("region_labels.txt","r")
    for row in region_file:
        fields = row[:-1].split("|")
        if prefix == fields[0]:
            break
        coords = dict([x.split(":") for x in [y for y in fields[2].split(",")]])
        contents = fields[3]
        if len(fields) == 5:
            if fields[4] != "Y":
                contents = fields[4]
        if len(contents) == 0:
            continue
        R = Rectangle(coords)
        region_list.append([R, contents])
        for region_type in contents.split("+"):
            if region_type not in type_lookup:
                type_lookup[region_type] = []
            type_lookup[region_type].append(R)

    region_file.close()

from statistics import mean,stdev

avg_regions = []
for region_type, region_recs in type_lookup.items():
    this_avg = {}
    this_var = {}
    this_counts = {}
    this_max = {}
    this_avg['fl'] = mean([r.fl for r in region_recs])
    if len(region_recs) > 1:
        this_var['fl'] = stdev([r.fl for r in region_recs])
    else:
        this_var['fl'] = 0
    this_avg['fr'] = mean([r.fr for r in region_recs])
    if len(region_recs) > 1:
        this_var['fr'] = stdev([r.fr for r in region_recs])
    else:
        this_var['fr'] = 0
    this_avg['hp'] = mean([r.hp for r in region_recs])
    if len(region_recs) > 1:
        this_var['hp'] = stdev([r.hp for r in region_recs])
    else:
        this_var['hp'] = 0
    this_avg['lp'] = mean([r.lp for r in region_recs])
    this_counts['lp'] = len(region_recs)
    this_max['lp'] = max([r.lp for r in region_recs])
    if len(region_recs) > 1:
        this_var['lp'] = stdev([r.lp for r in region_recs])
    else:
        this_var['lp'] = 0
    avg_r = Rectangle(this_avg)
    avg_regions.append([avg_r, region_type])
    #if region_type == "subjecttext":
    #    avg_r.hp -= this_var["hp"]
    #    avg_r.lp += this_var["lp"]
    if show_average:
        draw.rectangle(((avg_r.fl, avg_r.hp), (avg_r.fr, avg_r.lp)), outline = "blue", fill = None, width = 3)



region_file = open("region_labels.txt","a")
for i, reg in enumerate(textregions):
    this_R = reg[1]
    r_id = reg[0]
    print_order = [['fl',str(this_R.fl)], ['hp',str(this_R.hp)], ['fr',str(this_R.fr)], ['lp',str(this_R.lp)]]
    coords = ",".join([x for x in [":".join(y) for y in print_order]])
    draw.rectangle(((this_R.fl, this_R.hp), (this_R.fr, this_R.lp)), outline = "red", fill = None, width = 3)
    this_content = ""
    had_labels = set()
    for tr in avg_regions:
        reg_R = tr[0]
        contents = tr[1]
        if contents in had_labels:
            continue
        had_labels.add(contents)
        if this_R.get_rcc8_class(reg_R) not in ["EC","DC"]:
            this_content += "+" + contents
    if save:
        region_file.write(prefix + "|" + r_id + "|" + coords + "|")
        if len(this_content) > 0:
            region_file.write(this_content[1:])
        region_file.write("\n")

region_file.close()


if show_average:
    image.save("/home/dataowner/vn_share/Images/qfa_textregions_avg_" + prefix + ".jpg")
else:
    image.save("/home/dataowner/vn_share/Images/qfa_textregions_" + prefix + ".jpg")



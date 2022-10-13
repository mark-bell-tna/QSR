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
file_prefixes = ['690762_0012_26191178', '690762_0011_26191177', '690762_0010_26191176']
file_prefixes += ['690762_0018_26191184', '690762_0015_26191181', '690762_0016_26191182']
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
            line_id = ln["@id"]
            R = Rectangle(ln['Coords']['@points'])
            textregions.append([line_id,R])

from PIL import Image, ImageDraw

image = Image.open(data_dir + prefix + ".jpg")
draw = ImageDraw.Draw(image)

for i, reg in enumerate(textregions):
    if i == int(sys.argv[2]):
        R = reg[1]
        draw.rectangle(((R.fl, R.hp), (R.fr, R.lp)), outline = "red", fill = None, width = 3)
        print(R)
        break


image.save("/home/dataowner/vn_share/Images/qfa_textregions_" + prefix + ".jpg")



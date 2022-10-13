#!/usr/bin/python3

import xmltodict

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

import os

data_root = "/home/research1/QSR/Data/"
for yr in ['Seals']:
    data_dir = data_root + yr + "/"
    filenames = os.listdir(data_dir)
    for f in filenames:
        X = xmltodict.parse(open(data_dir + f, 'rb'))

        V = X['alto']['Layout']['Page'].values()

        if 'TextBlock' not in X['alto']['Layout']['Page']['PrintSpace']:
            continue
        for k,v in enumerate(X['alto']['Layout']['Page']['PrintSpace']['TextBlock']):
            if isinstance(v, list):
                continue
            if isinstance(v, str):
                continue
            try:
                textline = v['TextLine']
            except:
                print(v, type(v))
                print("error")
                exit()
            if not isinstance(textline, list):
                textline = [textline]
            print("******* BLOCK",k,"**********")
            for i,line in enumerate(textline):
                #print(v['@HPOS'], line['@HPOS'])
                line = line['String']
                t = []
                #print(type(line),line)
                if not isinstance(line, list):
                    line = [line]
                for e,entry in enumerate(line):
                    #print(entry)
                    content = entry['@CONTENT']
                    if e == 0:
                        form = chartotype(content)
                        if form not in formats:
                            formats[form] = 1
                        else:
                            formats[form] += 1
                    t.append(entry['@CONTENT'])
                print(i," ".join(t))

from operator import itemgetter

print("**************numbers*****************")
numeric_forms = sorted([(k,v) for k,v in formats.items() if '9' in k], key=itemgetter(1), reverse=True)
for sf in numeric_forms[0:10]:
    print(sf)

print("**************text*****************")
text_forms = sorted([(k,v) for k,v in formats.items() if '9' not in k], key=itemgetter(1), reverse=True)
for sf in text_forms[0:10]:
    print(sf)

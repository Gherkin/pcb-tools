#!/usr/bin/python

import csv
from collections import defaultdict
def read_bom(filename):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = []
        header = next(reader)
        for row in reader:
            d = defaultdict(str)
            for i in range(len(row)):
                if(header[i] == "Designator"):
                    d[header[i]] = row[i].split(',')
                    d['Count'] = len(d[header[i]])
                else:
                    d[header[i]] = row[i]
            data.append(d)
                
    return data

import numpy as np
def bom_data_to_arr(data):
    out = []
    
    headers = []
    for item in data:
        headers += list(item.keys())
    headers = np.unique(headers)
    
    out.append(headers)
    row = ''
    for item in data:
        out.append([','.join(item[header]) if type(item[header]) == list else str(item[header]) for header in headers if header in item.keys()])
        
    return out

import numpy as np
def export_bom(data):
    out = []
    
    headers = []
    for item in data:
        headers += list(item.keys())
    headers = np.unique(headers)
    
    out.append(';'.join(headers))
    row = ''
    for item in data:
        out.append(';'.join([','.join(item[header]) if type(item[header]) == list else str(item[header]) for header in headers if header in item.keys()]))
        
    return '\n'.join(out)

import numpy as np
from functools import reduce

def merge_boms(datas):
    lcsc_sns = np.unique([[item['LCSC'] for item in data if 'LCSC' in item.keys() and item['LCSC'] != ''] for data in datas])
    
    print([[[key for key in item.keys() if key != 'LCSC' and key != 'Count'] for item in data] for data in datas])
    keys = np.unique(np.asanyarray([[[key for key in item.keys() if key != 'LCSC' and key != 'Count'] for item in data] for data in datas]).flatten())
    data = []
    
    row = {}
    datas = datas.copy()
    for i in range(len(datas)):
        dn = datas[i]
        for item in dn:
            for key in keys:
                print(key)
                print(item)
                item[key + '_' + str(i)] = item.pop(key)
    for sn in lcsc_sns:
        d = [[item for item in data if item['LCSC'] == sn] for data in datas]
        d = [x[0] for x in d]
        for item in d:
            item.pop('LCSC')
        tot_count = reduce(lambda m,x: m + x, [item['Count'] for item in d])
        for item in d:
            item.pop('Count')
        d = reduce(lambda m,x: m | x, d)
        d['Count'] = tot_count
        d['LCSC'] = sn
            
        data.append(d)
                
            
            
    return data



if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print('provide boms in csv form as filenames as arguments')
        exit()

    boms = [read_bom(file) for file in sys.argv[1:]]
    if len(boms) > 1:
        bom = merge_boms(boms)
    else:
        bom = boms[0]
    print(export_bom(bom))

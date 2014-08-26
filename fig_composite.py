#!/usr/bin/env python2
#-*-coding:utf-8 -*-
import os
import sys
import re
import PIL
from PIL import Image

pic_raw_path = 'pic_raw/'
pic_resize_path = 'pic_resize/'
pic_trans_path = 'pic_trans/'

def conv_black2transparency(in_file):
    pic_trans_file = in_file.replace("pic_resize","pic_trans")
    img = Image.open(in_file)
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    ensure_dir(pic_trans_file)
    img.save(pic_trans_file, "PNG")
    return 0

raw_file_list = []
#get pic file list recursively
def get_file_list(path_in):
    subdir_file_list = os.listdir(path_in)
    for file_name in subdir_file_list:
        full_file_name = os.path.join(path_in, file_name)
        if os.path.isdir(full_file_name):
            get_file_list(full_file_name)
        elif (None != re.search('(png|bmp|jpg|jpeg)$', file_name, re.IGNORECASE)):
            raw_file_list.append(full_file_name)
    return raw_file_list

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
    return 0

# Resize raw pictures
pic_raw_file_list = get_file_list(pic_raw_path)
img_size = 500,400

for fn in pic_raw_file_list:
    print("Resizing file %s to 500x400...") %fn
    pic_resize_file = fn.replace("pic_raw","pic_resize")
    ensure_dir(pic_resize_file)
    img = Image.open(fn)
    img = img.resize(img_size,Image.ANTIALIAS)
    fname,extension = os.path.splitext(pic_resize_file)
    newfile = fname+extension
    if extension != ".png" :
        newfile = fname + ".png"

    ensure_dir(newfile)
    img.save(newfile,"PNG")

# Convert uniformed pictures into transparency
raw_file_list = []
pic_resize_file_list = get_file_list(pic_resize_path)
for fn in pic_resize_file_list:
    pic_trans_file = fn.replace("pic_resize","pic_trans")
    if fn.find('original.png') == -1:
        print("Convert file %s into transparency...") %fn
        conv_black2transparency(fn)
    else:
        print("original.png need not transparent, give up...")

# Composite original.png with other element.png
raw_file_list = []
pic_trans_file_list = get_file_list(pic_trans_path)
img_base = Image.open(pic_resize_path + 'original.png')
for fn in pic_trans_file_list:
    composite_file = fn.replace("pic_trans","pic_composite")
    ensure_dir(composite_file)
    fname,extension = os.path.splitext(composite_file)
    pic_composite_file = fname + '-' + 'original' + extension
    print("Composite original.png with file %s...") %fn
    img_element = Image.open(fn)
    Image.alpha_composite(img_base, img_element).save(pic_composite_file, "PNG")
    print("Final composite file %s") %pic_composite_file
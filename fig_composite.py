#!/usr/bin/env python2
#-*-coding:utf-8 -*-
import os
import sys
import re
import PIL
from PIL import Image

#fig_in_path = os.path.dirname(os.path.realpath(sys.argv[0])) 
fig_in_path = os.path.relpath(os.path.dirname(os.path.realpath(sys.argv[0])))

fig_out_path = fig_in_path + "/fig_trans/"
fig_resize_out_path = fig_in_path + "/fig_resize/"

def conv_black2transparency(in_file, out_path):
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

    out_file = out_path + in_file
    ensure_dir(out_file)
    img.save(out_file, "PNG")

    return 0

#get the file recursively
file_list = []
trans_flag = False
def get_recursive_file_list(path):
    current_files = os.listdir(path)
    for file_name in current_files:
        full_file_name = os.path.join(path, file_name)
        print full_file_name
        
        if  os.path.isdir(full_file_name):
            if trans_flag == False:
                if os.path.realpath(full_file_name).find("fig_trans") != -1:
                    print "Transparence fig already done"
                    continue
            get_recursive_file_list(full_file_name)
        elif (None != re.search('(png|bmp|jpg|jpeg)$', file_name, re.IGNORECASE)):
            file_list.append(full_file_name)
 
    return file_list

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

    return 0

fig_in_list = get_recursive_file_list(fig_in_path)
img_size = 500,400

for fn in fig_in_list:
    img = Image.open(fn)
    img = img.resize(img_size,Image.ANTIALIAS)
    fname,extension = os.path.splitext(fn)
    newfile = fname+extension
    if extension != ".png" :
        newfile = fname + ".png"

    #fig_resize_out_file = fig_resize_out_path + newfile
    #ensure_dir(fig_resize_out_file)
    img.save(fn,"PNG")
    print "Resizing file : %s" % (fn)

    conv_black2transparency(fn, fig_out_path)
    print("File %s is converted to transparency.") %fn

print("Congratulations! All of the raw fig have been converted to transparency.")

trans_flag = True
file_list = []
trans_fig_list = get_recursive_file_list(fig_out_path)
print "fig_out_path=%s" %fig_out_path
print trans_fig_list
fig_temp = "fig_final.png"
img0 = Image.open(trans_fig_list[0])
img1 = Image.open(trans_fig_list[1])
Image.alpha_composite(img0, img1).save(fig_temp, "PNG")
print "First composition"

for i in xrange(2,len(trans_fig_list)):
    img0 = Image.open(fig_temp)
    img1 = Image.open(trans_fig_list[i])
    Image.alpha_composite(img0, img1).save(fig_temp, "PNG")

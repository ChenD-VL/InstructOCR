import os
import scipy.io
import random
import pickle
from tqdm import tqdm
import argparse
from shapely.geometry import Point, LineString
import numpy as np
import csv
from PIL import Image

def replace_all(s, old, new, reg = False):
    if reg:
        import re
        targets = re.findall(old, s)
        for t in targets:
            s = s.replace(t, new)
    else:
        s = s.replace(old, new)
    return s

def prepare_annotation(image_dir,txt_dir,save_dir):
    imgnames = os.listdir(image_dir)
    imgdir = imgnames

    for i,key in enumerate(imgnames):
        key = key.replace('png', 'jpg')
        key = key.replace('jpeg', 'jpg')
        imgnames[i] = key
    all_texts = []
    for i,key in enumerate(imgnames):
        annotation_key = 'gt_' + key
        annotation_key = annotation_key.replace('jpg','txt')
        if not os.path.exists(os.path.join(txt_dir, annotation_key)):
            print(os.path.join(txt_dir, annotation_key))
            continue
        label_line = []
        with open(os.path.join(txt_dir, annotation_key), 'r', encoding='UTF-8') as f: 
             lines = f.readlines()
             polygons = []
             texts = []
             for line in lines:
                 line = line.encode('utf-8').decode('utf-8-sig')
                 line = replace_all(line, '\xef\xbb\xbf', '')
                 label_line.append(line.strip())
             print("key:", key)
             print("i:", i)
        all_texts.append(label_line)

    with open(save_dir, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["image_path", "results"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for i in (range(len(imgdir))):
            i_name = imgdir[i]
            i_txt = all_texts[i]
            all_str = ""
            for str_index in range(len(i_txt)):
                points = i_txt[str_index].split(",")[:8]
                text = i_txt[str_index].split(",")[8:]
                print(points,text)
                point_str = str()
                text_str = str()
                for point in points:
                    point_str += point + ","
                for text_split in text:
                    text_str += text_split +","
                
                all_str += point_str[:-1] + "&rec&" +text_str[:-1]
                if str_index != len(i_txt)-1:
                    all_str += "&&tab&&"
            writer.writerow({"image_path": i_name, "results": all_str})

if __name__ == "__main__":
    image_dir = "./ic15_train_image"
    label_dir = "./ic15_train_label"
    save_dir = "./ic15_train.csv"
    prepare_annotation(image_dir,label_dir,save_dir)
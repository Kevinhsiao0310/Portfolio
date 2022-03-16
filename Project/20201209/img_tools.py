import os, xml.dom.minidom, sys, argparse, cv2, ast
import matplotlib.pyplot as plt 
import numpy as np
from scipy.optimize import linear_sum_assignment
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from PMXLIB_Draw import video2imgs, imgs2video
from PMXLIB_Evaluation import  Isin, BBox, AIresults, LoadAItxt, PrintDiff
from PMXLIB_Utils      import  LOGname, ReadLog
from PMXLIB_Mouse_Event import Mouse_event

IMG_LIST = []
vertex_lst = []

YOLOV4_W = 608 
YOLOV4_H = 608 
SSD_W    = 1920 
SSD_H    = 1080

AI_LOG = None

def Argparse():

    parser = argparse.ArgumentParser()
    parser.add_argument("--v",    help = "tansform the imgs to video (Img Folder Path) ===> example/Pic")
    parser.add_argument("--m",    help = "transform the video to imgs (Video Path) ===> example/test.mp4")
    parser.add_argument("--d",    help = "draw box on the video or imgs (Log Path) ===> example/Log/SSD/ssd.txt")
    parser.add_argument("--l",    help = "draw line on the video or imgs (Give 'read' to  load vertex.txt ,give img path to draw)")
    parser.add_argument("--show", help = "Show pics or not (bool)", default = False, type = bool)   
    parser.add_argument("--save", help = "Save or not (bool)",      default = False, type = bool)  

    args = parser.parse_args()

    return args

def AIinlog(AILOG):
    for idx, A in enumerate(AILOG):
        L = []
        for log in A.boxes:
            if log.type == str('Person'):
                if (50 <= log.x1 <= 95) and (120 <= log.x2 <= 160):
                        continue
                if 110 <= log.x1 <= 145 and 185 <= log.x2 < 250:
                        continue
                else:
                    if not (log.x2 - log.x1) >= 1920 * 0.6:
                        L.append(log)
            if log.type == str('Vehicle'):
                if 1290 <= log.x1 <= 1340 and 1380 <= log.x2 <= 1425 and log.y1 <= 129:
                    continue
                else:
                    L.append(log)
            if log.type == str('Bike'):
                if not log.x2 - log.x1 >= 1920 * 0.6:
                    L.append(log)
            if log.type == str('Pet'):
                if not log.x2 - log.x1 >= 1920 * 0.6:
                    L.append(log)
        AILOG[idx].boxes = L 
    return AILOG


if __name__ == "__main__" :

    args = Argparse()
    save_pics  = args.save
    show_mode  = args.show
    draw_boxes = args.d

    if args.l == 'read':
        namebox = ReadLog(args.d, "draw")
        f1 = open("vertex_list.txt", "r")
        lines = f1.readlines()
        name = None
        lastname = None
        for line in lines:
            line   = line.strip('\n')
            if namebox.vname in line:
                line = line.split(':')[1]
                v_list = ast.literal_eval(line)
        for i in v_list:
            i[0] = round(i[0])
            i[1] = round(i[1])
            t = tuple(i)
            vertex_lst.append(t)
        f1.close()
    elif args.l:
        namebox = ReadLog(args.d, "draw")
        vertex = Mouse_event()
        v_list = vertex.OpenImg(args.l)
        for i in v_list:
            i[0] = round(i[0])
            i[1] = round(i[1])
            t = tuple(i)
            vertex_lst.append(t)
    else:
        vertex_lst = [(0,0), (1920,0), (1920,1080), (0,1080), (0,0)]

    if args.v:         
        videoname = input("Video Name (.mp4) :")

        try :
            input_shape = (int(input("input_picwidth : ")), int(input("input_picheight : ")))
        except ValueError:
            input_shape = (1920, 1080)


        if draw_boxes:
            AILOG = LoadAItxt(draw_boxes , 'ssd', SSD_W, SSD_H)
            for L in AILOG:
                print("L:", L.fname)
                for l in L.boxes:
                    print(l.box)
#            LOG = AILOG.copy() 
            LOG = AIinlog(AILOG)
            imgs2video(args.v, videoname, draw_boxes, vertex_lst, save_pics, LOG, show_mode, input_shape)
        else:
            AILOG = None
            imgs2video(args.v, videoname, draw_boxes, vertex_lst, save_pics, AILOG, show_mode, input_shape)

    elif args.m:
        video2imgs(args.m)  #create the file have the same name to the video in order to store the imgs 




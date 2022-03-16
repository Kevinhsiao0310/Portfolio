#!/usr/bin/python3
import os, xml.dom.minidom, sys, argparse, random, cv2, copy, ast
import numpy as np

VERTEX_PATH = os.path.join(os.getcwd(), 'vertex', 'vertex_list.txt')

# Add LIB_PATH for import,(if want to run per pic)
LIB_PATH_ALL = os.path.join(os.getcwd(), "..")
sys.path.append(LIB_PATH_ALL)

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from libs.PMXLIB_Evaluation  import Isin, BBox, AIresults, loadPics, loadAItxt, createaXML,\
                                    GetAnnotBoxLoc, readXMLs, writeXMLs, checkLoad, calIOU, collectEvaluation, locationCheck, createDict
from libs.PMXLIB_Utils       import LOGname, readLog
from libs.PMXLIB_Mouse_Event import Mouse_event

def argParse():
    example = (
        "Command Example: \n"
        "python3 evaluatePrecisionRecall.py \n"
        "--ssd_path ../example/logs/20201104-part2_ssd_v5.1.1_640x360_Data20210420-retrain5b-160k.txt \n"
        "--yolo_path ../example/logs/20201104-part2_yolo_608x608.txt \n"
        "--gt_path ../example/GT/20201104-part2/ \n" 
        "--pic_path ../example/pics/20201104-part2/ \n"
        "--resolution [1920,1080] \n "
        "--draw_line Read \n "
    )

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, epilog=example
    )
    parser.add_argument("-ssd",  "--ssd_path", type=str, help="ssd_log_path. (log .txt)")
    parser.add_argument("-yolo", "--yolo_path", type=str, help="yolo_path. (log .txt)")
    parser.add_argument("-gt",   "--gt_path", type=str, help="gt_path. (xml folder)")
    parser.add_argument("-pic",  "--pic_path", type=str, help="pic_path. (image folder")
    parser.add_argument("-dl",   "--draw_line", help=" Sample Pic Path or Read (from txt).")
    parser.add_argument("-res",  "--resolution", type=str, default="None", 
                         help="Input Resolution in list, ex : [1920, 1080]. If no input or input is not list, read resolution by pic_path.")
    args = parser.parse_args()

    return args

def checkAIinZONE(AI_dict, vertex_lst):

    for key, value in sorted(AI_dict.items(), key=lambda x: x[0]):
        collect = []                      # allocate a list for collecting which AIinZone
	
        if value.boxes is None: continue
        if len(value.boxes)> 0:
            
            shape = value.shape
            vertex_lst_byratio = transformVertex2ratio(shape, vertex_lst)
            for b in value.boxes:
	       
                isin = locationCheck(b.x2, b.y2, vertex_lst_byratio)
                
                if isin:
               	    collect.append(b)
            value.boxes = collect         # replace collect to boxes 

    return AI_dict

def loadVertex(log_path):

    nameboxobj = readLog(log_path, "draw")
    v_list = []

    vertex_txt = open(VERTEX_PATH, "r")
    lines = vertex_txt.readlines()

    for line in lines:
        line  = line.strip('\n')
        if nameboxobj.vname in line:
            line = line.split(':')[1]
            v_list.append(ast.literal_eval(line))

    for idx, positon in enumerate(v_list):
        print(idx, ':', positon)

    num = int(input('Which vertex_lst do you want to draw: '))
    vertex_lst = v_list[num]
    print('vertex_lst :', vertex_lst)
    vertex_txt.close()
        
    return  vertex_lst

def setVertex(log_path, pic_path):

    img      = os.listdir(pic_path)[0]
    img_path = os.path.join(pic_path, img)

    nameboxobj = readLog(log_path, "draw")

    vertex = Mouse_event()
    vertex_lst = vertex.OpenImg(img_path)

    f1 = open(VERTEX_PATH, "a")
    f1.write("\n")
    f1.write(nameboxobj.vname)
    f1.write(':')
    f1.write(str(vertex_lst))
    f1.write("\n")
    f1.close()
    
    return  vertex_lst

def transformVertex2ratio(shape, vertex_lst): 
    #When we set up a line for evaluating Precision and Recall by selecting
    #from vertex_list.txt or detecting from line drawn on sample pic, all 
    #position coordinates of line will be divided by the height or width of pic 
    #for normalization.

    #The x-coordinate is divided by the width of pic.
    #The y-coordiante is divided by the height of pic.
    #[[x,y],...]

    return [[v[0] / shape[1],  v[1] / shape[0]] for v in vertex_lst]



def collectLogs(ssd_path, yolo_path, gt_path, pic_path, resolution, vertex_lst):
    
    
    picnamedict_ssd,  loglist_ssd  = createDict(pic_path, ssd_path)
    picnamedict_yolo, loglist_yolo = createDict(pic_path, yolo_path)
    log_ssd  = loadAItxt('ssd',  pic_path, resolution, picnamedict_ssd,  loglist_ssd)
    log_yolo = loadAItxt('yolo', pic_path, resolution, picnamedict_yolo, loglist_yolo)                                                                                                         
    log_GT = readXMLs(gt_path, picnamedict_ssd)
    
    if vertex_lst == None:
        pass
    else:
        log_ssd  = checkAIinZONE(log_ssd,  vertex_lst)
        log_yolo = checkAIinZONE(log_yolo, vertex_lst)
        log_GT   = checkAIinZONE(log_GT,   vertex_lst)
    
    return log_ssd, log_yolo, log_GT

def collectLogsinZONE(log_ssd, log_yolo, log_GT, vertex_lst):

    log_ssd  = checkAIinZONE(log_ssd,  vertex_lst)
    log_yolo = checkAIinZONE(log_yolo, vertex_lst)
    log_GT   = checkAIinZONE(log_GT,   vertex_lst)
  
    return log_ssd, log_yolo, log_GT

def createOutputfile(ssd_path, draw_mode, vertex_lst):
    
    if vertex_lst == None:
        draw_mode = 'ndraw'
        nameboxobj = readLog(ssd_path, draw_mode)
        file = sys.stdout
        sys.stdout = open(r"outPut/{}".format(nameboxobj.fullname), 'w')
    else:
        draw_mode = 'draw'
        nameboxobj = readLog(ssd_path, draw_mode)
        file = sys.stdout
        sys.stdout = open(r"outPut/{}".format(nameboxobj.fullname), 'w')
    
    return file 

if __name__== "__main__":

    args = argParse()
    gt_path  = args.gt_path
    ssd_path = args.ssd_path
    yolo_path = args.yolo_path
    pic_path = args.pic_path
    
    try:
        resolution = ast.literal_eval(args.resolution)
    except ValueError:
        resolution = None
    
    vertex_lst = None
    draw_mode = 'ndraw'

    if  args.draw_line:
        
        if args.draw_line == 'read' or args.draw_line == 'Read':
            vertex_lst = loadVertex(ssd_path)
            print("Type: ", type(vertex_lst))
        
        else:
            vertex_lst = setVertex(ssd_path, pic_path)
        file = createOutputfile(ssd_path, draw_mode, vertex_lst)
        log_ssd, log_yolo, log_GT = collectLogs(ssd_path, yolo_path, gt_path, pic_path, resolution, vertex_lst)        
        
    else:
        file = createOutputfile(ssd_path, draw_mode, vertex_lst)
        log_ssd, log_yolo, log_GT = collectLogs(ssd_path, yolo_path, gt_path, pic_path, resolution, vertex_lst)

    print("vertex_list: ", vertex_lst)

    print("\n======== SSD vs. YoloV4 ========\n")
    collectEvaluation(log_ssd, log_yolo)
    
    #=========================================#
    print("\n======== SSD vs. GT ========\n")
    collectEvaluation(log_ssd, log_GT)

    #==========================================#
    print("\n======== YoloV4 vs. GT ========\n")
    collectEvaluation(log_yolo, log_GT)

    sys.stdout.close()
    sys.stdout = file


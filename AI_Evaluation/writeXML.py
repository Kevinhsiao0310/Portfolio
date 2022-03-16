#!/usr/bin/python3
import os, xml.dom.minidom, sys, argparse, random, cv2, copy, ast
import numpy as np

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# Add LIB_PATH for import
LIB_PATH_ALL = os.path.join(os.getcwd(), "..")
sys.path.append(LIB_PATH_ALL)


from libs.PMXLIB_Evaluation import (Isin, BBox, AIresults, loadPics, loadAItxt, 
    createaXML, GetAnnotBoxLoc, readXMLs, writeXMLs, checkLoad, calIOU, 
    collectEvaluation, locationCheck, createDict, transformDict)

def Argparse():
    example = (
        "Command Example: \n"
        "python3 writeXML.py \n"
        "--yolo_path ../example/logs/20201104-part2_yolo_608x608.txt \n"
        "--pic_path ../example/pics/20201104-part2 \n "
    )

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, epilog=example)
    parser.add_argument("-ssd",  "--ssd_path", type=str, help="SSD_PATH.")
    parser.add_argument("-yolo", "--yolo_path", type=str, help="YOLO_PATH.")
    parser.add_argument("-pic",  "--pic_path", type=str, help="Pic Path.")

    args = parser.parse_args()

    return args

def createLoginfo(ssd_path, yolo_path):
    log_path = str(ssd_path).strip("None") + str(yolo_path).strip("None")
    log_mode = log_path.split("_")[1]
    
    return log_path, log_mode

if __name__== '__main__':

    args      = Argparse()
    ssd_path  = args.ssd_path
    yolo_path = args.yolo_path
    pic_path  = args.pic_path
    
    if pic_path:
        if os.path.isdir(pic_path):
            imgs = os.listdir(pic_path)
            for i, img in enumerate(imgs):
                if img.endswith('.jpg'): continue
                else:
                    exit()
	
    if ssd_path and yolo_path:
        print("Don't give 2 sources. 1 sources at once!")
        exit()
	
    elif ssd_path or yolo_path:
        log_path, log_mode = createLoginfo(ssd_path, yolo_path)
                
        if os.path.isfile(log_path):
            if yolo_path == None and log_mode == 'ssd' or\
               ssd_path == None and log_mode == 'yolo':
                print("Load {}_log from {}".format(log_mode, log_path))
            else:
                print("Make sure you input -{}, {} is a {}_path"\
                      .format(log_mode, log_path, log_mode))
                exit()
        else:
            print("{} is not a ssd or yolo path".format(log_path))

        picnamedict, AIlist = createDict(pic_path, log_path)
        log = loadAItxt(log_mode, pic_path, None, picnamedict, AIlist)
        
        log = transformDict(log) #ratio2real

        filename = os.path.basename(os.path.join(log_path.rstrip(".txt")))
        filename = filename.split("_")[0]
        xml_path = os.path.join(os.getcwd(),"..","GT/{}").format(filename)
	    
    if not os.path.isdir(xml_path):
        os.makedirs(xml_path, exist_ok=True)
    writeXMLs(log, xml_path, pic_path)



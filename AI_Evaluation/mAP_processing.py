from genericpath import samefile
import os, xml.dom.minidom, sys, argparse, random, cv2, copy, ast
import numpy as np
from tqdm import tqdm
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

LIB_PATH_ALL = os.path.join(os.getcwd(), "..")
sys.path.append(LIB_PATH_ALL)

from libs.PMXLIB_Evaluation  import  loadAItxt, readXMLs, createDict, transformDict

SSD_W = 640
SSD_H = 360

SAVEPATH_AI = "./AILOG/"
SAVEPATH_GT = "./GTLOG/"
SAVEPATH_RESULTS = "./results/"

def Argparse():
    example = (
        "Command Example: \n"
        "python3 mAP_processing.py \n"
        "--gt_path ../example/GT/20201104-part2 \n"
        "--ai_path ../example/logs/20201104-part2_ssd_v5.1.1_640x360_Data20210420-retrain5b-160k.txt \n"
        "--pic_path ../example/pics/20201104-part2 \n"
        "--auto \n"
        "--resolution [1920,1080] \n "
    )

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, epilog=example)
    parser.add_argument("-gt", "--gt_path", type=str, help="The path of GT(.xml) files.")
    parser.add_argument("-ai", "--ai_path", type=str, help="The path of AI(ssd or yolo) log.")
    parser.add_argument("-pic", "--pic_path", type=str, help="The path of pics which is neccesary to rewrite AI logs and load resolution.")
    parser.add_argument("-res", "--resolution", type=str, help="Input Resolution ex : [1920, 1080]")
    parser.add_argument("-a", "--auto", action="store_true",help="Run pascalvoc.py to calculate mAP automatically")
    args = parser.parse_args()

    return args

def checkSavePath(SAVEPATH_AI, SAVEPATH_GT):

    savepaths = [SAVEPATH_AI, SAVEPATH_GT]

    for savepath in savepaths:
        if os.path.isdir(savepath):
            os.system('rm -rf {} && mkdir {}'.format(savepath, savepath))
        else:
            os.system('mkdir {}'.format(savepath))

def findAImodel(log_path_AI):

    AI_file  = os.path.basename(log_path_AI)
    AI_model = AI_file.split("_")[1]

    return AI_model

def rewriteAIlog(log_path_AI, pic_path, resolution):

    if log_path_AI.endswith('txt'):
        picnamedict, loglist = createDict(pic_path, log_path_AI)
#        print("picnamedict", picnamedict)
#        print("loglist", loglist)
        AI_model = findAImodel(log_path_AI)
        log_AI   = loadAItxt(AI_model, pic_path, resolution, picnamedict, loglist)
        log_AI   = transformDict(log_AI) #ratio2real
        print("\n======== rewrite AILOG ========\n")

        for key, value in tqdm(sorted(log_AI.items(), key = lambda x : x[0])):

            txtname = value.fname.replace('jpg', 'txt')
            txtfile = os.path.join(SAVEPATH_AI, txtname)

            with open(txtfile, 'a') as  f1:
                
                for log in value.boxes:
                    box = log.box[:5]
                    box.insert(1, log.box[5])
                    box = [str(i) for i in box]
                    f1.write(" ".join(box))
                    f1.write("\n")
    
    return picnamedict

def rewriteGTlog(log_path_GT, picnamedict):


    for root, dirs, files in os.walk(log_path_GT):
        log_GT = readXMLs(root, picnamedict)
        log_GT = transformDict(log_GT) #ratio2real

        print("\n======== rewrite GTLOG ========\n")
        
        for key, value in tqdm(sorted(log_GT.items(), key = lambda x : x[0])):

            if len(value.boxes) > 0:
                txtname = value.fname.split('/')[-1].replace('xml', 'txt')
                txtfile = os.path.join(SAVEPATH_GT, txtname)
                
            with open(txtfile, 'a') as  f1:
                
                for log in value.boxes:
                    box = log.box[:5]
                    # box.insert(1, log.box[5])
                    box = [str(i) for i in box]
                    f1.write(" ".join(box))
                    f1.write("\n")

def rewriteLogs(log_path_AI, log_path_GT, pic_path, resolution):

    picnamedict = rewriteAIlog(log_path_AI, pic_path, resolution)
    rewriteGTlog(log_path_GT, picnamedict)

def compareLogs(SAVEPATH_AI, SAVEPATH_GT):

    loglist_AI = os.listdir(SAVEPATH_AI)
    loglist_GT = os.listdir(SAVEPATH_GT)
    print("\n======== Comparison AILOG File With GTLOG File ========\n")
    for filename in tqdm(loglist_AI):
        if filename not in loglist_GT:
            unnecessary_file = os.path.join(SAVEPATH_AI, filename)
            os.system('rm {}'.format(unnecessary_file))

def autoRunpacalvoc(SAVEPATH_AI, SAVEPATH_GT, SAVEPATH_RESULTS):

    if os.path.isdir(SAVEPATH_RESULTS):
        os.system("rm -rf {}".format(SAVEPATH_RESULTS))
    os.system("python3 pascalvoc.py -gt {} -ai {} -t 0.2 -np".format(SAVEPATH_GT, SAVEPATH_AI))

if __name__== '__main__':
    args        = Argparse()
    log_path_GT = args.gt_path
    log_path_AI = args.ai_path
    pic_path    = args.pic_path
    resolution  = [1920, 1080]

    if args.resolution:
        resolution = ast.literal_eval(args.resolution)

    
    checkSavePath(SAVEPATH_AI, SAVEPATH_GT)
    rewriteLogs(log_path_AI, log_path_GT, pic_path, resolution)
    compareLogs(SAVEPATH_AI, SAVEPATH_GT)

    if args.auto:
        print("\n======== auto Run pacalvoc ========\n")
        autoRunpacalvoc(SAVEPATH_AI, SAVEPATH_GT, SAVEPATH_RESULTS)
        print("\n")

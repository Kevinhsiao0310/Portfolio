import os, xml.dom.minidom, sys, argparse, cv2, ast
import matplotlib.pyplot as plt 
import numpy as np
from tqdm import tqdm

VERTEX_PATH = os.path.join(os.getcwd(), 'vertex', 'vertex_list.txt')

# Add LIB_PATH for import
LIB_PATH = os.path.join(os.getcwd(), "..")
sys.path.append(LIB_PATH)

from scipy.optimize import linear_sum_assignment
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from libs.PMXLIB_Draw        import video2Imgs, imgs2Video
from libs.PMXLIB_Evaluation  import Isin, BBox, AIresults, loadAItxt, collectEvaluation, createDict, transformDict
from libs.PMXLIB_Utils       import LOGname, readLog
from libs.PMXLIB_Mouse_Event import Mouse_event

VERTEX_LIST = []

def argParse():
    example = (
        "Command Example: \n"
        "\nImage -> Video \n"
        "python3 img_tools.py -i2v \n"
        "--pic_path ../example/pics/20201104-part2 \n"
        "--video_name 20201104-part2.mp4 \n"
        "--ai_path ../example/logs/20201104-part2_ssd_v5.1.1_640x360_Data20210420-retrain5b-160k.txt \n"
        "--draw_line read \n"
        "\nVideo -> Image \n"
        "python3 img_tools.py -v2i --video_name outPut/20201104-part2.mp4 \n "
    )

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, epilog=example
    )
    parser.add_argument("-i2v", action="store_true", help="transform the imgs to video")
    parser.add_argument("-v2i", action="store_true", help="transform the video to imgs")
    parser.add_argument("-show", action="store_true", help="Show pics or not")   
    parser.add_argument("-save", action="store_true", help="Save or not")  
    parser.add_argument("--video_name", type=str, 
                        help="input a videoname when transforming imgs to video(.mp4) ===> example/test.mp4")
    parser.add_argument("-dl", "--draw_line", type=str, 
                        help="draw line on the video or imgs (Give'read' to  load vertex.txt ,give img path to use Mouse_event)")
    parser.add_argument("-pic", "--pic_path", type=str, help="(Img Folder Path) ===> example/Pic")
    parser.add_argument("-ai", "--ai_path", type=str, help="draw box on the video or imgs (Log Path) ===> example/Log/SSD/ssd.txt")

    args = parser.parse_args()

    return args

def loadVertex(LOG_PATH):

    namebox = readLog(draw_boxes, "draw")
    VERTEX_PATH = os.path.join(os.getcwd(), "vertex", "vertex_list.txt") #add the path of vertex_list.txt
    f1 = open(VERTEX_PATH, "r")
    lines = f1.readlines()
    v_list = []

    for line in lines:
        line = line.strip('\n')
        if namebox.vname in line:
            line = line.split(':')[1]
            v_list.append(ast.literal_eval(line))

    for idx, l in enumerate(v_list):
        print(idx, ':', l)

    num = int(input('Which vertex_lst do you want to draw: '))
    vertex_lst = v_list[num]

    for i in vertex_lst:
        i[0] = round(i[0])
        i[1] = round(i[1])
        t = tuple(i)
        VERTEX_LIST.append(t)

    f1.close()

    return VERTEX_LIST

def setVertex(LOG_PATH, PIC_PATH):

    img = os.listdir(PIC_PATH)[0]
    img_path = os.path.join(PIC_PATH, img)
    namebox = readLog(draw_boxes, "draw")
    vertex = Mouse_event()
    v_list = vertex.OpenImg(img_path)

    for i in v_list:
        i[0] = round(i[0])
        i[1] = round(i[1])
        t = tuple(i)
        VERTEXLIST.append(t)

    return VERTEX_LIST

def checkResolution(PIC_PATH):
    print("\n======== checkResolution from {} ========\n".format(os.path.basename(PIC_PATH)))
    imgs = sorted(os.listdir(PIC_PATH))
    for i, img in enumerate(tqdm(imgs)):
        resolution         = cv2.imread(os.path.join(PIC_PATH, imgs[0])).shape
        resolution_control = cv2.imread(os.path.join(PIC_PATH, imgs[i])).shape
        shape = (resolution[1], resolution[0])
        if resolution != resolution_control:
            print("Different resolution between {}{} and {}{}".\
                   format(imgs[0], resolution, imgs[i], resolution_control))
            exit()
        else: continue

    return shape


if __name__ == "__main__" :

    args = argParse()
    save_pics  = args.save
    show_mode  = args.show
    draw_boxes = args.ai_path

    i2v_picpath     = args.pic_path        # in i2v mode, the input is a picpath with images.
    i2v_videoname   = args.video_name      # in i2v mode, the output is a video. 
    v2i_videoname   = args.video_name      # in v2i mode, the input is a video.

    if args.draw_line == 'read':
        vertex_list = loadVertex(draw_boxes)
    elif args.draw_line:
        vertex_list = setVertex(draw_boxes, i2v_picpath)
    else:
        vertex_list = [(0,0), (1920,0), (1920,1080), (0,1080), (0,0)]
    
    if args.i2v:
        shape = checkResolution(i2v_picpath)
        AIdict = None

        if draw_boxes:
            picnamedict, AIlist = createDict(i2v_picpath, draw_boxes)
            AIdict = loadAItxt('ssd', i2v_picpath, shape, picnamedict, AIlist)
            AIdict = transformDict(AIdict) #ratio2real

        imgs2Video(i2v_picpath, i2v_videoname, vertex_list, save_pics, AIdict, show_mode, shape)


    elif args.v2i:
        video2Imgs(v2i_videoname)  # create the directoy with the same name to the video, in order to store the imgs. 


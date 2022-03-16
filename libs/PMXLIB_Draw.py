import os, xml.dom.minidom, sys, argparse, cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linear_sum_assignment
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from libs.PMXLIB_Evaluation import Isin, BBox, AIresults, countLabels


PRIMAX_NAMES = ["Bike", "Vehicle", "Person", "Pet", "None"]
PRIMAX_COUNT = [0, 0, 0, 0, 0]

def video2Imgs(video_name):  # convert video to photo

    print("\n======== video2Imgs ========\n")

    if video_name.endswith("mp4"):
        folder_path = video_name.rstrip(".mp4")
        vname = os.path.splitext(os.path.basename(video_name))[0]
        cap = cv2.VideoCapture(video_name)
        if cap.isOpened() and cap is not None:
            if not os.path.isdir(folder_path):
                os.mkdir(folder_path)
        else:
            print("Load {} failed.".format(video_name))
            exit()
    else:
        print("{} is not a mp4 file.".format(video_name))
        exit()

    count = 0
    while True:
        ret, frame = cap.read()
        if ret:
            img_path = os.path.join(folder_path, vname + "_" + str(count).zfill(5) + ".jpg")
            print(img_path, end="\r")
            cv2.imwrite(img_path, frame)
            cv2.waitKey(30)  # number of pic per second
            count += 1
        else:
            cap.release()
            break
    os.system("mv {}/ outPut/".format(folder_path))

def imgs2Video(pic_path, save_name, vertex_lst, save_pics, AI_dict, show, shape=(1920, 1080)):

    fps = 30
    num = 0
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(save_name, fourcc, fps, shape)

    if not os.path.isdir(pic_path):
        print("Load {} failed".format(pic_path))
        exit()

    if not save_name.endswith("mp4"):
        print("{} is not a mp4 file".format(save_name))
        exit()

    for i in sorted(os.listdir(pic_path)):
        img_name = os.path.join(pic_path, i)
        if AI_dict is not None:
            num, show = makeVideo(img_name, video_writer, vertex_lst, AI_dict[i].boxes, save_pics, show, num)
        else:
            num, show = makeVideo(img_name, video_writer, vertex_lst, None, save_pics, show, num)

    print("{} : {}".format(PRIMAX_NAMES, PRIMAX_COUNT))
    video_writer.release()
    os.system("mv {} outPut/".format(save_name))

def makeVideo(img_name, video_writer, vertex_lst, AIbox, save_pics, show, num):

    frame = cv2.imread(img_name)
    frame = draw(frame, AIbox, num, vertex_lst)
    if show:
        show = showPic(img_name, frame, show)
    if save_pics:
        savePic(img_name, frame)
    video_writer.write(frame)
    print("====== frame : {} =======".format(num), end="\r")
    num += 1

    return num, show

def draw(img_frame, AIbox, num, vertex_lst):

    COUNT = 0

    # draw line first
    if vertex_lst != [(0, 0), (1920, 0), (1920, 1080), (0, 1080), (0, 0)]:
        cv2.line(img_frame, vertex_lst[0], vertex_lst[1], (255, 0, 0), 3)
    # draw frame num
    cv2.putText(img_frame, "frame :{}".format(num),(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    if AIbox == None:
        return img_frame

    for BOX in AIbox:
        if BOX.type == "Person":
            COUNT += 1
        if BOX.type == None:
            return img_frame
        box = BOX.box
        color = (0, 128, 0)

        label = str(box[0])
        PRIMAX_COUNT[PRIMAX_NAMES.index(label)] += 1
        cv2.rectangle(img_frame, (int(box[1]), int(box[2])), (int(box[3]), int(box[4])), color, 3)    # KP bounding box
        cv2.rectangle(img_frame, (int(box[1]) - 2, int(box[2]) - 40), (int(box[3]) + 2, int(box[2])), color, -1) # KP ID box
        cv2.putText(img_frame, "{} ID:{}".format(box[0], box[6]), (int(box[1]), int(box[2]) - 12), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img_frame, "{} ".format(box[0]), (int(box[1]), int(box[2]) - 12), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
    # Draw a rectangle fill up green
    # Draw people count
    # cv2.rectangle(img_frame, (0, 0), (200, 40), color, thickness = -1)
    # cv2.putText(img_frame, "{}: {}".format('people', count), (5, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255, 255, 255), 2, cv2.LINE_AA)

    return img_frame

def showPic(img_name, frame, show):

    if show:
        cv2.imshow(img_name, frame)
        key = cv2.waitKey(0)
        if key == ord("q") or key == 27:
            cv2.destroyAllWindows()
            show = False
        else:
            pass

    return show

def savePic(img_name, frame):

    draw_pics = os.path.join(os.getcwd(), "Draw_Pics")
    if not os.path.isdir(draw_pics):
        os.system("mkdir {} ".format(draw_pics))
    imgbase = os.path.basename(img_name)
    cv2.imwrite(os.path.join(draw_pics, imgbase), frame)

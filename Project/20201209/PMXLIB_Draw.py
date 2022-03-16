import os, xml.dom.minidom, sys, argparse, cv2
import matplotlib.pyplot as plt 
import numpy as np
from scipy.optimize import linear_sum_assignment
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from PMXLIB_Evaluation import  Isin, BBox, AIresults, LoadAItxt, Select_count



def video2imgs(video_name):    #convert video to photo
    if video_name.endswith("mp4"):
        cap = cv2.VideoCapture(video_name)
        count = 0 
        folder_path = video_name.strip(".mp4")
        if not os.path.isdir(folder_path):  
            os.mkdir(folder_path)
        while(True):
            ret,frame = cap.read()
            if ret:
                img_name = video_name.split("/")[-1].split(".mp4")[0]+ "_"+ str(count).zfill(5)+ ".jpg"#number of digit and output_file_type
                img_path = os.path.join(folder_path, img_name)
                print(img_path)
                cv2.imwrite(img_path, frame)
                cv2.waitKey(30)#number of pic per second
                count += 1    
            else:
                break
    cap.release()


def imgs2video(Imgs_dir, Save_name, Draw_mode, Vertex_lst, Save_pics, AILOG, Show, Shape=(1920, 1080)):

    fps = 30
    primax_label = []
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(Save_name, fourcc, fps, Shape)
    j = 0 

    for i in sorted(os.listdir(Imgs_dir)):
        img_name = os.path.join(Imgs_dir, i )
        frame = cv2.imread(img_name)
        if Draw_mode == None:
            cv2.line(frame, Vertex_lst[0], Vertex_lst[1], (255, 0, 0), 3)
            if Show == True:
                cv2.imshow(img_name, frame)
                key = cv2.waitKey(0)
                if key == ord("q"):
                    Show = False
                    cv2.destroyAllWindows()
                else:
                    pass
            if Save_pics == True:
                Draw_Pics = os.path.join(os.getcwd(), "Draw_Pics")
                if not os.path.isdir(Draw_Pics):
                    os.system("mkdir {} ".format(Draw_Pics))
                imgbase = os.path.basename(img_name)
                cv2.imwrite(os.path.join(Draw_Pics, imgbase), frame)
            print("====== frame : {} =======".format(i))
            video_writer.write(frame)
        else:
            num = 0
            for A in AILOG:
                if A.fname in img_name:
                    frame, label = draw(frame, A.boxes, num, Vertex_lst, primax_label)
                    if Show == True:
                        cv2.imshow(img_name, frame)
                        key = cv2.waitKey(0)
                        if key == ord("q"):
                            Show = False
                            cv2.destroyAllWindows()
                        else:
                            pass
                    if Save_pics == True:
                        Draw_Pics = os.path.join(os.getcwd(), "Draw_Pics")
                        if not os.path.isdir(Draw_Pics):
                            os.system("mkdir {} ".format(Draw_Pics))
                        imgbase = os.path.basename(img_name)
                        cv2.imwrite(os.path.join(Draw_Pics, imgbase), frame)
                    video_writer.write(frame)
                    print("====== frame : {} =======".format(i)) #default:num
                    num += 1
                    j += 1
                    cv2.destroyAllWindows()

    primax_count = Select_count(primax_label)
    print("[Bike, Vehicle, Person, Pet] = {}".format(primax_count))

def draw(img, log, frame, vertex_lst, label_lst):
    count = 0
    # draw line first
    if vertex_lst != [(0,0), (1920,0), (1920,1080), (0,1080), (0,0)]:
        cv2.line(img, vertex_lst[0], vertex_lst[1], (255, 0, 0), 3)
    # draw frame num
    #cv2.putText(img, "frame :{}".format(frame),(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    if log == None:
        return img 

    for l in log:
        # Count peple in every pic
        if l.type == 'Person':
            count += 1
        box = l.box
        color = (0, 128, 0) #KP change color

        label = box[0]
        label_lst.append(label)
        cv2.rectangle(img, (box[1], box[2]), (box[3], box[4]), color, 3)    # KP bounding box
        cv2.rectangle(img, (box[1] - 2, box[2] - 40), (box[3] + 2, box[2]), color, -1) # KP ID box                                                       
        cv2.putText(img, "{} ID:{}".format(box[0], box[6]), (box[1], box[2] - 12), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 1, cv2.LINE_AA)

        #print("gt:", box)
    # Draw a rectangle fill up green
    # Draw people count
    cv2.rectangle(img, (0, 0), (200, 40), color, thickness = -1)
    cv2.putText(img, "{}: {}".format('people', count), (5, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
    
    return img, label_lst

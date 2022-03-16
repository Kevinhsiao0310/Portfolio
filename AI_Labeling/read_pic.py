import os,sys
sys.path.append("/usr/lib")
import argparse
import random

def Find_Pics(path, JPG):

    name_list = []

    for dirPath, dirNames, fileNames in os.walk(path):
        for f in sorted(fileNames):
            if JPG == "ALL":
                if f.endswith(".jpg") or f.endswith(".xml"):
                    name_list.append(os.path.join(dirPath, f))
            elif JPG == "JPG":
                if f.endswith(".jpg"):
                    name_list.append(os.path.join(dirPath, f))
    return name_list


def Copy_Pics(pic_list, PATH, SPLIT_NUM, DEST):

    count = int(len(pic_list) // SPLIT_NUM)

    for idx, d in enumerate(pic_list):
        d_name = os.path.basename(d)
        if idx % count == 0:    
            folder = os.path.join(DEST, "slice_" + str(idx // count))
            if not os.path.isdir(folder):
                os.system("mkdir {} ".format(folder))
        print("copy {} -----> {} ".format(d_name, folder))
        os.system("cp {} {} ".format(d, folder))

def Move_Pics(pic_list, PATH, SPLIT_NUM, DEST):

    count = int(len(pic_list) // SPLIT_NUM)

    for idx, d in enumerate(pic_list):
        d_name = os.path.basename(d)
        if idx % count == 0:    
            folder = os.path.join(DEST, "slice_" + str(idx // count))
            if not os.path.isdir(folder):
                os.system("mkdir {} ".format(folder))
        print("move {} -----> {} ".format(p_name, folder))
        os.system("mv {} {} ".format(p, folder))

def Random_Pics(path):

    pic_list = []

    for dirPath, dirNames, fileNames in os.walk(path):
        for f in sorted(fileNames):
            if f.endswith(".jpg"):
                pic_list.append(os.path.join(dirPath, f))
    random.shuffle(pic_list)

    return pic_list
     
if __name__ == "__main__":

    print("Your File Path :")
    INPUT_PATH  = str(input())
    print("Your Destination Path :")
    DEST_C      = str(input())
    print("Data Mode : ----> ALL or JPG")
    DATA_MODE   = str(input())
    print("Split How Many Folder:")
    PICS_CUT    = int(input())-1
    print("Copy Or Move :")
    FILE_MODE   = str(input())
    print("Do You Want Random Shuffle ? --> Yes / No")
    RANDOM      = str(input())

    if RANDOM == "Yes" or "yes":
        print("===========Random Shuffle Pics===========")
        RANDOM_PICS = Random_Pics(INPUT_PATH)
        if FILE_MODE == "Copy" or "copy":
            Copy_Pics(RANDOM_PICS, INPUT_PATH, PICS_CUT, DEST_C)
        elif FILE_MODE == "Move" or "move":
            Move_Pics(RANDOM_PICS, INPUT_PATH, PICS_CUT, DEST_C)
    elif RANDOM == "No" or "no":
        ORG_PICS = Find_Pics(INPUT_PATH, DATA_MODE)
        if FILE_MODE == "Copy" or "copy":
            Copy_Pics(ORG_PICS, INPUT_PATH, PICS_CUT, DEST_C)
        elif FILE_MODE == "Move" or "move":
            Move_Pics(ORG_PICS, INPUT_PATH, PICS_CUT, DEST_C)

import os,sys, argparse
import numpy as np
from matplotlib import pyplot as plt

ONELOOP = []
VP      = []
ARM     = []
def Argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_path", type = str, help = "RAW_PATH")

    args = parser.parse_args()
    return args

def drawhist(oneloop_table,vp_table,arm_table):
    
    plt.subplot(2,1,1)
    n, bins, patches=plt.hist(oneloop_table)
    plt.xlabel("time(us)")
    plt.ylabel("Frequency")
    plt.title("Oneloop")
    plt.subplot(2,2,3)
    n, bins, patches=plt.hist(vp_table)
    plt.xlabel("time(us)")
    plt.ylabel("Frequency")
    plt.title("VP")
    plt.subplot(2,2,4)
    n, bins, patches=plt.hist(arm_table)
    plt.xlabel("time(us)")
    plt.ylabel("Frequency")
    plt.title("ARM")
    plt.show()

if __name__== '__main__':
    args = Argparse()
    RAW_PATH = args.raw_path
    with open(RAW_PATH, "r") as f:
        print("Open: " + RAW_PATH.split("/")[-1] + " for counting One loop time" )
        for line in f:
            a = np.empty(shape=1)
            if "VP" in line:
                oneloop       = int(line.split(" ")[3])
                vp            = int(line.split(" ")[8])
                arm           = int(line.split(" ")[13])
                ONELOOP.append(oneloop)
                VP.append(vp)
                ARM.append(arm)
    oneloop_table = np.array(ONELOOP)
    vp_table      = np.array(VP)
    arm_table     = np.array(ARM)
    print("OneLoop time:",np.mean(oneloop_table, dtype = np.float32),"us")
    print("VP time:",np.mean(vp_table, dtype = np.float32),"us")
    print("ARM time:",np.mean(arm_table, dtype = np.float32),"us")
    
    #drawhist(oneloop_table,vp_table,arm_table) #if u want to draw histgram,u can open this.
    
    f.close()

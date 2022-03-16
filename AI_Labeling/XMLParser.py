import os, xml.dom.minidom, sys, argparse
from tqdm import tqdm

# Add LIB_PATH for import
LIB_PATH = os.path.join(os.getcwd(), "..")
sys.path.append(LIB_PATH)

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from libs.PMXLIB_Evaluation import Isin, BBox, CreateDict, AIresults, LoadPics, LoadAItxt, CreateXML, GetAnnotBoxLoc, ReadXMLs, WriteXML, Checkload, CalIOU, Evaluation, PrintDiff, LocationCheck, CountLabels

COUNT_NAME = []
COUNT = []
SSD_W = 640
SSD_H = 360

GT_PATH  = None
XML_PATH = None
PIC_PATH = None
TXTFILE = "Big.txt"
COPY = None
BOX  = None

# raw data
START = "raw_data"
# collected
END   = "collected" 
#
TMP   = "tmp"

def Argparse():

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "-gt_path",  type=str, help="GT_PATH")
    parser.add_argument("-x", "-xml_path", type=str, help="XML_PATH")
    parser.add_argument("-pic", "-pic_path",  type=str, help="PIC_PATH")
    parser.add_argument("-copy", help="copy the pics you want.", action="store_true")

    args = parser.parse_args()
    return args

def BoxWidth(box):

    return abs(box.x2 - box.x1)

def CreateIndex(XML_PATH):
    
    index_xmls = []
    index_jpgs = []
    BOXindex = {}
    os.system("rm -rf {} && mkdir -p {}".format(TMP, TMP))

    for dirPath, dirNames, fileNames in tqdm(list(os.walk(XML_PATH))):
        for f in fileNames:
            ff = os.path.join(dirPath, f)
            if 'tmp' not in ff:
                ff = os.path.join(os.getcwd(), ff)
                if ff.endswith(".xml"):
                    #print("xml:", ff, f)
                    index_xmls.append(ff)
                    key = str(len(index_xmls)-1) + ".jpg"
                    BOXindex[key] = None
                    os.system("ln -s {} {}".format(ff, os.path.join(TMP, str(len(index_xmls)-1) + ".xml")))
                else:
                    #print("jpg:", ff, f)
                    index_jpgs.append(ff)
                    os.system("ln -s {} {}".format(ff, os.path.join(TMP, str(len(index_jpgs)-1) + ".jpg")))
    return index_xmls, index_jpgs, BOXindex

def RunBoxes(LOG, index_xmls=None, index_jpgs=None):
    
    big_count = 0
    big_pic_count = 0
    for key, value in tqdm(sorted(LOG.items(), key = lambda x : x[0])):
        if len(value.boxes) > 0:
    # for L in tqdm(LOG):
            big = False
            count = 0
            if XML_PATH :
                num = int(os.path.splitext(os.path.basename(value.fname))[0])
            for box in value.boxes:
                if box.type == "Person":
                    count += 1
                    if GT_PATH:
                        if BoxWidth(box) >= 1920 * 0.5:
                            big = True
                            big_count += 1
                    else:
                        if BoxWidth(box) >= value.shape[0] * 0.5:
                            big = True
                            big_count += 1
            if count >= 5 and big:
                # write pics names which has big bbox
                big_pic_count += 1
                f = open(TXTFILE, 'a')
                f.write(value.fname)
                f.write('\n')
                f.close()

                if COPY and index_jpgs and index_xmls:

                    xml_fullname = index_xmls[num]
                    jpg_fullname = index_jpgs[num]
                    xml_dir = os.path.split(xml_fullname)[0].replace(START, END)
                    jpg_dir = os.path.split(jpg_fullname)[0].replace(START, END)

                    if not os.path.isdir(xml_dir):
                        os.system("mkdir -p {}".format(xml_dir))
                    os.system("cp {} {}".format(xml_fullname, xml_fullname.replace(START, END)))

                    if not os.path.isdir(jpg_dir):
                        os.system("mkdir -p {}".format(jpg_dir))
                    os.system("cp {} {}".format(jpg_fullname, jpg_fullname.replace(START, END)))

                    #os.system("cp {} {}".format(os.path.join(START, L.fname), END))
                    #os.system("cp {} {}".format(os.path.join(START, L.fname.replace('.xml', '.jpg')), END))

    print("{} oversized bboxes in {} pics.".format(big_count, big_pic_count))

if __name__== '__main__':

    ## Preliminary Work
    args = Argparse()
    COPY = args.copy
    GT_PATH  = args.g
    XML_PATH = args.x
    PIC_PATH = args.pic

    if os.path.isfile(TXTFILE):
        os.system("rm {}".format(TXTFILE))

    if GT_PATH and XML_PATH:
        print("Don't give 2 sources. 1 source at once!")
        exit()

    ## for a txt files:
    elif GT_PATH:
        print('Read LOG')
        ALLPIC_SSD, AILIST_SSD = CreateDict(PIC_PATH, GT_PATH)
        BOX = LoadAItxt('ssd', None, [1920, 1080], ALLPIC_SSD, AILIST_SSD)
        RunBoxes(BOX)
        #exit()
    ## for a xml-folder:
    elif XML_PATH:
        print('Read XML')
        index_xmls, index_jpgs, ALLPIC_SSD = CreateIndex(XML_PATH)
        BOX = ReadXMLs(TMP, ALLPIC_SSD)
        RunBoxes(BOX, index_xmls, index_jpgs)

    if BOX is not None:
        LABEL, LABEL_COUNT = CountLabels(BOX)
        print(LABEL, "->", LABEL_COUNT)
    else:
        print("Run Error -> BOX is None.")


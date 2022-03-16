import os, xml.dom.minidom, sys, argparse, cv2
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from tqdm import tqdm
from scipy.optimize import linear_sum_assignment
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


# for voc2007
# COCO_PED  = ['person', 'pedestrian']
# COCO_CAR  = ['car', 'bus', 'vehicle']
# COCO_PET  = ['cat', 'dog', 'pet']
# COCO_BIKE = ['bicycle', 'motorbike', 'bike']

COCO_PED  = ['person', 'pedestrian']
COCO_CAR  = ['car', 'bus', 'train', 'truck', 'vehicle']
COCO_PET  = ['cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'pet']
COCO_BIKE = ['bicycle', 'motorbike', 'bike']

COCO_NAMES   = [COCO_BIKE, COCO_CAR, COCO_PED, COCO_PET]

LOWER_PRIMAX_NAMES = ["bike", "vehicle", "pedestrian", "pet"] 
PRIMAX_NAMES = ["Bike", "Vehicle", "Person", "Pet"]
PRIMAX_THRESHOLD = [0.2, 0.2, 0.2, 0.2]
PRIMAX_COUNT = [0, 0, 0, 0]
IOU_THRESHOLD = 0.3

class Isin:
    def __init__(self):
        self.poi = []
        self.vertex_lst = []
        self.isin = 0


    def isinpolygon(point, vertex_lst:list, contain_boundary=True):#i要不要大寫
        #檢測點是否位於區域外接矩形內
        lngaxis, lataxis = zip(*vertex_lst)
        minlng, maxlng = min(lngaxis), max(lngaxis)
        minlat, maxlat = min(lataxis), max(lataxis)
        lng, lat = point
        if contain_boundary:
            isin = (minlng <= lng <= maxlng) & (minlat <= lat <= maxlat)
        else:
            isin = (minlng < lng < maxlng) & (minlat < lat < maxlat)
        return isin

    def isintersect(poi, spoi, epoi):
        #輸入：判斷點，邊起點，邊終點，都是[lng,lat]格式數組
        #射線為向東的緯線
        #可能存在的bug，當區域橫跨本初子午線或180度經線的時候可能有問題
        lng, lat = poi
        slng, slat = spoi
        elng, elat = epoi
        if poi == spoi:
            #print("在頂點上")
            return None
        if slat == elat: #排除與射線平行、重合，線段首尾端點重合的情況
            return False
        if slat > lat and elat > lat: #線段在射線上邊
            return False
        if slat < lat and elat < lat: #線段在射線下邊
            return False
        if slat == lat and elat > lat: #交點為下端點，對應spoint
            return False
        if elat == lat and slat > lat: #交點為下端點，對應epoint
            return False
        if slng < lng and elat < lat: #線段在射線左邊
            return False
        #求交點
        xseg = elng - (elng - slng) * (elat - lat) / (elat - slat)
        if xseg == lng:
            #print("點在多邊形的邊上")
            return None
        if xseg < lng: #交點在射線起點的左側
            return False

        return True  #排除上述情況之后

    def isin_multipolygon(poi, vertex_lst, contain_boundary=True): 
        # 判斷是否在外包矩形內，如果不在，直接返回false    
        if not Isin.isinpolygon(poi, vertex_lst, contain_boundary):
            return False
        sinsc = 0        
        for spoi, epoi in zip(vertex_lst[:-1], vertex_lst[1::]):
            intersect = Isin.isintersect(poi, spoi, epoi)
            if intersect is None:
                return (False, True)[contain_boundary]
            elif intersect:
                sinsc += 1          

        return sinsc%2 == 1

def locationCheck(X, Y, vertex_lst):

    poi = [X, Y]
    img_isin = Isin.isin_multipolygon(poi, vertex_lst, contain_boundary=True)

    return img_isin 


class BBox:
    def __init__(self):
        self.type = None
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.conf = 0.0
        self.box = None
        self.checked = 0  # for P/R calculation
        self.mode = None
        self.ID = None

    def fillbbox(self, classname, conf, x1, y1, x2, y2, ID):  #, width, height):    # maybe is useless
        classname_tmp = None

        if classname not in PRIMAX_NAMES:
            for idN, N in enumerate(COCO_NAMES):
                if classname in N:
                    if float(conf) >= PRIMAX_THRESHOLD[idN]:
                        classname_tmp = PRIMAX_NAMES[idN]
        else:
            for idN, N in enumerate(PRIMAX_NAMES):
               if classname == N:
                    if float(conf) >= PRIMAX_THRESHOLD[idN]:
                        classname_tmp = classname

        if classname not in PRIMAX_NAMES:
            classname = None
            
        self.type = classname_tmp
        self.x1 = round(float(x1), 5)
        self.y1 = round(float(y1), 5)
        self.x2 = round(float(x2), 5)
        self.y2 = round(float(y2), 5)
        self.conf = float(conf)
        self.ID = ID
        self.box = [classname_tmp, self.x1, self.y1, self.x2, self.y2, self.conf, self.ID]

        return self.box
class AIresults:

    def __init__(self):
        self.fname = None
        self.boxes = []
        self.exist = 0
        self.shape = []
        self.ratio = True  # "real"

    def fillAIresults(self, BBox):
        self.boxes.append(BBox)

    def initAI(self, path, shape):
        self.fname = path
        self.shape = shape

    def transformBox(self):
        if self.boxes != []:
            self.boxes = [self.transform(BBox) for BBox in self.boxes]
            self.ratio = not (self.ratio)

    def transform(self, BBox):
        box = BBox.box
        # ratio2real
        if self.ratio:
            BBox.x1 = box[1] = int(box[1] * self.shape[1])
            BBox.y1 = box[2] = int(box[2] * self.shape[0])
            BBox.x2 = box[3] = int(box[3] * self.shape[1])
            BBox.y2 = box[4] = int(box[4] * self.shape[0])
        # real2ratio
        else:
            BBox.x1 = box[1] = float(box[1] / self.shape[1])
            BBox.y1 = box[2] = float(box[2] / self.shape[0])
            BBox.x2 = box[3] = float(box[3] / self.shape[1])
            BBox.y2 = box[4] = float(box[4] / self.shape[0])

        return BBox

def loadPics(pic_path):

    if os.path.isdir(pic_path):
        for p in sorted(os.listdir(pic_path)):
            print("Pic:", p)
    else:
        print("Wrong path!")

def createDict(pic_path, log_path):

    if os.path.isfile(log_path):
        print("Load log from {}.".format(log_path))
    else:
        print("Wrong log file: {}!".format(log_path))
        exit()

    if os.path.isdir(pic_path):
        print("Load pics from {}.".format(pic_path))
    else:
        print("Wrong pic path: {}!".format(pic_path))
        exit()

    BOXindex = {picname: None for picname in sorted(os.listdir(pic_path))}
    picnamelist = sorted(list(BOXindex.keys()))
    AILOG = []

    fp = open(log_path, "r")
    lines = sorted(fp.readlines())
    #The index used for searching in KEYS list.
    head = 0
    #The index when log under specific picname first time be read.
    start = 0
    #The index when log under specific picname last time be read.
    end = 0

    for idx, line in enumerate(lines):
        a_log = line.strip('\n').split(",")
        picname = a_log[0]#a_log名字可以再想
        
        if picname not in picnamelist:
            start = idx + 1

        while picname in picnamelist and (picname != picnamelist[head] and head < len(picnamelist) - 1):
            head += 1
            start = idx

        if (picname == picnamelist[head]):
            end = idx
            BOXindex[picnamelist[head]] = [start, end]
            
        AILOG.append(a_log)

    fp.close()

    return BOXindex, AILOG

def loadAItxt(model, pic_path, resolution, pic_dict, AI_list): 

    print("\n======== loadAItxt from {} ========\n".format(model))

    AI_dict = pic_dict.copy()  # AI_dict


    for key, value in tqdm(sorted(AI_dict.items(), key=lambda x: x[0])):
        boxes = []
        imgbox = AIresults()

        if not resolution:
            img = cv2.imread(os.path.join(pic_path, key))
            shape = img.shape
        else:
            shape = (resolution[1], resolution[0], 3)

        imgbox.initAI(key, shape)

        if value is not None:
            head = value[0]
            end  = value[1]

            while(head < (end + 1)):
                box = BBox()
                if head < len(AI_list):
                    split = AI_list[head]

                    if model == "yolo":
                        classname = split[1].strip(' ')
                        ID = None
                    elif model == "ssd":
                        classname = PRIMAX_NAMES[int(split[1]) - 1]
                        ID = split[7]

                    box.fillbbox(classname, split[6], split[2], split[3], split[4], split[5], ID) # , shape[1], shape[0])
                    boxes.append(box)
                    head += 1
                else:
                    break

        imgbox.boxes = boxes
        AI_dict[key] = imgbox

    return AI_dict


def transformDict(log_dict):

    print("\n======== transformDict ========\n")

    for key, value in log_dict.items():
        value.transformBox()
        log_dict[key] = value

    return log_dict


def createaXML(xml_path, filename, boxes, pic_path, picwidth, picheight, mode = 'default'):

    if not pic_path:
        pic_path = 'Pics'
    doc = xml.dom.minidom.Document()
    root = doc.createElement('annotation')
    doc.appendChild(root)
    
    folderElem = doc.createElement("folder")    # foldername"Pics"
    folderElem.appendChild(doc.createTextNode(pic_path))
    root.appendChild(folderElem)
    
    filenameElem = doc.createElement('filename')
    filenameElem.appendChild(doc.createTextNode(filename))
    root.appendChild(filenameElem)
    
    path = doc.createElement('path')
    path.appendChild(doc.createTextNode(filename))
    root.appendChild(path)
    
    src = doc.createElement('source')
    db = doc.createElement('database')
    db.appendChild(doc.createTextNode('Unknown'))
    src.appendChild(db)
    root.appendChild(src)
    
    size = doc.createElement('size')
    width = doc.createElement('width')
    height = doc.createElement('height')
    depth = doc.createElement('depth')
    
    width.appendChild(doc.createTextNode(str(picwidth)))
    height.appendChild(doc.createTextNode(str(picheight)))
    depth.appendChild(doc.createTextNode(str(3)))
    size.appendChild(width);size.appendChild(height);size.appendChild(depth);
    root.appendChild(size)
    
    seg = doc.createElement('segmented')
    seg.appendChild(doc.createTextNode('0'))
    root.appendChild(seg)
    
    for b in boxes:#loop for boxes
        classname = None
        if b.type is not None and b.box[0] is not None:
            if mode == 'rewrite':                    
                if b.type not in LOWER_PRIMAX_NAMES and b.type not in PRIMAX_NAMES:
                    print('Please check {} class name'.format(filename))
                    exit()
                elif b.type in PRIMAX_NAMES:
                    classname = LOWER_PRIMAX_NAMES[PRIMAX_NAMES.index(b.type)]
                    
            else:        
                if b.type not in PRIMAX_NAMES:
                    for idN, N in enumerate(COCO_NAMES):      
                        if b.type in N:
                            classname = PRIMAX_NAMES[idN]
                else:
                    classname = b.type
            obj = doc.createElement('object')
            name = doc.createElement('name')
            name.appendChild(doc.createTextNode(classname))
            pose = doc.createElement('pose')
            pose.appendChild(doc.createTextNode('Unspecified'))
            truncated = doc.createElement('truncated')
            truncated.appendChild(doc.createTextNode('0'))
            difficult = doc.createElement('difficult')
            difficult.appendChild(doc.createTextNode('0'))
            obj.appendChild(name);obj.appendChild(pose);obj.appendChild(truncated);obj.appendChild(difficult);
            root.appendChild(obj)
        
            xmin = doc.createElement('xmin')
            if not b.x1 < 0:
                xmin.appendChild(doc.createTextNode(str(int(b.x1))))
            else:
                xmin.appendChild(doc.createTextNode(str(0)))

            ymin = doc.createElement('ymin')
            if not b.y1 < 0:
                ymin.appendChild(doc.createTextNode(str(int(b.y1))))
            else:
                ymin.appendChild(doc.createTextNode(str(0)))

            xmax = doc.createElement('xmax')
            if not b.x2 > picwidth:
                xmax.appendChild(doc.createTextNode(str(int(b.x2))))
            else:
                xmax.appendChild(doc.createTextNode(str(picwidth)))

            ymax = doc.createElement('ymax')
            if not b.y2 > picheight:
                ymax.appendChild(doc.createTextNode(str(int(b.y2))))
            else:
               ymax.appendChild(doc.createTextNode(str(picheight)))

            bndbox = doc.createElement('bndbox')
            bndbox.appendChild(xmin);bndbox.appendChild(ymin);bndbox.appendChild(xmax);bndbox.appendChild(ymax);
            obj.appendChild(bndbox)
   
        
    f = open(os.path.join(xml_path, filename.split("/")[-1].replace("jpg", "xml")), 'w+');
    doc.writexml(f, indent='\t', addindent='\t', newl= '\n')
    f.close()
     
def writeXMLs(AI_dict, xml_path, pic_path):
    	
    GT_path = os.path.join(os.getcwd(),"..","GT")
    print("WriteXML to {}".format(GT_path))

    for key, value in sorted(AI_dict.items(), key = lambda x : x[0]):
        if value.boxes is None: continue
        if len(value.boxes) > 0:
            createaXML(xml_path, value.fname, value.boxes, pic_path, value.shape[1], value.shape[0])

def GetAnnotBoxLoc(AnotPath):             #AnotPath VOC標註文件路徑#anotpath

    tree = ET.ElementTree(file=AnotPath)  #打開文件，解析成一棵樹型結構
    root = tree.getroot()                 #獲取樹型結構的根

    # Get resolution part
    ObjectSize = root.findall('size') #objectsize
    for Object in ObjectSize:
        width  = int(Object.find('width').text)
        height = int(Object.find('height').text)
        depth  = int(Object.find('depth').text)
    ObjSizeSet = [height, width, depth]

    # Get bounding box parts
    ObjectSet = root.findall('object')    #找到文件中所有含有object關鍵字的地方，這些地方含有標註目標
    ObjBndBoxSet = {}                     #以目標類別爲關鍵字，目標框爲值組成的字典結構
    for Object in ObjectSet:
        ObjName = Object.find('name').text
        BndBox  = Object.find('bndbox')
        x1 = int(BndBox.find('xmin').text)#-1 #-1是因爲程序是按0作爲起始位置的
        y1 = int(BndBox.find('ymin').text)#-1
        x2 = int(BndBox.find('xmax').text)#-1
        y2 = int(BndBox.find('ymax').text)#-1
        BndBoxLoc = [x1,y1,x2,y2]
        if ObjName in ObjBndBoxSet:
            ObjBndBoxSet[ObjName].append(BndBoxLoc) #如果字典結構中含有這個類別了，那麼這個目標框要追加到其值的末尾
        else:
            ObjBndBoxSet[ObjName] = [BndBoxLoc]     #如果字典結構中沒有這個類別，那麼這個目標框就直接賦值給其值吧

    return ObjBndBoxSet, ObjSizeSet


def readaXML(xml_name):

    boxes = []
    xmlbox = AIresults()

    if os.path.isfile(xml_name):
        ObjBndBoxSet, ObjSizeSet = GetAnnotBoxLoc(xml_name)
        xmlbox.initAI(xml_name, ObjSizeSet)


        for key1, value1 in ObjBndBoxSet.items():
            for v in value1:
                box = BBox()
                box.fillbbox(key1, 1, v[0]/ObjSizeSet[1], v[1]/ObjSizeSet[0], v[2]/ObjSizeSet[1], v[3]/ObjSizeSet[0], None)#, 1, 1)
                boxes.append(box)

        xmlbox.boxes = boxes

    else:
        print("{} is not exist".format(xml_name))
        exit()

    return xmlbox                

def readXMLs(xml_path, pic_dict):

    GT_dict = pic_dict.copy()
    xml_list = []

    if os.path.isdir(xml_path):
        print("\n======== Read xml files from {} ========\n".format(xml_path))
    else:
        print("No GT path!!")
        exit()

    xml_list = sorted(os.listdir(xml_path))

    for key, value in tqdm(sorted(GT_dict.items(), key=lambda x:x[0])):
        if key.replace('.jpg', '.xml') in xml_list:
            xmlname = os.path.join(xml_path, key.replace('.jpg', '.xml'))
            xmlbox = readaXML(xmlname)
        else:
            xmlbox = AIresults()

        GT_dict[key] = xmlbox

    return GT_dict

def checkLoad(AIboxes, GTboxes):

    if len(AIboxes) != len(GTboxes) :
        print ("Length check failed.")
        return 

    error = 0

    for idA, A in enumerate(AIboxes):
        if A.fname.split(".")[0] != GTboxes[idA].fname.split(".")[0]:
            print("Fname not match:{}".format(A.fname.split(".")[0],))
            error += 1
            for ida, a in enumerate(A.boxes):
                if not a.box[0:4] == GTboxes[idA].boxes[ida].box[0:4]:
                    print(a.box, "<---->", GTboxes[idA].boxes[ida].box)
                    error += 1

    if error == 0:
        print("matched")

def calIOU(AIbox, GTbox):

    if AIbox[0] != GTbox[0]:
       return 0

    if AIbox[0] == 'None' or GTbox[0] == 'None':
        return None


    ax1, ay1, ax2, ay2 = AIbox[1:5]
    gx1, gy1, gx2, gy2 = GTbox[1:5]
    
    AA = (ax2 - ax1) * (ay2 - ay1)
    AG = (gx2 - gx1) * (gy2 - gy1)

    Over_x1 = max(ax1, gx1) 
    Over_y1 = max(ay1, gy1) 
    Over_x2 = min(ax2, gx2) 
    Over_y2 = min(ay2, gy2) 

    Over_w = max(0, Over_x2 - Over_x1)
    Over_h = max(0, Over_y2 - Over_y1)

    A_Over = Over_w * Over_h

    iou = A_Over / (AA + AG - A_Over)

    return iou

def boxesPairing(AIbox, GTbox):


    TP = 0
    TPtable = [0, 0, 0, 0]
    iou_list = np.zeros((len(GTbox.boxes), len(AIbox.boxes)), dtype = np.float32)
    
    for idg, gt in enumerate(GTbox.boxes):    
        for ida, ai in enumerate(AIbox.boxes):
            iou = calIOU(gt.box, ai.box)
            iou_list[idg][ida] = 1-iou

    row_ind, col_ind = linear_sum_assignment(iou_list)

    for x in range(len(row_ind)):
        max_iou = 1-iou_list[row_ind[x], col_ind[x]]
        if max_iou >= IOU_THRESHOLD:
            TP += 1
            for i in range(len(PRIMAX_NAMES)):
                if GTbox.boxes[row_ind[x]].type == PRIMAX_NAMES[i] and AIbox.boxes[col_ind[x]].type == PRIMAX_NAMES[i]:
                    TPtable[i] += 1

    return TP, TPtable

def generateTable(AI_dict, GT_dict, _print):

    for key, value in sorted(GT_dict.items(), key=lambda x:x[0]):   # sorted with keys

        if value is None: continue

        GTtable = [0, 0, 0, 0]  # a table for a GT
        GT = value               # a object of a GT
        count = 0
        if GT.boxes is  None: continue
        if len(GT.boxes) > 0:   # if GT is available, is ready to compare wih AI
            
            AItable = [0, 0, 0, 0]   # a table for an AI
            AI = AI_dict[key]        # a object an AI

            
            if _print: print("GTname:", GT.fname)
            for g in GT.boxes:
                if _print: print(g.box)
                for i in range(len(PRIMAX_NAMES)):
                    if g.type == PRIMAX_NAMES[i]:
                        GTtable[i] += 1
                        count += 1

            if _print: print("AIname:", AI.fname)
            for a in AI.boxes:
                if _print: print(a.box)
                for i in range(len(PRIMAX_NAMES)):
                    if a.type == PRIMAX_NAMES[i]:
                        AItable[i] += 1
            # print([AI, GT, AITABLE, GTTABLE, count])
            yield [AI, GT, AItable, GTtable, count]   # return info while AI compare with GT

def evaluation(AIbox, GTbox, AItable, GTtable, count_AI): 

    perpictureAIsum = len(AIbox.boxes)
    perpictureGTsum = len(GTbox.boxes)  

    Aidx = AIbox.fname.split(".")[0]   # filename
    if Aidx in GTbox.fname:
        TP_seg, TPtable_seg = boxesPairing(AIbox, GTbox)
        # if you want to know Precision & Recall per Pic, you can do it here.
        # printEval(perpictureAIsum, perpictureGTsum, TP_seg, TPtable_seg, count_AI, AItable, GTtable)
	
        return perpictureAIsum, perpictureGTsum, TP_seg, TPtable_seg

def collectEvaluation(AIboxes, GTboxes, _print=0):

    AItables = [0, 0, 0, 0]
    GTtables = [0, 0, 0, 0]
    TPtables = [0, 0, 0, 0]
    count_AI = 0
    sum_AI = 0
    sum_GT = 0
    TP = 0

    print(" Create Table ")

    g = generateTable(AIboxes, GTboxes, _print)

    for BOX in g:                                       #AIBOX  #GTBOX  #AITABLE #GTTABLE #Count
        AI_seg, GT_seg, TP_seg, TPtable_seg = evaluation(BOX[0], BOX[1], BOX[2], BOX[3], BOX[4])

        AItables = [AItables[idx] + i for idx, i in enumerate(BOX[2])]
        GTtables = [GTtables[idx] + i for idx, i in enumerate(BOX[3])]
        count_AI += BOX[4]
        sum_AI += AI_seg
        sum_GT += GT_seg
        TP += TP_seg
        TPtables = [i+j for i, j in zip(TPtables, TPtable_seg)]

    printEval(sum_AI, sum_GT, TP, TPtables, count_AI, AItables, GTtables)

def printEval(sum_AI, sum_GT, TP, TPtables, count_AI, AItables, GTtables):

    print(" Count AI in GT:", count_AI)
    print("\n")
    print(" Precision: {}\n Recall: {}\n TP: {}\n TP_TABLE: {}".format(div(TP, sum_AI), div(TP, sum_GT), TP, TPtables))
    print(" AI_TABLE: {}\n GT_TABLE: {}\n sum_AI: {}\n sum_GT: {}".format(AItables, GTtables, sum_AI, sum_GT))
    print("\nRESULTS:")
    print("                  Precision     Recall")
    for i in range(len(PRIMAX_NAMES) -1):
        print("{:<10s}  ->    {:<8.2f}\t{:.2f}".format(PRIMAX_NAMES[i], div(TPtables[i], AItables[i]), div(TPtables[i], GTtables[i])))

def countLabels(AIboxes):

    COUNT = [0, 0, 0, 0]
    LABEL_COUNT = []

    COUNT = np.array(COUNT)

    for key, value in sorted(AIboxes.items(), key = lambda x : x[0]):
        label, LABEL_COUNT = countLabel(value)
        LABEL_COUNT = np.array(LABEL_COUNT)
        COUNT = np.sum([COUNT, LABEL_COUNT], axis = 0).tolist()

    return PRIMAX_NAMES, COUNT

def countLabel(AIbox):
    
    COUNT = [0, 0, 0, 0]

    for A in AIbox.boxes:
        COUNT[PRIMAX_NAMES.index(A.type)] += 1

    return PRIMAX_NAMES, COUNT

def div(a, b):
    if b == 0:
        return 0
    else:
        return a / b

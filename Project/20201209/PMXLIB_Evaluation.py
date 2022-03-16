import os, xml.dom.minidom, sys, argparse, cv2
import matplotlib.pyplot as plt 
import numpy as np
from scipy.optimize import linear_sum_assignment
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

COCO_PED  = ['person']
COCO_CAR  = ['car', 'bus', 'train', 'truck']
COCO_PET  = ['cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe']
COCO_BIKE = ['bicycle', 'motorbike', ]
COCO_NAMES   = [COCO_BIKE, COCO_CAR, COCO_PED, COCO_PET]

PRIMAX_NAMES = ["Bike", "Vehicle", "Person", "Pet"]
PRIMAX_THRESHOLD = [0.2, 0.2, 0.2, 0.2]
PRIMAX_COUNT = [0, 0, 0, 0]
IOU_THRESHOLD = 0.3

class Isin:
    def __init__(self):
        self.poi        = []
        self.vertex_lst = []
        self.isin       = 0
   
    def isinpolygon(point, vertex_lst:list, contain_boundary=True):
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
        lng, lat   = poi
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

class BBox:
    def __init__(self):
        self.type    = None
        self.x1      = 0
        self.y1      = 0
        self.x2      = 0
        self.y2      = 0
        self.conf    = 0.0
        self.box     = None
        self.checked = 0  # for P/R calculation
        self.mode    = None
        self.ID    = None
    
    def fillbbox(self, classname, conf, x1, y1, x2, y2, ID, width, height, model):    # maybe is useless
        w_scale = 1920 / width
        h_scale = 1080 / height
        self.mode = model
        
        if self.mode == "yolo":
            for idN, N in enumerate(COCO_NAMES):
                if classname in N:
                    classname = PRIMAX_NAMES[idN]
                    if float(conf) < PRIMAX_THRESHOLD[idN]:
                        classname = None

        elif self.mode == "ssd" or self.mode == "gt":
            for idN, N in enumerate(PRIMAX_NAMES):      
                if classname == N:
                    if float(conf) < PRIMAX_THRESHOLD[idN]:
                        classname = None
        if classname not in PRIMAX_NAMES:
            classname = None
        
        self.type = classname
        self.x1   = int(float(x1) * w_scale)
        self.y1   = int(float(y1) * h_scale)
        self.x2   = int(float(x2) * w_scale)
        self.y2   = int(float(y2) * h_scale)
        self.conf = float(conf)
        self.ID = ID
        self.box = [classname, self.x1, self.y1, self.x2, self.y2, self.conf, self.ID]
        return self.box

    def fillbboxfromxml(self, classname, conf, x1, y1, x2, y2, width, height, model):
        if model == "primax_gt":
            for idN, N in enumerate(PRIMAX_NAMES):      
                if classname == N:
                    if float(conf) < PRIMAX_THRESHOLD[idN]:
                        classname = None
            if classname not in PRIMAX_NAMES:   # assume that class name is already converted to Primax representation.
                classname = None

        self.type = classname
        self.x1   = int(x1)
        self.y1   = int(y1)
        self.x2   = int(x2) 
        self.y2   = int(y2) 
        self.conf = float(conf)
        self.box  = [classname, self.x1, self.y1, self.x2, self.y2, self.conf]

        return self.box

class AIresults:
    def __init__(self):
        self.fname = None
        self.boxes = []
        self.exist = 0
        self.shape = []

    def addPATH(self, path):
        self.fname = path

    def addSHAPE(self, shape):
        self.shape = shape

    def fillAIresults(self, BBox):
        self.boxes.append(BBox)

def LoadPics(pic_path):

    if os.path.isdir(pic_path):
        for p in sorted(os.listdir(pic_path)):
            print ("pic:", p)     
    else:
        print ("wrong path!")   

def LoadAItxt(log_path, model, width, height): 

    if model not in ['yolo', 'ssd']:
        print("wrong model format name: {}!".format(model))
        exit()

    LOGBOXES = []        

    if os.path.isfile(log_path):
        print(" Load LOG {} from {}".format(model, log_path))
        fp = open(log_path, "r")
        lines = sorted(fp.readlines())
        name = None
        lastname = None

        for line in lines:
            line = line.strip('\n')
            split = line.split(",")
            name = split[0]

            if name != lastname:
                imgbox = AIresults()
                imgbox.addPATH(name)
                LOGBOXES.append(imgbox)
            box = BBox()
            if model == "yolo":
                box.fillbbox(split[1], split[6] , split[2], split[3], split[4], split[5], None, width, height, model)
            elif model == "ssd":
                box.fillbbox(PRIMAX_NAMES[int(split[1]) - 1], split[6] , float(split[2]) * width, float(split[3]) * height, float(split[4]) * width, float(split[5]) * height, split[7], width, height, model)
            if ((box.type is not None) and (box.box is not None)):
                imgbox.fillAIresults(box)
                 
            lastname = name
        fp.close()

    else:
        print ("wrong log file!")
        exit()

    #Sorting
    for L in LOGBOXES:
        L.boxes = sorted(L.boxes, key = lambda s : s.type)


    return LOGBOXES

def LocationCheck(x, y, vertex_lst):

    poi = [x, y]
    img_isin = Isin.isin_multipolygon(poi, vertex_lst, contain_boundary=True)

    return img_isin 

def CreateXML(picpath, xmlpath, filename, boxes, picwidth, picheight):

    doc = xml.dom.minidom.Document()
    root = doc.createElement('annotation')
    doc.appendChild(root)
    
    folderElem = doc.createElement("folder")    # foldername            "Pics"
    folderElem.appendChild(doc.createTextNode(picpath))
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
  
    ##  loop for boxes
    for b in boxes:
        if b.type is not None and b.box[0] is not None:
            obj = doc.createElement('object')
            name = doc.createElement('name')
            name.appendChild(doc.createTextNode(b.type))
            pose = doc.createElement('pose')
            pose.appendChild(doc.createTextNode('Unspecified'))
            truncated = doc.createElement('truncated')
            truncated.appendChild(doc.createTextNode('0'))
            difficult = doc.createElement('difficult')
            difficult.appendChild(doc.createTextNode('0'))
            obj.appendChild(name);obj.appendChild(pose);obj.appendChild(truncated);obj.appendChild(difficult);
            root.appendChild(obj)
        
            xmin = doc.createElement('xmin')
            xmin.appendChild(doc.createTextNode(str(b.x1)))
            ymin = doc.createElement('ymin')
            ymin.appendChild(doc.createTextNode(str(b.y1)))
            xmax = doc.createElement('xmax')
            xmax.appendChild(doc.createTextNode(str(b.x2)))
            ymax = doc.createElement('ymax')
            ymax.appendChild(doc.createTextNode(str(b.y2)))
            bndbox = doc.createElement('bndbox')
            bndbox.appendChild(xmin);bndbox.appendChild(ymin);bndbox.appendChild(xmax);bndbox.appendChild(ymax);
            obj.appendChild(bndbox)
    f = open(os.path.join(xmlpath, filename.split("/")[-1].replace("jpg", "xml")), 'w+');
    doc.writexml(f, indent='\t', addindent='\t', newl= '\n')
    f.close()
     
def GetAnnotBoxLoc(AnotPath):             #AnotPath VOC標註文件路徑

    tree = ET.ElementTree(file=AnotPath)  #打開文件，解析成一棵樹型結構
    root = tree.getroot()                 #獲取樹型結構的根

    # Get resolution part
    ObjectSize = root.findall('size')
    for Object in ObjectSize:
        width  = int(Object.find('width').text)
        height = int(Object.find('height').text)
        depth  = int(Object.find('depth').text)
    ObjSizeSet = [width, height, depth]

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

def ReadXML(XML_PATH, model):

    XMLBOXES = []

    if os.path.isdir(XML_PATH):
        print(" Read xml files from {}".format(XML_PATH))
        for xml in sorted(os.listdir(XML_PATH)):
            if xml.endswith("xml"):
                xmlbox = AIresults()
                xmlbox.addPATH(xml)
                ObjBndBoxSet, ObjSizeSet = GetAnnotBoxLoc(os.path.join(XML_PATH, xml))
                xmlbox.addSHAPE(ObjSizeSet)
                XMLBOXES.append(xmlbox)
                for key, value in ObjBndBoxSet.items():
                    for v in value:
                        box = BBox()
                        box.fillbboxfromxml(key, 1, v[0], v[1], v[2], v[3], 1920, 1080, model)
                        if box.type is not None:
                            xmlbox.fillAIresults(box)

        #Sorting
        for X in XMLBOXES:
            X.boxes = sorted(X.boxes, key = lambda s : s.type)

    else:
        print("no GT PATH!!")
        exit()

    return XMLBOXES

def WriteXML(LOG, XML_PATH, PIC_PATH, width, height):
  
    print(" WriteXML to {}".format(XML_PATH))

    for L in LOG:
        CreateXML(PIC_PATH, XML_PATH, L.fname, L.boxes, width, height)

def Checkload(AIBOXES, GTBOXES):

    if len(AIBOXES) != len(GTBOXES) :
        print ("length check failed.")
        return 

    error = 0

    for idA, A in enumerate(AIBOXES):
        if A.fname.split(".")[0] != GTBOXES[idA].fname.split(".")[0]:
            print("FNAME not match:{}".format(A.fname.split(".")[0],))
            error += 1
            for ida, a in enumerate(A.boxes):
                if not a.box[0:4] == GTBOXES[idA].boxes[ida].box[0:4]:
                    print(a.box, "<---->", GTBOXES[idA].boxes[ida].box)
                    error += 1

    if error == 0:
        print("matched")

def CalIOU(AIbox, GTbox):
    if AIbox[0] != GTbox[0]:
       return 0
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

def BoxesPairing(A, G):

    tp = 0
    tptable = [0, 0, 0, 0]
    iou_list = np.zeros((len(G.boxes), len(A.boxes)), dtype = np.float32)
    
    for idg, g in enumerate(G.boxes):    
        for ida, a in enumerate(A.boxes):
            iou = CalIOU(g.box, a.box)
            iou_list[idg][ida] = iou

    row_ind, col_ind = linear_sum_assignment(iou_list, maximize = True)

    for x in range(len(row_ind)):
        Max_iou = iou_list[row_ind[x], col_ind[x]]
        if Max_iou >= IOU_THRESHOLD:
            tp += 1
            for i in range(len(PRIMAX_NAMES)):
                if G.boxes[row_ind[x]].type == PRIMAX_NAMES[i] and A.boxes[col_ind[x]].type == PRIMAX_NAMES[i]:
                    tptable[i] += 1
    return tp, tptable

def Evaluation(AIBOXES, GTBOXES, AITABLE, GTTABLE): 

    tp = 0
    sum_AI = 0
    sum_GT = 0
    tptable = [0, 0, 0, 0] 

    for G in GTBOXES:
        sum_GT += len(G.boxes)    

    for A in AIBOXES:
        Aidx = A.fname.split(".")[0]   # filename
        for G in GTBOXES:
            if Aidx in G.fname:
                sum_AI += len(A.boxes)
                tp_seg, tptable_seg = BoxesPairing(A,G)
                tp += tp_seg
                tptable = [i+j for i, j in zip(tptable, tptable_seg)]

            continue

    print("\n")
    print(" Precision: {}\n Recall: {}\n TP: {}\n TP_table: {}".format(tp/sum_AI, tp/sum_GT, tp, tptable))
    print(" AITABLE: {}\n GTTABLE: {}\n sum_AI: {}\n sum_GT: {}".format(AITABLE, GTTABLE, sum_AI, sum_GT))
    print("\nRESULTS:")
    print("                  Precision     Recall")
    for i in range(len(PRIMAX_NAMES) -1):
        print("{:<10s}  ->    {:<8.2f}\t{:.2f}".format(PRIMAX_NAMES[i], tptable[i] / AITABLE[i], tptable[i] / GTTABLE[i]))

def PrintDiff(AIBOXES, GTBOXES, _print=0):

    print(" Create Table ")

    AITABLE = [0, 0, 0, 0]
    GTTABLE = [0, 0, 0, 0]
    count = 0

    for A in AIBOXES:
        Aidx = A.fname.split(".")[0]
        for G in GTBOXES:
            if Aidx in G.fname:
                for a in A.boxes:
                    if _print: print(a.box)
                    for i in range(len(PRIMAX_NAMES)):
                        if a.type == PRIMAX_NAMES[i]:
                            AITABLE[i] += 1
                break
                
    for G in GTBOXES:            
        for g in G.boxes:
            for i in range(len(PRIMAX_NAMES)):
                if g.type == PRIMAX_NAMES[i]:
                    GTTABLE[i] += 1
                    count += 1
    print(' Count AI in GT:', count)

    return AITABLE, GTTABLE

def Select_count(label_list):  # Select Pics Label Count

    Label_count = [0, 0, 0, 0]

    for l in label_list:
        Label_count[PRIMAX_NAMES.index(l)] += 1

    return Label_count

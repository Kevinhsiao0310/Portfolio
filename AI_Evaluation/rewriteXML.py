import os, xml.dom.minidom, sys, argparse
from tqdm import tqdm
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


# Add LIB_PATH for import,(if want to run per pic)
LIB_PATH_ALL = os.path.join(os.getcwd(), "..")
sys.path.append(LIB_PATH_ALL)

from libs.PMXLIB_Evaluation import  Isin, BBox, AIresults, loadAItxt, createaXML,\
                                    GetAnnotBoxLoc, readaXML


FOLDER_PATH = '/home/primax/Primax_AI_Doc/Datasets/raw_data/Primax/Guardian'

def Argparse():

    parser = argparse.ArgumentParser()
    parser.add_argument("-gt", "--gt_path", type=str, help="GT_PATH")

    args = parser.parse_args()

    return args

def findsize(filename):
    
    tree=ET.parse(filename)    
    roots = tree.getroot()
    for n in roots.findall('size'):
        width  = int(n.find('width').text)
        height = int(n.find('height').text)

    return width,height

if __name__== '__main__':

    args = Argparse()
    gt_path  = args.gt_path
    
    
    
    for root, dirs, files in tqdm(os.walk(gt_path),desc="Processing Bar: ", total=10, ncols=100):
        for xmlname in files:
            gt_dict  =  {xmlname: None}#Dict is used to store some information.
            filepath = os.path.join(root, xmlname)
            
            picwidth, picheight = findsize(filepath)#For generate size.    
            gtvalue = readaXML(filepath)
            gtvalue.rescaleBox()
            
            # generate path
            pic_path = filepath.replace("Annotations","JPEGImages")
            pic_path = pic_path[pic_path.index("JPEGImages"):pic_path.index(('/'+xmlname))]
            pic_path = os.path.join(FOLDER_PATH,pic_path)

            picturename = xmlname.replace('.xml','.jpg')

            savepath = os.path.join('temp',filepath.rstrip(xmlname))
            
            
            for key, value in sorted(gt_dict.items(), key=lambda x:x[0]):
                gt_dict[key] = gtvalue #Dict appends information.
                if not os.path.isdir(savepath):
                    os.system('mkdir -p {}'.format(savepath))
                createaXML(savepath, picturename, gt_dict[key].boxes, pic_path, picwidth, picheight, mode = 'rewrite')

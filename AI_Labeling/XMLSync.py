import os, sys, argparse
from tqdm import tqdm

# Annotation List
TXT_PATH = None
# Patch 
PATCH_PATH = None
# Storage for Downloading
RAW_PATH = None


def Argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("txt_path", type=str, help="train_*****.txt")
    parser.add_argument("-u", dest="upload_patch", help="{source path} for uploading patches.")
    parser.add_argument("-d", dest="download_from_raw", help="{storage path} for downloading from raw annotation.")
    args = parser.parse_args()
    return args

def CopyR(xmlp, xmln, jpgp, jpgn, RAW_PATH):

    xmls = xmlp.split("/")
    jpgs = jpgp.split("/")

    xmls = xmls[xmls.index("Annotations"):-1]
    jpgs = jpgs[jpgs.index("JPEGImages"):-1]

    xmldir = RAW_PATH[:]
    jpgdir = RAW_PATH[:]

    for i in range(len(xmls)):
        xmldir = os.path.join(xmldir, xmls[i])
        jpgdir = os.path.join(jpgdir, jpgs[i])

    if not os.path.isdir(xmldir):
        os.system("mkdir -p {}".format(xmldir))
    os.system("cp {} {}".format(xmlp, os.path.join(xmldir, xmln)))

    if not os.path.isdir(jpgdir):
        os.system("mkdir -p {}".format(jpgdir))
    os.system("cp {} {}".format(jpgp, os.path.join(jpgdir, jpgn)))

def CopyP(xmlp, xmln, PATCH_PATH):

    xmls = xmlp.split("/")
    xmls = xmls[xmls.index("Annotations"):-1]

    xmldir = PATCH_PATH[:]
    for i in range(len(xmls)):
        xmldir = os.path.join(xmldir, xmls[i])
    if os.path.isfile(os.path.join(xmldir, xmln)):
        os.system("cp {} {}".format(os.path.join(xmldir, xmln), xmlp))

def ReadFile(logname):

    f = open(logname, "r")
    lines = sorted(f.readlines())

    for l in tqdm(lines):
        split = l.strip("\n").split(" ")
        jpg_path = split[0]
        jpg_name = jpg_path.split("/")[-1]
        xml_path = split[1]
        xml_name = xml_path.split("/")[-1] 

        if PATCH_PATH:
            ## upload from one Folder.
            #os.system("cp {} {}".format(os.path.join(PATCH_PATH, xml_name), xml_path))
            ## upload from Folder recursively.
            CopyP(xml_path, xml_name, PATCH_PATH) 

        elif RAW_PATH:
            ## download to one Folder.
            #os.system("cp {} {}".format(xml_path, RAW_PATH))
            #os.system("cp {} {}".format(jpg_path, RAW_PATH))
            ## download to Folder recursively.
            CopyR(xml_path, xml_name, jpg_path, jpg_name, RAW_PATH)
        else:
            print('Please Check What You Want To Do')
            exit()

if __name__== '__main__':

    ## preliminary Work
    args = Argparse()
    TXT_PATH = args.txt_path
    RAW_PATH = args.download_from_raw
    PATCH_PATH = args.upload_patch
   
    if TXT_PATH is None:
        print("Plz give me a annotation list.")
        exit()
    else:
        if not TXT_PATH.endswith('txt'):
            print('TXT_PATH:{} is not a valid txt file.'.format(TXT_PATH))
            exit()

        if PATCH_PATH is None and RAW_PATH is None:
            print("Upload and Dowload dir are both None.")
            exit()

        elif RAW_PATH is not None:
            print("Download annotations and pics to {}.".format(RAW_PATH))
        elif PATCH_PATH is not None:
            print("Upload Patch from {}.".format(PATCH_PATH))

    if RAW_PATH is not None and not os.path.isdir(RAW_PATH):
        print("create dir -> {}".format(RAW_PATH))
        os.system("mkdir {}".format(RAW_PATH)) 

    ## main function
    ReadFile(args.txt_path)       

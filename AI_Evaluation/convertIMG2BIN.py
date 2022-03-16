import os,sys
import math
from collections import Counter
from tqdm import tqdm

if len(sys.argv)<2:
    raise ValueError("FOLDER_PATH is required. \ntry: python convertIMG2BIN.py ../example/pics/20201104-part2")

FOLDER_PATH = sys.argv[1]
if not os.path.isdir(FOLDER_PATH):
    raise NotADirectoryError("{} is not a directory".format(FOLDER_PATH))

WIDTH = int(input("Input Width:"))
HEIGHT = int(input("Input Height:"))
VERSION = str(input("SDK Version:"))

if VERSION not in ["2.5", "3.0"]:
    raise ValueError("SDK version must be 2.5 or 3.0")

FOLDER_PATH = os.path.join(os.getcwd(), FOLDER_PATH)
LABEL_PATH = os.path.join(FOLDER_PATH, "LabelImagework")
AMBA_PATH = os.path.join(FOLDER_PATH, "AMBA")
AMBA_PIC_PATH = os.path.join(AMBA_PATH, "Pics")
AMBA_BIN_PATH = os.path.join(AMBA_PATH, "Bins")

img_dir_list = []
bin_list = []

def convert_bin(path):
    for dirPath, dirNames, fileNames in os.walk(path):
        if str(dirPath) != str(LABEL_PATH):
            for d in sorted(dirNames):
                if "dra_pic" in d:
                    d_path = os.path.join(dirPath, d)
                    dra_bin_path = os.path.join(AMBA_BIN_PATH, "dra_bin{}".format(d.strip("dra_pic")))
                    list_path = dra_bin_path.replace("dra_bin0", "list")
                    os.system("mkdir -p {}".format(dra_bin_path))
                    print("=============================================")
                    print("{}  -----> {}".format(d,dra_bin_path))
                    print("=============================================")

                    if list_path.endswith("list"):
                        img_dra_list = os.path.join(list_path, "img_dra_list.txt")
                        dra_list = os.path.join(list_path, "dra_list.txt")
                        os.system("mkdir -p {}".format(list_path))
                        os.system("touch {}".format(img_dra_list))
                        os.system("touch {}".format(dra_list))
                   # os.system("gen_image_list.py -f {} -o {} -ns -e jpg -c 0 -d 0,0 -r {},{} -bf {} -bo {}".format(d_path, img_dra_list, HEIGHT, WIDTH, dra_bin_path, dra_list))       
                    if VERSION == "3.0" and d.strip("dra_pic") != "0":
                        dra_bin0_path = os.path.join(AMBA_BIN_PATH, "dra_bin0")
                        dra_pic0_path = os.path.join(AMBA_PIC_PATH, "dra_pic0")
                        print("\n======= move {} to {}=====\n".format(dra_bin_path, dra_bin0_path))

                        os.system("mv {}/* {}/".format(dra_bin_path, dra_bin0_path))
                        os.system("rm -d {}".format(dra_bin_path))

                        os.system("mv {}/* {}/".format(d_path, dra_pic0_path))
                        os.system("rm -d {}".format(d_path))


def check_bin(path):
    print("=============================================")
    print("              Check File Num                 ")
    print("=============================================")
    for dirPath, dirNames, fileNames in os.walk(AMBA_BIN_PATH):
        for b in sorted(dirNames):
            if b.startswith("dra_bin"):
                bin_path = os.path.join(dirPath, b)
                bin_list.append(bin_path)
    for b in bin_list:
        print("{} : ".format(b),len([name for name in os.listdir(b) if os.path.isfile(os.path.join(b, name))]))
   
    for dirPath, dirNames, fileNames in os.walk(path):
        for d in sorted(dirNames):
            if d.startswith("slice_"):
                img_dir_path = os.path.join(dirPath, d)
                img_dir_list.append(img_dir_path)
    for i in img_dir_list:
        print("{} : ".format(i),len([name for name in os.listdir(i) if os.path.isfile(os.path.join(i, name))]))

def run_script(path, version):
    print("=============================================")
    print("              Generate Script                ")
    print("=============================================")
    a = input("Yes(1)/No(0):")
    if a == "1":
        script = open("".join(["Run_bins.sh"]), "w+")
        script.write("rmmod ambarella_fb;modprobe ambarella_fb resolution={}x{} mode=clut8bpp buffernum=4 \n".format(WIDTH, HEIGHT))
        script.write("modprobe cavalry;cavalry_load -f /lib/firmware/cavalry.bin -r \n")
        for b in bin_list:
            bin_title = b.split("/")[-1]
            txtname = b.split("/")[-2].split("_")[0]
            script_content = findScriptbyVersion(VERSION, bin_title, txtname)
            script.write(script_content)
        script.close()
        os.system("mv Run_bins.sh {}".format(AMBA_BIN_PATH))
    else:
        print("bye bye")

def findScriptbyVersion(version, bin_title, txtname):

    if version == "2.5":
        script_content = "test_ssd -b $1 -t 1000 --in data=./{} --width {} --height {} --out mbox_loc --out mbox_conf_flatten  --class 5 --background_id 0 --top_k 200 --nms_top_k 400 --nms_threshold 0.25 --pri_threshold 0.2 --priorbox $2 -d >> {}.txt".format(bin_title, WIDTH, HEIGHT , txtname)+"\n"+"echo '{} finished'".format(bin_title)+"\n"

    if version == "3.0":
        script_content = "test_ssd -b $1 --in data --out_loc mbox_loc --out_conf mbox_conf_flatten --width {} --height {} --class_num 5 --background_id 0 --top_k 200 --nms_top_k 400 --nms_threshold 0.25 --pri_threshold 0.2 --priorbox $2 --input_dir ./dra_bin0 --output_dir . -d >> {}.txt".format(WIDTH, HEIGHT, txtname)+"\n"+"echo '{} finished'".format(bin_title)+"\n"

    return script_content

def process_pics(path,version, slice_):
    
    if not os.path.isdir(LABEL_PATH):
        os.system("mkdir {}".format(LABEL_PATH))
    if not os.path.isdir(AMBA_PATH):
        os.system("mkdir {} && mkdir {}".format(AMBA_PATH,AMBA_PIC_PATH))
    
    pathiter = tqdm(os.listdir(path))

    for p in pathiter:#p is a picname.
        
        if p.endswith('.jpg'):#check .jpg files into this loop.
            num = int(p.rstrip(".jpg").split("_")[-1])
            folder = os.path.join(LABEL_PATH, "slice_" + str(num % slice_))
            amba, amba_picname = findParametersbyVersion(VERSION, num, p)
        
            if not os.path.isdir(folder):#This part is about label work.
                os.system("mkdir {} ".format(folder))
            message = "move {} -----> {} ".format(p, os.path.basename(folder))
            pathiter.set_description(message)
            os.system("mv {} {} ".format(os.path.join(FOLDER_PATH,p), folder))

    
            if not os.path.isdir(amba):#This part is about AMBA.
                os.system("mkdir {} ".format(amba))
            message = "copy {} -----> {} ".format(p, os.path.basename(amba))
            pathiter.set_description(message)
            os.system("cp {} {} ".format(os.path.join(folder, p), os.path.join(amba, amba_picname)))

def findParametersbyVersion(version, num, picname):

    amba = os.path.join(AMBA_PIC_PATH, "dra_pic" + str(num // 1000))
    if version == "2.5":
        amba_picname = picname

    elif version == "3.0":
        amba_picname = "1x3x{}x{}_{}".format(HEIGHT, WIDTH, picname)

    return amba, amba_picname

if __name__ == "__main__":
    
    time_F = input("How much do you want to cut in LabelImagework? : ")
    time_F = int(time_F)
    process_pics(FOLDER_PATH,VERSION, time_F)       
    convert_bin(FOLDER_PATH)
    check_bin(FOLDER_PATH)
    run_script(FOLDER_PATH, VERSION)

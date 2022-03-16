import os,argparse
from os import listdir
from PIL import Image

def Argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("Pic_path1",type=str , help="input Pic_path1")
    parser.add_argument("Pic_path2",type=str , help="input Pic_path2")

    args = parser.parse_args()
    return args
 
def pinjie(pic_list, pic_name):
    # 获取当前文件夹中所有JPG图像
    im_list = pic_list
    im_list1 = [Image.open(im_list[0]), Image.open(im_list[1])]
    # 图片转化为相同的尺寸
    ims = []
    for i in im_list1:
        new_img = i.resize((1280, 1280), Image.BILINEAR)
        ims.append(new_img)
    # 单幅图像尺寸
    width, height = ims[0].size
    # 创建空白长图
    result = Image.new(ims[0].mode, (width, height * len(ims)))
    # 拼接图片
    for i, im in enumerate(ims):
        result.paste(im, box=(0, i * height))
    # 保存图片
    result.save(pic_name)
 
def find_jpg(path):
    name_list = []
    for dirPath, dirNames, fileNames in os.walk(path):
        for f in sorted(fileNames):
            if f.endswith(".jpg"):
                if "slice_" not in dirPath:#
                    name_list.append(os.path.join(dirPath, f)) 
    return name_list

if __name__ == '__main__':
    args = Argparse()
    name_list1 = find_jpg(args.Pic_path1)
    name_list2 = find_jpg(args.Pic_path2)
    for idx, x in enumerate(name_list1):
        for idy, y in enumerate(name_list2):
            if x.split('/')[-1].split('_')[-1] == y.split('/')[-1].split('_')[-1]:
                a = name_list1[idx]
                b = name_list2[idy]            
                im_list = [a, b]
                pic_name = a.split("/")[-1]
                pinjie(im_list, pic_name)
            else:
                continue

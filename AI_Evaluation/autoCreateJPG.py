import os

folderpath = os.path.join(os.getcwd(), "fakepics")
makefolder = "mkdir {}".format(folderpath)
os.system(makefolder) 

for i in range(0, 100):
    filenum  = str(i).zfill(5)
    filename = os.path.join(folderpath, filenum)
    outPut   = "touch {}.jpg".format(filename) 
    os.system(outPut)


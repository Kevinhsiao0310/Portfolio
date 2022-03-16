import os, sys, argparse


files = []

def Argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str, help="FILE_PATH")
    args = parser.parse_args()
    return args

def folder_size(path):
    for entry in os.scandir(path):
        byte = 0
        if entry.is_file():
            name = entry.path.split('/')[-1]
            byte = entry.stat().st_size
            n_byte = (name, byte)
            files.append(n_byte)
        elif entry.is_dir():
            dir_doc = folder_size(entry.path)
    return files

if __name__== '__main__':
    args = Argparse()
    FILE_PATH  = args.file_path
    FNAME = FILE_PATH.split('/')[-2]
    file = sys.stdout
    sys.stdout = open(FNAME + '.txt', 'w')
    doc = folder_size(FILE_PATH)
    for i in sorted(doc):
        print('{}'.format(i))
    sys.stdout.close()
    sys.stdout = file
import os,sys, argparse

Unlabel = []
RAW_PATH = None
LOG_NAME = None
TITLE    = None

def Argparse():

    example = (
        "Command Example: \n"
        "python convertSSDLogfromRaw_MergeVersion.py \n"
        "--raw_path ../example/logs/raw_log/SDK2.5/Bins2.5_ssd_v5.1.1_640x360_Data20211101-retrain3-145k.txt \n"
        "--save_name ../example/logs/20201104-part2_ssd_v5.1.1_640x360_Data20211101-retrain3-145k.txt \n"
        )
        

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, epilog=example)
    parser.add_argument("-raw", "--raw_path", type=str, help="RAW_PATH")
    parser.add_argument("--save_name", type=str, help="ssd_log_name")

    args = parser.parse_args()
    return args

def collectSSDlog(f):

    for line in f:
        if "File" in line:
            jpg = line.split("/")[-1].replace("bin", "jpg").rstrip(":\n")
        elif "Load raw file" in line:
            jpg = line.split('_')[-2]+'_'+line.split('_')[-1].replace('bin','jpg').rstrip("\n")
        
        if "(" in line:
            if "#" not in line and "Score" not in line:
                line = line.replace("\t", ", ")
                line = line.replace("(", "")
                line = line.replace(")", "")
                line = line.rstrip("\n")
                if len(line.split(",")[0]) == 1:
                    line = jpg + line[1:] + ","
                elif len(line.split(",")[0]) == 2:
                    line = jpg + line[2:] + ","
                Unlabel.append(line)
    
    return Unlabel


if __name__== '__main__':
    args = Argparse()
    RAW_PATH = args.raw_path
    LOG_NAME = args.save_name

    with open(RAW_PATH, "r") as f:
        print("Open: " + RAW_PATH.split("/")[-1] + " for writing SSD log" )
        Unlabel = collectSSDlog(f)

    with open(LOG_NAME, "w") as f:
        for u in Unlabel:
            f.write(u + " 1" + "\n")
    print("Write SSD log: " + LOG_NAME)

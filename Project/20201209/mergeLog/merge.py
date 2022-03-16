import cv2, numpy as np
from matplotlib import pyplot as plt


W = 1920
H = 1080

track = open("TrackingLOGS/20201104-part1_ssd_v5.1.1_640x360_20201024-145k.txt", "r+")
raw = open("LOGS/20201104-part1_ssd_v5.1.1_640x360_20201024-145k.txt", "r+")

final_write = open("track_20201104-part1_ssd_v5.1.1_640x360_20201024-145k.txt", "w+")

track_collect = []
raw_collect = []
merge_collect = []

def checkseg(str1 , str2, rate):   # str1 from raw, str2 from track
    print (str (int((float(str1) * rate))) , str2)
    print (str (int((float(str1) * rate))) == str2)

for f in raw.readlines():
    f_raw = f.strip("\n")
    split = f_raw.split(", ")
    raw_collect.append(split)

for f in track.readlines():
    f_track = f.strip("\n")
    split = f_track.split(", ") 
#    print(split)
    if split[0] == split[-1]:
        track_collect.append(split)

print("equal length ? {}".format(len(raw_collect) == len(track_collect)))
print(len(raw_collect), len(track_collect))

raw_collect.sort(key=lambda x: ( str(x[0]), - float(x[-2]), float(x[2])))
track_collect.sort(key=lambda x: ( int(x[0]), - float(x[-3]), float(x[2])))


for idr, r in enumerate(raw_collect):
    print(raw_collect[idr], track_collect[idr])
    raw_collect[idr][-1] = track_collect[idr][-2]
                
for r in raw_collect:
    for idrr, rr in enumerate(r):
        final_write.write(rr)
        if idrr < 7: final_write.write(", ")
    final_write.write("\n")     

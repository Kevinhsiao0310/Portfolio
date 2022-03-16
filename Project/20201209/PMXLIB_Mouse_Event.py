#!/usr/bin/python3
import os, sys, cv2, copy


class Mouse_event:
    def __init__(self):
        self.img = None
        self.DEFAULT = None
        self.node_lst = []
        self.vertex = []

    def Two_pointForm(self, ver_lst):
        k = (ver_lst[0][1] - ver_lst[1][1]) / (ver_lst[0][0] - ver_lst[1][0])
        xa = 0
        ya = k * (xa - ver_lst[1][0]) + ver_lst[1][1]
        xb = 1920
        yb = k * (xb - ver_lst[1][0]) + ver_lst[1][1]
        self.vertex = [[xa,ya], [xb,yb], [1920,1080], [0,1080], [0,0], [xa,ya]]

    def OnMouseAction(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print("Left Button Click")
            cv2.circle(self.img, (x,y), 5, (0,0,255), -1)
            self.node_lst.append([x,y])

    def OpenImg(self, pic_path):
        self.img = cv2.imread(pic_path)
        self.DEFAULT = copy.deepcopy(self.img)
        cv2.namedWindow('image') 
        cv2.setMouseCallback('image', self.OnMouseAction)
        while(1):    
            cv2.imshow('image', self.img)
            k = cv2.waitKey(1)
            if k == ord('q'):
                break
            if k == ord('c'):
                print("rewrite")
                self.img = copy.deepcopy(self.DEFAULT)
                self.node_lst.clear()
                continue
        cv2.destroyAllWindows()
        self.Two_pointForm(self.node_lst)
        return self.vertex
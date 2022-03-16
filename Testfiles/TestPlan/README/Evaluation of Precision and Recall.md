# Evaluation of Precision and Recall

### 1.介紹
evaluatePrecisionRecall.py是以libs/PMXLIB_Evaluation.py為Library的程式，其功能包含了寫XML及計算Precision & Recall。其中計算Precision & Recall包含了計算全畫面、畫線區域內兩種。

### 2.操作方式
#### 步驟1.
執行evaluatePricisionRecall.py時，輸入的指令由`(SSD_LOG) -> (YOLO_LOG) -> (GT_PATH) -> (Pic_PATH) -> (其他功能)` 所構成，可以用help (-h) 指令查詢。
```
python3 evaluatePrecisionRecall.py  --ssd_path {ssd_log .txt}  --yolo_path {yolo_log .txt} \
--gt_path {GT xml folder} –pic_path {image folder}  -res {resolution} --draw_line {Read or image path}
```

#### 步驟2.
執行程式所獲得的檔案（.txt）會被回存到資料夾當中。

### 3.Example
計算全畫面的Precision & Recall，假設此次需要進行計算的相關資料路徑如下，且照片解析度為預設的1920*1080。
>ssd_path: ../example/logs/20201104-part2_ssd_v5.1.1_640x360_Data20210420-retrain5b-160k.txt  
>yolo_path: ../example/logs/20201104-part2_yolo_608x608.txt  
>gt_path: ../example/GT/20201104-part2  
>pic_path: ../example/pics/20201104-part2 

#### 步驟1.
依據上方所提供的資料路徑執行evaluatePrecisionRecall.py，指令如下。若有需要自訂解析度，可輸入 -res指令。
```
python3 evaluatePrecisionRecall.py \
--ssd_path ../example/logs/20201104-part2_ssd_v5.1.1_640x360_Data20210420-retrain5b-160k.txt \
--yolo_path ../example/logs/20201104-part2_yolo_608x608.txt \
--gt_path ../example/GT/20201104-part2 \
--pic_path ../example/pics/20201104-part2 
```

#### 步驟2.
取得計算後的檔案（.txt）。

![運行結果](example/images/example_evaluatePrecisionRecall_2.png)

![運行結果](example/images/example_evaluationPrecisionRecall_8.png)

#### 狀況1：手動畫點計算畫線區域內的Precision & Recall
假如此次要以手動畫點的方式，完成對畫線區域內Precision & Recall的計算，相關資料路徑如下。
>ssd_path: ../example/logs/20201104-part2_ssd_v5.1.1_640x360_Data20210420-retrain5b-160k.txt  
>yolo_path: ../example/logs/20201104-part2_yolo_608x608.txt  
>gt_path: ../example/GT/20201104-part2  
>pic_path: ../example/pics/20201104-part2  
>sample pic path: ../example/pics/20201104-part2/20201104-part2_00000.jpg  

##### 步驟1.
執行evaluatePrecisionRecall.py，並開啟 -dl功能（輸入sample pic path）。
```
python3 evaluatePrecisionRecall.py \
--ssd_path ../example/logs/20201104-part2_ssd_v5.1.1_640x360_Data20210420-retrain5b-160k.txt \
--yolo_path ../example/logs/20201104-part2_yolo_608x608.txt \
--gt_path ../example/GT/20201104-part2 \
--pic_path ../example/pics/20201104-part2 \
--draw_line ../example/pics/20201104-part2/20201104-part2_00000.jpg  
```

##### 步驟2.
進入指定圖片後，需用滑鼠在照片上畫點形成區域。過程中若需重置視窗，可輸入 **C** 。完成後可輸入 **Q** 來關閉視窗。

![運行示意圖](example/images/example_evaluatePrecisionRecall_3.png)

##### 步驟3.
執行程式所獲得的檔案會存放到下方路徑中。

![運行結果](example/images/example_evaluatePrecisionRecall_4.png)

![運行結果](example/images/example_evaluatePrecisionRecall_5.png)

#### 狀況2：讀取座標計算畫線區域內的Precision & Recall
假如此次要以讀取座標的方式，完成對畫線區域內Precision & Recall的計算，相關資料路徑如下。
>ssd_path: ../example/logs/20201104-part2_ssd_v5.1.1_640x360_Data20210420-retrain5b-160k.txt  
>yolo_path: ../example/logs/20201104-part2_yolo_608x608.txt  
>gt_path: ../example/GT/20201104-part2  
>pic_path: ../example/pics/20201104-part2  

##### 步驟1.
執行evaluatePrecisionRecall.py，並開啟 -dl功能（輸入 read）。
```
python3 evaluatePrecisionRecall.py \
--ssd_path ../example/logs/20201104-part2_ssd_v5.1.1_640x360_Data20210420-retrain5b-160k.txt \
--yolo_path ../example/logs/20201104-part2_yolo_608x608.txt \
--gt_path ../example/GT/20201104-part2 \
--pic_path ../example/pics/20201104-part2 \
--draw_line read
```

##### 步驟2.
指令輸入後，會顯示已經被儲存的座標，此時僅需輸入前方編號即可繼續進行畫線工作。

![運行示意圖](example/images/example_evaluatePrecisionRecall_6.png)

##### 步驟3.
執行程式所獲得的檔案會存放到下方路徑中。

![運行結果](example/images/example_evaluatePrecisionRecall_4.png)

![運行結果](example/images/example_evaluatePrecisionRecall_7.png)

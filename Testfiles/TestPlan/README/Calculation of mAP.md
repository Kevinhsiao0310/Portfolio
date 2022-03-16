# Calculation of mAP

## A. mAP_processing.py

### 1. 介紹

mAP_processing.py 是一支對利用機器和不同model 所產生的ssd_log 或yolo_log 進行格式轉換的程式，目的是將其內容轉換為pascalvoc.py 所需的輸入項，將會存放於路徑下生成之GTLOG和AILOG資料夾中。  
若為Auto模式則會自動執行pascalvoc.py，不需修改到pascalvoc.py之參數。

### 2. 操作說明

#### 步驟1. 輸入所需之input

mAP_processing.py 進行格式轉換的輸入項包含：log_path_GT, log_path_AI 和pic_path 三者，執行的指令如下所示。  
若希望轉檔後，直接執行pascalvoc.py ，則可以執行auto 模式

```
python3 mAP_processing.py \
--gt_path {GT xml folder} --ai_path {ssd_log or yolo_log .txt} --pic_path {image folder} \
--auto
```

#### 步驟2. 取得轉檔後的檔案

mAP_processing.py 轉檔完成後，會將相同數量跟檔名的檔案分別以txt 的格式存放於GTLOG 和AILOG 兩個資料夾當中。

### 3. Example:
#### 狀況1:以一般模式完成對GT_log 和AI_log 的轉檔工作

假設執行mAP_processing.py 所需的檔案路徑如下所示，並且僅先取得轉檔後的檔案，沒有要同步執行pascalvoc.py 。

> gt_path: ../example/GT/20201104-part2  
> ai_path: ../example/logs/20201104-part2_ssd_v5.1.1_640x360_Data20210420-retrain5b-160k.txt  
> Pic path: ../example/pics/20201104-part2  

##### 步驟1. 輸入所需之input

操作指令如下所示。

```
python3 mAP_processing.py \
--gt_path ../example/GT/20201104-part2 \
--ai_path ../example/logs/20201104-part2_ssd_v5.1.1_640x360_Data20210420-retrain5b-160k.txt \
--pic_path ../example/pics/20201104-part2 
```

![運行示意圖](example/images/example_mAP_processing_1.png)

##### 步驟2. 取得轉檔後的GT_log 和AI_log 檔案

轉檔完成之檔案存放於GTLOG 和AILOG 兩個資料夾，可以看到兩個資料夾當中的檔案數量和檔名是相同的。

![運行示意圖](example/images/example_mAP_processing_2.png)

![運行示意圖](example/images/example_mAP_processing_3.png)

#### 狀況2:以auto 模式於完成轉檔的同時執行pascalvoc.py

##### 步驟1. 輸入所需之input

操作指令如下所示。

```
python3 mAP_processing.py \
--gt_path ../example/GT/20201104-part2 \
--ai_path ../example/logs/20201104-part2_ssd_v5.1.1_640x360_Data20210420-retrain5b-160k.txt \
--pic_path ../example/pics/20201104-part2 \
--auto
```

##### 步驟2. 取得轉檔成功的檔案和mAP 的計算結果

可看見在auto 模式下，mAP_processing.py 會直接執行計算mAP 的pascalvoc.py ，並取得紅框中的計算結果。關於pascalvoc.py 的用途與操作方式請參考下段的介紹。

![運行示意圖](example/images/example_mAP_processing_4.png)

## B. pascalvoc.py

### 1. 介紹

pascalvoc.py 是一支用於計算mAP之程式，取用自[rafaelpadilla 的github](https://github.com/rafaelpadilla/Object-Detection-Metrics.git "title")。若要了解mAP 的基礎概念，可點選[此處](https://chih-sheng-huang821.medium.com/深度學習系列-什麼是ap-map-aaf089920848 "title")。

### 2. 操作說明

pascalvoc.py 的主要輸入項包含轉檔完成後的GT_log 和AI_log ，以及對於計算mAP 有影響的Threshold 值，對於pascalvoc.py 運行的相關參數可以參考下圖。

![運行示意圖](example/images/example_pascalvoc_1.png)

#### 步驟1. 輸入相關參數

我們計算自機器所取得成果的mAP 時，Threshold 值固定為0.2 ，並採用不顯示圖片的方式，操作指令如下。

```
python pascalvoc.py -gt {轉檔完成之GT＿log path} -ai {轉檔完成之AI_log path} -t 0.2 -np
```

#### 步驟2. 取得mAP 的計算結果

計算mAP 所取得的各類別折線圖，會存放於results 資料夾當中，並依類別單張存取。


### 3. Example: 以pascalvoc.py 計算mAP

假設執行pascalvoc.py 所需的檔案路徑如下所示，且Threshold 值同樣為0.2 ，並同樣採用不顯示圖片的方式。

> 轉檔完成之GT_log path: ./GTLOG/  
> 轉檔完成之AI_log path: ./AILOG/  

#### 步驟1. 輸入相關參數

操作指令如下。

```
python pascalvoc.py -gt ./GTLOG/ -ai ./AILOG/ -t 0.2 -np
```

#### 步驟2. 取得mAP 的計算結果

![運行示意圖](example/images/example_pascalvoc_2.png)
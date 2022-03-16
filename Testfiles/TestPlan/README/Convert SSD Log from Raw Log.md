# Convert SSD Log from Raw Log

### 1.介紹
convertSSDLogfromRaw.py 是用來將SDK2.5和3.0版本的raw log 轉換成ssd_log 的程式。

### 2.操作方式
#### 步驟1.
執行 convertSSDLogfromRaw.py ，並依序輸入raw log path及ssd_log 檔案名稱。

ssd_log 檔案名稱的命名原則如下。
```
{videoname}_{model}_{版本號}_{解析度}_{model訓練釋出日}.txt。
```

操作指令如下。
```
python3 convertSSDLogfromRaw.py \
--raw_path {raw_log 檔案名稱} --save_name {ssd_log 儲存檔案名稱}  --version {version}
```

#### 步驟2.
於當前路徑取得轉出的ssd_log。

### 3.Example

#### 步驟1.
依據所提供的資料路徑執行convertSSDLogfromRaw，指令如下。

>raw log path: ../example/logs/raw_log/SDK2.5/Bins2.5_ssd_v5.1.1_640x360_Data20211101-retrain3-145k.txt  
>videoname: 20201104-part2  
>model: ssd  
>版本號: v5.1.1  
>解析度: 640x360  
>model訓練釋出日: Data20211101-retrain3-145k


```
python convertSSDLogfromRaw.py \
--raw_path ../example/logs/raw_log/SDK2.5/Bins2.5_ssd_v5.1.1_640x360_Data20211101-retrain3-145k.txt \
--save_name ../example/logs/20201104-part2_ssd_v5.1.1_640x360_Data20211101-retrain3-145k.txt \
--version 2.5 
```
![運行示意圖](example/images/example_convertSSDLogfromRaw_1.png)


>raw log path: ../example/logs/raw_log/SDK3.0/Bins3.0_ssd_v5.1.1_640x360_Data20211101-retrain4-155k.txt  
>videoname: 20201104-part2  
>model: ssd  
>版本號: v5.1.1  
>解析度: 640x360  
>model訓練釋出日: Data20211101-retrain4-155k 

```
python convertSSDLogfromRaw.py \
--raw_path ../example/logs/raw_log/SDK3.0/Bins3.0_ssd_v5.1.1_640x360_Data20211101-retrain4-155k.txt \
--save_name ../example/logs/20201104-part2_ssd_v5.1.1_640x360_Data20211101-retrain4-155k.txt \
--version 3.0
```
![運行示意圖](example/images/example_convertSSDLogfromRaw_3.png)

#### 步驟2.
取得轉出的ssd_log 。

![運行結果](example/images/example_convertSSDLogfromRaw_2.png)

![運行結果](example/images/example_convertSSDLogfromRaw_4.png)

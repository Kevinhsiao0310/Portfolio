# Convert images to bins



### 1.介紹

convertIMG2BIN.py是用於SDK2.5和3.0版本下，將照片按照我們設定好的格式去分配並轉成bin檔，為後續工作做準備的程式。

### 2.操作方式
#### 步驟1.
執行convertIMG2BIN.py，並輸入圖片位置。
```
python3 convertIMG2BIN.py {圖片位置資料夾}
```

#### 步驟2.
依序輸入解析度（640、360），SDK版本，以及要切分的資料夾數目。

#### 步驟3.
取得分配完成後的檔案及資料夾。

2.5版
+ 影片名稱資料夾
   + 影片名稱資料夾
        + LabelImagework
            + 依據輸入的切分資料夾數目分配到不同資料夾的圖片
        + AMBA
            + Pics
                + 以1000張為單位分配到不同資料夾的圖片
            + Bins
                + 以1000張為單位分配到不同資料夾的bin檔
                + list資料夾
                + Run_bins.sh
   + 影片 

3.0版
+ 影片名稱資料夾
   + 影片名稱資料夾
        + LabelImagework
            + 依據輸入的切分資料夾數目分配到不同資料夾的圖片
        + AMBA
            + Pics
                + 含有所有圖片的資料夾dra_pic0
            + Bins
                + 含有所有bin檔的資料夾dra_bin0
                + list資料夾
                + Run_bins.sh
   + 影片 

### 3.Example
#### 步驟1.
執行convertIMG2BIN.py。

```
python convertIMG2BIN.py ../example/pics/20201104-part2

```
![運行結果](example/images/example_convertIMG2BIN_1.png)

![運行結果](example/images/example_convertIMG2BIN_3.png)

#### 步驟2.
完成檔案分配，可見分配後的檔案路徑圖。

2.5版
![運行結果](example/images/example_convertIMG2BIN_2.png)
3.0版
![運行結果](example/images/example_convertIMG2BIN_4.png)

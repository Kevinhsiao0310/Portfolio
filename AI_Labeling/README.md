# AI Labeling

## A. read_pic.py
### 1.介紹
read_pic.py是一支可以將大量照片依據資料夾的切分數量，以複製或移動的方式將照片分入資料夾並存放到目的地路徑的程式。

### 2.操作方式
執行read_pic.py後，需要回覆以下五點資訊。
```
python3 read_pic.py
```
#### 輸入內容1.檔案來源位置
輸入需要切分入資料夾的大量照片所在位置。
>Your File Path:
#### 輸入內容2.目的資料夾位置
輸入照片分入資料夾後存放的目的地路徑。
>Your Destination Path:
#### 輸入內容3.檔案類型
檔案類型分為jpg+XML和jpg兩種，若選擇jpg+XML則輸入ALL，若選擇jpg則輸入JPG。
>Data Mode: ----> ALL or JPG
#### 輸入內容4.切分的資料夾數量
輸入需要切分的資料夾數值。需要注意的是，由於編號由0開始，因此若輸入數值為5，此時資料夾名稱分別為slice_0～slice_4。
>Split How Many Folder:
#### 輸入內容5.複製或移動
選擇是要採用複製或是移動的方式，複製的話輸入Copy，移動則輸入Move。
>Copy Or Move:
#### 輸入內容6.是否需要打亂順序
選擇是否隨機分入資料夾，是的話則輸入Yes。
>Do You Want Random Shuffle? --> Yes / No

### 3.Example
假設利用read_pic.py將下方來源路徑內的jpg+XML，以隨機分配的方式分入5個資料夾，並複製到目的地路徑中。
>File Path: ../pics/20201104-part2/  
>Destination Path: example/picsslice_example

#### 1.操作過程
![運行示意圖](AI_Labeling/example/images_example/readpic_example.PNG)

![運行示意圖](AI_Labeling/example/images_example/readpic_example2.png)

#### 2.操作結果
可於目的地路徑中，獲得已經分好的圖片資料夾。

![運行結果](AI_Labeling/example/images_example/readpic_example3.png)

## B. check_file.py
### 1.介紹
本地端電腦傳輸資料至Server端時，可能會有資料遺失的問題，因此可以使用check_file.py這支程式來確保兩邊資料相同。執行完這支程式會產生一個txt檔，產生之txt檔為檔案目錄資料夾名稱，裡面記錄了所給路徑下之檔案名以及檔案大小，之後將本地端和Server端產生之txt檔進行比對即可確保資料無遺失。

### 2.操作過程
#### 步驟1.
執行check_file.py，並輸入檔案目錄路徑。
```
python3 check_file.py "檔案目錄路徑"
```
#### 步驟2.
取得程式執行後產生的txt檔。
#### 步驟3.
將本地端產生之txt檔，和server端的txt檔進行比較，確認兩者之間是否相同。

### 3.Example
假設要比較下方路徑中的檔案和server端是否相同。
>../pics/20201104-part2/

#### 步驟1.
執行check_file.py。
```
python3 check_file.py ../pics/20201104-part2/
```
#### 步驟2.
取得程式執行後產生的txt檔，檔案名稱會與檔案目錄資料夾相同。

![運行示意圖](AI_Labeling/example/images_example/check_file_example2.PNG)

![運行示意圖](AI_Labeling/example/images_example/check_file_example3.png)
#### 步驟3.
將本地端產生的txt檔內容，和server端的txt檔進行比較。

![運行示意圖](AI_Labeling/example/images_example/check_file_example.PNG)


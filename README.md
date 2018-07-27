# Taipower Crawler說明文件
簡易的爬蟲程式把能源相關的資料有格式地爬下來，目前會爬下台灣電力工司和氣象資訊綠能虛擬營運中心的資料。

## Introduction
Crawler 總共分為5種類別：
1. YearCrawler:負責爬以`年`為單位的資料
2. DayCrawler:負責爬以`日`為單位的資料
3. DayAppendCrawl:負責爬以`日`為單位的資料，可是爬下的資料是一筆筆的，因此同時負責將爬下來的資料與已有資料合併
4. HourCrawler:負責爬以`小時`為單位的資料
5. MinuteCrawler:負責爬以`分鐘`為單位的資料

### 資料命名規則
爬下來的資料會以`當時時間`和`爬蟲類別`命名
例如：現在是`2018年7月4日 17:23`，利用DayCrawler爬下來的資料就會是`20180704.csv`，而MinuteCrawler爬下來的資料就會是`20180704-1720.csv`。
因為台電更新資料隔間是`每10鐘一次`。

### 資料與Crawler的對應關係
以下是資料與爬蟲程式會用到的相關參數:

|爬蟲資料 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|Path|Crawler Type|crawl() convert input function|Source Link|
|:---|---|---|---|---|
|今日電力資訊|`data/taipower/total`|DayAppendCrawler|format_usage_json()|https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadpara.txt|
|今日用電曲線(區域別)/用電量|`data/taipower/area/day_usage`|DayCrawler|None|https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadareas.csv|
|今日用電曲線(區域別)/用發電量|`data/taipower/area/gen_usage`|DayAppendCrawler|None|https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genloadareaperc.csv|
|今日用電曲線(能源別)|`data/taipower/fueltype`|DayCrawler|None|https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadfueltype.csv|
|今日備轉容量率|`data/taipower/reserve`|YearCrawler|None|https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/reserve.csv|
|各機組發電量|`data/taipower/genary`|MinuteCrawler|format_genary_json()|https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.txt|
|100m 風能發電量|`data/greenmet/wind/power_gen`|HourCrawler|None|http://greenmet.cwb.gov.tw/data/map_csv/Display/Range/Analysis/{time}/NOCWRF_03000_00_K01WEP_{time}_0000.csv|
|100m 風能密度|`data/greenmet/wind/density`|HourCrawler|None|http://greenmet.cwb.gov.tw/data/map_csv/Display/Range/Analysis/{time}/NOCWRF_03000_00_K01WED_{time}_0000.csv|
|100m 風速|`data/greenmet/wind/speed`|HourCrawler|None|http://greenmet.cwb.gov.tw/data/map_csv/Display/Range/Analysis/{time}/NOCWRF_03000_00_K01WSP_{time}_0000.csv|
|太陽能發電量|`data/greenmet/solar/power_gen`|HourCrawler|None|http://greenmet.cwb.gov.tw/data/map_csv/Display/Range/Analysis/{time}/HIMAW8_01000_00_B00SED_{time}_0000.csv|
|地表日射量|`data/greenmet/solar/radiation`|HourCrawler|None|http://greenmet.cwb.gov.tw/data/map_csv/Display/Range/Analysis/{time}/HIMAW8_01000_00_B00DIR_{time}_0000.csv|

PS.
* 在每個對應的路徑(Path)底下都會有更詳細的欄位說明
* time的格式為： `%Y%m%d%H`

資料來源：
* 台灣電力公司：https://www.taipower.com.tw/tc/page.aspx?mid=206
* 氣象資訊綠能虛擬營運中心：http://greenmet.cwb.gov.tw/monitor 

## Dependencies
* python3

## Usage
### Basic Usage
一般來說，只要每10分鐘執行一次`taipower_min.py`，每天的其中一個時間點執行`taipower_day.py`，每天的0、6、12、18時執行`greenmet_wind.py`，每天的0到11時和22-23時執行`greenmet_solar.py`，就可以把所有資料抓下來，因此可以使用排程程式去定時執行以上程式。
* taipower_min.py:負責把更新頻率為`分鐘`的台電資料爬下來（今日電力資訊、今日用電曲線、各機組發電量）
* taipower_day.py:負責把更新頻率為`天`的台電資料爬下來（今日備轉容量率）
* greenmet_wind.py:負責把`風能`相關的能源資料爬下來（100m 風能發電量、100m 風能密度、100m 風速）
* greenmet_solar.py:負責把`太陽能`相關的能源資料爬下來（太陽能發電量、地表日射量）

基本上在台電資料當中，`taipower_min.py`會負責抓取五種資料，剩下的`今日備轉容量率`資料會交由`taipower_day.py`負責，原因是資料的更新頻率不一致，所以要分開執行。

以下例子會教學怎樣定時排程執行這四個程式，將為以`crontab`為例：

1. 編輯`crontab`的內容
```
crontab -e
```
2. 輸入以下內容
```
*/10 * * * * python3 path/to/taipower_min.py
* 12 * * * python3 path/to/taipower_day.py
* 0,6,12,18 * * * python3 path/to/greenmed_wind.py
10 0-11,22,23 * * * python3 path/to/greenmed_solar.py
```
以上內容的意思是每10分鐘執行一次`taipower_min.py`，每天12點執行一次`taipower_day.py`，每天的0、6、12、18點執行一次`greenmed_wind.py`，每天的0到11和22到23點的10分執行一次`greenmed_solar.py`。

### Modify Contents
若需要更改網址內容或是下載路徑，或是要單獨抓取其中一款資料，可參考以下內容。

以下是`.py`內的程式碼

1.Import並生成所需要的crawler和function(以`今日電力資訊`為例)
```python
from crawler import DayAppendCrawler, format_usage_json
c = DayAppendCrawler(<url>,<path>)
```
`<url>`：為下載資料的連結，在上面的表格當中就是`Link`的意思
`<path>`： 把資料下載到的路徑

2. 利用 `try...except..` statment去執行Crawler的`crawl()` function，若要使用convert function就將function 作為`crawl()` 的 input。
```python
try:
    c.crawl(convert=format_usage_json)
except CrawFailException as e1:
    print(e1)
except DataMissingExcetion as e2:
    print(e2)
```
`crawl()` 有可能發生兩個Exception(下面另有說明)，使用者可以根據自己需求作處理。

## Exceptions
以下會說明Crawler執行`crawl()`時有可能發生的其中兩種意外：
### CrawFailException
程式會呼叫`os.system()`去執行`curl`把資料抓下來，若果基於任何原因而失敗的話，此意外將來被拋出。

#### 建議
如要處理這意外，可以寫一段小程式寄出一封email通知自己有意外情況發生。

### DataMissingException
程式抓回來的資料會被程式檢查，檢查有沒有抓對時間的資料或是抓完之後的筆數有沒有正確（詳見`crawler.py`中的`check()`），若果檢查沒通過程式就會拋出此意外。

以範本程式(`taipower_min.py`)為例，抓回來的資料會對比筆數，抓回來的筆數數量，和當時時間應該擁有幾筆資料作比較。
例子：假設要抓`今日用電曲線(區域別)/用電量`的資料，抓取時間為`2018年7月4日 17:23`，由於每10分鐘就有一筆新資料，那麼`./data/area/day_usage/` 中的 `20180704.csv` 應該要有`17*6 + int(23/10) + 1 = 105`筆資料，可是由於台電資料並不是準時更新，因此，程式抓下來的資料可能只有`104`筆，由於資料數量不對齊，所以此意外就會出現。

#### 注意
使用`DayAppendCrawler`的程式碼時，由於剛開始的時候只抓到一筆下來，除非是`00:00`執行程式，不然對那份資料來說，筆數會永遠對不上，因為之前的資料都錯過了，因此可以單純印出訊息代替，直到隔天`00:00`開始，資料才會開始對上。


#### 建議
用一個`while`無限迴圈不斷抓出這個意外，直到資料筆數正確為止，期間可以先設定等待時間，每隔多久再抓一次。


以下是範本中的程式碼：
```python
success_flag = False
while not success_flag:
    try:
        c.crawl()
        success_flag = True
    except DataMissingException:
        print('Waiting 1 minute for data upload...')
        time.sleep(60)
```

## Coding
如果要撰寫新的Crawler class，可以參考以下內容。

對應不同的情況下，已經寫好的Crawler class不一定會長久適用，因此為了應對這樣的情況，已經寫好Crawler class的template(abstract class)，只要繼承`AbsCrawler`這個class並implement當中abstract method就可以省略其他程式碼，要實作的方法有以下兩個：
1. `_set_filename(self)`: 要如何更改抓下來的檔案名稱，回傳`string`
2. `check(self)`: 怎樣檢查抓下來的資料，才算通過，回傳`True`/`False`

## Contacts
如有不懂歡迎寄信，Email: grandq33769@gmail.com (梁樂謙)

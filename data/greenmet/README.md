# 氣象資訊綠能虛擬營運中心
## 資料格式
* line 1: 橫向資料長度, 縱向資料長度, c, 起點經度(東經), 起點緯度(北緯), 終點經度(東經), 終點緯度(北緯), 資料型態, -999, -999, EPSG
* 起點與終點形成一個矩形
* 矩形會依據縱橫向資料長度平均切割，形成矩陣
* Line 4 為矩陣的起始，每個點的資料都會對應到矩陣上

## Remark
* Line 3 的意義不明，有待確認。

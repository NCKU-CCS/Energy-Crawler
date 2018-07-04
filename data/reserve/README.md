# 單年備轉容量 (reserve)
---
* 檔案命名格式：`%Y.csv`
* Crawler class: YearCrawler
* 合理爬蟲間隔：最少每`1天`一次

||日期|瞬時尖峰負載|備轉容量|備轉容量率|
|---|---|---|---|---|
|**Attribute Name**|Date|Peak_Load|Operating_Reserve|Oper_Reser_Rate|
|**Type**|date `month/day`|float|float|percentage `%`|

ps.單位：`萬瓩`

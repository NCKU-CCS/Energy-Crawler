# 單日各區用電 (area/day_usage)
---
* 檔案命名格式：`%Y%m%d.csv`
* Crawler class: DayCrawler
* 合理爬蟲間隔：最少在每天的`23:50-23:59`一次

||時間|東部用電量|南部用電量|中部用電量|北部用電量|
|---|---|---|---|---|---|
|**Attribute Name**|Time|Eastern|Southern|Central|Northern|
|**Type**|time `hr:min`|float|float|float|float|

ps.單位：`萬瓩`

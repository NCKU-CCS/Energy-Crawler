# 單日各區發用電量 (area/gen_usage)
---
* 檔案命名格式：`%Y%m%d.csv`
* Crawler class: DayAppendCrawler
* 合理爬蟲間隔：最少每`10分鐘`一次

||時間|北部發電量|北部用電量|中部發電量|中部用電量|南部發電量|南部用電量|東部發電量|東部用電量|
|---|---|---|---|---|---|---|---|---|---|
|**Attribute Name**|Time|Northern_Gen|Northern_Usage|Central_Gen|Central_Usage|Southern_Gen|Southern_Usage|Eastern_Gen|Eastern_Usage|
|**Type**|time `hr:min`|float|float|float|float|float|float|float|float|

ps.單位：`萬瓩`

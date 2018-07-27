# 單日各類別發電量 (fueltype)
---
* 檔案命名格式：`%Y%m%d.csv`
* Crawler class: DayCrawler
* 合理爬蟲間隔：最少在每天的`23:50-23:59`一次

||時間|核能|燃煤|汽車共生|民營電廠-燃煤|燃氣|民營電廠-燃氣|重油|輕油|水力|風力|太陽能|抽蓄發電|抽蓄負載|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Attribute Name**|Time|Nuclear|Coal|Co_Gen|IPP_Coal|LNG|IPP_LNG|Oil|Diesel|Hydro|Wind|Solar|Pumping_Gen|Pump_Load|
|**Type**|time     `hr:min`|float|float|float|float|float|float|float|float|float|float|float|float|float|

ps.單位：`萬瓩`

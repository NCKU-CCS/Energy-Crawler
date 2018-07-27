# 單日用電總量 (total)
* 檔案命名格式：`%Y%m%d.csv`
* Crawler class: DayAppendCrawler
* 合理爬蟲間隔：最少每`10分鐘`一次

||時間|目前用電量|預估最高用電|最大供電能力|
|---|---|---|---|---|
|**Attribute Name**|Time|Curr_Usage|Pred_Max_Usage|Max_Sup|
|**Type**|time `hr:min`|float|float|float|

ps.單位：`MW` 
若要轉換成`萬瓩`，請將數字 `/10`

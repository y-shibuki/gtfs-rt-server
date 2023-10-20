# GTFS_Realtimeのサーバー

直近1ヶ月間のRealtimeデータを表示

## crontabの設定

cronに以下の内容を追記しましょう。

```bash
*/2 * * * * bash $HOME/gtfs_rt_server/main.sh update_gtfs_rt;
```

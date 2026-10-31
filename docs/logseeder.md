# Sentinel LogSeeder：ASIMサンプル投入の検証

対象期間: 2026-10-21〜23 · 公開日: 2026-10-31 · 種別: 作業記録

## 目的と構成

解析・検知の確認に使うサンプルをLog Analyticsへ投入し、テーブル、DCR、取り込み権限、イベント時刻の関係を確認した。環境はWindows PowerShell 7 / WSL Ubuntu、検証用ワークスペース、DCE、ASIM用DCR。

対象は`ASimAuthenticationEventLogs`、`ASimNetworkSessionLogs`、`ASimDnsActivityLogs`。当時のレコードはそれぞれ89列・97列・75列の構成だった。全バージョンに共通する列数ではない。

## 結果とトラブル

| 事象 | 対応・結果の記録 |
|---|---|
| DNS用DCRの初回作成失敗 | 再作成後に成功 |
| IngestionのHTTPエラー | 再試行後に成功した記録あり |
| 権限整理 | DCRスコープのMonitoring Metrics Publisher等を確認 |
| レコードの確認 | DNSの時刻、EventType、EventResult等をPowerShellで表示 |

投入件数、バッチ成功率、取り込み遅延の分布はこの版に収録していない。HTTPで受理されたことと、テーブルに検索可能な行が現れたことは分けて確認する。

## 再確認の例

実行:

```kusto
ASimDnsActivityLogs
| where TimeGenerated > ago(1d)
| take 10
```

確認:

```kusto
ASimDnsActivityLogs
| where TimeGenerated > ago(1d)
| summarize Rows=count(), Latest=max(TimeGenerated)
```

これは確認例であり今回の実行結果ではない。サンプル時刻が古い場合は検索期間を調整する。

## 学び

ASIM合成ログで条件を確認できても、WAFやFirewallが実イベントを生成した証拠にはならない。機器側のイベント生成、診断設定、転送経路まで評価する場合は実イベントとの照合が必要。

当時付与したロールをそのまま最小権限の推奨セットとは扱わず、管理操作と継続的な投入の権限を分けて考える。

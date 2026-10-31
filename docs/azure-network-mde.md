# Azure Firewall・DNS Resolver・MDEの検証メモ

公開日: 2026-10-31 · 種別: 作業記録 / 一部計画

## Firewall：経路と拒否

サブネット間通信をAzure Firewallへ通す構成を作り、UDRとNetwork Ruleで通信制御を試した。複数のSKU・Policy構成を検討したため、すべてを同一構成の結果として扱わない。

| 項目 | 記録 | 未確定な点 |
|---|---|---|
| ルーティング | サブネットからFirewallへのUDRを構成 | 試行ごとの有効ルート表は未添付 |
| Network Rule | サブネットA→BのDenyを試行 | 全条件の網羅試験ではない |
| 診断ログ | Network / Application / NAT / Threat Intel等を確認対象にした | 各カテゴリの生ログは未収録 |
| User-Agentを使う試行 | Denyの確認記録 | IDPS起因かは署名ログとの突合が必要 |
| IDPS | 署名ログ・Flow Traceを評価対象として検討 | SKU・モード・署名ID付きの証跡は未収録 |

Denyが見えただけでIDPS検知成功と結論づけず、経路・Rule・Threat Intelligence・IDPSの処理を分ける。

## DNS Private Resolver：削除失敗

2026-10-29、Resolver本体の削除で`CannotDeleteResource`が発生。エラーにoutbound endpointの残存が示された。分かったのは、親を削除しようとした時点で子リソースがあったこと。

子endpointから親Resolverへ削除順を整理する。この資料では原因の理解までを記録し、削除完了を確認済みとは扱わない。

## MDE：Linux導入

Ubuntu検証端末3台にMDEを導入し、`mdatp health`を確認した作業記録がある。デバイスグループを使う運用も検討した。

実行:

```bash
mdatp health
```

確認:

```bash
systemctl status mdatp --no-pager
```

インストール済み端末の確認例であり、今回の環境では実行していない。サービス稼働・health確認は特定攻撃へのアラート生成を証明しない。SSH認証試行による検知評価は検討として残し、実行・検知済みの結果には含めない。

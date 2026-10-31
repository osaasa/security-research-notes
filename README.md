# Security Research Notes — AI・Cloud・SDR

**Author: osaasa · 初版公開: 2026-10-31 (JST)**

AIを使ったセキュリティ検証、Microsoft Sentinel / Azureの運用検証、SDR / RFの研究を整理した日本語の技術ノート集です。ツールを動かすだけでなく、結果をどう確認し、防御側のログと結びつけるかを重視しています。

ChatGPT / Codexを構成理解、コード・設定の検討、トラブルシューティング、文書化に活用しています。既存ツールの原著作者と、自分が行った環境構築・改修・検証を区別しています。

## 最初に読む2本

1. **[ARTEX：既存コードの改修とMCP検証](docs/artex-mcp-lab.md)** — Docker、Responses API対応、実行経路と証跡の扱い。
2. **[SDR / RF：GNSS・TEMPEST研究ノート](docs/sdr-rf-research.md)** — 所有機材、実験経験、評価設計、今後残す測定記録。

## 記事一覧

| 分野 | 記事 | 内容 |
|---|---|---|
| AI / MCP | [ARTEX](docs/artex-mcp-lab.md) | コード変更の確認、Docker / MCPの作業記録 |
| SOC / SOAR | [SentinelとLogic Appの再クエリ](docs/sentinel-replay.md) | 6キー方式、合成40件・5件の再取得、集合照合 |
| WAF | [Application Gateway / Front Door](docs/azure-waf.md) | HTTP応答、診断設定、クォータの切り分け |
| ログ基盤 | [Sentinel LogSeeder](docs/logseeder.md) | ASIMサンプル投入、DCR、権限、再試行 |
| Network / EDR | [Firewall・DNS・MDE](docs/azure-network-mde.md) | 経路・拒否・削除エラー・Linux導入確認 |
| SDR / RF | [GNSS・TEMPEST](docs/sdr-rf-research.md) | 研究テーマ、経験、再現可能な評価方法 |
| ローカルAI | [ローカルLLMとMCP Fetch](docs/local-llm.md) | 小型モデルの運用、ツール接続、性能評価の課題 |
| 負荷・検知評価 | [GoldenEye Lab](docs/goldeneye-lab.md) | 改修レビューと検知評価の指標 |

## 結果の読み方

| 表記 | 意味 |
|---|---|
| ソース確認 | ファイルやコミットを読んで実装の存在を確認。テスト実行成功とは別 |
| 検証資料の記録 | 保存された資料に結果がある。公開版には原本・生ログを添付していない |
| 作業記録 | 過去の操作・対話記録の整理。公開作業で再実行したものではない |
| 本人申告 | 経験の申告があるが、この版では測定ログを確認していない |
| 調査・計画 | 設計・評価方法。実装完了や成功を意味しない |
| 合成例 | 説明・追試のために今回用意したデータ。過去の実測値ではない |

Mockの完走、実HTTP応答、脆弱性の成立、SIEMの検知成功は、それぞれ別の結果として扱います。数値は確認できた資料の範囲で示し、未測定の値を補いません。

## 小さく追試する

[合成データ](examples/replay-fixture.json)と[照合スクリプト](examples/verify_replay.py)を使い、40件・5件の件数と集合を確認できます。ネットワーク接続やクラウド操作は行いません。

実行:

```bash
python3 examples/verify_replay.py examples/replay-fixture.json
```

期待する出力:

```text
A: 40 resources, exact set match
B: 5 resources, exact set match
PASS: groups are disjoint; synthetic fixture only
```

[KQLの合成例](examples/replay-function.kql)と[RF観測記録テンプレート](templates/rf-observation.md)も収録しています。

## 記録方針

- 元ツールの導入・構成変更・自作部分を分ける。
- 目的、実行、確認方法、失敗条件を残す。
- 実測・合成・Mockを区別する。
- 顧客情報、実接続先、クラウド識別子、認証情報を掲載しない。
- 第三者の書籍・ソース一式・生データを転載しない。

詳細は[証拠と編集方針](docs/evidence-policy.md)を参照してください。

## 次に取り組むこと

ARTEXの実行証跡とSentinelログを時系列で照合し、検知率・検知遅延・失敗原因を評価すること。SDRでは、RF条件と受信機の観測値をセットで記録し、測定報告として公開することです。いずれも今後の作業として位置づけています。

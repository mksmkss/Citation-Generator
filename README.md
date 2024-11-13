# Citation Generator Manual
バージョン 1.0.0

## 概要
Citation Generatorは、WebページのURLや手動入力から BibTeX形式と日本語の文献引用形式を生成するツールです。

## 主な機能
1. URLからの自動メタデータ取得
2. リアルタイムな引用形式の生成
3. BibTeX形式と日本語文献引用形式の同時生成
4. クリップボードへのコピー機能

## 使い方

### URLからの引用生成
1. 上部のURL入力フィールドにWebページのURLを入力
2. 「Fetch Metadata」ボタンをクリック
3. メタデータが自動的に各フィールドに入力され、引用が生成されます

### 手動での引用生成
以下のフィールドに直接入力することができます：
- Title（タイトル）: 文献のタイトル
- Author（著者）: 著者名
- Year（年）: 発行年
- URL Date（アクセス日）: Webページにアクセスした日付
- Note（注釈）: 追加情報

※入力すると自動的に引用が生成されます

### 出力形式

#### BibTeX形式
```bibtex
@misc{key2024,
    title = {タイトル},
    author = {著者},
    year = {2024},
    url = {URL},
    urldate = {2024/02/14},
    note = {Online; accessed 2024/02/14}
}
```

#### 日本語文献引用形式
```
著者『タイトル』,2024,URL, 2024/02/14閲覧.
```

### 便利な機能

#### コピー機能
- 「Copy BibTeX」: BibTeX形式の引用をクリップボードにコピー
- 「Copy Text」: 日本語文献引用形式をクリップボードにコピー

#### クリア機能
- 「Clear All」ボタン: すべての入力フィールドと出力をクリア

## 注意事項
1. URLからのメタデータ取得は、Webサイトの構造によって成功率が異なります
2. 取得したメタデータは手動で編集可能です
3. 入力フィールドの変更は即座に引用形式に反映されます

## エラー対応
- URLが無効な場合: エラーメッセージが表示されます
- メタデータ取得失敗時: 手動での入力が必要です
- 必須フィールドが空の場合: 引用は生成されません

## 推奨環境
- Python 3.7以上
- 必要なパッケージ:
  - customtkinter
  - requests
  - beautifulsoup4
  - pyperclip

## インストール方法
```bash
pip install customtkinter requests beautifulsoup4 pyperclip
```

## お願い
追加して欲しい機能やバグの報告は、[Issues](https://github.com/mksmkss/Citation-Generator/issues)にてお願いします。
たくさんのフィードバックをお待ちしております。

## 更新履歴
### Version 1.0.0
- 初回リリース
- 基本機能の実装
- リアルタイム生成機能の追加

## ライセンス
MIT License
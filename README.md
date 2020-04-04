# scrapbox2md
クリップボード上で，scrapbox記法の文章をmarkdownに変換する

---

### 使い方

1. クリップボードにscrapboxのテキストをコピーする
2. pythonスクリプト(python3)を実行する
3. 変換された文字列がクリップボードにコピーされるのでgithubの編集画面に貼り付ける

```py
python scrapbox.py
```

※ MacやLinuxの場合，PATHへの追加やunix実行ファイルの作成などにするとより便利に使うことができる

---

### 動作環境

**python**
- python3

**ライブラリ**
- re
- pyperclip

---

### 対応するscrapbox記法

- タイトル
  - 一行目を見出し1(h1)にする
- URLの変換
- 表の変換
- 画像の変換
  - gyazoのURLを利用して表示
- ソースコード記法の変換
  - インデントが深い場所にあるものは未対応
- 箇条書き
  - 深さ5のインデントまで対応
- 見出し，強調の変換
  - アスタリスクx1 ~ x7まで対応

`変換表`
| scrapbox | markdown |
|:---------|:---------|
| \[* text] | \*\*text\*\* |
| \[** text] | #### text |
| \[*** text] | ### text |
| \[**** text] | ## text |
| \[***** text] | # text |
| \[****** text] | # text |
| \[******* text] | # text |


### 対応していないscrapbox記法

- インデントが深い場所にあるソースコード
- アイコン
- リンク
- タグ

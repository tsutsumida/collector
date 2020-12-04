# collector
Twitterの推しアカウントの投稿した画像を収集するプログラム

## How to Use
1. Twitter アプリを作成し各種キーやトークンを取得する。詳細は<a href="https://developer.twitter.com/ja">こちら</a>や他の方法紹介ページを参照ください。
2. 取得したキーやトークンの値をconfig.iniに登録する。
3. set_search_accountメソッド中の_accountsに、好きなアカウントを追加する。（デフォルトは日本Twitterの公式アカウントが登録されている）
4. プログラムを実行する。

## 注意点
画像を取得できる範囲は対象アカウントの全ツイート分ではありません。

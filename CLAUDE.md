# 買取大吉 法隆寺店 オリジナルLP（horyuji.bng.co.jp）

運営：株式会社Bingo（代表 吉原 涼）。買取大吉のフランチャイズ店「法隆寺店」の自社サイト。
GitHub Pages で公開。main に push すると1〜2分で https://horyuji.bng.co.jp に反映される。

## 店舗情報（NAP。この表記で統一。「102号」は入れない）
- 店名：買取大吉 法隆寺店
- 住所：奈良県生駒郡斑鳩町興留5-1-35サンメゾン法隆寺
- 電話：06-7777-6590
- 営業：10:00〜19:00・年中無休・予約不要・無料駐車場（建物裏）・半個室
- LINE：https://line.me/ti/p/CZCmVd4SQf
- Googleマップ：https://maps.app.goo.gl/qmBYRcdpAQeCupgSA
- Instagram：https://www.instagram.com/daikichi_horyuji
- 古物商許可番号 第62106R070875号（大阪府公安委員会）／インボイス T2120001281633

## ファイル
- index.html：LP本体（1ファイル）
- google96fb46d6bf441024.html：Googleサーチコンソールの所有権確認ファイル。消さない
- img/：写真（.jpgと.webp。ページでは.webpを使う）
- blog/：店長ブログ（自動生成。直接編集しない）
- _tools/posts.py：ブログ記事のデータ。新しい記事は POSTS の先頭に追加
- _tools/build.py：`python3 _tools/build.py` でブログページ・一覧・LPの実績/ブログ欄・参考価格ページ（/price/）・sitemap.xml を作り直す
- _tools/cats.py：品目別ページ6つ（/gold/ /jewelry/ /brand/ /watch/ /ihin/ /stamp-coin/）の中身。実績は実際の記事slugだけを入れる
- index.html のA/Bテスト：FVの問いかけ文（.ab-a / .ab-b）。?ab=A / ?ab=B で確認。結果はGA4（GA_IDを入れたら）
- _tools/price_raw.tsv：参考価格100点（カテゴリ／品名／価格／本部画像パス）。本部サイトから取得

## ブログ記事の追加手順
1. 写真を img/ に保存（位置情報を消し、長辺1400pxに縮小、.jpgと.webpの両方）
2. _tools/posts.py の POSTS 先頭に dict(slug, cat, img, alt, title, desc, body) を追加
3. `python3 _tools/build.py` を実行
4. index.html の「お買取り実績・店長ブログ」欄（各6件）は build.py が自動で更新する（AUTO:LATEST の間は手で直さない）
5. commit して main に push

## 守ること
- 買取実績・口コミ・金額は、実際にあったものだけ。作り話は書かない
- お客さんの顔・名前・住所・本人確認書類が写った写真は使わない
- 「地域No.1」「最高額」など根拠のない表現は使わない
- 口コミは原文のまま、名前はイニシャル
- 片付け・不用品：値段がつく物は買取、処分は「提携の許可業者がお引き取り」と書く
- ロゴの形・色・文字は変えない
- 文体：50〜70代女性向けに、やさしく短い文で

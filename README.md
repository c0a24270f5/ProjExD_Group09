# 弾幕ゲーム

## 実行環境の必要条件
* python >= 3.10
* pygame >= 2.1

## ゲームの概要
* プレイヤー（飛行機）がBOSS（こうかとん）を倒す

## ゲームの遊び方
* 矢印キーで飛行機を操作し，スペースキーでビームを打ち出す

## ゲームの実装
### 共通基本機能
* 背景画像と主人公キャラクターの描画

### 分担追加機能
* BOSS（こうかとん）の表示と攻撃
* HP関連（味方）(担当:山口):左上にHPバーを表示、その下にHPの値を表示するクラス
* 背景画像を動かす
* プレイヤーの攻撃
* 味方側の敵の攻撃を消せる能力 
* ゲームオーバー、クリア画面

### ToDo
- 一目見てわかる関数名
- 授業の関数名を参考に
- コメントをつけてください
- 敵のHPに関するクラスの作成(内容は味方用とほぼ同じ)

### メモ
<<<<<<< HEAD
* gameoverとgameclearの関数の条件付けは敵の環境が出来次第
=======
* * ボスのHPは　boss.sprites()[0].hp　で取得
追加したクラス
check_inscreen(obj_rct: pg.Rect) -> tuple[bool, bool]
 オブジェクトが画面外かを判定し，真理値タプルを返す関数

calc_orientation(org,dst)
 orgから見てdstがどこにあるかを計算し方向ベクトルをタプルで返す

facing(self_rect, player_rect) 
 self_rectがplayer_rectの方向を向く角度を計算してangleを返す

Boss(pg.sprite.Sprite)
ボスに関するクラス

Bosscolor(pg.sprite.Sprite)
ボスの色を変えるクラス

Danmaku(pg.sprite.Sprite)
弾幕に関するクラス
>>>>>>> C0A24086/boss

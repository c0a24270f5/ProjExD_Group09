import math
import os
import random
import sys
import time
import pygame as pg


WIDTH = 1100  # ゲームウィンドウの幅
HEIGHT = 650  # ゲームウィンドウの高さ
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとんや爆弾，ビームなどのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


class Player(pg.sprite.Sprite):
    """
    ゲームキャラクターに関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
    }

    def __init__(self, xy: tuple[int, int]):
        """
        キャラクター画像Surfaceを生成する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 xy：こうかとん画像の位置座標タプル
        """
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/2091142.png"), 0, 0.9)
        self.image = pg.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.speed = 10
        self.hp = 3

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rect.move_ip(self.speed*sum_mv[0], self.speed*sum_mv[1])
        if check_bound(self.rect) != (True, True):
            self.rect.move_ip(-self.speed*sum_mv[0], -self.speed*sum_mv[1])
        screen.blit(self.image, self.rect)

class My_Life(pg.sprite.Sprite):
    """
    自機のHP表示に関するクラス
    """
    def __init__(self, player: Player):
        super().__init__()
        self.player = player  
        self.font = pg.font.Font(None, 40)
        self.image = pg.Surface((player.hp * 60, 20))
        pg.draw.rect(self.image, (0, 0, 255), (0, 0, player.hp * 60, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = (5, 5)


    def update(self):
        hp = self.player.hp
        bar_width = max(hp * 60, 1)
        bar_height = 20
        text_height = 25
        total_height = bar_height + text_height

        # 新しいSurfaceを作成（透明背景）
        self.image = pg.Surface((bar_width + 100, total_height), pg.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        # ライフバーを描画
        pg.draw.rect(self.image, (0, 0, 255), (0, 0, bar_width, bar_height))

        # HP数値を描画
        text = self.font.render(f"HP: {hp}", True, (255, 255, 255))
        self.image.blit(text, (0, bar_height))

        # rectも更新
        self.rect = self.image.get_rect()
        self.rect.topleft = (5, 5)



def main():
    pg.display.set_caption("真！こうかとん無双")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"fig/26466996.jpg")

    player = Player((900, 400))
    my_life = pg.sprite.Group()
    my_life_bar = My_Life(player)
    my_life.add(my_life_bar)


    tmr = 0
    clock = pg.time.Clock()
    while True:
        screen.blit(bg_img, [0,0])
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0

        player.update(key_lst, screen)

        my_life.update()
        my_life.draw(screen)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

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


class Boss(pg.sprite.Sprite):
    """
    ボスに関するクラス
    """
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(f"fig/3.png")
        self.rect = self.image.get_rect()
        self.rect.center = 1200,HEIGHT/2
        self.vx, self.vy = 0,0
        self.stop_xy =[900,HEIGHT/2]  # 停止位置を指定
        self.movestate = "moving"  #初期状態
        self.state,self.state_num = "move",0
        self.image = pg.transform.scale(self.image,(200,200))
        self.hp=1000
    def update(self):
        if self.state == "move" and self.movestate == "stop":#上下に動く
            self.vy+=0.05
            if self.state_num==0:
                self.rect.move_ip(0,self.vy)
            if self.state_num==1:
                self.rect.move_ip(0,-self.vy)
            if self.rect.centery < 150 and self.state_num == 1:
                self.state_num = 0
                self.vy=0
            if self.rect.centery > HEIGHT-150 and self.state_num == 0:
                self.state_num = 1
                self.vy=0
                
        if self.movestate != "stop": #停止位置まで移動
            self.vx+=0.4 #加速度
            self.vy+=0.4
            if self.rect.centerx < self.stop_xy[0]:
                self.rect.move_ip(self.vx,0)
                if self.rect.centerx > self.stop_xy[0]:
                    self.rect.centerx = self.stop_xy[0]
            if self.rect.centerx > self.stop_xy[0]:
                self.rect.move_ip(-self.vx,0)
                if self.rect.centerx < self.stop_xy[0]:
                    self.rect.centerx = self.stop_xy[0]
            if self.rect.centery < self.stop_xy[1]:
                self.rect.move_ip(0,self.vy)
                if self.rect.centery < self.stop_xy[1]:
                    self.rect.centery = self.stop_xy[1]
            if self.rect.centery > self.stop_xy[1]:
                self.rect.move_ip(0,-self.vy)
                if self.rect.centery < self.stop_xy[1]:
                    self.rect.centery = self.stop_xy[1]
            if self.rect.centerx == self.stop_xy[0] and self.rect.centery == self.stop_xy[1]:
                self.movestate = "stop"
                self.vx=0
                self.vy=0
            
def main():
    pg.display.set_caption("真！こうかとん無双")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"fig/26466996.jpg")

    player = Player((900, 400))
    boss = pg.sprite.Group()
    boss.add(Boss())#こうかとんを出現
    tmr = 0
    clock = pg.time.Clock()
     #----デバック用テキスト----
    fonto = pg.font.Font(None, 20)
    txt = fonto.render("test", False, (255, 255, 255))
    #------------------------
    while True:
        screen.blit(bg_img, [0,0])
         #----デバック用テキスト----
        if boss.sprites():
            txt = fonto.render(f"{boss.sprites()[0].rect,boss.sprites()[0].rect.center,boss.sprites()[0].movestate}", False, (255, 255, 255))

        screen.blit(txt, [0, 0])
        #------------------------
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
        boss.update()
        boss.draw(screen)
        player.update(key_lst, screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

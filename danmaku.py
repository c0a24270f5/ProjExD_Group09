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
        self.triple_beam_tmr = 0 #三方向ビームの時間
        self.fast_beam_tmr = 0 #ビームのクールタイムが短くなる時間
        self.shield_tmr = 0 #バリアの時間

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


class Beam(pg.sprite.Sprite):
    """
      機体が放つビームに関するクラス
    """
    def __init__(self, player:"Player", angle = 0):
        """
        ビーム画像Surfaceを生成する
        引数 player：ビームを放つ機体（Playerインスタンス）
        """
        self.img = pg.image.load(f"fig/beam.png")
        self.rct = self.img.get_rect()
        self.rct.centery = player.rect.centery
        self.rct.left = player.rect.right
        rad = math.radians(angle)
        self.vx = 5 * math.cos(rad)
        self.vy = 5 * math.sin(rad)

    def update(self, screen: pg.Surface):
        """
        ビームを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rct.move_ip(self.vx, self.vy)
        if check_bound(self.rct) == (True, True):
            screen.blit(self.img, self.rct)


class Item(pg.sprite.Sprite):
    """
    アイテムに関するクラス
    """
    imgs = [pg.image.load(f"fig/item{i}.png") for i in range(1, 4)]
    
    def __init__(self, spawn_frame: int):
        super().__init__()
        self.item_type = random.randint(1, 3)
        self.image = pg.transform.rotozoom(__class__.imgs[self.item_type-1], 0, 0.04)
        self.rect = self.image.get_rect()
        img_width = self.rect.width
        img_height = self.rect.height
        x = random.randint(img_width // 2, WIDTH - img_width // 2)
        y = random.randint(img_height // 2, HEIGHT - img_height // 2)
        self.rect.center = (x, y)
        self.vx, self.vy = 0, 0
        self.spawn_frame = spawn_frame
        

    def update(self, screen: pg.Surface, tmr: int):
        """
        アイテムがあるかどうかの確認
        戻り値：画面内にアイテムがあるか
        """
        if tmr - self.spawn_frame >= 200:
            return False
        screen.blit(self.image, self.rect)
        return True
    

def main():
    pg.display.set_caption("真！こうかとん無双")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"fig/26466996.jpg")

    player = Player((900, 400))
    beams = []
    items = []
    last_beam_time = 0   #最後に打ったビームの時間
    last_item_spawn = 0  #最後に現れたアイテムの時間
    next_spawn_interval = 200 #次にアイテムが出るまでの時間
    tmr = 0
    clock = pg.time.Clock()
    while True:
        screen.blit(bg_img, [0,0])
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            
        current_time = pg.time.get_ticks() #現在の時間

        if player.fast_beam_tmr > 0:
            beam_cool_tmr = 400 #ビームのクールタイム（アイテム使用時）
        else:
            beam_cool_tmr = 800 #ビームのクールタイム（通常）
            
        if key_lst[pg.K_SPACE]:    #スペースキー長押しでビーム投下
            if current_time - last_beam_time >= beam_cool_tmr:
                last_beam_time = current_time   
                beams.append(Beam(player)) 
                if player.triple_beam_tmr > 0: #三方向にビームを出す
                    for angle in [0, 30, -30]:
                        beams.append(Beam(player, angle))
                else:
                    beams.append(Beam(player)) #通常のビーム

        if player.shield_tmr > 0:
            pg.draw.circle(screen, (0, 255, 255), player.rect.center, 60, 5)

        if tmr - last_item_spawn >= next_spawn_interval:
            items.append(Item(tmr))
            last_item_spawn = tmr
            next_spawn_interval = random.randint(400, 600) #次のアイテムが400~600フレームの間に出現する

        for item in items:
            if player.rect.colliderect(item.rect):
                if item.item_type == 1:
                    player.triple_beam_tmr = 200 #200フレームの間三方向ビーム

                elif item.item_type == 2:
                    player.fast_beam_tmr = 200

                elif item.item_type == 3:
                    player.shield_tmr = 200
                items.remove(item)


        for i, beam in enumerate(beams):
            beams = [ beam for beam in beams if beam is not None]

        if player.triple_beam_tmr > 0:
            player.triple_beam_tmr -= 1
        if player.fast_beam_tmr >0:
            player.fast_beam_tmr -= 1
        if player.shield_tmr > 0:
            player.shield_tmr -= 1

        player.update(key_lst, screen)
        items = [item for item in items if item.update(screen, tmr)]          
        for beam in beams: 
            beam.update(screen)  
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()


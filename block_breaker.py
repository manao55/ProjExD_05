from typing import Any
import pygame as pg
import sys
WIDTH, HEIGHT = 1600, 900
F_P_SIZE = 30

class Block(pg.sprite.Sprite):
    """
    ブロックに関するクラス
    """
    def __init__(self,width:int,height:int,x:int,y:int):
        super().__init__()
        self.img = pg.Surface((width, height))
        self.img.fill((255, 255, 255))  # 白色で塗りつぶす
        self.rect = self.img.get_rect()
        self.rect.center = x,y
    def update(self,screen: pg.Surface):
        screen.blit(self.img,self.rect)
    
class Score():
    """
    初期化メソッド
    """
    def __init__(self):
        self.font  = pg.font.SysFont("hgep006", F_P_SIZE)
        self.point = 0
    """
    スコア計算
    """
    def cal_score(self, point):
        self.point += point * 100
    """
    スピード更新メソッド
    """
    def update_speed(self):
        if self.point < 1000:
            time_scale = 1.0
        elif self.point < 2000:
            time_scale = 1.5
        elif self.point < 3000:
            time_scale = 2.0
        else:
            time_scale = 2.5
        # タイムスケールを設定する
        # set_time_scale(time_scale)
    """
    スコア描画
    """
    def draw(self, surface):
        text = self.font.render("{:04d}".format(self.point), True, (63,255,63))
        surface.blit(text, [10, 5])
    

def main():
    pg.display.set_caption("ブロック崩し改")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    blocks = pg.sprite.Group()
    ball = pg.sprite.Group()
    
    # 初期ブロックの追加
    for i in range(1,10):
        for j in range(1,10):
            blocks.add(Block(100, 25,200+(110*i),100+(30*j)))
    
    while True:
        key_lst = pg.key.get_pressed()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0

        # ブロックの更新と描画
        blocks.update(screen)
        
        # 画面の更新
        pg.display.flip()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
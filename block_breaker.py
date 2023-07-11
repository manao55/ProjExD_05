from typing import Any
import pygame as pg
import sys
WIDTH, HEIGHT = 1600, 900
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


class Sound():
    """
    サウンドに関するクラス
    """
    def __init__(self):
        self.BoundSE = pg.mixer.Sound("ex05/sounds/boundSE.mp3")
        self.BGM = pg.mixer.Sound("ex05/sounds/maou_bgm_8bit28.mp3")
        
    def playBoundSE(self):
        """
        ボールが反射したときに実行してください
        """
        self.SE.play()
        
    def playBGM(self, time:int):
        self.BGM.play(time)
        
    
def main():
    pg.display.set_caption("ブロック崩し改")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    blocks = pg.sprite.Group()
    ball = pg.sprite.Group()
    sound = Sound()
    
    # 初期ブロックの追加
    for i in range(1,10):
        for j in range(1,10):
            blocks.add(Block(100, 25,200+(110*i),100+(30*j)))
    
    sound.playBGM(-1)  # BGM再生
    
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
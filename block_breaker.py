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
        self.BGM = pg.mixer.Sound("ex05/sounds/maou_bgm_8bit28.mp3")
        self.BoundSE = pg.mixer.Sound("ex05/sounds/select01.mp3")
        self.ExpSE = pg.mixer.Sound("ex05/sounds/explosion03.mp3")
        self.ShotSE = [pg.mixer.Sound("ex05/sounds/hit01.mp3"),
                       pg.mixer.Sound("ex05/sounds/laser_beam.mp3")]
        self.DamageSE = pg.mixer.Sound("ex05/sounds/hit06.mp3")

    def playBGM(self, time:int):
        """
        BGMを再生
        引数に-1を指定することでループ再生できる
        """
        self.BGM.play(time)
        
    def playBoundSE(self):
        """
        ボールの反射音を再生
        ボールが反射したときに実行
        """
        self.BoundSE.play()
        
    def playExpSE(self):
        """
        敵の爆発音を再生
        敵を倒した時に実行
        """
        self.ExpSE.play()
        
    def playShotSE(self, num:int):
        """
        敵が弾を発射した時に再生
        引数0でミサイルの発射音、引数1で雷の発射音
        引数は発射時に指定するbulletNumを渡す 
        """
        self.ShotSE[num].play()
    
    def playDamageSE(self):
        """
        被弾音を再生
        被弾時に実行
        """
        self.DamageSE.play()
    
    
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
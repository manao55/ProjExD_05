from typing import Any
import pygame as pg
import sys
WIDTH, HEIGHT = 1600, 900
F_P_SIZE = 30 # 追加

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

class Ball(pg.sprite.Sprite):
    """
    ボールに関するクラス
    """
    def __init__(self,x:int,y:int):
        super().__init__()
        self.img = pg.Surface((20, 20))
        pg.draw.circle(self.img,(255,255,255),(10,10),10)
        self.rect = self.img.get_rect()
        self.rect.center = x,y
        self.speed_x = 5
        self.speed_y = -5

    def update(self,screen: pg.Surface,paddle:pg.sprite.Sprite,blocks:pg.sprite.Group):
        screen.blit(self.img,self.rect)
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1

        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_y *= -1

        if pg.sprite.collide_rect(self,paddle):
            self.speed_y *= -1

        block_collide_list = pg.sprite.spritecollide(self,blocks,True)
        if block_collide_list:
            self.speed_y *= -1

class Paddle(pg.sprite.Sprite):
    """
    パドルに関するクラス
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
        self.font  = pg.font.SysFont("hgep006", F_P_SIZE) # 変更
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
        # set_time_scale(time_scale) # 削除

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
    
    # 初期ブロックの追加
    for i in range(1,10):
        for j in range(1,10):
            blocks.add(Block(100, 25,200+(110*i),100+(30*j)))
    
    ball_group = pg.sprite.GroupSingle()
    
    ball_group.add(Ball(WIDTH//2,HEIGHT//2))
    
    paddle_group = pg.sprite.GroupSingle()
    
    paddle_group.add(Paddle(100,20,WIDTH//2,HEIGHT-50))
    
    while True:
        key_lst = pg.key.get_pressed()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0

        if key_lst[pg.K_LEFT]:
            paddle_group.sprite.rect.x -= 5
        if key_lst[pg.K_RIGHT]:
            paddle_group.sprite.rect.x += 5

        screen.fill((0,0,0))
        
        # ブロックの更新と描画
        blocks.update(screen)
        
        # ボールの更新と描画
        ball_group.update(screen,paddle_group.sprite,blocks)
        
        # パドルの更新と描画
        paddle_group.update(screen)
        
        # 画面の更新
        pg.display.flip()
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

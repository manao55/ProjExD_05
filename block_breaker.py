from typing import Any
import pygame as pg
import sys
import math
WIDTH, HEIGHT = 1600, 900

def check_bound_out(obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数 obj：オブジェクト（爆弾，こうかとん，ビーム）SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.left < 0 or WIDTH < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate


def check_bound_rects(ball:pg.Rect, rct:pg.Rect) -> tuple[bool, bool]:
    """
    ボールのどこがrctに当たったか判定する関数
    引数１ ball：ボールSurface
    引数２ rct：rectのSurface
    戻り値 横、縦の当たり判定（Trueで当たっている)
    """
    r_l_t_b = [0, 0, 0, 0]
    if ball.colliderect(rct):
        if ball.right >= rct.left and ball.centery >= rct.top and ball.centery <= rct.bottom:
            r_l_t_b[0] = 1
        elif ball.left <= rct.right and ball.centery >= rct.top and ball.centery <= rct.bottom:
            r_l_t_b[1] = 1
        elif ball.top <= rct.bottom and ball.centerx <= rct.right and ball.centerx >= rct.left:
            r_l_t_b[2] = 1
        elif ball.bottom >= rct.top and ball.centerx <= rct.right and ball.centerx >= rct.left:
            r_l_t_b[3] = 1
    if r_l_t_b[0] == 1 or r_l_t_b[1] == 1:
        return 1, 0
    elif r_l_t_b[2] == 1 or r_l_t_b[3] == 1:
        return 0, 1
    return 0, 0


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
    def __init__(self, r:int, x:int, y:int):
        """
        ボールSurfaceを作成する
        引数１ r：半径
        引数２、３ x,y：ボールの中心座標
        """
        super().__init__()
        self.image = pg.Surface((r*2, r*2))
        pg.draw.circle(self.image, (255, 255, 255), (r, r), r)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        self.rad = math.pi/4
        self.vx = -math.cos(self.rad)
        self.vy = -math.sin(self.rad)
        self.speed = 2
    
    def update(self):
        """
        ボールを速度ベクトルself.vx, self.vyに基づき移動させる
        check_bound_out関数によって画面外に出たかどうか判定すし、速度を変更する。
        """
        if check_bound_out(self.rect)[0] == 0:
            self.vx *= -1
        elif check_bound_out(self.rect)[1] == 0:
            self.vy *= -1
        self.rect.move_ip(+self.speed*self.vx, +self.speed*self.vy)
        if self.rect.bottom >= HEIGHT:
            self.kill()


def main():
    pg.display.set_caption("ブロック崩し改")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.Surface((WIDTH, HEIGHT))  #背景を追加、必要に応じて消してください
    bg_img.fill((0, 0, 0))
    blocks = pg.sprite.Group()
    balls = pg.sprite.Group()  
    balls.add(Ball(10, WIDTH/2, HEIGHT-100))  #ボールを生成する(半径10)
    
    # 初期ブロックの追加
    for i in range(1,10):
        for j in range(1,10):
            blocks.add(Block(100, 25,200+(110*i),100+(30*j)))
    
    while True:
        key_lst = pg.key.get_pressed()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
        screen.blit(bg_img, [0, 0])  #背景の描写、必要に応じて消してください

        #ブロックとの衝突判定
        for ball in balls:
            for block in blocks:
                if check_bound_rects(ball.rect, block.rect)[0] == 1:
                    ball.vx *= -1
                elif check_bound_rects(ball.rect, block.rect)[1] == 1:
                    ball.vy *= -1


        # ブロックの更新と描画
        blocks.update(screen)
        balls.update()  #ボールの更新と描画
        balls.draw(screen)
        
        # 画面の更新
        pg.display.update()
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
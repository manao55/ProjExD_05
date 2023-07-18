import pygame as pg
import sys
F_P_SIZE = 30
WIDTH, HEIGHT = 1200, 900
B_BLANK = 15
B_LEFT = 30
B_TOP = 10
import math

def check_bound_out(obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数 obj：オブジェクト SurfaceのRect
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
    def __init__(self, x: int, y: int, life: int):
        """
        ブロックSurfaceを生成する
        引数1 x：左上の開始ブロックのx座標
        引数2 y：左上の開始ブロックのy座標
        引数3 life:ブロックの耐久値
        """
        super().__init__()

        self.life = life
        self.color_list = [(0, 255, 0), (255, 255, 0), (255, 0, 0)]
        self.image = pg.Surface((100, 20))  # 100*25のブロックを生成
        self.image.fill(self.color_list[3 - (self.life)])
        self.rect = self.image.get_rect()
        self.rect.left = x * (self.rect.width + B_BLANK) + B_LEFT
        self.rect.top = y * (self.rect.height + B_BLANK) + B_TOP

    def update(self, screen: pg.Surface):
        screen.blit(self.image, self.rect)

    def collision(self,screen):#ボールとの衝突時
        self.life -= 1
        if self.life <= 0:
            return
        self.image.fill(self.color_list[3 - (self.life)])
        self.update(screen)

    def handle_event(self, event,screen):#デバッグ用関数
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:#ボールクラスが現状存在しないためクリックにて対応
            if self.rect.collidepoint(event.pos):
                if self.life >0:
                    self.collision(screen)
                if self.life <= 0:
                    self.kill()
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
        # aaa
    """
    スコア描画
    """
    def draw(self, surface):
        text = self.font.render("{:04d}".format(self.point), True, (63,255,63))
        surface.blit(text, [10, 5])

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
        self.vx = math.cos(self.rad)
        self.vy = -math.sin(self.rad)
        self.speed = 5
    
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
    for i in range(10):
        for j in range(8):
            blocks.add(Block(i, j, 3))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            else:
                for block in blocks.copy():#デバッグ用であるためマージ時削除
                    block.handle_event(event,screen)
        screen.blit(bg_img, [0, 0])  #背景の描写、必要に応じて消してください

        #ブロックとの衝突判定
        for ball in balls:
            for block in blocks:
                if check_bound_rects(ball.rect, block.rect)[0] == 1:
                    ball.vx *= -1
                elif check_bound_rects(ball.rect, block.rect)[1] == 1:
                    ball.vy *= -1

        # ブロックの更新と描画
        screen.fill((0, 0, 0))  # 画面をクリア
        blocks.update(screen)
        blocks.draw(screen)
        balls.update()  #ボールの更新と描画
        balls.draw(screen)

        # 画面の更新
        pg.display.flip()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
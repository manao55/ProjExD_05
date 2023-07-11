import pygame as pg
import sys

WIDTH, HEIGHT = 1200, 900
B_BLANK = 15
B_LEFT = 30
B_TOP = 10

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

    def collision(self,screen):
        self.life -= 1
        if self.life <= 0:
            return
        self.image.fill(self.color_list[3 - (self.life)])
        self.update(screen)

    def handle_event(self, event,screen):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.life >0:
                    self.collision(screen)
                if self.life <= 0:
                    self.kill()


def main():
    pg.display.set_caption("ブロック崩し改")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    blocks = pg.sprite.Group()

    # 初期ブロックの追加
    for i in range(10):
        for j in range(8):
            blocks.add(Block(i, j, 3))

    while True:
        key_lst = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            else:
                for block in blocks.copy():
                    block.handle_event(event,screen)

        # ブロックの更新と描画
        screen.fill((0, 0, 0))  # 画面をクリア
        blocks.update(screen)
        blocks.draw(screen)

        # 画面の更新
        pg.display.flip()


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

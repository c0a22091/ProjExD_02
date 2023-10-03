import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1600, 900


delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")

    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)

    kk_img_forward = pg.transform.flip(kk_img, True, False)
    kk_img_backward = pg.transform.flip(kk_img_forward, True, False)

    # こうかとんのSurfaceの二重dict
    # dictの1つ目のキーが横向き・2つ目のキーが縦向きのスピード
    # スピードが負のときキーは-1, 0のとき0, 正のとき1
    kk_img_list = {1: {
        1: pg.transform.rotozoom(kk_img_forward, -45, 1.0),
        0: pg.transform.rotozoom(kk_img_forward, 0, 1.0),
        -1: pg.transform.rotozoom(kk_img_forward, 45, 1.0)
    }, 0: {
        1: pg.transform.rotozoom(kk_img_forward, 90, 1.0),
        0: pg.transform.rotozoom(kk_img_forward, 0, 1.0),
        -1: pg.transform.rotozoom(kk_img_forward, -90, 1.0),
    }, -1:{
        1: pg.transform.rotozoom(kk_img_backward, 45, 1.0),
        0: pg.transform.rotozoom(kk_img_backward, 0, 1.0),
        -1: pg.transform.rotozoom(kk_img_backward, -45, 1.0)
    }}

    kk_x = 900
    kk_y = 400
    kk_img_rct = kk_img.get_rect()
    kk_img_rct.center = kk_x, kk_y

    clock = pg.time.Clock()
    tmr = 0

    bomb_color = (255, 0, 0)
    bomb_r = 10
    bomb_x = random.randint(0, WIDTH)
    bomb_y = random.randint(0, HEIGHT)
    bomb_speed = 5

    bomb_img = make_bomb_surface(bomb_r, bomb_color)
    bomb_img_rct = bomb_img.get_rect()
    bomb_img_rct.center = bomb_x, bomb_y

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        keys = pg.key.get_pressed()
        kk_speeds = [0, 0]
        for key, mv in delta.items():
            if (keys[key]):
                kk_speeds[0] += mv[0]
                kk_speeds[1] += mv[1]

        # 爆弾の半径が1000になるまで定期的に巨大化・加速
        if tmr % 200 == 0 and tmr > 0 and bomb_r < 1000:
            bomb_r += 5
            bomb_speed *= 1.2
            bomb_img = make_bomb_surface(bomb_r, bomb_color)

        kk_img_rct.move_ip(kk_speeds)
        bomb_img_rct.move_ip(bomb_speed, bomb_speed)

        kk_img = select_kk_imgs(kk_img_list, kk_speeds[0], kk_speeds[1])

        if (True in check_bound(kk_img_rct)):
            kk_img_rct.center = kk_x, kk_y
        if (True in check_bound(bomb_img_rct)):
            bomb_speed *= -1

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_img_rct)
        screen.blit(bomb_img, bomb_img_rct)

        pg.display.update()

        if kk_img_rct.colliderect(bomb_img_rct):
            kk_img = pg.image.load("ex02/fig/8.png")
            kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)

            screen.blit(bg_img, [0, 0])
            screen.blit(kk_img, kk_img_rct)
            screen.blit(bomb_img, bomb_img_rct)

            pg.display.update()

            # 5秒待つ
            time.sleep(5)
            return

        tmr += 1
        clock.tick(50)


def check_bound(rect: pg.rect):
    return (
      rect.left < 0 or rect.right > WIDTH,
      rect.top < 0 or rect.bottom > HEIGHT
    )


def select_kk_imgs(kk_imgs: dict[dict[pg.Surface]], vx: int, vy: int) -> pg.Surface:
    """
    -1, 0, 1 いずれかのキーを持つこうかとんのSurfaceの二重dictから、vx, vyにあったこうかとんのSurfaceを返す
    引数1 kk_imgs: こうかとんのSurfaceの二重dict
                    dictの1つ目のキー: vx, 2つ目のキー: vy, vx/vyが負のとき-1, 0のとき0, 正のとき1
    引数2 vx: こうかとんの横向きのスピード
    引数3 vy: こうかとんの縦向きのスピード
    """
    kk_img_index_1 = 0 if vx == 0 else vx/abs(vx)
    kk_img_index_2 = 0 if vy == 0 else vy/abs(vy)

    return kk_imgs[kk_img_index_1][kk_img_index_2]


def make_bomb_surface(r: int, color: tuple[int, int, int]) -> pg.Surface:
    """
    爆弾のSurfaceを生成する
    引数1 r: 爆弾の半径
    引数2 color: 爆弾のカラーコードのtuple
    """
    img = pg.Surface((r*2, r*2))
    img.set_colorkey((0, 0, 0))
    pg.draw.circle(img, color, (r, r), r)
    return img


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
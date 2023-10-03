import pygame as pg
import sys
import random
WIDTH, HEIGHT = 1600,900
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0)
}

def check_bound(obj_rct: pg.Rect):
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: # 横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: # 縦方向判定
        tate = False
    return yoko, tate

def main():
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)

    
    kk_imgs = {
        pg.K_UP: pg.transform.rotozoom(kk_img, -90, 1.0),
        pg.K_DOWN: pg.transform.rotozoom(kk_img, 90,1.0),
        pg.K_LEFT: pg.transform.rotozoom(kk_img, 0, 1.0),
        pg.K_RIGHT: pg.transform.flip(kk_img, True,False)

    }
    

    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    """こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)  # 練習３：こうかとんの初期座標を設定する
    """ばくだん"""
    bd_img = pg.Surface((20, 20))  # 練習１：爆弾Surfaceを作成する
    bd_img.set_colorkey((0, 0, 0))  # 練習１：黒い部分を透明にする
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()  # 練習１：SurfaceからRectを抽出する
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bd_rct.center = (x, y)  # 練習１：Rectにランダムな座標を設定する
    vx, vy = +5, +5  # 練習２：爆弾の速度
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bd_rct):  # 練習５：ぶつかってたら
            print("ゲームオーバー")
            return

        
        

        key_states = pg.key.get_pressed()
        movement = [0, 0]
        for key, (dx, dy) in DELTA.items():
            if key_states[key]:
                movement[0] += dx
                movement[1] += dy
        
        kk_rct.move_ip(movement[0], movement[1])
        screen.blit(bg_img, [0, 0])
        # ここでキーに応じて画像を切り替える
        if movement[0] > 0:
            kk_img = kk_imgs[pg.K_RIGHT]
        elif movement[0] < 0:
            kk_img = kk_imgs[pg.K_LEFT]
        elif movement[1] > 0:
            kk_img = kk_imgs[pg.K_DOWN]
        elif movement[1] < 0:
            kk_img = kk_imgs[pg.K_UP]
        else:
            kk_img # デフォルトの向き

        if check_bound(kk_rct) != (True, True):  # 練習４：はみだし判定
            kk_rct.move_ip(-movement[0], -movement[1]) 
        screen.blit(kk_img, kk_rct)  # 練習３：移動後の座標に表示させる

        
        screen.blit(kk_img, kk_rct)
        screen.blit(kk_img, kk_rct)  # 練習３：移動後の座標に表示させる
        """"ばくだん"""
        bd_rct.move_ip(vx, vy)  # 練習２：爆弾を移動させる
        yoko, tate = check_bound(bd_rct)
        if not yoko:  # 練習４：横方向にはみ出たら
            vx *= -1
        if not tate:  # 練習４：縦方向にはみ出たら
            vy *= -1
        screen.blit(bd_img, bd_rct)
        pg.display.flip()
        clock.tick(60)


def acc():
    accs = [a for a in range(1,11)]

    for r in range(1,11):
        bb_img = pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        bb_imgs.append(bb_img)
    

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
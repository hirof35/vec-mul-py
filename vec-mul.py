"""
vector_mul.py - ベクトルの実数倍（スカラー倍）シミュレーター（改良版）
"""
import sys
from math import floor
import pygame
from pygame.locals import Rect, QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

# 定数管理によるマジックナンバーの排除
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 550
GRID_AREA_HEIGHT = 500
ORIGIN_X = 250
ORIGIN_Y = 250
PIXELS_PER_UNIT = 25

def main():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Vector Scalar Multiplication")
    fps_clock = pygame.time.Clock()

    # スライダの初期化（初期値 1.0 に設定、ノブの位置を自動計算）
    slider = Slider(Rect(20, 510, 460, 35), min_value=-3.0, max_value=3.0, default_value=1.0)

    # 状態管理変数
    vec_base = [2.0, -2.0]  # 初期ベクトル (x, y) 
    is_dragging_slider = False

    while True:
        # --- 1. イベント制御 ---
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # 左クリック
                    if slider.rect.collidepoint(event.pos):
                        is_dragging_slider = True
                        slider.set_pos_by_x(event.pos[0])
                    elif event.pos[1] < GRID_AREA_HEIGHT:
                        # グリッド上の座標を数学的ベクトル座標に変換 (四捨五入で直感的に)
                        vx = round((event.pos[0] - ORIGIN_X) / PIXELS_PER_UNIT)
                        vy = round((event.pos[1] - ORIGIN_Y) / PIXELS_PER_UNIT)
                        vec_base = [vx, vy]

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    is_dragging_slider = False

            elif event.type == MOUSEMOTION:
                if is_dragging_slider:
                    slider.set_pos_by_x(event.pos[0])

        # --- 2. 演算処理 ---
        scalar = slider.get_value()
        # スカラー倍ベクトルの計算
        vec_scaled = [vec_base[0] * scalar, vec_base[1] * scalar]

        # --- 3. 描画処理 ---
        surface.fill((15, 15, 20))  # 視認性の高いダークテーマ

        # グリッド（背景点）の描画
        for ypos in range(0, GRID_AREA_HEIGHT, PIXELS_PER_UNIT):
            for xpos in range(0, SCREEN_WIDTH, PIXELS_PER_UNIT):
                pygame.draw.circle(surface, (50, 50, 60), (xpos, ypos), 1)

        # 座標軸の描画 (X軸/Y軸)
        pygame.draw.line(surface, (80, 80, 100), (ORIGIN_X, 0), (ORIGIN_X, GRID_AREA_HEIGHT), 2)
        pygame.draw.line(surface, (80, 80, 100), (0, ORIGIN_Y), (SCREEN_WIDTH, ORIGIN_Y), 2)

        # 元ベクトル (緑: Green) の描画
        target_pix_0 = (int(ORIGIN_X + vec_base[0] * PIXELS_PER_UNIT),
                        int(ORIGIN_Y + vec_base[1] * PIXELS_PER_UNIT))
        pygame.draw.line(surface, (46, 204, 113), (ORIGIN_X, ORIGIN_Y), target_pix_0, 5)

        # スカラー倍ベクトル (青: Cyan) の描画（太さを変えて重ねても見えるように調整）
        target_pix_1 = (int(ORIGIN_X + vec_scaled[0] * PIXELS_PER_UNIT),
                        int(ORIGIN_Y + vec_scaled[1] * PIXELS_PER_UNIT))
        pygame.draw.line(surface, (52, 152, 219), (ORIGIN_X, ORIGIN_Y), target_pix_1, 2)

        # UI要素の描画
        slider.draw(surface)

        pygame.display.update()
        fps_clock.tick(60)  # 60FPSで滑らかに動作


class Slider:
    """ 
    スライダコンポーネント (自己完結型リファクタリング版)
    """
    def __init__(self, rect, min_value, max_value, default_value):
        self.rect = rect
        # レール部分のパディング設定
        self.track_rect = rect.inflate(-40, -24)
        
        self.min_value = min_value
        self.max_value = max_value
        
        # ノブの矩形定義
        self.knob_rect = Rect(0, 0, 12, rect.height - 10)
        
        # 初期値に基づくノブ位置の設定
        init_ratio = (default_value - min_value) / (max_value - min_value)
        init_x = self.track_rect.left + (self.track_rect.width * init_ratio)
        self.knob_rect.center = (int(init_x), rect.centery)

    def draw(self, surface):
        """ 指定されたSurfaceにスライダ構造を描画 """
        # ベースの背景
        pygame.draw.rect(surface, (44, 62, 80), self.rect, border_radius=6)
        # スライダのレール
        pygame.draw.rect(surface, (127, 140, 141), self.track_rect, border_radius=3)
        # センターライン（0の位置をわかりやすくするためのガイド）
        center_x = self.track_rect.left + self.track_rect.width / 2
        pygame.draw.line(surface, (231, 76, 60), (center_x, self.track_rect.top), (center_x, self.track_rect.bottom), 2)
        # つまみ（ノブ）
        pygame.draw.rect(surface, (236, 240, 241), self.knob_rect, border_radius=4)

    def set_pos_by_x(self, xpos):
        """ マウスのX座標からノブの位置を更新（レール内にクランプ） """
        bounded_x = max(self.track_rect.left, min(self.track_rect.right, xpos))
        self.knob_rect.centerx = bounded_x

    def get_value(self):
        """ 現在のノブの位置から対応するスカラー値を計算 """
        if self.track_rect.width == 0:
            return self.min_value
        ratio = (self.knob_rect.centerx - self.track_rect.left) / self.track_rect.width
        return self.min_value + (self.max_value - self.min_value) * ratio

if __name__ == '__main__':
    main()

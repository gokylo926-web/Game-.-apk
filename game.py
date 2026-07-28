import pygame
import sys
import random

# Pygame Başlatma
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash & Savaş Oyunu - PC/Mobil")
clock = pygame.time.Clock()

# Renkler
BG_COLOR = (12, 12, 20)
CURSOR_COLOR = (0, 255, 200)
BORDER_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (255, 40, 90)
GROUND_COLOR = (25, 25, 35)
TEXT_COLOR = (255, 255, 255)
BTN_COLOR = (40, 120, 220)
BTN_MOB_COLOR = (200, 120, 20)

font = pygame.font.SysFont("Arial", 24, bold=True)
title_font = pygame.font.SysFont("Arial", 36, bold=True)
menu_font = pygame.font.SysFont("Arial", 28, bold=True)

# Sınırlar
GROUND_Y = HEIGHT - 50
CEILING_Y = 50

# --- 6 LEVEL VERİSİ ---
LEVELS = [
    {"name": "Level 1: Giris", "length": 3000, "speed": 5.5, "obstacles": [(600, 180, 380, 50), (1000, 220, 420, 50), (1400, 150, 350, 50), (1800, 250, 450, 50), (2200, 170, 370, 50), (2600, 200, 400, 50)]},
    {"name": "Level 2: Zikzak", "length": 3500, "speed": 6.2, "obstacles": [(500, 240, 400, 45), (800, 120, 280, 45), (1100, 280, 440, 45), (1450, 150, 310, 45), (1800, 220, 380, 45), (2150, 100, 260, 45), (2500, 260, 420, 45), (2900, 180, 340, 45)]},
    {"name": "Level 3: Dar Gecit", "length": 4000, "speed": 7.0, "obstacles": [(450, 200, 340, 40), (750, 160, 300, 40), (1050, 230, 370, 40), (1350, 140, 280, 40), (1650, 250, 390, 40), (1950, 120, 260, 40), (2250, 220, 360, 40), (2550, 180, 320, 40), (2850, 260, 400, 40), (3200, 150, 290, 40), (3550, 210, 350, 40)]},
    {"name": "Level 4: Hizli Kabus", "length": 4500, "speed": 7.8, "obstacles": [(400, 220, 350, 35), (700, 100, 230, 35), (950, 280, 410, 35), (1200, 150, 280, 35), (1500, 240, 370, 35), (1750, 120, 250, 35), (2050, 300, 430, 35), (2350, 180, 310, 35), (2650, 220, 350, 35), (2950, 140, 270, 35), (3250, 260, 390, 35), (3600, 160, 290, 35), (3950, 200, 330, 35)]},
    {"name": "Level 5: Labirent", "length": 5000, "speed": 8.5, "obstacles": [(400, 200, 310, 30), (650, 130, 240, 30), (900, 270, 380, 30), (1150, 160, 270, 30), (1400, 220, 330, 30), (1650, 110, 220, 30), (1950, 290, 400, 30), (2200, 180, 290, 30), (2450, 240, 350, 30), (2750, 140, 250, 30), (3000, 260, 370, 30), (3300, 100, 210, 30), (3600, 220, 330, 30), (3900, 160, 270, 30), (4250, 200, 310, 30), (4550, 120, 230, 30)]},
    {"name": "Level 6: SON SINAV", "length": 6000, "speed": 9.2, "obstacles": [(400, 180, 280, 28), (600, 250, 350, 28), (850, 120, 220, 28), (1100, 220, 320, 28), (1350, 150, 250, 28), (1600, 280, 380, 28), (1850, 100, 200, 28), (2100, 210, 310, 28), (2350, 170, 270, 28), (2650, 240, 340, 28), (2900, 130, 230, 28), (3200, 260, 360, 28), (3450, 160, 260, 28), (3750, 220, 320, 28), (4050, 110, 210, 28), (4300, 290, 390, 28), (4600, 150, 250, 28), (4900, 200, 300, 28), (5250, 120, 220, 28), (5550, 240, 340, 28)]}
]

# Oyun Durumları: "MENU", "PLATFORM_SELECT", "IMLEC_PLAY", vb.
game_state = "MENU"
selected_mode = "" # "IMLEC" veya "SAVAS"
device_type = ""   # "PC" veya "MOBIL"

# İmleç Modu Değişkenleri
current_level_idx = 0
camera_x = 0
cursor_x = 150
cursor_y = 300
velocity_y = 0.0
gravity = 0.45
thrust = -0.85
max_speed = 8.5
angle = 0

# Savaş Modu Değişkenleri
player_x = 100
player_y = 300
player_size = 40
bullets = []
enemies = []
enemy_spawn_timer = 0
savas_score = 0

# Mobil Kontrol Durumları (Dokunmatik için)
btn_up_pressed = False
btn_down_pressed = False

def reset_imlec_level():
    global camera_x, cursor_y, velocity_y, angle, game_state
    camera_x = 0
    cursor_y = 300
    velocity_y = 0.0
    angle = 0
    game_state = "IMLEC_PLAY"

def reset_savas_mode():
    global player_y, bullets, enemies, enemy_spawn_timer, savas_score, game_state
    player_y = 300
    bullets.clear()
    enemies.clear()
    enemy_spawn_timer = 0
    savas_score = 0
    game_state = "SAVAS_PLAY"

def draw_cursor(surface, x, y, rot_angle):
    c_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    points = [(35, 20), (5, 5), (12, 20), (5, 35)]
    pygame.draw.polygon(c_surf, CURSOR_COLOR, points)
    pygame.draw.polygon(c_surf, BORDER_COLOR, points, 2)
    rotated_surf = pygame.transform.rotate(c_surf, rot_angle)
    rect = rotated_surf.get_rect(center=(x, y))
    surface.blit(rotated_surf, rect.topleft)
    return pygame.Rect(x - 12, y - 12, 24, 24)

# Ana Oyun Döngüsü
running = True
while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    touching = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
            click_x, click_y = event.pos if event.type == pygame.MOUSEBUTTONDOWN else (int(event.x * WIDTH), int(event.y * HEIGHT))

            # 1. ANA MENÜ
            if game_state == "MENU":
                if 150 <= click_x <= 380 and 250 <= click_y <= 370:
                    selected_mode = "IMLEC"
                    game_state = "PLATFORM_SELECT"
                elif 420 <= click_x <= 650 and 250 <= click_y <= 370:
                    selected_mode = "SAVAS"
                    game_state = "PLATFORM_SELECT"

            # 2. PLATFORM SEÇİMİ (PC veya Mobil)
            elif game_state == "PLATFORM_SELECT":
                if 150 <= click_x <= 380 and 250 <= click_y <= 370:
                    device_type = "PC"
                    if selected_mode == "IMLEC": reset_imlec_level()
                    else: reset_savas_mode()
                elif 420 <= click_x <= 650 and 250 <= click_y <= 370:
                    device_type = "MOBIL"
                    if selected_mode == "IMLEC": reset_imlec_level()
                    else: reset_savas_mode()

            # 3. İMLEÇ MODU GEÇİŞLERİ
            elif game_state == "IMLEC_DEAD":
                reset_imlec_level()
            elif game_state == "IMLEC_WIN":
                current_level_idx += 1
                if current_level_idx >= len(LEVELS):
                    game_state = "IMLEC_COMPLETE"
                else:
                    reset_imlec_level()
            elif game_state == "IMLEC_COMPLETE":
                game_state = "MENU"

            # 4. SAVAŞ MODU BİTİŞ
            elif game_state == "SAVAS_DEAD":
                game_state = "MENU"

            # 5. MOBİL SAVAŞ KONTROL BUTONLARI (Dokunmatik)
            elif game_state == "SAVAS_PLAY" and device_type == "MOBIL":
                # Yukarı Tuşu Kontrolü
                if 50 <= click_x <= 150 and HEIGHT - 160 <= click_y <= HEIGHT - 90:
                    btn_up_pressed = True
                    btn_down_pressed = False
                # Aşağı Tuşu Kontrolü
                elif 50 <= click_x <= 150 and HEIGHT - 80 <= click_y <= HEIGHT - 10:
                    btn_down_pressed = True
                    btn_up_pressed = False
                # Ateş Etme Butonu
                elif WIDTH - 160 <= click_x <= WIDTH - 40 and HEIGHT - 120 <= click_y <= HEIGHT - 40:
                    bullets.append([player_x + player_size, player_y + player_size // 2])

            # PC Savaş Modu Ateş Etme
            elif game_state == "SAVAS_PLAY" and device_type == "PC":
                bullets.append([player_x + player_size, player_y + player_size // 2])

        # Dokunma kalktığında mobil hareket butonlarını bırak
        if event.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
            if game_state == "SAVAS_PLAY" and device_type == "MOBIL":
                btn_up_pressed = False
                btn_down_pressed = False

    # PC Klavye Kontrolleri (Eğer PC seçildiyse)
    if game_state == "SAVAS_PLAY" and device_type == "PC":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y = max(CEILING_Y + 10, player_y - 6)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y = min(GROUND_Y - player_size - 10, player_y + 6)

    # Mobil Ekran Basılı Tutma Hareketleri
    if game_state == "SAVAS_PLAY" and device_type == "MOBIL":
        if btn_up_pressed:
            player_y = max(CEILING_Y + 10, player_y - 6)
        if btn_down_pressed:
            player_y = min(GROUND_Y - player_size - 10, player_y + 6)

    # ================= OYUN GÜNCELLEMELERİ =================
    if game_state == "IMLEC_PLAY":
        level_data = LEVELS[current_level_idx]
        camera_x += level_data["speed"]

        if touching:
            velocity_y += thrust
        else:
            velocity_y += gravity

        velocity_y = max(-max_speed, min(velocity_y, max_speed))
        cursor_y += velocity_y

        target_angle = -velocity_y * 4.5
        angle += (target_angle - angle) * 0.2

        if cursor_y >= GROUND_Y - 15 or cursor_y <= CEILING_Y + 15:
            game_state = "IMLEC_DEAD"

        if camera_x >= level_data["length"]:
            game_state = "IMLEC_WIN"

    elif game_state == "SAVAS_PLAY":
        enemy_spawn_timer += 1
        if enemy_spawn_timer > 45:
            enemy_y = random.randint(CEILING_Y + 20, GROUND_Y - 70)
            enemies.append([WIDTH, enemy_y, 40, 40])
            enemy_spawn_timer = 0

        for bullet in bullets[:]:
            bullet[0] += 10
            if bullet[0] > WIDTH:
                bullets.remove(bullet)

        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for enemy in enemies[:]:
            enemy[0] -= 4
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy[2], enemy[3])

            if player_rect.colliderect(enemy_rect):
                game_state = "SAVAS_DEAD"

            for bullet in bullets[:]:
                bullet_rect = pygame.Rect(bullet[0], bullet[1], 12, 4)
                if bullet_rect.colliderect(enemy_rect):
                    if bullet in bullets: bullets.remove(bullet)
                    if enemy in enemies: enemies.remove(enemy)
                    savas_score += 10
                    break

            if enemy[0] < -50:
                enemies.remove(enemy)

    # ================= ÇİZİM (RENDER) =================
    screen.fill(BG_COLOR)

    pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
    pygame.draw.rect(screen, GROUND_COLOR, (0, 0, WIDTH, CEILING_Y))
    pygame.draw.line(screen, BORDER_COLOR, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
    pygame.draw.line(screen, BORDER_COLOR, (0, CEILING_Y), (WIDTH, CEILING_Y), 2)

    # 1. ANA MENÜ
    if game_state == "MENU":
        title = title_font.render("GEOMETRY DASH - ARCADE", True, (255, 215, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        btn1 = pygame.Rect(150, 250, 230, 120)
        pygame.draw.rect(screen, BTN_COLOR, btn1, border_radius=15)
        pygame.draw.rect(screen, BORDER_COLOR, btn1, 2, border_radius=15)
        t1 = menu_font.render("İMLEÇ MODU", True, TEXT_COLOR)
        screen.blit(t1, (btn1.centerx - t1.get_width() // 2, btn1.centery - t1.get_height() // 2))

        btn2 = pygame.Rect(420, 250, 230, 120)
        pygame.draw.rect(screen, (200, 50, 80), btn2, border_radius=15)
        pygame.draw.rect(screen, BORDER_COLOR, btn2, 2, border_radius=15)
        t2 = menu_font.render("SAVAŞ MODU", True, TEXT_COLOR)
        screen.blit(t2, (btn2.centerx - t2.get_width() // 2, btn2.centery - t2.get_height() // 2))

        sub = font.render("Oynamak istediğin modu seç", True, (180, 180, 200))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 430))

    # 2. PLATFORM SEÇİMİ (PC veya Mobil)
    elif game_state == "PLATFORM_SELECT":
        title = title_font.render("PLATFORM SEÇİNİZ", True, (255, 215, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        btn_pc = pygame.Rect(150, 250, 230, 120)
        pygame.draw.rect(screen, BTN_COLOR, btn_pc, border_radius=15)
        pygame.draw.rect(screen, BORDER_COLOR, btn_pc, 2, border_radius=15)
        tp = menu_font.render("PC VERSİYONU", True, TEXT_COLOR)
        screen.blit(tp, (btn_pc.centerx - tp.get_width() // 2, btn_pc.centery - tp.get_height() // 2))

        btn_mob = pygame.Rect(420, 250, 230, 120)
        pygame.draw.rect(screen, BTN_MOB_COLOR, btn_mob, border_radius=15)
        pygame.draw.rect(screen, BORDER_COLOR, btn_mob, 2, border_radius=15)
        tm = menu_font.render("MOBİL VERSİYON", True, TEXT_COLOR)
        screen.blit(tm, (btn_mob.centerx - tm.get_width() // 2, btn_mob.centery - tm.get_height() // 2))

    # 3. İMLEÇ MODU OYNANIŞI
    elif game_state == "IMLEC_PLAY":
        level_data = LEVELS[current_level_idx]
        player_hitbox = pygame.Rect(cursor_x - 12, cursor_y - 12, 24, 24)

        for obs in level_data["obstacles"]:
            obs_x = obs[0] - camera_x
            top_h = obs[1]
            bot_y = obs[2]
            obs_w = obs[3]

            if -obs_w < obs_x < WIDTH:
                top_rect = pygame.Rect(obs_x, CEILING_Y, obs_w, top_h - CEILING_Y)
                bot_rect = pygame.Rect(obs_x, bot_y, obs_w, GROUND_Y - bot_y)
                pygame.draw.rect(screen, OBSTACLE_COLOR, top_rect)
                pygame.draw.rect(screen, BORDER_COLOR, top_rect, 2)
                pygame.draw.rect(screen, OBSTACLE_COLOR, bot_rect)
                pygame.draw.rect(screen, BORDER_COLOR, bot_rect, 2)

                if player_hitbox.colliderect(top_rect) or player_hitbox.colliderect(bot_rect):
                    game_state = "IMLEC_DEAD"

        finish_x = level_data["length"] - camera_x
        if -50 < finish_x < WIDTH:
            pygame.draw.rect(screen, (0, 255, 0), (finish_x, CEILING_Y, 20, GROUND_Y - CEILING_Y))

        draw_cursor(screen, cursor_x, cursor_y, angle)

        progress = min(1.0, camera_x / level_data["length"])
        pygame.draw.rect(screen, (50, 50, 70), (200, 15, 400, 15))
        pygame.draw.rect(screen, CURSOR_COLOR, (200, 15, 400 * progress, 15))
        lvl_text = font.render(f"{level_data['name']} - %{int(progress * 100)}", True, TEXT_COLOR)
        screen.blit(lvl_text, (20, 10))

    # 4. SAVAŞ MODU OYNANIŞI
    elif game_state == "SAVAS_PLAY":
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        pygame.draw.rect(screen, (0, 255, 120), player_rect, border_radius=6)
        pygame.draw.rect(screen, BORDER_COLOR, player_rect, 2, border_radius=6)

        for b in bullets:
            pygame.draw.rect(screen, (255, 255, 0), (b[0], b[1], 12, 4))

        for e in enemies:
            pygame.draw.rect(screen, OBSTACLE_COLOR, (e[0], e[1], e[2], e[3]), border_radius=8)
            pygame.draw.rect(screen, BORDER_COLOR, (e[0], e[1], e[2], e[3]), 2, border_radius=8)

        score_txt = font.render(f"Skor: {savas_score}", True, TEXT_COLOR)
        screen.blit(score_txt, (20, 15))

        # Eğer Mobil Mod seçildiyse ekrana dokunmatik butonlar çiz
        if device_type == "MOBIL":
            # Yukarı Butonu
            up_btn = pygame.Rect(50, HEIGHT - 160, 100, 70)
            pygame.draw.rect(screen, (60, 60, 90), up_btn, border_radius=10)
            pygame.draw.rect(screen, BORDER_COLOR, up_btn, 2, border_radius=10)
            tu = font.render("YUKARI", True, TEXT_COLOR)
            screen.blit(tu, (up_btn.centerx - tu.get_width() // 2, up_btn.centery - tu.get_height() // 2))

            # Aşağı Butonu
            down_btn = pygame.Rect(50, HEIGHT - 80, 100, 70)
            pygame.draw.rect(screen, (60, 60, 90), down_btn, border_radius=10)
            pygame.draw.rect(screen, BORDER_COLOR, down_btn, 2, border_radius=10)
            td = font.render("AŞAĞI", True, TEXT_COLOR)
            screen.blit(td, (down_btn.centerx - td.get_width() // 2, down_btn.centery - td.get_height() // 2))

            # Ateş Et Butonu
            fire_btn = pygame.Rect(WIDTH - 160, HEIGHT - 120, 110, 80)
            pygame.draw.rect(screen, (200, 50, 50), fire_btn, border_radius=15)
            pygame.draw.rect(screen, BORDER_COLOR, fire_btn, 2, border_radius=15)
            tf = font.render("ATEŞ ET", True, TEXT_COLOR)
            screen.blit(tf, (fire_btn.centerx - tf.get_width() // 2, fire_btn.centery - tf.get_height() // 2))
        else:
            info_txt = font.render("W/S ile hareket et, Tıkla ile ateş et!", True, (150, 150, 180))
            screen.blit(info_txt, (200, 15))

    # Durum Ekranları
    if game_state == "IMLEC_DEAD":
        t = title_font.render("ÖLDÜN!", True, (255, 70, 70))
        sub = font.render("Yeniden denemek için ekrana tıkla", True, TEXT_COLOR)
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 10))

    elif game_state == "IMLEC_WIN":
        t = title_font.render("BÖLÜM TAMAMLANDI!", True, (0, 255, 120))
        sub = font.render("Sonraki level için ekrana tıkla", True, TEXT_COLOR)
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 10))

    elif game_state == "IMLEC_COMPLETE":
        t = title_font.render("TEBRİKLER! TÜM OYUNU BİTİRDİN!", True, (255, 215, 0))
        sub = font.render("Ana menüye dönmek için ekrana tıkla", True, TEXT_COLOR)
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 10))

    elif game_state == "SAVAS_DEAD":
        t = title_font.render("KAYBETTİN!", True, (255, 70, 70))
        sub = font.render(f"Toplam Skorun: {savas_score} - Ana menüye dönmek için tıkla", True, TEXT_COLOR)
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 10))

    pygame.display.flip()

pygame.quit()
sys.exit()

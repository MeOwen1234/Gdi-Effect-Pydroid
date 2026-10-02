# Harmless 15 unique stages + fullscreen + bytebeat
# Each stage looks and sounds different

import pygame
import math
import time
import sys
import array
import random

# ============== CONFIG ==============
STAGE_DURATION = 25
TOTAL_STAGES   = 15
SAMPLE_RATE    = 22050
# ====================================

pygame.mixer.pre_init(SAMPLE_RATE, -16, 1, 1024)
pygame.init()

audio_ok = True
try:
    pygame.mixer.init()
except Exception as e:
    print("Audio failed (running silent):", e)
    audio_ok = False

# ===== FULLSCREEN =====
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Harmless Stages")
clock = pygame.time.Clock()

font_big   = pygame.font.SysFont(None, 70)
font_med   = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 32)

# ---------- Bytebeat (different formulas) ----------
def bytebeat(t, stage):
    t = int(t)
    formulas = [
        lambda t: (t * (t >> 5 | t >> 8)) >> (t >> 16),
        lambda t: t * ((t >> 9 | t >> 13) & 15) & 129,
        lambda t: (t >> 6 | t | t >> (t >> 16)) * 10 + ((t >> 11) & 7),
        lambda t: t * (42 & t >> 10),
        lambda t: (t * (t >> 8 | t >> 9) & 46 & t >> 8) ^ (t & t >> 13 | t >> 6),
        lambda t: t * ((t&4096 and t>>12 or t>>11) ^ t >> 8),
        lambda t: (t>>7|t|t>>6)*10 + 4*(t&t>>13|t>>6),
        lambda t: t*(t>>9|t>>7)&100|t&t>>9|t>>8,
        lambda t: (t*5&(t>>7))|t*3&(t*3>>10),
        lambda t: (t>>6|t|t>>(t>>16))*10+((t>>11)&7),
        lambda t: t*((t>>9|t>>13)&15)&129,
        lambda t: (t*(t>>5|t>>8))>>(t>>16),
        lambda t: t*(42&(t>>10)),
        lambda t: (t*(t>>8|t>>9)&46&t>>8)^(t&t>>13|t>>6),
        lambda t: t*((t&4096 and t>>12 or t>>11)^t>>8),
    ]
    v = formulas[stage % len(formulas)](t)
    return (v & 255) - 128

def make_looping_sound(stage):
    if not audio_ok:
        return None
    try:
        length = SAMPLE_RATE // 2
        buf = array.array('h')
        for i in range(length):
            val = bytebeat(i + stage * 9000, stage) * 100
            val = max(-32767, min(32767, val))
            buf.append(val)
        sound = pygame.mixer.Sound(buffer=buf)
        sound.set_volume(0.32)
        return sound
    except Exception as e:
        print("Sound error:", e)
        return None

# ---------- 15 UNIQUE VISUAL PAYLOADS ----------
def payload_0(elapsed, stage):  # Plasma waves
    for y in range(0, HEIGHT, 4):
        for x in range(0, WIDTH, 4):
            v = math.sin(x*0.02 + elapsed) + math.sin(y*0.03 + elapsed*1.3) + math.sin((x+y)*0.015 + elapsed*0.7)
            c = int(128 + 127 * v / 3)
            col = ((c + 40) % 255, (c * 2) % 255, (255 - c) % 255)
            pygame.draw.rect(screen, col, (x, y, 4, 4))

def payload_1(elapsed, stage):  # Expanding circles
    cx, cy = WIDTH//2, HEIGHT//2
    for i in range(1, 40):
        r = int((elapsed * 80 + i * 25) % (max(WIDTH, HEIGHT)))
        col = ((i*20 + int(elapsed*50)) % 255, (i*40) % 255, (255 - i*15) % 255)
        pygame.draw.circle(screen, col, (cx, cy), r, 3)

def payload_2(elapsed, stage):  # Matrix rain style
    for x in range(0, WIDTH, 18):
        for y in range(0, HEIGHT, 22):
            if random.random() < 0.15:
                bright = random.randint(80, 255)
                col = (0, bright, 0)
                char = random.choice("01アイウエオカキクケコ")
                txt = font_small.render(char, True, col)
                screen.blit(txt, (x, (y + int(elapsed*120)) % HEIGHT))

def payload_3(elapsed, stage):  # Rotating spiral
    cx, cy = WIDTH//2, HEIGHT//2
    for i in range(300):
        angle = i * 0.2 + elapsed * 2
        r = i * 1.8
        x = cx + int(r * math.cos(angle))
        y = cy + int(r * math.sin(angle))
        col = ((i*3) % 255, (i*5 + 50) % 255, (255 - i) % 255)
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            pygame.draw.circle(screen, col, (x, y), 3)

def payload_4(elapsed, stage):  # Color bars + wave
    for y in range(HEIGHT):
        wave = int(40 * math.sin(y*0.03 + elapsed*3))
        col = ((y*2 + int(elapsed*80)) % 255, (y + 100) % 255, (255 - y) % 255)
        pygame.draw.line(screen, col, (0, y), (WIDTH//2 + wave, y), 2)
        pygame.draw.line(screen, col, (WIDTH, y), (WIDTH//2 - wave, y), 2)

def payload_5(elapsed, stage):  # Bouncing squares
    for i in range(25):
        x = int((math.sin(elapsed*1.5 + i) * 0.5 + 0.5) * (WIDTH - 60))
        y = int((math.cos(elapsed*1.2 + i*0.7) * 0.5 + 0.5) * (HEIGHT - 60))
        size = 30 + int(20 * math.sin(elapsed*3 + i))
        col = ((i*30) % 255, (i*50 + 80) % 255, (255 - i*20) % 255)
        pygame.draw.rect(screen, col, (x, y, size, size))

def payload_6(elapsed, stage):  # Tunnel effect
    cx, cy = WIDTH//2, HEIGHT//2
    for i in range(60, 0, -1):
        r = int(i * 12 + elapsed * 40) % 400
        col = ((i*8) % 255, (i*12) % 255, (255 - i*6) % 255)
        pygame.draw.circle(screen, col, (cx, cy), r, 4)

def payload_7(elapsed, stage):  # Horizontal glitch lines
    for i in range(40):
        y = random.randint(0, HEIGHT)
        h = random.randint(2, 12)
        col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        pygame.draw.rect(screen, col, (0, y, WIDTH, h))
    # moving noise blocks
    for _ in range(15):
        x = random.randint(0, WIDTH-50)
        y = int((elapsed*90 + random.randint(0,200)) % HEIGHT)
        pygame.draw.rect(screen, (255,255,255), (x, y, 50, 8))

def payload_8(elapsed, stage):  # Starfield zoom
    cx, cy = WIDTH//2, HEIGHT//2
    for i in range(150):
        angle = i * 0.1
        dist = ((elapsed * 80 + i * 17) % 500)
        x = cx + int(dist * math.cos(angle))
        y = cy + int(dist * math.sin(angle))
        size = max(1, int(dist / 40))
        col = (200, 220, 255) if i % 3 else (255, 180, 100)
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            pygame.draw.circle(screen, col, (x, y), size)

def payload_9(elapsed, stage):  # Checker + wave distortion
    size = 40
    for y in range(0, HEIGHT, size):
        for x in range(0, WIDTH, size):
            wave = int(15 * math.sin(x*0.02 + elapsed*2) * math.cos(y*0.02 + elapsed))
            if ((x//size) + (y//size)) % 2 == 0:
                col = (30 + wave, 30, 80 + wave)
            else:
                col = (200, 50 + wave, 100)
            pygame.draw.rect(screen, col, (x, y, size, size))

def payload_10(elapsed, stage):  # Plasma balls
    for i in range(12):
        x = int(WIDTH/2 + math.sin(elapsed*1.1 + i)*WIDTH*0.4)
        y = int(HEIGHT/2 + math.cos(elapsed*0.9 + i*0.8)*HEIGHT*0.4)
        r = 40 + int(30 * math.sin(elapsed*3 + i))
        for rad in range(r, 0, -8):
            c = int(255 * (rad / r))
            col = (c, (c + i*20) % 255, 255 - c)
            pygame.draw.circle(screen, col, (x, y), rad)

def payload_11(elapsed, stage):  # Vertical scanlines + color shift
    for x in range(0, WIDTH, 3):
        col = ((x + int(elapsed*100)) % 255, (x*2) % 255, (255 - x) % 255)
        pygame.draw.line(screen, col, (x, 0), (x, HEIGHT), 2)
    # moving bright bar
    by = int((elapsed * 150) % HEIGHT)
    pygame.draw.rect(screen, (255, 255, 255), (0, by, WIDTH, 6))

def payload_12(elapsed, stage):  # Flower / mandala
    cx, cy = WIDTH//2, HEIGHT//2
    for i in range(8):
        angle = elapsed * 1.5 + i * (math.pi/4)
        for r in range(20, 280, 15):
            x = cx + int(r * math.cos(angle + r*0.02))
            y = cy + int(r * math.sin(angle + r*0.02))
            col = ((i*40 + r) % 255, (i*60) % 255, (255 - r) % 255)
            pygame.draw.circle(screen, col, (x, y), 6)

def payload_13(elapsed, stage):  # Noise static + flashes
    for _ in range(800):
        x = random.randint(0, WIDTH-1)
        y = random.randint(0, HEIGHT-1)
        c = random.randint(0, 255)
        screen.set_at((x, y), (c, c, c))
    if int(elapsed * 4) % 7 == 0:
        screen.fill((255, 255, 255))

def payload_14(elapsed, stage):  # Final dramatic: big expanding rings + text
    cx, cy = WIDTH//2, HEIGHT//2
    for i in range(20):
        r = int((elapsed * 60 + i * 30) % 600)
        col = (255, 50 + i*10, 50)
        pygame.draw.circle(screen, col, (cx, cy), r, 5)
    txt = font_big.render("FINAL STAGE", True, (255, 80, 80))
    screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 40))

payloads = [
    payload_0, payload_1, payload_2, payload_3, payload_4,
    payload_5, payload_6, payload_7, payload_8, payload_9,
    payload_10, payload_11, payload_12, payload_13, payload_14
]

def draw_stage(stage, elapsed):
    screen.fill((0, 0, 0))
    # Call the unique payload for this stage
    payloads[stage](elapsed, stage)

    # Overlay info (semi-transparent look)
    title = font_big.render(f"STAGE {stage+1}/{TOTAL_STAGES}", True, (0, 255, 180))
    screen.blit(title, (20, 20))

    remaining = max(0.0, STAGE_DURATION - elapsed)
    time_txt = font_med.render(f"{remaining:.1f}s", True, (200, 220, 255))
    screen.blit(time_txt, (WIDTH - time_txt.get_width() - 20, 25))

    if stage == TOTAL_STAGES - 1:
        msg = font_small.render("Last stage – will exit automatically", True, (255, 100, 100))
        screen.blit(msg, (20, HEIGHT - 40))

    pygame.display.flip()

def main():
    current_stage = 0
    stage_start = time.time()
    channel = None

    current_sound = make_looping_sound(current_stage)
    if current_sound:
        channel = current_sound.play(loops=-1)

    running = True
    while running and current_stage < TOTAL_STAGES:
        now = time.time()
        elapsed = now - stage_start

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_AC_BACK):
                    running = False

        draw_stage(current_stage, elapsed)

        if elapsed >= STAGE_DURATION:
            if channel:
                channel.stop()
            current_stage += 1
            if current_stage >= TOTAL_STAGES:
                break
            stage_start = time.time()
            current_sound = make_looping_sound(current_stage)
            if current_sound:
                channel = current_sound.play(loops=-1)

        clock.tick(30)

    # End screen
    if channel:
        channel.stop()
    screen.fill((0, 0, 0))
    end = font_big.render("END – Demo finished", True, (0, 255, 120))
    screen.blit(end, (WIDTH//2 - end.get_width()//2, HEIGHT//2 - 30))
    pygame.display.flip()
    time.sleep(2.5)

    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()
        input("Press Enter to close...")
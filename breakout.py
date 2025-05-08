import pygame
import random
import sys # Nepieciešams, lai korekti aizvērtu programmu

# --- Konstantes ---
# Ekrāna izmēri
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Krāsas (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)

# Lāpstiņas (paddle) parametri
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8

# Bumbiņas (ball) parametri
BALL_RADIUS = 8 # Izmantosim kvadrātu, lai vieglāk ar Rect
BALL_SPEED_X_INITIAL = 4
BALL_SPEED_Y_INITIAL = -4 # Sākumā kustas uz augšu

# Ķieģeļu (brick) parametri
BRICK_WIDTH = 70
BRICK_HEIGHT = 20
BRICK_PADDING = 5
BRICK_OFFSET_TOP = 50
BRICK_OFFSET_LEFT = 30

# --- Spēles objekti ---

# Lāpstiņa
# pygame.Rect(left, top, width, height)
paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

# Bumbiņa
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x = BALL_SPEED_X_INITIAL
ball_speed_y = BALL_SPEED_Y_INITIAL

# Ķieģeļu saraksts
bricks = []
brick_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, CYAN, PINK] # Dažādas krāsas ķieģeļiem

# --- Spēles mainīgie ---
score = 0
current_level = 1
max_levels = 3 # Cik līmeņu kopā būs
game_over = False
game_won = False
level_complete = False

# --- Funkcijas ---

def create_bricks(level):
    """Ģenerē ķieģeļu sarakstu atkarībā no līmeņa."""
    bricks.clear() # Notīra iepriekšējā līmeņa ķieģeļus
    rows = 0
    cols = (SCREEN_WIDTH - 2 * BRICK_OFFSET_LEFT) // (BRICK_WIDTH + BRICK_PADDING)

    if level == 1:
        rows = 4
        for row in range(rows):
            for col in range(cols):
                brick_x = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
                brick_y = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
                color_index = row % len(brick_colors) # Piešķir krāsu atkarībā no rindas
                brick_rect = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
                bricks.append({"rect": brick_rect, "color": brick_colors[color_index]})

    elif level == 2:
        rows = 6
        for row in range(rows):
            # Veidojam šaha galdiņa rakstu
            start_col = 0 if row % 2 == 0 else 1
            for col in range(start_col, cols, 2): # Katru otro ķieģeli
                brick_x = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
                brick_y = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
                color_index = (row + col) % len(brick_colors) # Citādāka krāsu loģika
                brick_rect = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
                bricks.append({"rect": brick_rect, "color": brick_colors[color_index]})

    elif level == 3:
        rows = 7
        # Veidojam piramīdas vai citu formu
        for row in range(rows):
            bricks_in_row = cols - row # Mazāk ķieģeļu augstākās rindās
            start_offset = (cols - bricks_in_row) * (BRICK_WIDTH + BRICK_PADDING) // 2
            for col in range(bricks_in_row):
                 brick_x = BRICK_OFFSET_LEFT + start_offset + col * (BRICK_WIDTH + BRICK_PADDING)
                 brick_y = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
                 color_index = row % len(brick_colors)
                 brick_rect = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
                 bricks.append({"rect": brick_rect, "color": brick_colors[color_index]})

def reset_ball_and_paddle():
    """Atiestata bumbiņas un lāpstiņas pozīciju."""
    global ball_speed_x, ball_speed_y
    paddle.x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
    paddle.y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
    ball.x = SCREEN_WIDTH // 2 - BALL_RADIUS
    ball.y = SCREEN_HEIGHT // 2 - BALL_RADIUS # Sākt tuvāk centram nākamajos līmeņos
    # Nedaudz pamaina ātrumu, lai nav vienādi
    ball_speed_x = random.choice([BALL_SPEED_X_INITIAL, -BALL_SPEED_X_INITIAL])
    ball_speed_y = BALL_SPEED_Y_INITIAL

def draw_text(surface, text, size, x, y, color=WHITE):
    """Uzzīmē tekstu uz ekrāna."""
    font = pygame.font.Font(pygame.font.match_font('arial'), size) # Izmanto noklusēto Arial fontu
    text_surface = font.render(text, True, color) # True nozīmē anti-aliasing
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# --- Spēles inicializācija ---
pygame.init() # Inicializē visas pygame moduļus
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Izveido spēles logu
pygame.display.set_caption("Breakout (bez attēliem)") # Loga virsraksts
clock = pygame.time.Clock() # Pulkstenis, lai kontrolētu FPS

# Izveido pirmā līmeņa ķieģeļus
create_bricks(current_level)

# --- Galvenais spēles cikls ---
running = True
while running:
    # --- Notikumu apstrāde ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Ja lietotājs nospiež aizvēršanas pogu
            running = False
            # Pievienots sys.exit(), lai izvairītos no kļūdām dažās vidēs
            pygame.quit()
            sys.exit()

    if not game_over and not game_won and not level_complete:
        # --- Spēlētāja ievade ---
        keys = pygame.key.get_pressed() # Nolasa nospiestos taustiņus
        if keys[pygame.K_LEFT]:
            paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT]:
            paddle.x += PADDLE_SPEED

        # Neļauj lāpstiņai iziet ārpus ekrāna
        if paddle.left < 0:
            paddle.left = 0
        if paddle.right > SCREEN_WIDTH:
            paddle.right = SCREEN_WIDTH

        # --- Spēles loģikas atjaunināšana ---
        # Bumbiņas kustība
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Sadursmes ar sienām
        if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
            ball_speed_x *= -1 # Maina horizontālo virzienu
        if ball.top <= 0:
            ball_speed_y *= -1 # Maina vertikālo virzienu
        if ball.bottom >= SCREEN_HEIGHT:
            # Spēle zaudēta
            game_over = True

        # Sadursme ar lāpstiņu
        if ball.colliderect(paddle):
            # Pārbauda, vai bumbiņa nāk no augšas (lai nesprūstu lāpstiņā)
            if ball_speed_y > 0:
                 ball_speed_y *= -1
                 # Nedaudz pielāgo bumbiņas pozīciju, lai tā būtu virs lāpstiņas
                 ball.bottom = paddle.top

                 # (Pēc izvēles) Maina x ātrumu atkarībā no trāpījuma vietas uz lāpstiņas
                 delta_x = ball.centerx - paddle.centerx
                 ball_speed_x = ball_speed_x + delta_x * 0.1 # Jo tālāk no centra, jo lielāka izmaiņa
                 # Ierobežo max x ātrumu
                 ball_speed_x = max(-abs(BALL_SPEED_X_INITIAL * 1.5), min(abs(BALL_SPEED_X_INITIAL * 1.5), ball_speed_x))


        # Sadursmes ar ķieģeļiem
        brick_to_remove = None
        for brick_item in bricks:
            brick_rect = brick_item["rect"]
            if ball.colliderect(brick_rect):
                brick_to_remove = brick_item
                ball_speed_y *= -1 # Vienkāršākais veids - vienmēr maina Y virzienu
                score += 10 # Pievieno punktus par ķieģeļa izsišanu
                break # Apstrādā tikai vienu ķieģeli vienā kadrā

        if brick_to_remove:
            bricks.remove(brick_to_remove) # Noņem izsisto ķieģeli no saraksta

        # Pārbauda, vai līmenis ir pabeigts
        if not bricks:
            if current_level < max_levels:
                level_complete = True
            else:
                game_won = True # Visi līmeņi pabeigti

    # --- Zīmēšana / Renderēšana ---
    screen.fill(BLACK) # Aizpilda fonu ar melnu krāsu

    # Zīmē lāpstiņu
    pygame.draw.rect(screen, BLUE, paddle)

    # Zīmē bumbiņu
    pygame.draw.ellipse(screen, WHITE, ball) # Zīmē kā apli (ellipse ar vienādiem rādiusiem)

    # Zīmē ķieģeļus
    for brick_item in bricks:
        pygame.draw.rect(screen, brick_item["color"], brick_item["rect"])

    # Zīmē punktus un līmeni
    draw_text(screen, f"Punkti: {score}", 24, SCREEN_WIDTH // 2, 10)
    draw_text(screen, f"Līmenis: {current_level}", 24, 80, 10)

    # --- Paziņojumi par spēles stāvokli ---
    if level_complete:
        draw_text(screen, f"LĪMENIS {current_level} PABEIGTS!", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        draw_text(screen, "Nospied jebkuru taustiņu, lai turpinātu", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)
        pygame.display.flip() # Parāda paziņojumu
        # Gaida taustiņa nospiešanu, lai sāktu nākamo līmeni
        waiting = True
        while waiting:
             clock.tick(60) # Lai nepatērētu pārāk daudz resursu gaidot
             for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                      running = False
                      waiting = False
                      pygame.quit()
                      sys.exit()
                  if event.type == pygame.KEYDOWN:
                      current_level += 1
                      create_bricks(current_level)
                      reset_ball_and_paddle()
                      level_complete = False
                      waiting = False

    if game_over:
        draw_text(screen, "SPĒLE BEIGUSIES!", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, RED)
        draw_text(screen, f"Tavs rezultāts: {score}", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, WHITE)
        draw_text(screen, "Aizver logu, lai izietu.", 20, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, WHITE)

    if game_won:
        draw_text(screen, "APSVEICAM! TU UZVARĒJI!", 55, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, GREEN)
        draw_text(screen, f"Gala rezultāts: {score}", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, WHITE)
        draw_text(screen, "Aizver logu, lai izietu.", 20, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, WHITE)


    # Atjaunina ekrānu (parāda visu uzzīmēto)
    if running: # Pārbauda, vai cikls vēl darbojas pirms flip
        pygame.display.flip()

    # Kontrolē kadru skaitu sekundē (FPS)
    clock.tick(60) # Mēģina uzturēt 60 kadrus sekundē

# --- Spēles beigas ---
# pygame.quit() tiek izsaukts jau notikumu cilpā vai gaidīšanas cilpā

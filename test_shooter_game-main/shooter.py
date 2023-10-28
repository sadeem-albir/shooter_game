import pygame
import random
pygame.init()


WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("video game")

clock = pygame.time.Clock()
FPS = 60
player_width, player_height = 100, 25
bullet_width, bullet_height = 8, 16
enemy_width, enemy_height = 50, 50
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 127, 0)
GREEN = (0, 255, 0)
PURPLE = (0, 100, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
CYAN = (165, 217, 228, 255)
font = pygame.font.SysFont('comicsans', 30)

click_sound = pygame.mixer.Sound(
    '/home/sadeem-albir/TheGame/test_shooter_game-main/click.mp3')
shoot_sound = pygame.mixer.Sound(
    '/home/sadeem-albir/TheGame/test_shooter_game-main/shoot.mp3')
bang_sound = pygame.mixer.Sound(
    '/home/sadeem-albir/TheGame/test_shooter_game-main/boom.mp3')
# shoot_sound.set_volume(0.25)


class Player:
    vel = 15

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y,
                                           self.width, self.height))

    def self_drive(self, enemy):
        if self.x + (self.width/2) > enemy.x + (enemy.width/2):
            self.x -= self.vel
        if self.x + (self.width/2) < enemy.x + (enemy.width/2):
            self.x += self.vel


class Scope:
    def __init__(self, color, owner):
        self.x = owner.x + (owner.width/2)
        self.y = HEIGHT / 2
        self.radius = owner.width / 2
        self.color = color

    def move(self, owner):
        self.x = owner.x + (owner.width/2)

    def position(self, target):
        global scoped_in
        if self.x >= target.x and self.x <= target.x + target.width:
            self.y = target.y + (target.height/2)
            scoped_in = True
        else:
            self.y = HEIGHT / 2
            scoped_in = False

    def draw(self, win):
        pygame.draw.circle(
            win, self.color, (self.x, self.y), self.radius, 1)
        pygame.draw.line(win, self.color, (self.x - self.radius,
                                           self.y), (self.x + self.radius, self.y), 1)
        pygame.draw.line(win, self.color, (self.x,
                                           self.y - self.radius), (self.x, self.y + self.radius), 1)


class Bullet:
    vel = 50

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, YELLOW, (self.x, self.y,
                                       self.width, self.height/4))

    def move(self):
        if 0 <= self.y <= HEIGHT:
            self.y -= self.vel


class Enemy:
    vel = 2

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))

    def collision(self, rocket):
        if rocket.x + rocket.width >= self.x and rocket.x <= self.x + self.width:
            if rocket.y >= self.y and rocket.y <= self.y + self.height:
                return True


class Button:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def hover_click(self, mouse, color, color2, action_type, identify):
        global control_settings
        global game_functions
        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
            self.color = color2
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    click_sound.play()
                    if identify == "control":
                        control_settings = action_type
                        self.color = color2
                    elif identify == "game":
                        game_functions = action_type
        else:
            self.color = color

    def draw(self, win, input):
        font = pygame.font.SysFont('comicsans', 30, True)
        text = font.render(input, 1, BLACK)
        self.width, self.height = text.get_width(), text.get_height()
        pygame.draw.rect(
            win, self.color, (self.x, self.y, text.get_width(), text.get_height()))
        win.blit(text, (self.x, self.y))


def draw(win):
    mouse_pos = pygame.mouse.get_pos()
    global condition_met
    global click_stack
    win.fill(CYAN)
    txt_rocket_count = font.render(
        f"Rockets: {len(bullets)}", 1, WHITE)
    txt_rocket_speed = font.render(
        f"Velocity: {Bullet.vel}", 1, WHITE)
    txt_cool_down = font.render(
        f"Cool-down: {cool_down_limit}", 1, WHITE)
    txt_kills = font.render(f"Kills: {kills}", 1, WHITE)
    txt_spawn_rate = font.render(
        f"Enemies: {enemies_remaining}", 1, WHITE)
    win.blit(txt_rocket_count,
             (WIDTH - txt_rocket_count.get_width() - 15, HEIGHT/2.5))
    win.blit(txt_rocket_speed,
             (WIDTH - txt_rocket_speed.get_width() - 15, HEIGHT/2.2))
    win.blit(txt_cool_down,
             (WIDTH - txt_cool_down.get_width() - 15, HEIGHT/1.9))
    win.blit(txt_kills, (WIDTH - txt_kills.get_width() - 15, HEIGHT/1.6))
    win.blit(txt_spawn_rate,
             (WIDTH - txt_spawn_rate.get_width() - 15, HEIGHT/1.3))
    player.draw(win)
    ai_mode_button.draw(win, f"AI Mode {switch}")
    ai_mode_button.hover_click(
        mouse_pos, ai_mode_color, ai_mode_color, "ai_mode", "game")
    mouse_activate_button.draw(win, "Mouse")
    mouse_activate_button.hover_click(
        mouse_pos, GREEN, YELLOW, "mouse", "control")
    keyboard_activate_button.draw(win, "Keyboard")
    keyboard_activate_button.hover_click(
        mouse_pos, GREEN, YELLOW, "keyboard", "control")
    velocity_button_inc.draw(win, "Speed Up")
    velocity_button_inc.hover_click(
        mouse_pos, BLUE, YELLOW, "speed +", "game")
    velocity_button_dec.draw(win, "Slow Down")
    velocity_button_dec.hover_click(
        mouse_pos, BLUE, YELLOW, "speed -", "game")
    cool_down_button_inc.draw(win, "Cool Down +")
    cool_down_button_inc.hover_click(
        mouse_pos, BLUE, YELLOW, "cool_down +", "game")
    cool_down_button_dec.draw(win, "Cool Down -")
    cool_down_button_dec.hover_click(
        mouse_pos, BLUE, YELLOW, "cool_down -", "game")
    for bullet in bullets:
        bullet.draw(win)
    for enemy in enemies:
        enemy.draw(win)
    scope.draw(win)
    pygame.display.update()


switch = "OFF"
ai_mode_color = RED
player = Player(WIDTH/2-player_width/2, HEIGHT * 7 /
                8, player_width, player_height, WHITE)
scope = Scope(BLACK, player)
scoped_in = False
ai_mode = False
ai_mode_button = Button((6.5/8) * WIDTH, 20 + player_height *
                        4, player_width, player_height * 2, PURPLE)
mouse_activate_button = Button(
    20, 20, player_width, player_height * 2, GREEN)
keyboard_activate_button = Button(
    20, 20 + player_height, player_width, player_height * 2, GREEN)
velocity_button_inc = Button(
    6.5/8 * WIDTH, 20, player_width, player_height * 2, BLUE)
velocity_button_dec = Button(
    6.5/8 * WIDTH, 20 + player_height, player_width, player_height * 2, BLUE)
cool_down_button_inc = Button(
    6.5/8 * WIDTH, 20 + player_height*2, player_width, player_height*2, BLUE)
cool_down_button_dec = Button(
    6.5/8 * WIDTH, 20 + player_height * 3, player_width, player_height*2, BLUE)
bullets = []
enemies = []
enemies.append(Enemy(random.choice(range(
    10, WIDTH - enemy_width - (HEIGHT//8))), -enemy_height, enemy_width, enemy_height, RED))
shoot_cool_down = 0
spawn_cool_down = 0
spawn_rate = 7
spawn_count = 1
spawn_max = 30
enemies_remaining = spawn_max
spawn_delta = 1
kills = 0
cool_down_limit = 20
control_settings = "keyboard"
game_functions = "none"
run = True
while run:
    clock.tick(FPS)

    if shoot_cool_down > 0:
        shoot_cool_down += 1
    if shoot_cool_down > cool_down_limit:
        shoot_cool_down = 0

    if spawn_cool_down > 0:
        spawn_cool_down += 1
    if spawn_cool_down > spawn_rate:
        spawn_cool_down = 0

    draw(WIN)

    key = pygame.key.get_pressed()

    if len(enemies) == 0:
        scope.y = HEIGHT / 2
        scoped_in = False

    if ai_mode:
        for enemy in enemies:
            player.self_drive(enemy)
        if scoped_in and shoot_cool_down == 0:
            bullets.append(Bullet(player.x + player.width/2 - bullet_width/2, player.y -
                                  bullet_height, bullet_width, bullet_height, ORANGE))
            shoot_sound.play()
            shoot_cool_down = 1
    elif not ai_mode:
        if control_settings == "keyboard":
            if key[pygame.K_LEFT] and player.x - player.vel >= 0:
                player.x -= player.vel
            if key[pygame.K_RIGHT] and player.x + player.width + player.vel <= WIDTH:
                player.x += player.vel
            if key[pygame.K_SPACE] and shoot_cool_down == 0:
                bullets.append(Bullet(player.x + player.width/2 - bullet_width/2, player.y -
                                      bullet_height, bullet_width, bullet_height, ORANGE))
                shoot_sound.play()
                shoot_cool_down = 1
        elif control_settings == "mouse":
            mouse_pos = pygame.mouse.get_pos()
            player.x = mouse_pos[0] - player_width/2
            if pygame.mouse.get_pressed()[2] and shoot_cool_down == 0:
                bullets.append(Bullet(player.x + player.width/2 - bullet_width/2, player.y -
                                      bullet_height, bullet_width, bullet_height, ORANGE))
                shoot_cool_down = 1
                shoot_sound.play()

    if spawn_cool_down == 0 and spawn_count < spawn_max and len(enemies) < 1:
        enemies.append(Enemy(random.choice(range(
            10, WIDTH - enemy_width - (HEIGHT//8))), -enemy_height, enemy_width, enemy_height, RED))
        spawn_cool_down = 1
        spawn_count += 1

    scope.move(player)
    for enemy in enemies:
        scope.position(enemy)
        if -enemy_height <= enemy.y <= HEIGHT:
            enemy.y += enemy.vel
        if -enemy_height > enemy.y or enemy.y > HEIGHT:
            enemies.pop(enemies.index(enemy))

        for bullet in bullets:
            if enemy.collision(bullet):
                pygame.time.delay(10)
                bang_sound.play()
                enemies.pop(enemies.index(enemy))
                enemy.color = RED
                enemy.vel *= -1
                bullets.pop(bullets.index(bullet))
                kills += 1

    if game_functions == "speed +":
        Bullet.vel += 1
        game_functions = "none"
    elif game_functions == "speed -" and Bullet.vel > 1:
        Bullet.vel -= 1
        game_functions = "none"
    elif game_functions == "cool_down +":
        cool_down_limit += 1
        game_functions = "none"
    elif game_functions == "cool_down -" and cool_down_limit > 1:
        cool_down_limit -= 1
        game_functions = "none"
    elif game_functions == "ai_mode":
        if not ai_mode:
            ai_mode = True
            switch = "ON"
            ai_mode_color = GREEN
        elif ai_mode:
            ai_mode = False
            switch = "OFF"
            ai_mode_color = RED
        game_functions = "none"
    for bullet in bullets:
        bullet.move()
        if bullet.y < 0 or bullet.y + bullet_height > HEIGHT:
            bullets.pop(bullets.index(bullet))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()

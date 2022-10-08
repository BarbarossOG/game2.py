import pygame
import random


pygame.init()


# ДЛЯ ОТЛАДКИ, потом убрать
random.seed(10)


# загружаем изображения
player_img = pygame.image.load('resources/img/player.png')
icon_img = pygame.image.load('resources/img/ufo.png')
bullet_img = pygame.image.load('resources/img/bullet.png')
enemy_img = pygame.image.load('resources/img/enemy.png')
background_img = pygame.image.load('resources/img/background.png')
boss_img = pygame.image.load('resources/img/boss.png')


# размеры окна
display_width = 800
display_height = 600
display_size = (display_width, display_height)


# создаем окно
display = pygame.display.set_mode(display_size)
pygame.display.set_caption('Space Invaders')
pygame.display.set_icon(icon_img)


# бэкграунд
background_width = background_img.get_width()
background_height = background_img.get_height()
background_x = 0
background_y = 0


# игрок
player_width = player_img.get_width()
player_height = player_img.get_height()
player_gap = 10
player_x = display_width // 2 - player_width // 2
player_y = display_height - player_height - player_gap
player_speed = 3
player_dx = 0


# Босс
boss_alive = False
boss_width = boss_img.get_width()
boss_height = boss_img.get_height()
boss_x, boss_y = 0, 0
boss_dx, boss_dy = 0, 0


# пуля
bullet_alive = False
bullet_width = bullet_img.get_width()
bullet_height = bullet_img.get_height()
bullet_x, bullet_y = 0, 0
bullet_dy = 7

# враг
enemy_alive = False
enemy_width = enemy_img.get_width()
enemy_height = enemy_img.get_height()
enemy_x, enemy_y = 0, 0
enemy_dx, enemy_dy = 0, 0

# game over
game_over_status = False

# обновление моделей
def player_update():
    global player_x
    player_x += player_dx  # player_x = player_x + player_dx
    # не дадим игроку выходить за пределы окна
    if player_x < 0:
        player_x = 0
    if player_x > display_width - player_width:
        player_x = display_width - player_width


def bullet_update():
    global bullet_y
    if not bullet_alive:
        return
    bullet_y -= bullet_dy


def collision_enemy(x, y, width, height):
    """враг столкнулся с указанным объектом (передан прямоугольник)"""
    rect_enemy = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    rect_other = pygame.Rect(x, y, width, height)
    return rect_enemy.colliderect(rect_other)


def collision_boss(x, y, width, height):
    rect_boss = pygame.Rect(boss_x, boss_y, boss_width, boss_height)
    rect_other = pygame.Rect(x, y, width, height)
    return rect_boss.colliderect(rect_other)


def enemy_update():
    global enemy_alive, enemy_x, enemy_y, enemy_dx, enemy_dy
    if not enemy_alive:
        enemy_x, enemy_y, enemy_dx, enemy_dy = enemy_create()
    enemy_x += enemy_dx
    enemy_y += enemy_dy

    # столкновение с игроком
    if collision_enemy(player_x, player_y, player_width, player_height):
        enemy_alive = False
        game_over()


def boss_update():
    global boss_alive, boss_x, boss_y, boss_dx, boss_dy
    if not boss_alive:
        boss_x, boss_y, boss_dx, boss_dy = boss_create()
    boss_x += boss_dx
    boss_y += boss_dy

    # столкновение с игроком
    if collision_boss(player_x, player_y, player_width, player_height):
        boss_alive = False
        game_over()

def model_update():
    player_update()
    bullet_update()
    enemy_update()
    boss_update()

def bullet_create():
    """Создаем пулю над игроком, она летит вертикально вверх"""
    global bullet_alive
    x = player_x
    y = player_y - bullet_height
    bullet_alive = True
    return x, y

def enemy_create():
    """Создаем врага в случайном месте, он случайно летит наискосок вниз"""
    global enemy_alive
    # x = random.randint(0, display_width)
    x = player_x
    y = 30

    # dx = random.randint(-2, 3)
    # dy = random.randint(1, 3) / 2
    dx = 0
    dy = 1

    enemy_alive = True
    return x, y, dx, dy


def boss_create():
    global boss_alive
    # x = random.randint(0, display_width)
    x = player_x - 300
    y = 30

    # dx = random.randint(-2, 3)
    # dy = random.randint(1, 3) / 2
    dx = 0
    dy = 0.2
    boss_alive = True
    return x, y, dx, dy



def game_over():
    global game_over_status
    game_over_status = True


# перерисовки
def display_redraw():
    display.fill((0, 0, 0), (0, 0, display_width, display_height))
    display.blit(background_img, (background_x, background_y))
    display.blit(player_img, (player_x, player_y))
    if bullet_alive:
        display.blit(bullet_img, (bullet_x, bullet_y))
    if enemy_alive:
        display.blit(enemy_img, (enemy_x, enemy_y))
    if boss_alive:
        display.blit(boss_img, (boss_x, boss_y))
    pygame.display.update()


# события
def event_quit(event):
    return event.type != pygame.QUIT

def event_player(event):
    global player_dx
    # нажали клавишу
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            player_dx = -player_speed
        elif event.key == pygame.K_RIGHT:
            player_dx = player_speed
    # отпустили клавишу
    if event.type == pygame.KEYUP:
        player_dx = 0

def event_bullet(event):
    global bullet_x, bullet_y, bullet_alive
    if event.type == pygame.MOUSEBUTTONDOWN:
        key = pygame.mouse.get_pressed()
        if key[0] and not bullet_alive:
            bullet_x, bullet_y = bullet_create()

def event_process():
    running_status = True
    for event in pygame.event.get():
        running_status = event_quit(event)
        if game_over_status:
            continue
        event_player(event)
        event_bullet(event)
    return running_status


running = True
while running:
    model_update()
    display_redraw()
    running = event_process()





class Boss:
    DEFAULT_DX = 0
    DEFAULT_DY = 0.1
    DEFAULT_Y = 30

    def __init__(self, display_size):
        self.bound_size = self.bound_width, self.bound_height = display_size
        self.img = pygame.image.load(RSC['img']['boss'])
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x, self.y, self.dx, self.dy = self.create_at_random_position()

    def create_at_center(self):
        x = self.bound_width // 2 - self.width // 2
        y = self.DEFAULT_Y
        dx = self.DEFAULT_DX
        dy = self.DEFAULT_DY
        return x, y, dx, dy

    def create_at_random_position(self):
        x = random.randint(0, self.bound_width)
        y = self.DEFAULT_Y
        dx = random.randint(-2, 3) / 10
        dy = random.randint(1, 3) / 20
        return x, y, dx, dy

    def model_update(self):
        self.x += self.dx
        self.y += self.dy

    def rect(self):
        return self.x, self.y, self.width, self.height

    def into_bounds(self):
        bound = pygame.Rect(0, 0, self.bound_width, self.bound_height)
        return bound.contains(self.x, self.y, self.width, self.height)

    def redraw(self, display):
        display.blit(self.img, (self.x, self.y))



        if self.intersection(self.boss, self.bullet):
            self.boss = None
            self.bullet = None

        if self.boss is None:
            self.boss = Boss(self.size)
        self.boss.model_update()
        if not self.boss.into_bounds():
            self.boss = None




        if self.boss:
            self.boss.redraw(display)
import pygame
import sys
import os

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Побег из леса')
FPS = 50
clock = pygame.time.Clock()
pygame.mixer.music.load('mus.mp3')
pygame.mixer.music.play(999, 0.0, 0)


def load_image(name, colorkey=-1):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        # image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


tile_images = {
    'wall': load_image('les.png'),
    'empty': load_image('dirt.png'),
    'emptyend': load_image('end.png'),
    'nonempty': load_image('dirt.png'),
    'nonwall': load_image('les.png'),
    'death': load_image('lava.png')
}
player_image = load_image('hero4.png')

tile_width = tile_height = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ПОБЕГ ИЗ ЛЕСА",
                  "Управление происходит с помощью стрелочек", 'или WASD',
                  "Цель игры:",
                  "Пройти лабиринт, добраться до золотых блоков",
                  'Подсказка: не наступай на лаву, иначе ', 'проиграешь, и не доверяй своим глазам!!!']

    fon = pygame.transform.scale(load_image('fon_les.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def death_screen():
    intro_text = ["Ты попался на ловушку!", "Будь осторожней в следующий раз", '', 'ИГРА ОКОНЧЕНА']

    fon = pygame.transform.scale(load_image('death_fon1.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    intro_text = ["Ты сбежал из леса!", "", '', '', 'Конец игры']

    fon = pygame.transform.scale(load_image('end_fon3.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        camera.dx -= tile_width * (x - self.pos[0])
        camera.dy -= tile_height * (y - self.pos[1])
        self.pos = (x, y)
        for sprite in sprite_group:
            camera.apply(sprite)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.abs_pos[0] + self.dx
        obj.rect.y = obj.abs_pos[1] + self.dy

    def update(self, target):
        self.dx = 0
        self.dy = 0


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == 'g':
                Tile('emptyend', x, y)
            elif level[y][x] == 'l':
                Tile('death', x, y)
            elif level[y][x] == 'n':
                Tile('nonempty', x, y)
            elif level[y][x] == 's':
                Tile('nonwall', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def move(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and (level_map[y - 1][x] == '@' or level_map[y - 1][x] == '.' or level_map[y - 1][x] == 'g' or
                      level_map[y - 1][x] == 's' or level_map[y - 1][x] == 'l'):
            hero.move(x, y - 1)
            if y > 0 and level_map[y - 1][x] == 'l':
                death_screen()
            elif y > 0 and level_map[y - 1][x] == 'g':
                end_screen()
    elif movement == 'down':
        if y < max_y and (level_map[y + 1][x] == '@' or level_map[y + 1][x] == '.' or
                          level_map[y + 1][x] == 's' or level_map[y + 1][x] == 'l' or
                          level_map[y + 1][x] == 'g'):
            hero.move(x, y + 1)
            if y < max_y and level_map[y + 1][x] == 'l':
                death_screen()
            elif y < max_y and level_map[y + 1][x] == 'g':
                end_screen()
    elif movement == 'left':
        if x > 0 and (level_map[y][x - 1] == '.' or level_map[y][x - 1] == '@' or
                      level_map[y][x - 1] == 's' or level_map[y][x - 1] == 'l' or
                      level_map[y][x - 1] == 'g'):
            hero.move(x - 1, y)
            if x > 0 and level_map[y][x - 1] == 'l':
                death_screen()
            elif x > 0 and level_map[y][x - 1] == 'g':
                end_screen()
    elif movement == 'right':
        if x < max_x and (level_map[y][x + 1] == '.' or level_map[y][x + 1] == '@' or
                          level_map[y][x + 1] == 's' or level_map[y][x + 1] == 'l' or
                          level_map[y][x + 1] == 'g'):
            hero.move(x + 1, y)
            if x < max_x and level_map[y][x + 1] == 'l':
                death_screen()
            elif x < max_x and level_map[y][x + 1] == 'g':
                end_screen()


# группы спрайтов
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
# player_group = pygame.sprite.Group()
start_screen()
camera = Camera()
level_map = load_level('map2.txt')
# print(level_map)

running = True
player, max_x, max_y = generate_level(load_level('map2.txt'))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                move(player, 'up')
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                move(player, 'down')
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move(player, 'left')
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move(player, 'right')
    screen.fill((71, 167, 106))
    sprite_group.draw(screen)
    hero_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()

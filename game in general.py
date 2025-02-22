import os
import sys
import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, app, pos):
        self.app = app
        super().__init__(app.player_group, app.all_sprites)
        self.image = self.app.load_image("mar.png")
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.rect = self.image.get_rect().move(
            self.app.tile_width * pos[0] + 15, self.app.tile_height * pos[1] + 5)

    def update(self, pos):
        if (0 <= self.rect.x + pos[0] <= self.app.width) and (0 <= self.rect.y + pos[1] <= self.app.height):
            self.rect.x += pos[0]
            self.rect.y += pos[1]
        if pygame.sprite.spritecollideany(self, self.app.tiles_group):
            self.rect.x -= pos[0]
            self.rect.y -= pos[1]

class Tile(pygame.sprite.Sprite):
    def __init__(self, app, tile_type, pos_x, pos_y):
        super().__init__(app.all_sprites)
        tile_images = {
            'wall': app.load_image('box.png'),
            'empty': app.load_image('grass.png')
        }
        tile_width = tile_height = 50
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class App:
    def __init__(self):
        pygame.init()
        self.width, self.height = 600, 600
        self.game_over = 0
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Mario')
        self.fps = 15
        self.tile_width = self.tile_height = 50
        pygame.key.set_repeat(200, 70)
        self.n = 1

    def terminate(self):
        pygame.quit()
        sys.exit()

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def run_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.hero, level_x, level_y = self.generate_level(self.load_level(f'data/map{self.n}.txt'))
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.game_over += 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.n += 1
                    self.run_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.hero.update((0, self.tile_height))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.hero.update((0, -self.tile_height))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.hero.update((self.tile_width, 0))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.hero.update((-self.tile_width, 0))
            if self.game_over == 5:
                self.start_screen()
                run = False
            # update

            # render
            self.screen.fill(pygame.Color('blue'))
            self.all_sprites.draw(self.screen)
            self.player_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)

    def start_screen(self):
        intro_text = ["ЗАСТАВКА", "",
                      "Правила игры",
                      "Если в правилах несколько строк,",
                      "приходится выводить их построчно",
                      "Чтобы сменить уровень, нажмите пробел"]

        fon = pygame.transform.scale(self.load_image('fon.jpg'), (self.width, self.height))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            self.clock.tick(self.fps)

    def load_level(self, filename):
        try:
            # читаем уровень, убирая символы перевода строки
            with open(filename, 'r') as mapFile:
                level_map = [line.strip() for line in mapFile]

            # и подсчитываем максимальную длину
            max_width = max(map(len, level_map))

            # дополняем каждую строку пустыми клетками ('.')
            return list(map(lambda x: x.ljust(max_width, '.'), level_map))
        except FileNotFoundError:
            print('Уровни закончились')
            sys.exit()

    def generate_level(self, level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile(self, 'empty', x, y)
                elif level[y][x] == '#':
                    self.tiles_group.add(Tile(self, 'wall', x, y))
                elif level[y][x] == '@':
                    Tile(self, 'empty', x, y)
                    new_player = Hero(self, (x, y))
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y


if __name__ == '__main__':
    app = App()
    app.run_game()

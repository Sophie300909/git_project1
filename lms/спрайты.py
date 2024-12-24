import pygame
import os
import sys


def load_image(name, colorkey=None):
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


class Arrow(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('arrow.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, *pos):
        if pos:
            self.rect.x = pos[0][0]
            self.rect.y = pos[0][1]


def main():
    pygame.init()
    size = 500, 300
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 60

    arrows = pygame.sprite.Group()
    arrow = Arrow(arrows)
    running = True
    while running:
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                arrow.update(event.pos)
        screen.fill((255, 255, 255))
        if pygame.mouse.get_focused():
            arrows.draw(screen)
        arrows.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
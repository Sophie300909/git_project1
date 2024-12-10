import pygame
pygame.init()


screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption('Кирпичи')


def draw():
    for i in range(10):
        pygame.draw.rect(screen, pygame.Color('#ff0000'), (i * 30 + 2, 0, 30, 15))


draw()
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
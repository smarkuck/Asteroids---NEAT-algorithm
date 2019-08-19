import pygame
from resolution import *
from ship import Ship

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
done = False

clock = pygame.time.Clock()
ship = Ship(pygame.math.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), SHORT_SIDE * 0.1)

bullets = []

while not done:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullets.append(ship.shoot())

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]: ship.rotateLeft()
    if pressed[pygame.K_RIGHT]: ship.rotateRight()
    if pressed[pygame.K_UP]: ship.boost()

    ship.update()
    for bullet in bullets:
        bullet.update()
        if bullet.life <= 0: bullets.remove(bullet)

    screen.fill((0, 0, 0))
    ship.draw(screen)
    for bullet in bullets: bullet.draw(screen)

    pygame.display.flip()
    clock.tick(60)

import pygame
import colors
from resolution import *
from ship import Ship
from asteroid import Asteroid
from collision_system import CollisionSystem

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
done = False

clock = pygame.time.Clock()
ship = Ship(pygame.math.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), SHORT_SIDE * 0.1)

bullets = []
asteroids = []
asteroids.append(Asteroid(pygame.math.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT), 3, SHORT_SIDE * 0.1))
asteroids.append(Asteroid(pygame.math.Vector2(0, 0), 3, SHORT_SIDE * 0.1))
asteroids.append(Asteroid(pygame.math.Vector2(0, SCREEN_HEIGHT), 3, SHORT_SIDE * 0.1))
asteroids.append(Asteroid(pygame.math.Vector2(SCREEN_WIDTH, 0), 3, SHORT_SIDE * 0.1))

collisionSystem = CollisionSystem(ship, asteroids, bullets)

while not done:
    bullets[:] = [bullet for bullet in bullets if bullet.alive]
    asteroids[:] = [asteroid for asteroid in asteroids if asteroid.alive]

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
    for bullet in bullets: bullet.update()
    for asteroid in asteroids: asteroid.update()

    collisionSystem.checkCollisions()

    screen.fill(colors.black)
    ship.draw(screen)
    for bullet in bullets: bullet.draw(screen)
    for asteroid in asteroids: asteroid.draw(screen)

    pygame.display.flip()
    clock.tick(60)

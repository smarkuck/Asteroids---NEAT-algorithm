import pygame
import colors
from neat.genome import Genome

from resolution import *
from ship import Ship
from asteroid import Asteroid
from collision_system import CollisionSystem

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
done = False

playerIsHuman = False

clock = pygame.time.Clock()
ship = Ship(pygame.math.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), SHORT_SIDE * 0.1)

bullets = []
asteroids = []
asteroids.append(Asteroid(pygame.math.Vector2(SCREEN_WIDTH/4, SCREEN_HEIGHT/4), 3, SHORT_SIDE * 0.1))
asteroids.append(Asteroid(pygame.math.Vector2(0, 0), 3, SHORT_SIDE * 0.1))
asteroids.append(Asteroid(pygame.math.Vector2(0, SCREEN_HEIGHT), 3, SHORT_SIDE * 0.1))
asteroids.append(Asteroid(pygame.math.Vector2(SCREEN_WIDTH, 0), 3, SHORT_SIDE * 0.1))

collisionSystem = CollisionSystem(ship, asteroids, bullets)

g = Genome(51, 4)
g.connectNodes()

while not done:
    bullets[:] = [bullet for bullet in bullets if bullet.alive]
    asteroids[:] = [asteroid for asteroid in asteroids if asteroid.alive]

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if playerIsHuman and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullets.extend(ship.shoot())

    if playerIsHuman:
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]: ship.rotateLeft()
        if pressed[pygame.K_RIGHT]: ship.rotateRight()
        if pressed[pygame.K_UP]: ship.boost()

    else:
        input = []
        input.extend([ship.position.x/SCREEN_WIDTH, ship.position.y/SCREEN_WIDTH, ship.RADIUS/SCREEN_WIDTH])
        for asteroid in asteroids:
            input.extend([asteroid.position.x/SCREEN_WIDTH, asteroid.position.y/SCREEN_WIDTH, asteroid.RADIUS/SCREEN_WIDTH])

        inputSize = len(input)
        if inputSize < 51:
            toFill = 51 - inputSize
            for i in range(toFill):
                input.append(0)

        output = g.feedforward(input)

        if output[0] > 0.5: bullets.extend(ship.shoot())
        if output[1] > 0.5: ship.rotateLeft()
        if output[2] > 0.5: ship.rotateRight()
        if output[3] > 0.5: ship.boost()

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


import pygame
import colors
from neat.population import Population

from resolution import *
from ship import Ship
from asteroid import Asteroid
from collision_system import CollisionSystem

class Game:
    def __init__(self, genome, isRendered):
        self.score = 0
        self.isRendered = isRendered
        if genome is None:
            self.playerIsHuman = True
        else:
            self.playerIsHuman = False
            self.genome = genome

    @classmethod
    def forHuman(cls):
        return cls(None, True)

    @classmethod
    def forAI(cls, genome, isRendered = True):
        return cls(genome, isRendered)

    def run(self):
        if self.isRendered:
            pygame.init()
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            clock = pygame.time.Clock()

        done = False

        ship = Ship(pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), SHORT_SIDE * 0.1)

        bullets = []
        asteroids = []
        asteroids.append(Asteroid(pygame.math.Vector2(SCREEN_WIDTH * 3/4., SCREEN_HEIGHT * 3/4.), 3, SHORT_SIDE * 0.1))
        asteroids.append(Asteroid(pygame.math.Vector2(SCREEN_WIDTH / 4., SCREEN_HEIGHT / 4.), 3, SHORT_SIDE * 0.1))
        asteroids.append(Asteroid(pygame.math.Vector2(SCREEN_WIDTH / 4., SCREEN_HEIGHT * 3/4.), 3, SHORT_SIDE * 0.1))
        asteroids.append(Asteroid(pygame.math.Vector2(SCREEN_WIDTH * 3/4., SCREEN_HEIGHT / 4.), 3, SHORT_SIDE * 0.1))

        collisionSystem = CollisionSystem(self, ship, asteroids, bullets)

        while not done:
            bullets[:] = [bullet for bullet in bullets if bullet.alive]
            asteroids[:] = [asteroid for asteroid in asteroids if asteroid.alive]

            if len(asteroids) == 0 or not ship.alive:
                done = True

            if self.isRendered:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    if self.playerIsHuman and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        bullets.extend(ship.shoot())

            if self.playerIsHuman:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_LEFT]: ship.rotateLeft()
                if pressed[pygame.K_RIGHT]: ship.rotateRight()
                if pressed[pygame.K_UP]: ship.boost()

            else:
                input = []
                input.extend(
                    [ship.position.x / SCREEN_WIDTH, ship.position.y / SCREEN_WIDTH, ship.RADIUS / SCREEN_WIDTH])
                for asteroid in asteroids:
                    input.extend([asteroid.position.x / SCREEN_WIDTH, asteroid.position.y / SCREEN_WIDTH,
                                  asteroid.RADIUS / SCREEN_WIDTH])

                inputSize = len(input)
                if inputSize < 51:
                    toFill = 51 - inputSize
                    for i in range(toFill):
                        input.append(0)

                output = genome.feedforward(input)

                if output[0] > 0.5: bullets.extend(ship.shoot())
                if output[1] > 0.5: ship.rotateLeft()
                if output[2] > 0.5: ship.rotateRight()
                if output[3] > 0.5: ship.boost()

            ship.update()
            for bullet in bullets: bullet.update()
            for asteroid in asteroids: asteroid.update()

            collisionSystem.checkCollisions()

            if self.isRendered:
                screen.fill(colors.black)
                ship.draw(screen)
                for bullet in bullets: bullet.draw(screen)
                for asteroid in asteroids: asteroid.draw(screen)

                pygame.display.flip()
                clock.tick(60)

        return self.score

p = Population(100)
for i in range(100):
    for genome in p.genomes:
        genome.fitness = Game.forAI(genome, False).run()
    p.naturalSelection()

Game.forAI(p.bestGenome).run()
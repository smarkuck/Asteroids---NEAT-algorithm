import pygame
import colors
from neat.population import Population

from resolution import *
from ship import Ship
from asteroid import Asteroid
from collision_system import CollisionSystem

import math

import random

class Game:
    def __init__(self, genome, isRendered):
        self.score = 0.0
        self.time = 0.0
        self.shoots = 0.0

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
        for i in range(4):
            rnd = random.random()
            if rnd < 0.25:
                rnd_x = random.randint(0, 200)
                rnd_y = random.randint(0, 600)
            elif rnd < 0.5:
                rnd_x = random.randint(600, 800)
                rnd_y = random.randint(0, 600)
            elif rnd < 0.75:
                rnd_x = random.randint(0, 800)
                rnd_y = random.randint(0, 150)
            else:
                rnd_x = random.randint(0, 800)
                rnd_y = random.randint(450, 600)

            asteroids.append(Asteroid(pygame.math.Vector2(rnd_x, rnd_y), 3, SHORT_SIDE * 0.1))

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
                        self.shoots += 1

            input = [0] * 32
            for i in range(32):
                min_dist = SCREEN_WIDTH * 2
                for asteroid in asteroids:
                    vision = pygame.math.Vector2(100, 0).rotate(ship.rotation + i * 11.25)
                    a = pygame.math.Vector2(asteroid.position)
                    if ship.position.x - ship.RADIUS > asteroid.position.x + asteroid.RADIUS and vision.x > 0:
                        a.x += SCREEN_WIDTH + asteroid.RADIUS * 2
                    elif ship.position.x + ship.RADIUS < asteroid.position.x - asteroid.RADIUS and vision.x < 0:
                        a.x -= SCREEN_WIDTH + asteroid.RADIUS * 2
                    if ship.position.y - ship.RADIUS > asteroid.position.y + asteroid.RADIUS and vision.y > 0:
                        a.y += SCREEN_HEIGHT + asteroid.RADIUS * 2
                    elif ship.position.y + ship.RADIUS < asteroid.position.y - asteroid.RADIUS and vision.y < 0:
                        a.y -= SCREEN_HEIGHT + asteroid.RADIUS * 2

                    if vision.x == 0:
                        D = abs(ship.position.x - a.x)
                        p = pygame.math.Vector2(ship.position.x, a.y)
                    else:
                        D = abs(vision.y/vision.x*a.x - a.y + ship.position.y - vision.y*ship.position.x/vision.x) / math.sqrt((vision.y/vision.x)**2 + 1)
                        if vision.y == 0: p = pygame.math.Vector2(a.x, ship.position.y)
                        else:
                            a1 = vision.y/vision.x
                            b1 = ship.position.y - vision.y*ship.position.x/vision.x
                            a2 = -vision.x/vision.y
                            b2 = a.y + vision.x*a.x/vision.y
                            p = pygame.math.Vector2((b2 - b1)/(a1 - a2), (a1*b2 - a2*b1)/(a1 - a2))

                    if D <= asteroid.RADIUS:
                        x = math.sqrt(asteroid.RADIUS**2 - D**2)
                        dist = ship.position.distance_to(p) - x
                        if dist < min_dist: min_dist = dist

                input[i] = min_dist/(SCREEN_WIDTH * 2)

            if self.playerIsHuman:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_LEFT]: ship.rotateLeft()
                if pressed[pygame.K_RIGHT]: ship.rotateRight()
                if pressed[pygame.K_UP]: ship.boost()

            else:
                output = self.genome.feedforward(input)

                if output[0] > 0.5:
                    bullets.extend(ship.shoot())
                    self.shoots += 1
                if output[1] > 0.5: ship.rotateLeft()
                if output[2] > 0.5: ship.rotateRight()
                if output[3] > 0.5: ship.boost()

            ship.update()
            for bullet in bullets: bullet.update()
            for asteroid in asteroids: asteroid.update()
            self.time += 1
            if not self.playerIsHuman and self.time >= 4000:
                done = True

            collisionSystem.checkCollisions()

            if self.isRendered:
                screen.fill(colors.black)
                ship.draw(screen)
                for bullet in bullets: bullet.draw(screen)
                for asteroid in asteroids: asteroid.draw(screen)

                pygame.display.flip()
                clock.tick(60)

        fitness = self.score
        if self.shoots > 0: fitness += self.score/self.shoots * 68
        fitness += self.time/4000 * 68
        return [fitness, self.score]

p = Population(300)
for i in range(100):
    for genome in p.genomes:
        for j in range(5):
            result = Game.forAI(genome, False).run()
            genome.fitness += result[0]/5
            if result[1] > genome.score: genome.score = result[1]
    print "======================================================="
    print "best fitness: %s" % max([g.fitness for g in p.genomes])
    p.naturalSelection()

while True:
    raw_input("Press Enter")
    Game.forAI(p.champion).run()
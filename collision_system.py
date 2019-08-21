import pygame

class CollisionSystem:
    def __init__(self, game, ship, asteroids, bullets):
        self.game = game
        self.ship = ship
        self.asteroids = asteroids
        self.bullets = bullets

    def checkCollisions(self):
        for asteroid in self.asteroids:
            if self.ship.alive and asteroid.alive and \
                asteroid.position.distance_to(self.ship.position) < (asteroid.RADIUS + self.ship.RADIUS * 0.7):
                self.asteroids.extend(asteroid.destroy())
                self.ship.destroy()

        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if bullet.alive and asteroid.alive and \
                    bullet.position.distance_to(asteroid.position) < (asteroid.RADIUS + bullet.RADIUS):
                    self.asteroids.extend(asteroid.destroy())
                    bullet.destroy()
                    self.game.score += 1
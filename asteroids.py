import pygame
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SHORT_SIDE = SCREEN_WIDTH if SCREEN_WIDTH < SCREEN_HEIGHT else SCREEN_HEIGHT

class Ship:
    x = SCREEN_WIDTH/2
    y = SCREEN_HEIGHT/2
    angle = 90
    angleBetweenRearIndices = 70
    radius = 0.05*SHORT_SIDE
    acceleration = 0.0005*SHORT_SIDE
    max_speed = 0.02*SHORT_SIDE
    speed = 0

    def rotateLeft(self):
        self.angle += 2

    def rotateRight(self):
        self.angle += -2

    def boost(self):
        self.speed = min(self.max_speed, self.speed + self.acceleration)

    def shoot(self):
        return Bullet(self.x + self.radius*math.cos(math.radians(self.angle)), self.y + self.radius*math.sin(math.radians(self.angle)), self.angle)

    def update(self):
        self.speed *= 0.98
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.boundary()

    def boundary(self):
        if self.x > SCREEN_WIDTH + self.radius: self.x = -self.radius
        elif self.x < -self.radius: self.x = SCREEN_WIDTH + self.radius

        if self.y > SCREEN_HEIGHT + self.radius: self.y = -self.radius
        elif self.y < -self.radius: self.y = SCREEN_HEIGHT + self.radius

    def draw(self):
        angleBetweenFrontAndRearIndices = 180 - self.angleBetweenRearIndices/2.
        p1 = (self.x + self.radius*math.cos(math.radians(self.angle)), SCREEN_HEIGHT - self.y - self.radius*math.sin(math.radians(self.angle)))
        p2 = (self.x + self.radius*math.cos(math.radians(self.angle+angleBetweenFrontAndRearIndices)), SCREEN_HEIGHT - self.y - self.radius*math.sin(math.radians(self.angle+angleBetweenFrontAndRearIndices)))
        p3 = (self.x + self.radius*math.cos(math.radians(self.angle-angleBetweenFrontAndRearIndices)), SCREEN_HEIGHT - self.y - self.radius*math.sin(math.radians(self.angle-angleBetweenFrontAndRearIndices)))
        pygame.draw.polygon(screen, (255,255,255), (p1, p2, p3), 1)

class Bullet:
    speed = 0.025*SHORT_SIDE
    radius = 0.005*SHORT_SIDE
    life = 35

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def draw(self):
        pygame.draw.circle(screen, (255,255,255), (int(self.x), int(SCREEN_HEIGHT - self.y)), int(self.radius))

    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.boundary()
        self.life -= 1

    def boundary(self):
        if self.x > SCREEN_WIDTH: self.x = 0
        elif self.x < 0: self.x = SCREEN_WIDTH

        if self.y > SCREEN_HEIGHT: self.y = 0
        elif self.y < 0: self.y = SCREEN_HEIGHT

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
done = False

clock = pygame.time.Clock()
ship = Ship()

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
        ship.draw()
        for bullet in bullets: bullet.draw()

        pygame.display.flip()
        clock.tick(60)

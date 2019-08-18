import pygame
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SHORT_SIDE = SCREEN_WIDTH if SCREEN_WIDTH < SCREEN_HEIGHT else SCREEN_HEIGHT

class Ship:
    x = SCREEN_WIDTH/2
    y = SCREEN_HEIGHT/2
    angle = 90
    r = 0.05*SHORT_SIDE
    acceleration = 0.0005*SHORT_SIDE
    max_speed = 0.02*SHORT_SIDE
    speed = 0

    def rotateLeft(self):
        self.angle += 2

    def rotateRight(self):
        self.angle += -2

    def boost(self):
        self.speed = min(self.max_speed, self.speed + self.acceleration)

    def update(self):
        self.speed *= 0.98
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.boundary()

    def boundary(self):
        if self.x > SCREEN_WIDTH + self.r: self.x = -self.r
        elif self.x < -self.r: self.x = SCREEN_WIDTH + self.r

        if self.y > SCREEN_HEIGHT + self.r: self.y = -self.r
        elif self.y < -self.r: self.y = SCREEN_HEIGHT + self.r

    def draw(self):
        p1 = (self.x + self.r*math.cos(math.radians(self.angle)), SCREEN_HEIGHT - self.y - self.r*math.sin(math.radians(self.angle)))
        p2 = (self.x + self.r*math.cos(math.radians(self.angle+140)), SCREEN_HEIGHT - self.y - self.r*math.sin(math.radians(self.angle+140)))
        p3 = (self.x + self.r*math.cos(math.radians(self.angle-140)), SCREEN_HEIGHT - self.y - self.r*math.sin(math.radians(self.angle-140)))
        pygame.draw.polygon(screen, (255,255,255), (p1, p2, p3), 1)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
done = False

clock = pygame.time.Clock()
ship = Ship()

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]: ship.rotateLeft()
        if pressed[pygame.K_RIGHT]: ship.rotateRight()
        if pressed[pygame.K_UP]: ship.boost()

        ship.update()

        screen.fill((0, 0, 0))
        ship.draw()

        pygame.display.flip()
        clock.tick(60)

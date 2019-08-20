import pygame
import tools
import colors

class Bullet:
    def __init__(self, position, rotation, scale):
        self.VELOCITY = 0.3 * scale
        self.RADIUS = 0.05 * scale
        self.LIFE_DECREASE_RATE = 1

        self.position = pygame.math.Vector2(position)
        self.rotation = rotation
        self.life = 35
        self.alive = True

    def draw(self, screen):
        if not self.alive: return
        positionOnScreen = tools.vector2CoordsToInt(tools.screenCoords(self.position))
        pygame.draw.circle(screen, colors.white, positionOnScreen, int(self.RADIUS))

    def update(self):
        self.position += pygame.math.Vector2(1, 0).rotate(self.rotation) * self.VELOCITY
        self.position = tools.boundaryLoop(self.position, self.RADIUS)
        self.life -= self.LIFE_DECREASE_RATE
        if self.life <= 0: self.destroy()

    def destroy(self):
        self.alive = False
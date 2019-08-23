import pygame
import tools
import colors
import random

class Asteroid:
    def __init__(self, position, size, scale):
        self.SCALE = scale
        self.VELOCITY = 0.007 * scale * pygame.math.Vector2(1, 0).rotate(random.random()*360) * 3/size
        self.SIZE = size
        self.RADIUS = self.getRadius()
        self.LINE_WIDTH = 2

        self.position = pygame.math.Vector2(position)
        self.vertices = self.createVertices()
        self.alive = True

    def getRadius(self):
        if self.SIZE == 1:
            radius = 0.3
        elif self.SIZE == 2:
            radius = 1
        elif self.SIZE == 3:
            radius = 2
        return radius * self.SCALE

    def createVertices(self):
        vertices = []
        if self.SIZE == 1:
            verticesQuantity = random.randint(5, 6)
        elif self.SIZE == 2:
            verticesQuantity = random.randint(7, 8)
        elif self.SIZE == 3:
            verticesQuantity = random.randint(8, 9)

        angleBetween = 360./verticesQuantity
        for i in range(verticesQuantity):
            deviation = (random.random() - 0.5) * 2 * angleBetween * 0.25
            vector = pygame.math.Vector2(1, 0).rotate(angleBetween * i + deviation) * self.RADIUS
            vertices.append(vector)
        return vertices

    def draw(self, screen):
        if not self.alive: return
        positionOnScreen = [tools.screenCoords(self.position + vertex) for vertex in self.vertices]
        pygame.draw.polygon(screen, colors.white, positionOnScreen, self.LINE_WIDTH)

    def update(self):
        self.position += self.VELOCITY
        self.position = tools.boundaryLoop(self.position, self.RADIUS)

    def destroy(self):
        self.alive = False
        if self.SIZE > 1:
            return [Asteroid(self.position, self.SIZE - 1, self.SCALE),
                    Asteroid(self.position, self.SIZE - 1, self.SCALE)]
        else:
            return []

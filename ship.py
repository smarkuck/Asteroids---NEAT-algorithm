import pygame
import colors
import tools
from bullet import Bullet

class Ship:
    def __init__(self, position, scale):
        self.RADIUS = scale / 2
        self.ANGLE_BETWEEN_REAR_INDICES = 70
        self.LINE_WIDTH = 2
        self.SCALE = scale
        self.ACCELERATION = 0.003 * scale
        self.MAX_VELOCITY = 0.2 * scale
        self.DECELERATION_RATE = 0.98
        self.ROTATION_SPEED = 5

        self.position = pygame.math.Vector2(position)
        self.rotation = 90
        self.velocity = pygame.math.Vector2()
        self.alive = True

        self.vertices = []
        for i in range(3): self.vertices.append(pygame.math.Vector2())
        self.updateVertices()

    def updateVertices(self):
        ANGLE_BETWEEN_FRONT_AND_REAR_INDICES = 180 - self.ANGLE_BETWEEN_REAR_INDICES / 2.
        frontVertex = pygame.math.Vector2(self.RADIUS, 0).rotate(self.rotation)

        self.vertices[0] = self.position + frontVertex
        self.vertices[1] = self.position + frontVertex.rotate(ANGLE_BETWEEN_FRONT_AND_REAR_INDICES)
        self.vertices[2] = self.position + frontVertex.rotate(-ANGLE_BETWEEN_FRONT_AND_REAR_INDICES)

    def rotateLeft(self):
        self.rotation += self.ROTATION_SPEED

    def rotateRight(self):
        self.rotation += -self.ROTATION_SPEED

    def boost(self):
        self.velocity += pygame.math.Vector2(1, 0).rotate(self.rotation) * self.ACCELERATION
        if self.velocity.length() > self.MAX_VELOCITY:
            self.velocity = self.velocity.normalize() * self.MAX_VELOCITY

    def shoot(self):
        return Bullet(self.vertices[0], self.rotation, self.SCALE)

    def draw(self, screen):
        if not self.alive: return
        verticesOnScreen = [tools.screenCoords(vertex) for vertex in self.vertices]
        pygame.draw.polygon(screen, colors.white, verticesOnScreen, self.LINE_WIDTH)

    def update(self):
        self.velocity *= self.DECELERATION_RATE
        self.position += self.velocity
        self.position = tools.boundaryLoop(self.position, self.RADIUS)
        self.updateVertices()

    def destroy(self):
        self.alive = False
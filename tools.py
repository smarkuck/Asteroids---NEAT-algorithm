import pygame
from resolution import *

def vector2CoordsToInt(vector):
    return (int(vector.x), int(vector.y))

def screenCoords(coords):
    return pygame.math.Vector2(coords.x, SCREEN_HEIGHT - coords.y)

def boundaryLoop(position, margin = 0):
    result = pygame.math.Vector2(position)

    if result.x > SCREEN_WIDTH + margin: result.x = -margin
    elif result.x < -margin: result.x = SCREEN_WIDTH + margin

    if result.y > SCREEN_HEIGHT + margin: result.y = -margin
    elif result.y < -margin: result.y = SCREEN_HEIGHT + margin

    return result
import math

def get_direction(src, target):
    diff = map(lambda a, b: a - b, target, src)
    mag = math.sqrt(sum(map(lambda a: a ** 2, diff)))
    if mag == 0:
        return [0, 0]
    return map(lambda a: a / mag, diff)

def distance(pos1, pos2):
    return math.sqrt(sum(map(lambda a: a ** 2, map(lambda a, b: a - b, pos1, pos2))))

def magnitude(vector):
    return math.sqrt(sum(map(lambda a: a ** 2, vector)))

class Drawable(object):
    def draw(self, surface, camera=(0, 0)):
        coordinates = (self.rect.left - camera[0], self.rect.top - camera[1])
        surface.blit(self.image, coordinates)

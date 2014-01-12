class Rect(object):
    def __init__(self, *args):
        if args is None:
            raise RuntimeError, "None is not allowed as Rect arguments"

        if len(args) == 4:
            self.init4(args[0], args[1], args[2], args[3])
        elif len(args) == 2:
            self.init2(args[0], args[1])
        elif len(args) == 1:
            self.init1(args[0])
        else:
            raise RuntimeError, "Rect accepts 3 or 5 arguments (self included), not " + str(len(args) + 1)

    def init4(self, left, top, width, height):
        self._x = int(left)
        self._y = int(top)
        self._w = int(width)
        self._h = int(height)

    def init2(self, topleft, size):
        self._x = int(topleft[0])
        self._y = int(topleft[1])
        self._w = int(size[0])
        self._h = int(size[1])

    def init1(self, rect):
        if type(rect) is not Rect:
            raise RuntimeError, "rect must be of type Rect, not " + type(rect) + " : " + str(rect)

        self._x = rect._x
        self._y = rect._y
        self._w = rect._w
        self._h = rect._h

    def __str__(self):
        return "<rect(" + str(self._x) + "," + str(self._y) + "," + str(self._w) + "," + str(self._h) + ")>"

    def __repr__(self):
        return str(self)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = int(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = int(value)

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = int(value)

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):
        self._h = int(value)

    @property
    def width(self):
        return self._w

    @width.setter
    def width(self, value):
        self._w = int(value)

    @property
    def height(self):
        return self._h

    @height.setter
    def height(self, value):
        self._h = int(value)

    @property
    def size(self):
        return (self._w, self._h)

    @size.setter
    def size(self, value):
        self._w = int(value[0])
        self._h = int(value[1])

    @property
    def top(self):
        return self._y

    @top.setter
    def top(self, value):
        self._y = int(value)

    @property
    def bottom(self):
        return self._y + self._h

    @bottom.setter
    def bottom(self, value):
        self._y = int(value) - self._h

    @property
    def left(self):
        return self._x

    @left.setter
    def left(self, value):
        self._x = int(value)

    @property
    def right(self):
        return self._x + self._w

    @right.setter
    def right(self, value):
        self._x = int(value) - self._w

    @property
    def topleft(self):
        return (self._x, self._y)

    @topleft.setter
    def topleft(self, value):
        self._x = int(value[0])
        self._y = int(value[1])

    @property
    def topright(self):
        return (self.right, self._y)

    @topright.setter
    def topright(self, value):
        self.right = int(value[0])
        self._y = int(value[1])

    @property
    def bottomleft(self):
        return (self._x, self.bottom)

    @bottomleft.setter
    def bottomleft(self, value):
        self._x = int(value[0])
        self.bottom = int(value[1])

    @property
    def bottomright(self):
        return (self.right, self.bottom)

    @bottomright.setter
    def bottomright(self, value):
        self.right = int(value[0])
        self.bottom = int(value[1])

    @property
    def centerx(self):
        return self._x + self._w / 2

    @centerx.setter
    def centerx(self, value):
        self._x = int(value) - self._w / 2

    @property
    def centery(self):
        return self._y + self._h / 2

    @centery.setter
    def centery(self, value):
        self._y = int(value) - self._h / 2

    @property
    def center(self):
        return (self.centerx, self.centery)

    @center.setter
    def center(self, value):
        self.centerx = int(value[0])
        self.centery = int(value[1])

    @property
    def midtop(self):
        return (self.centerx, self._y)

    @midtop.setter
    def midtop(self, value):
        self.centerx = int(value[0])
        self._y = int(value[1])

    @property
    def midbottom(self):
        return (self.centerx, self.bottom)

    @midbottom.setter
    def midbottom(self, value):
        self.centerx = int(value[0])
        self.bottom = int(value[1])

    @property
    def midleft(self):
        return (self._x, self.centery)

    @midleft.setter
    def midleft(self, value):
        self._x = int(value[0])
        self.centery = int(value[1])

    @property
    def midright(self):
        return (self.right, self.centery)

    @midright.setter
    def midright(self, value):
        self.right = int(value[0])
        self.centery = int(value[1])

    def copy(self):
        return Rect(self._x, self._y, self._w, self._h)

    def convert(self, cls):
        return cls(self._x, self._y, self._w, self._h)

    def collidepoint(self, *args):
        if args is None:
            raise RuntimeError, "None is not allowed as collidepoint arguments"

        if len(args) == 2:
            x = args[0]
            y = args[1]
        elif len(args) == 1:
            x = args[0][0]
            y = args[0][1]
        else:
            raise RuntimeError, "collidepoint accepts 2 or 3 arguments (self included), not " + str(len(args) + 1)

        miss = False
        miss |= self.top > y
        miss |= self.bottom <= y
        miss |= self.left > x
        miss |= self.right <= x

        if miss:
            return 0
        else:
            return 1

    def init4(self, left, top, width, height):
        self._x = int(left)
        self._y = int(top)
        self._w = int(width)
        self._h = int(height)

    def init2(self, topleft, size):
        self._x = int(topleft[0])
        self._y = int(topleft[1])
        self._w = int(size[0])
        self._h = int(size[1])

    def colliderect(self, rect):
        miss = False
        miss |= self.top >= rect.bottom
        miss |= self.bottom <= rect.top
        miss |= self.left >= rect.right
        miss |= self.right <= rect.left

        if miss:
            return 0
        else:
            return 1

    def move(self, x, y):
        return Rect(self._x + int(x), self._y + int(y), self._w, self._h)

    def move_ip(self, x, y):
        self._x += int(x)
        self._y += int(y)



# not imlemented:
#   clamp
#   clamp_ip
#   clip
#   collidedict
#   collidedictall
#   collidelist
#   collidelistall
#   collidepoint
#   contains
#   fit
#   inflate
#   inflate_ip
#   normalize
#   union
#   union_ip
#   unionall
#   unionall_ip

if __name__ == "__main__":
    pass

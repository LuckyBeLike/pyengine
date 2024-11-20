import os; os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', "yep, hide it we no needin' that!")
import pygame
import random

def clamp(n, min_value, max_value):
    return max(min_value, min(n, max_value))

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def add(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)
    def subtract(self, other: 'Vector') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y)
    def multiply(self, other: 'Vector') -> 'Vector':
        return Vector(self.x * other.x, self.y * other.y)
    def divide(self, other: 'Vector') -> 'Vector':
        return Vector(self.x / other.x, self.y / other.y)
    
    def addSc(self, scalar: float) -> 'Vector':
        return Vector(self.x + scalar, self.y + scalar)
    def subtractSc(self, scalar: float) -> 'Vector':
        return Vector(self.x - scalar, self.y - scalar)
    def multiplySc(self, scalar: float) -> 'Vector':
        return Vector(self.x * scalar, self.y * scalar)
    def divideSc(self, scalar: float) -> 'Vector':
        return Vector(self.x / scalar, self.y / scalar)
    
    def equals(self, other: 'Vector') -> bool:
        return self.x == other.x and self.y == other.y

    def toTuple(self) -> tuple:
        return (self.x, self.y)
        
    
    @staticmethod
    def zero() -> 'Vector':
        return Vector(0, 0)
    @staticmethod
    def copy(other: 'Vector') -> 'Vector':
        if other is not None:
            return Vector(other.x, other.y)
        else:
            return Vector(0, 0)
    @staticmethod
    def fromTuple(other: tuple) -> 'Vector':
        if other is not None:
            return Vector(other[0], other[1])
        else:
            return Vector(0, 0)

class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def toTuple(self) -> tuple:
        return (self.r, self.g, self.b)

class Component:
    def __init__(self, object):
        self.object: Object = object
        self.enabled: bool = True
        self.requiredComponents = []

class Components:
    class Rectangle(Component):
        def __init__(self, object):
            super().__init__(object)
            self.position: Vector = Vector(0, 0)
            self.size: Vector = Vector(0, 0)
            self.color: Color = Color(255, 255, 255)
            self.invisible: bool = False

        def toTuple(self) -> tuple:
            return (self.position.x, self.position.y, self.size.x, self.size.y)
        
        def intersects(self, other: 'Components.Rectangle') -> bool:
            return (self.position.x < other.position.x + other.size.x and
                    self.position.x + self.size.x > other.position.x and
                    self.position.y < other.position.y + other.size.y and
                    self.position.y + self.size.y > other.position.y)

        @property
        def left(self):
            return self.position.x
        @property
        def right(self):
            return self.position.x + self.size.x
        @property
        def top(self):
            return self.position.y
        @property
        def bottom(self):
            return self.position.y + self.size.y
        
    class Camera(Component):
        def __init__(self, object):
            super().__init__(object)
            self.position: Vector = Vector(0, 0)
        
        def relativeTuple(self, other: tuple) -> tuple:
            if len(other) > 2:
                return (other[0] - self.position.x, other[1] - self.position.y, other[2], other[3])
            else:
                return (other[0] - self.position.x, other[1] - self.position.y)
        
        def relativeVector(self, vector: Vector) -> Vector:
            return Vector(vector.x - self.position.x, vector.y - self.position.y)

    class Image(Component):
        def __init__(self, object):
            super().__init__(object)
            self.image: pygame.Surface = None
            self.requiredComponents = [Components.Rectangle]
        
        def rescale(self):
            rect: Components.Rectangle = self.object.getComponent(Components.Rectangle)
            if rect:
                try:
                    self.image = pygame.transform.scale(self.image, rect.size.toTuple())
                except Exception:
                    print("Image not set, but still trying to rescale")
    
    class Collider(Component):
        def __init__(self, object):
            super().__init__(object)
            self.requiredComponents = [Components.Rectangle]

    class Physics(Component):
        gravity = Vector(0, 9.8)
        friction = 1.5
        deltaTime = 0.016

        def __init__(self, object):
            super().__init__(object)
            self.mass: float = 1
            self.force: Vector = Vector(0, 0)
            self.gravity: bool = True
            self.requiredComponents = [Components.Collider]
        
        def addForce(self, force: Vector):
            self.force = self.force.add(force)

class Object:
    def __init__(self):
        self.name: str = "name"
        self.components = []
        objects.append(self)
    
    def addComponent(self, component) -> Component:
        for existing in self.components:
            if type(existing) == component:
                return
        instance: Component = component(self)
        self.components.append(instance)
        for component in instance.requiredComponents:
            if self.getComponent(component) is None:
                self.addComponent(component)
        return instance
    
    def getComponent(self, component) -> Component:
        for i in self.components:
            if type(i) == component:
                return i
        return None

class Objects:
    class Rectangle(Object):
        def __init__(self):
            super().__init__()
            self.addComponent(Components.Rectangle)

    class Camera(Object):
        def __init__(self):
            super().__init__()
            self.addComponent(Components.Camera)

    class StaticBody(Object):
        def __init__(self):
            super().__init__()
            self.addComponent(Components.Rectangle)
            self.addComponent(Components.Collider)

    class PhysicalBody(Object):
        def __init__(self):
            super().__init__()
            self.addComponent(Components.Rectangle)
            self.addComponent(Components.Collider)
            self.addComponent(Components.Physics)

class Input:
    @staticmethod
    def getEvents() -> list:
        return events
    
    @staticmethod
    def getPressedKeys() -> list:
        return keys
    
    @staticmethod
    def getKeyRaw(key: str, eventType) -> bool:
        for event in events:
            if event.type == eventType:
                try:
                    key_constant = getattr(pygame, f"K_{key}")
                    return event.key == key_constant
                except AttributeError:
                    print(f"Key '{key}' is not a valid key.")
                    return False

    @staticmethod
    def getKeyDown(key: str) -> bool:
        return Input.getKeyRaw(key, pygame.KEYDOWN)
    
    @staticmethod
    def getKeyUp(key: str) -> bool:
        return Input.getKeyRaw(key, pygame.KEYUP)
        
    @staticmethod
    def getKey(key: str) -> bool:
        try:
            key_constant = getattr(pygame, f"K_{key}")
            return keys[key_constant]
        except AttributeError:
            print(f"Key '{key}' is not a valid key.")
            return False
        
    @staticmethod
    def getKeyAxis(key1: str, key2: str) -> int:
        return (1 if Input.getKey(key2) else 0) - (1 if Input.getKey(key1) else 0)
    
    @staticmethod
    def getFPS() -> float:
        return clock.get_fps()
    
    @staticmethod
    def getMousePos() -> Vector:
        x, y = pygame.mouse.get_pos()
        return Vector(x, y)
    
    @staticmethod
    def getMouseButtons() -> tuple[bool, bool, bool]:
        return pygame.mouse.get_pressed()
    
    @staticmethod
    def getMouseButton(index: int) -> bool:
        buttons = Input.getMouseButtons()
        return buttons[clamp(index) + 1, 1, 3]
    
    @staticmethod
    def getMouseButtonRaw(index: int, eventType) -> bool:
        for event in events:
            if event.type == eventType and event.button == index:
                return True
        return False
    
    @staticmethod
    def getMouseButtonDown(index: int) -> bool:
        return Input.getMouseButtonRaw(index, pygame.MOUSEBUTTONDOWN)
    
    @staticmethod
    def getMouseButtonUp(index: int) -> bool:
        return Input.getMouseButtonRaw(index, pygame.MOUSEBUTTONUP)
    
    @staticmethod
    def getMouseMotion() -> Vector:
        dx, dy = 0, 0
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                dx += event.rel[0]
                dy += event.rel[1]
        return Vector(dx, dy)
    
    @staticmethod
    def screenToWorld(vector: Vector) -> Vector:
        return Vector(vector.x + camera.position.x, vector.y + camera.position.y)

def setSize(w, h):
    global screen
    screen = pygame.display.set_mode((w, h))

def getSize():
    return pygame.display.get_window_size()

def setTitle(text):
    pygame.display.set_caption(text)

def getTitle():
    pygame.display.get_caption()

def addUpdateListener(func):
    updateListeners.append(func)

def randomInt(min: int, max: int) -> int:
    return random.randint(min, max)

def randomFloat(min: float, max: float) -> float:
    return min + random.random() * (max - min)

def wait(ms: int):
    pygame.time.wait(ms)

def loadImage(path: str):
    return pygame.image.load(path).convert()

def doPhysics():
    """
    Internal function for physics, do not call!
    """

    for obj in objects:
        phys: Components.Physics = obj.getComponent(Components.Physics)
        rect: Components.Rectangle = obj.getComponent(Components.Rectangle)
        if phys and rect:
            if phys.gravity:
                phys.addForce(Components.Physics.gravity.multiplySc(phys.mass / 50))
            rect.position = rect.position.add(phys.force.multiplySc(Components.Physics.deltaTime * 1000))
            phys.force = phys.force.divideSc((Components.Physics.friction))
            if abs(phys.force.x) < 0.001: phys.force.x = 0
            if abs(phys.force.y) < 0.001: phys.force.y = 0

def checkCollisions():
    """
    Internal function for checking collisions, do not call!
    """

    for obj in objects:
        collider: Components.Collider = obj.getComponent(Components.Collider)
        if collider and collider.enabled:
            rect: Components.Rectangle = obj.getComponent(Components.Rectangle)
            if rect:
                for other in objects:
                    if other is not obj:
                        otherCollider: Components.Collider = other.getComponent(Components.Collider)
                        if otherCollider and otherCollider.enabled:
                            otherRect: Components.Rectangle = other.getComponent(Components.Rectangle)
                            if otherRect and rect.intersects(otherRect):
                                overlap_x1 = rect.right - otherRect.left
                                overlap_x2 = otherRect.right - rect.left
                                overlap_y1 = rect.bottom - otherRect.top
                                overlap_y2 = otherRect.bottom - rect.top
                                overlaps = {
                                    'left': overlap_x1,
                                    'right': overlap_x2,
                                    'top': overlap_y1,
                                    'bottom': overlap_y2
                                }
                                min_overlap = min(overlaps.values())
                                for direction, overlap in overlaps.items():
                                    if overlap == min_overlap:
                                        if direction == 'left':
                                            rect.position.x -= overlap
                                        elif direction == 'right':
                                            rect.position.x += overlap
                                        elif direction == 'top':
                                            rect.position.y -= overlap
                                        elif direction == 'bottom':
                                            rect.position.y += overlap
                                        break

def process():
    """
    Internal process function, do not call!
    """

    doPhysics()

def draw():
    """
    Internal draw function, do not call!
    """

    for obj in objects:
        rect: Components.Rectangle = obj.getComponent(Components.Rectangle)
        img: Components.Image = obj.getComponent(Components.Image)
        if rect:
            if rect.enabled:
                camPos = camera.relativeTuple(rect.toTuple())
                if img:
                    if img.enabled:
                        if img.image:
                            screen.blit(img.image, camPos)
                elif not rect.invisible:
                    pygame.draw.rect(screen, rect.color.toTuple(), camPos)

def run():
    """
    Start the engine loop.
    """

    global _running, events, keys

    _running = True
    while _running:
        Components.Physics.deltaTime = clock.tick(60) / 1000.0
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                _running = False
                quit()

        screen.fill(bgc)
        process()
        for func in updateListeners:
            func()
        checkCollisions()
        draw()
        pygame.display.flip()
        clock.tick(60)

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('pyengine window')

bgc = (0, 0, 0)
updateListeners = []
clock = pygame.time.Clock()

objects = []
events = []
keys = []

_running = False

camera: Components.Camera = Objects.Camera().getComponent(Components.Camera)
from abc import ABCMeta, abstractmethod

#Interface
class Weapon(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def render(self, screen): pass

    @abstractmethod
    def shoot(self, power, angle, tank, screen): pass

    @abstractmethod
    def collision_detection(self, player): pass

    #разрыв снарядаpno
    @abstractmethod
    def animation(self): pass

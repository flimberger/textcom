# Copyright (c) 2015 TachyonNZ
# Copyright (c) 2015 Florian Limberger <flo@snakeoilproductions.net>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER # LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import random
import time


class Weapon:
    """Base class for all weapon classes."""

    def __init__(self, name, damage, clip_size):
        self.name = name
        self.damage = damage
        self.clip_size = clip_size
        self.ammo = clip_size

    def get_sound(self):
        """Sound interface method"""
        pass

    def reload(self):
        self.ammo = self.clip_size
        time.sleep(0.5)

    def shoot(self):
        time.sleep(0.5)
        print(self.get_sound())
        time.sleep(0.5)
        if (self.ammo == 0):
            print('Out of ammo')
            return 0
        self.ammo -= 1
        return self.damage + random.randrange(-1, 2)


class AlienWeapon(Weapon):
    """Base class for alien weapons."""

    def __init__(self, name, damage, clip_size, elerium, fragments):
        super().__init__(name, damage, clip_size)
        self.elerium = elerium
        self.fragments = fragments

    def get_materials(self):
        """Returns the amount of ressources gained from this weapon."""

        return self.elerium, self.fragments


class BallisticPistol(Weapon):
    def __init__(self):
        super().__init__('Ballistic Pistol', 2, 10)

    def get_sound(self):
        return '*Dak*'


class Autopistol(Weapon):
    def __init__(self):
        super().__init__('Autopistol', 2, 10)

    def get_sound(self):
        return '*Dakdakdak*'


class PlasmaPistol(AlienWeapon):
    def __init__(self):
        super().__init__('Plasma Pistol', 2, 10,1,1)

    def get_sound(self):
        return '*Whap*'


class AlloyPistol(Weapon):
    def __init__(self):
        super().__init__('Alloy Pistol', 4, 10)

    def get_sound(self):
        return '*Kchak!*'


class BallisticCarbine(Weapon):
    def __init__(self):
        super().__init__('Ballistic Carbine', 2, 3)

    def get_sound(self):
        return '*Dakkadakkadakka*'


class BallisticRifle(Weapon):
    def __init__(self):
        super().__init__('Ballistic Rifle', 3, 4)

    def get_sound(self):
        return '*Dakkadakkadakka*'


class LaserCarbine(Weapon):
    def __init__(self):
        super().__init__('Beam Carbine', 3, 999)

    def get_sound(self):
        return '*Zzzaaaaaap!*'


class LaserRifle(Weapon):
    def __init__(self):
        super().__init__('Beam Rifle', 4, 999)

    def get_sound(self):
        return '*Zzzaaaaaap!*'


class PlasmaCarbine(AlienWeapon):
    def __init__(self):
        super().__init__('Light Plasma Rifle', 4, 4, 1, 2)

    def get_sound(self):
        return '*Whap-whap-whap*'


class PlasmaRifle(AlienWeapon):
    def __init__(self):
        super().__init__('Plasma Rifle', 6, 5, 2, 4)

    def get_sound(self):
        return '*Whap-whap-whap*'


class BradfordsPistol(Weapon):
    def __init__(self):
        super().__init__("Bradford's Pistol", 5, 999)

    def get_sound(self):
        return '*Dak*'

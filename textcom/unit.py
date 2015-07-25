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

from textcom.items import ITEM_SCOPE
from textcom.ui import status
from textcom.weapons import BallisticCarbine, LaserCarbine, PlasmaCarbine


class Unit:
    """Base class for all fighting entities.

    Users *must* implement a `_handle_death` method.
    """

    def __init__(self, hp, aim, mobility, nrank, firstname, lastname,
                 armour, weapon, items, mods):
        self.hp = hp
        self.aim = aim
        self.mobility = mobility
        self.nrank = nrank
        self.firstname = firstname
        self.lastname = lastname
        self.armour = armour
        self.weapon = weapon
        self.items = items
        self.mods = mods
        self.cover = 0
        self.on_overwatch = False
        self.alive = True

    def _handle_kill(self, target):
        """Called when an opponent was killed.

        The default handler does nothing, which is appropriate for
        non-player units.
        """
        pass

    def _handle_overwatch(self, target):
        """Generic overwatch handler which shoots at the target."""
        return self.shoot_at(target, 10)

    def aim_at(self, target):
        """Calculates the percentage of the chance to hit the target."""
        hit_chance = self.aim - target.cover
        if ITEM_SCOPE in self.items:
            hit_chance += 10
        # Carbines get an aim bonus
        if type(self.weapon) is BallisticCarbine                              \
           or type(self.weapon) is LaserCarbine                               \
           or type(self.weapon) is PlasmaCarbine:
            hit_chance += 10
        if hit_chance < 0:
            hit_chance = 5
        if hit_chance > 100:
            hit_chance = 95
        return hit_chance

    def check_death(self):
        """Check for unit death and call death handler, if unit is dead.

        If the unit is not dead, `False` is returned and nothing
        happens, else the `_handle_death` method implemented by the
        subclass is called.
        """
        if self.hp <= 0:
            self._handle_death()
            return True
        return False

    def overwatch(self, target):
        """Perform overwatch reaction if unit is on overwatch.

        If the unit is on overwatch, the `_handle_overwatch` method is
        called (overwrite this to customize the overwatch handling) and
        `True` is returned, else `False` is returned and nothing
        happens.
        """
        if self.on_overwatch:
            self.on_overwatch = False
            status(str(self) + ' reacts!')
            self._handle_overwatch(target)
            return True
        return False

    def reload(self):
        """Reload the primary weapon."""
        self.weapon.reload()

    def shoot_at(self, target, situation_modificator=0):
        """Perform an attack at the target.

        Returns `True` if the target was hit, `False` otherwise.  If the
        target was hit, hit points are discounted and the death check is
        performed.
        """
        hit_chance = self.aim_at(target) + situation_modificator
        damage = self.weapon.shoot()
        if random.randrange(0, 100) < hit_chance:
            status(str(damage) + ' damage!')
            target.hp -= damage
            if target.check_death():
                self._handle_kill(target)
            return True
        else:
            status(' Missed!')
        return False

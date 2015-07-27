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

import textcom


class Item:
    """Base class for items.

    Items with an `use_ap_costs` of 0 are passive items.  Active items
    must provide a `use` method.
    """

    def __init__(self, name, use_ap_costs, effect_descr):
        self.name = name
        self.use_ap_costs = use_ap_costs
        self.effect_descr = effect_descr


class Explosive(Item):
    def __init__(self, name, use_ap_costs, damage, sound_descr):
        super().__init__(name, use_ap_costs, '{} dmg'.format(damage))
        self.damage = damage
        self.sound_descr = sound_descr

    def use(self, game_map):
        print(self.sound_descr)
        pod = game_map.get_current_room()
        # The grenade only affects some of the aliens in the room, but
        # is guaranteed to hit at least 1. It's not a bug, it's a
        # feature.
        affected_aliens = [random.choice(pod)]
        for alien in pod:
            if alien not in affected_aliens and random.randrange(100) < 10:
                affected_aliens.append(alien)
        for alien in affected_aliens:
            alien.hp -= self.damage
            alien.cover = textcom.COVER_NONE
            if alien.check_death():
                game_map.drop()
                game_map.soldier.check_promotion()


class Medkit(Item):
    def __init__(self):
        super().__init__('Medkit', 10, '+4 HP')

    def use(self, game_map):
        print("HP restored.")
        game_map.soldier.hp += 4


# XCOM items
ITEM_SCOPE = Item('Scope', 0, 'Increase aim')
ITEM_FRAG_GRENADE = Explosive('Frag Grenade', 10, 2, 'BAM!')
ITEM_ALIEN_GRENADE = Explosive('Alien Grenade', 15, 4, '**BLAM**!')
ITEM_MEDKIT = Medkit()


# Alien items
# Alien grenade is also available to XCOM
ITEM_ALLOY_PLATING = Item('Alloy Plating', 0, 'Increase defense')

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

import time
import random

import textcom
from textcom.alien import create_alien
import textcom.ui as ui


class Map:
    def __init__(self, pods, soldier):
        self.rooms = pods
        self.soldier = soldier
        self.current_room = 0

    def check_for_alien_overwatch(self):
        for alien in self.rooms[self.current_room]:
            alien.overwatch(self.soldier)

    def drop(self):
        itemdrop = random.randrange(0, 5)
        if random.randrange(1, 100) <= 5:
            ui.status('Recovered a ' + drops[itemdrop] + '!')
            if itemdrop == 0:
                self.soldier.items.append(ITEM_FRAG_GRENADE)
            elif itemdrop == 1:
                self.soldier.items.append(ITEM_MEDKIT)
            elif itemdrop == 3:
                self.soldier.weapon = PlasmaCarbine()
            elif itemdrop == 4:
                self.soldier.weapon = PlasmaRifle()
            elif itemdrop == 5:
                self.soldier.items.append(ITEM_ALIEN_GRENADE)

    def enter_room(self):
        for alien in self.rooms[self.current_room]:
            ui.status(str(alien) + ' spotted!')
        time.sleep(0.5)
        # Scatter the aliens in a room, some won't find any cover.
        for alien in self.rooms[self.current_room]:
            cover = textcom.COVER_NONE
            cover_str = ''
            rnd = random.randrange(100)
            if rnd > 75:
                cover = textcom.COVER_FULL
                cover_str = 'full'
            elif rnd > 10:
                cover = textcom.COVER_HALF
                cover_str = 'half'
            alien.cover = cover
            if not alien.cover == textcom.COVER_NONE:
                ui.status(str(alien) + ' moves to ' + cover_str + ' cover!')
            else:
                ui.status(str(alien) + " can't find any cover!")
        time.sleep(0.5)
        print()

    def get_current_room(self):
        return self.rooms[self.current_room]

    def next_room(self):
        self.current_room += 1


def create_map(number_of_rooms, soldier, scripted_levels={}):
    # the first room is empty, since the player starts there
    options = ['Sectoid', 'Thinman', 'Floater', 'Muton']
    pods = [[]]
    for i in range(1, number_of_rooms):
        if i in scripted_levels:
            pods.append(scripted_levels[i])
        else:
            pod = []
            # more aliens per room the further along you are
            for j in range(3 + random.randrange(-2, 2 + round(i / 10))):
                # determine alien species
                species = options[0]
                nrank = 0
                if 3 < i and i < 10:
                    species = random.choice(options[:2])
                elif 10 <= i and i < 20:
                    species = random.choice(options)
                else:
                    species = random.choice(options[2:])
                # determine rank
                # if species == 'Sectoid':
                maxrank = 4
                if species == 'Thinman':
                    maxrank = 5
                elif species == 'Floater':
                    maxrank = 6
                elif species == 'Muton':
                    maxrank = 8
                nrank = random.randrange(round(i / (number_of_rooms /
                                                    (maxrank - 1))), maxrank)
                alien = create_alien(j, i, species, nrank=nrank)
                pod.append(alien)
            pods.append(pod)
    return Map(pods, soldier)

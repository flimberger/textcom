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
from textcom import COVER_FLANKED, COVER_FULL, COVER_HALF
from textcom.map import check_for_alien_overwatch, checkspot, scatter
from textcom.soldier import BRADFORD


class Action:
    '''Base class for actions'''

    def __init__(self, soldier, name, ap_costs, ends_turn):
        self.soldier = soldier
        self.name = name
        self.ap_costs = ap_costs
        self.ends_turn = ends_turn

    def __str__(self):
        return self.name

    def perform(self):
        '''Interface method to perform action'''
        pass

    def _calc_ap(self):
        '''Should be the first thing executed by the perform functions'''
        if self.soldier.ap < self.ap_costs:
            raise Exception("Not enough AP to perform action '{}'".
                            format(self.name))
        if self.ends_turn:
            self.soldier.ap = 0
        else:
            self.soldier.ap -= self.ap_costs


class AdvanceAction(Action):
    def __init__(self, soldier):
        super().__init__(soldier, 'Advance', 1, True)

    def perform(self):
        global fragments
        global elerium
        global meld
        global alloy

        self._calc_ap()
        textcom.roomNo += 1
        if not "Drop Zone" in textcom.room[textcom.roomNo]:
            checkspot(textcom.roomNo)
            scatter(textcom.roomNo)
        else:
            if self.soldier.lastname == BRADFORD:
                tactical = 'Tactical Supervisor'
            else:
                tactical = BRADFORD
            print(tactical + ': Reached an access point, Commander. Requesting'
                             'additional goods!')
            print(tactical + ': We only have a short time before the aliens'
                             'close it off!')
            ap = 60
            while ap != 0:
                print("Fragments:",fragments)
                print("Elerium:",elerium)
                print("Meld:",meld)
                print("Alloy:",alloy)
                sel = displayShop(ap, self.soldier)

                if sel == "AimBonus":
                    soldier.mods.append("Aim")
                    soldier.aim += 5
                    meld -= 15
                    ap -= 60
                    print("Depth Perception Insta-Genemod applied!")
                elif sel == "HPBonus":
                    soldier.mods.append("HP")
                    soldier.hp += 5
                    meld -= 20
                    ap -= 60
                    print("Muscle Regeneration Insta-Genemod applied!")
                elif sel == "APBonus":
                    soldier.mods.append("HP")
                    soldier.mobility += 2
                    meld -=15
                    ap -= 60
                    print("Micro Servomotors Augment inserted!")
                elif sel == "NadeBonus":
                    soldier.mods.append("Nade")
                    soldier.item.append(0)
                    soldier.item.append(0)
                    meld -= 20
                    ap -= 60
                    print("Grenade Launcher Augment inserted!")
                elif sel == "LaserRifle":
                    soldier.weapon = LaserRifle()
                    fragments -= 40
                    elerium -= 20
                    ap -= 40
                    print("Beam Rifle fabricated!")
                elif sel == "LaserCarbine":
                    soldier.weapon = LaserCarbine()
                    fragments -= 20
                    elerium -= 10
                    ap -= 40
                    print("Beam Carbine fabricated!")
                elif sel == "Frag":
                    soldier.items.append(0)
                    alloy -= 4
                    fragments -= 20
                    ap -= 20
                    print("Frag Grenade fabricated!")
                elif sel == "Meds":
                    soldier.items.append(1)
                    meld -= 10
                    fragments -= 10
                    ap -= 20
                    print("Nano Serum fabricated!")
                elif sel == "Reload":
                    soldier.weapon.ammo = soldier.weapon.clip_size
                    ap -= 20
                    print("Weapon reloaded!")
                elif sel == "Heal":
                    soldier.hp += 1
                    ap -= 20
                    print("Healed 1HP!")
                elif sel == "Advance":
                    ap = 0
                time.sleep(0.5)
            time.sleep(0.5)
            soldier.say("All out of time! I'll have to keep moving!")
            time.sleep(0.5)
            textcom.roomNo += 1
            checkspot(textcom.roomNo)
            scatter(textcom.roomNo)


class EndTurnAction(Action):
    def __init__(self, soldier):
        super().__init__(soldier, 'End turn', 0, True)

    def perform(self):
        self._calc_ap()


class FireAction(Action):
    def __init__(self, soldier, target):
        super().__init__(soldier, 'Fire', 6, False)
        self.target = target
        self.hit_chance = soldier.aim_at(target)

    def __str__(self):
        return '(~{} dmg)(6AP) Fire {} at {} - {} HP - ({}%)'.\
               format(self.soldier.weapon.damage, self.soldier.weapon.name,   \
                      self.target, self.target.hp, self.hit_chance)

    def perform(self):
        self._calc_ap()
        self.soldier.say(self.soldier.get_retort())
        self.soldier.shoot_at(self.target)


class HunkerDownAction(Action):
    def __init__(self, soldier):
        super().__init__(soldier, 'Hunker down', 1, True)

    def perform(self):
        self._calc_ap()
        if self.soldier.cover == COVER_HALF                                   \
           or self.soldier.cover == COVER_FULL:
            self.soldier.hunkerbonus += 20
        self.soldier.say('Taking cover!')
        time.sleep(0.5)


class OverwatchAction(Action):
    def __init__(self, soldier):
        super().__init__(soldier, 'Overwatch', 6, True)

    def perform(self):
        self._calc_ap()
        self.soldier.say(self.soldier.get_overwatch_confirmation())
        time.sleep(0.5)
        self.soldier.ap = 0 # TODO check if this is necessary
        self.soldier.on_overwatch = True


class ReloadAction(Action):
    def __init__(self, soldier):
        super().__init__(soldier, 'Reload', 8, False)

    def perform(self):
        self._calc_ap()
        self.soldier.reload()
        time.sleep(0.5)


class RepositionAction(Action):
    def __init__(self, soldier):
        super().__init__(soldier, 'Reposition', 3, False)

    def perform(self):
        self._calc_ap()
        # if any aliens are on overwatch, check and be shot at if they are
        check_for_alien_overwatch(self.soldier)
        self.soldier.cover = 40 # ?!
        self.soldier.say(self.soldier.get_reposition_confirmation())
        time.sleep(0.5)
        #chance to flank an alien
        if random.randrange(0, 100) < 50:
            alien = random.choice(textcom.room[textcom.roomNo])

            textcom.ui.status(str(alien) + ' is flanked!')
            alien.cover = COVER_FLANKED


class UseItemAction(Action):
    def __init__(self, soldier, item):
        super().__init__(soldier, 'Use ' + item.name, item.use_ap_costs, False)
        self.item = item

    def __str__(self):
        return '({}) ({} AP) {}'.format(self.item.effect_descr,                     \
               self.item.use_ap_costs, self.name)

    def perform(self):
        self._calc_ap()
        items = self.soldier.items
        del items[items.index(self.item)]
        self.item.use(self.soldier)

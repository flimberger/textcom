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
import unittest

from textcom import COVER_FLANKED, COVER_FULL, COVER_HALF, COVER_NONE
from textcom.items import ITEM_SCOPE
from textcom.unit import Unit
from textcom.weapons import BallisticPistol,                           \
                            BallisticCarbine,                          \
                            LaserCarbine,                              \
                            PlasmaCarbine


def test_aim_at():
    aim_value = 50
    a = Unit(10, aim_value, 10, 1, 'Test', 'Alfa', '', BallisticPistol(), [],
             [])
    b = Unit(10, aim_value, 10, 1, 'Test', 'Bravo', '', None, [], [])
    # Without modifiers, hit chance is equal to the aim value
    b.cover = COVER_NONE
    assert a.aim_at(b) == aim_value

    # cover is discounted from the aim, a flanked target is easier to hit
    for cover in [COVER_FULL, COVER_HALF, COVER_FLANKED]:
        b.cover = cover
        assert a.aim_at(b) == aim_value - cover
    b.cover = COVER_NONE

    # a scope gives an aim bonus
    a.items = [ITEM_SCOPE]
    assert a.aim_at(b) == aim_value + 10
    a.items = []

    # carbines give an aim bonus
    for carbine in [BallisticCarbine, LaserCarbine, PlasmaCarbine]:
        a.weapon = carbine()
        assert a.aim_at(b) == aim_value + 10
    a.weapon = BallisticPistol()

    # minimum hit chance is 5%
    a.aim = 0
    assert a.aim_at(b) == 5
    # maximum hit chance is 95%
    a.aim = 100
    assert a.aim_at(b) == 95
    # an aim higher than the maximum is allowed, if the resulting chance is
    # at maximum 95%
    b.cover = COVER_HALF
    assert a.aim_at(b) == 100 - COVER_HALF
    a.aim = aim_value

    # boni and modifiers stack correctly
    a.weapon = BallisticCarbine()
    a.items = [ITEM_SCOPE]
    b.cover = COVER_HALF
    assert a.aim_at(b) == aim_value + 10 + 10 - COVER_HALF


def test_death():
    death_handler_called = False

    def death_handler():
        nonlocal death_handler_called
        death_handler_called = True

    a = Unit(10, 10, 10, 1, 'Test', 'Alfa', '', BallisticPistol(), [], [])
    a._handle_death = death_handler

    # low hp is not death
    a.hp = 1
    a.alive = True
    assert not a.check_death()
    assert not death_handler_called
    assert a.alive

    # 0 hp is death
    death_handler_called = False
    a.hp = 0
    assert a.check_death()
    assert death_handler_called
    assert not a.alive

    # negative hp is death
    death_handler_called = False
    a.hp = -1
    a.alive = True
    assert a.check_death()
    assert death_handler_called
    assert not a.alive

    # check that the death handler is only called once
    death_handler_called = False
    assert a.check_death()
    assert not death_handler_called
    assert not a.alive


def test_overwatch():
    overwatch_handler_called = False

    def overwatch_handler(target):
        nonlocal overwatch_handler_called
        overwatch_handler_called = True

    a = Unit(10, 50, 10, 1, 'Test', 'Alfa', '', BallisticPistol(), [], [])
    a._handle_overwatch = overwatch_handler

    # no overwatch
    assert not a.overwatch(None)
    assert not overwatch_handler_called
    assert not a.on_overwatch

    # overwatch
    a.on_overwatch = True
    assert a.overwatch(None)
    assert overwatch_handler_called
    assert not a.on_overwatch


def test_reload():
    pistol = BallisticPistol()
    pistol.ammo = 0
    a = Unit(10, 50, 10, 1, 'Test', 'Alfa', '', pistol, [], [])
    a.reload()
    assert pistol.ammo == pistol.clip_size


def test_shoot_at():
    # This test greatly increases the testing duration because the tested
    # methods involve various sleeps
    hp = 10
    a = Unit(hp, 100, 10, 1, 'Test', 'Alfa', '', BallisticPistol(), [],
             [])
    b = Unit(hp, 50, 10, 1, 'Test', 'Bravo', '', None, [], [])

    # randomness is difficult to test
    test_fulfilled = False
    while not test_fulfilled:
        if a.shoot_at(b):
            # the method reported success, so unit a should have hit
            assert b.hp < hp
            test_fulfilled = True
        # else: the method reported a miss, try again
        # reload the weapon; weapon.reload() is not used because it sleeps
        a.weapon.ammo = a.weapon.clip_size

    b.hp = hp
    a.aim = 0
    test_fulfilled = False
    while not test_fulfilled:
        if a.shoot_at(b):
            # the method reported a hit, reset hp
            b.hp = hp
            # reload the weapon; weapon.reload() is not used because it sleeps
            a.weapon.ammo = a.weapon.clip_size
        else:
            assert b.hp == hp
            test_fulfilled = True

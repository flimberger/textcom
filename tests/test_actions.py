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

from textcom import COVER_FULL, COVER_HALF
from textcom.actions import Action,                                    \
                            EndTurnAction,                             \
                            HunkerDownAction,                          \
                            OverwatchAction,                           \
                            ReloadAction
from textcom.alien import create_alien
from textcom.map import create_map
from textcom.soldier import Soldier
from textcom.weapons import BallisticPistol


def setup_map():
    soldier = Soldier(0, 'f', 5, 70, 10, 0, 'Jane', 'Doe', '', None, [], [])
    soldier.ap = soldier.mobility
    test_map = create_map(1, soldier)
    return test_map


def test_calc_ap():
    aps = 10
    apd = 10
    m = setup_map()
    s = m.soldier
    a = Action(m, 'Test Action', aps, False)

    # check if aps are correctly subtracted
    s.ap = aps + apd
    a._calc_ap()
    assert s.ap == apd

    # check if the soldiers ap are 0 when the action ends a turn
    s.ap = aps
    a.ends_turn = True
    a._calc_ap()
    assert s.ap == 0

    # check if the method raises an exception if it is erroneously called when
    # the soldier has not enough aps left
    s.ap = aps
    a.ap_costs = aps + apd
    exception = None
    try:
        a._calc_ap()
    except Exception as e:
        exception = e
    assert exception is not None
    assert str(exception) == "Not enough AP to perform action 'Test Action'"


def test_end_turn_action():
    m = setup_map()
    s = m.soldier
    s.ap = s.mobility
    a = EndTurnAction(m)
    a.perform()
    # the End Turn action only sets the soldiers ap to 0
    assert s.ap == 0


def test_hunker_down_action():
    m = setup_map()
    s = m.soldier
    a = HunkerDownAction(m)

    # default soldier has no cover, so hunkering does nothing
    a.perform()
    assert s.hunkerbonus == 0
    # hunkering ends the turn, so there must no aps be left
    assert s.ap == 0
    s.ap = s.mobility

    # if soldier is in cover, the hunkerbonus is applied
    for cover in [COVER_FULL, COVER_HALF]:
        s.cover = cover
        a.perform()
        assert s.hunkerbonus == 20
        s.hunkerbonus = 0
        s.ap = s.mobility


def test_overwatch_action():
    m = setup_map()
    s = m.soldier
    a = OverwatchAction(m)
    a.perform()
    assert s.on_overwatch == True
    # hunkering ends the turn, so there must no aps be left
    assert s.ap == 0


def test_reload_action():
    m = setup_map()
    s = m.soldier
    s.weapon = BallisticPistol()
    s.weapon.ammo = 0
    a = ReloadAction(m)
    a.perform()
    assert s.weapon.ammo == s.weapon.clip_size

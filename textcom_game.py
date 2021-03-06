#TEXT-COM, V0.1
#
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

from textcom import COVER_FLANKED, COVER_FULL, COVER_HALF, COVER_NONE,        \
                    globals_hack_init
import textcom
from textcom.actions import AdvanceAction,                                    \
                            EndTurnAction,                                    \
                            FireAction,                                       \
                            HunkerDownAction,                                 \
                            OverwatchAction,                                  \
                            ReloadAction,                                     \
                            RepositionAction,                                 \
                            UseItemAction
from textcom.alien import create_alien
from textcom.map import create_map
from textcom.soldier import create_soldier
from textcom.ui import get_int_input, status


NUMBER_OF_ROOMS = 31


def prompt_player(actions):
    for index, action in enumerate(actions):
        ap_str = ''
        ap_costs = action.ap_costs
        if ap_costs > 0:
            ap_str = ' (' + str(ap_costs) + ' AP) '
        print('[' + str(index + 1) + '] ' + ap_str + str(action))
    return actions[get_int_input('> ', 1, len(actions)) - 1]


#ah, the player's turn.
def playerTurn(game_map):
    soldier = game_map.soldier
    pod = game_map.get_current_room()
    soldier.ap = soldier.mobility
    soldier.on_overwatch = False
    soldier.hunkerbonus = 0

    # currently redundant and inefficient
    advance_action = AdvanceAction(game_map)
    end_turn_action = EndTurnAction(game_map)
    hunker_down_action = HunkerDownAction(game_map)
    overwatch_action = OverwatchAction(game_map)
    reload_action = ReloadAction(game_map)
    reposition_action = RepositionAction(game_map)

    #maybe just have these as def's instead of classes?

    # while the player has spare action points left
    while soldier.ap > 0 and soldier.alive == True:
        # displays stats
        status('HP: ' + str(soldier.hp) + '\tAP: ' + str(soldier.ap))
        if soldier.cover >= 40:
            status(str(soldier) + ' is in FULL cover.')
        else:
            status(str(soldier) + ' is in HALF cover.')
        actions = []
        if len(pod) == 0:
            actions.append(advance_action)
            if soldier.ap >= reload_action.ap_costs:
                actions.append(reload_action)
            actions.append(end_turn_action)
        else:
            if soldier.weapon.ammo > 0:
                if soldier.ap >= 6: # TODO make the ap_cost a static member
                    for alien in pod:
                        actions.append(FireAction(game_map, alien))
                if soldier.ap >= overwatch_action.ap_costs:
                    actions.append(overwatch_action)
            if soldier.weapon.ammo < soldier.weapon.clip_size                 \
               and soldier.ap >= reload_action.ap_costs:
                actions.append(reload_action)
            for item in soldier.items:
                if item.use_ap_costs > 0 and soldier.ap >= item.use_ap_costs:
                    actions.append(UseItemAction(game_map, item))
            if soldier.ap >= reposition_action.ap_costs:
                actions.append(reposition_action)
            if soldier.cover > COVER_NONE                                     \
               and soldier.ap >= hunker_down_action.ap_costs:
                    actions.append(hunker_down_action)
            actions.append(end_turn_action)
        prompt_player(actions).perform()


def displayShop(soldier, ap):
    options = []
    print("Time: "+str(ap))
    options.append("Advance")
    print(len(options) + "Advance")
    if ap == 60:
        if textcom.meld >= 15:
            if not "Aim" in soldier.mods:
                options.append("AimBonus")
                print(len(options) + "(60 Time) (15m) Insta-Genemod: Depth"
                                     "Perception (+5 aim)")
            if not "AP" in soldier.mods:
                options.append("APBonus")
                print(len(options) + "(60 Time) (15m) Micro-Augment: Reflex"
                                     "Servomotors (+2 AP)")
            options.append("")
        if textcom.meld >= 20:
            if not "HP" in soldier.mods:
                options.append("HPBonus")
                print(len(options) + "(60 Time) (20m) Insta-Genemod:"
                                     "Muscle Regeneration (+5 HP)")
            if not "Nade" in soldier.mods:
                options.append("NadeBonus")
                print(len(options) + "(60 Time) (20m) Micro-Augment: Grenade"
                                     "Launcher (+2 Frag Grenades)")
    if ap >= 50:
        if not type(soldier.weapon) is LaserRifle() and elerium >= 20         \
           and textcom.fragments >= 40:
            options.append("LaserRifle")
            print(len(options) + "(40 Time) (20e) (40f) Get Laser Rifle")
            print("     (~4dmg), infinite ammo")
        if not type(soldier.weapon) is LaserCarbine() and elerium >= 10       \
           and textcom.fragments >= 30:
            options.append("LaserCarbine")
            print(len(options) + "(40 Time) (10e) (30f) Get Laser Carbine")
            print("     (~3dmg), infinite ammo, +10% aim")
    if ap >= 30:
        if textcom.meld >= 10 and textcom.fragments >= 10:
            options.append("Meds")
            print(len(options) + "(30 Time) (10m) (10f) Get Nano Serum")
        if textcom.alloy >= 4 and textcom.fragments >= 20:
            options.append("Frag")
            print(len(options) + "(30 Time) (20f) (4a) Get Frag Grenade")
    if ap >= 20:
        if textcom.meld >= 5:
            options.append("Heal")
            print(len(options) + "(20 Time) (5m) Recuperate (+1 HP)")
        options.append("Reload")
        print(len(options) + "(20 Time) Reload Weapon")
    options.append("Skip")
    print(len(options) + "("+str(ap)+" Time) Advance (Skip this Drop Zone)")
    selection = get_int_input('> ', 1, len(options) - 1)
    print('selected option ' + str(selection))
    return options[selection - 1]


def fire(alien, soldier):
    hit_chance = alien.aim_at(soldier)
    if hit_chance > 0:
        status(str(alien) + ' fires at ' + str(soldier) + ' ('            \
               + str(hit_chance) + '%)' + '('                  \
               + alien.weapon.name + ')')
        alien.shoot_at(soldier)
    else:
        if random.randrange(0,100) < 80:
            ow(alien)
        else:
            if ITEM_ALIEN_GRENADE in alien.items:
                nade(alien, soldier)


def nade(alien, soldier):
    if ITEM_ALIEN_GRENADE not in alien.items:
        raise Exception('No grenade in inventory')
    if alien.alive == True:
        status(str(alien) + ' uses Alien Grenade!')
        time.sleep(0.5)
        print('**BLAM!**')
        time.sleep(0.5)
        del alien.items[alien.items.index(ITEM_ALIEN_GRENADE)]
        #sets the aliens item to 'none', no more grenades for you
        status('3 damage!')
        soldier.cover = 20
        soldier.hp -= 3
        soldier.check_death()


def ow(alien):
    status(str(alien) + ' went on overwatch!')
    alien.on_overwatch = True


def move(alien, cover, soldier):
    if alien.alive == True:
        time.sleep(0.5)
        if cover == 40:
            # if an alien has no cover, it will run to full cover.
            # same goes if it's flanked
            status(str(alien) + ' runs to Full cover!')
        elif cover == 20:
            status(str(alien) + ' runs to Half cover!')
        time.sleep(0.5)
        soldier.overwatch(alien)
        alien.on_overwatch = False
        alien.cover = cover


def alienTurn(game_map):
    pod = game_map.get_current_room()
    soldier = game_map.soldier
    for alien in pod:
        if not alien.alive:
            del pod[pod.index(alien)]
            continue
        if soldier.alive:
            cthplayer = alien.aim_at(soldier)
            if alien.cover < 20:
                if random.randrange(0,100) < 80:
                    move(alien, 40, soldier)
                elif random.randrange(0, 100) < 40:
                    fire(alien, soldier)
                else:
                    move(alien, 20, soldier)
            elif alien.cover < 40:
                if cthplayer > 50 + random.randrange(0,20):
                    fire(alien, soldier)
                elif random.randrange(0,100) < 20:
                    if ITEM_ALIEN_GRENADE in alien.items:
                        nade(alien, soldier)
                    else:
                        fire(alien, soldier)
                elif random.randrange(0, 100) < 20:
                    #randomly moves to different cover sometimes
                    if random.randrange(0, 100) < 50:
                        move(alien, 40, soldier)
                    else:
                        move(alien, 20, soldier)
                else:
                    if random.randrange(0, 100) < 20:
                        ow(alien)
                    else:
                        fire(alien, soldier)
            else:
                if cthplayer > 30 + random.randrange(0,20):
                    fire(alien, soldier)
                elif random.randrange(0,100) < 80:
                    move(alien, 20, soldier)
                else:
                    ow(alien)
        time.sleep(0.5)


def dump_map(the_map):
    for index, location in enumerate(the_map):
        print('#{}:'.format(index))
        for pod in location:
            print('{}'.format(pod))


def main():
    textcom.globals_hack_init()

    print("Bradford: Welcome Commander. We've discovered an Alien Base, and "
          "it's your job to send someone out to deal with it.")
    print('Bradford: Choose a soldier from the 3 below to go on the mission.')

    barracks = []
    #generates soldiers
    for i in range(3):
        x = create_soldier(i)
        barracks.append(x)

    #displays a list of the soldiers
    for i in range(len(barracks)):
        print(str(i + 1) + ': ')
        barracks[i].print_summary()
        print()

    #forces you to pick only one soldier
    soldier = barracks[get_int_input('# ', 1, 3) - 1]

    if soldier.lastname == "Bradford":
        soldier.say("What? There must have been a mistake on the sheet, "
                    "Commander! You can't send --")
    elif soldier.lastname == "Van Doorn":
        soldier.say("I'm the Ops team?")
    else:
        soldier.say('Ready for duty, Commander!')

    scripted_levels = {
        1:  [create_alien(1, 1, 'Sectoid', nrank=0)],
        2:  [
                create_alien(1, 2, 'Sectoid', nrank=0),
                create_alien(1, 2, 'Sectoid', nrank=0)
            ],
        3:  [
                create_alien(1, 3, 'Sectoid', nrank=0),
                create_alien(1, 3, 'Sectoid', nrank=1)
            ],
        5:  ["Drop Zone"],
        10: ["Drop Zone"],
        15: ["Drop Zone"],
        20: ["Drop Zone"],
        30: [create_alien(1, 1, 'Muton', nrank=8, hp=50)]
    }

    game_map = create_map(NUMBER_OF_ROOMS, soldier, scripted_levels)
    # dump_map(game_map)

    # Yeah, I feel pretty bad about this, but currently I have no idea how to
    # make the current room index available for the death handler score
    # .calculation.  Maybe everything works out fine if components are
    # introduced.  I hope so.
    soldier.game_map = game_map

    #game loop, runs until your soldier is killed
    while soldier.alive == True:
        try:
            old_room = game_map.get_current_room()
            playerTurn(game_map)
            status(str(soldier) + ' is out of AP!')

            current_room = game_map.get_current_room()
            # Aliens are not allowed to act after the room was changed,
            # because they already scattered when the player entered the new
            # room.  Also, there is no need for an alien turn if there are
            # no more aliens in the room.
            if soldier.alive == True and old_room == current_room             \
               and len(current_room) > 0:
                print()
                print("--------------Alien Activity!--------------")
                print()
                time.sleep(1)
                alienTurn(game_map)
                print()
                print("--------------XCOM Turn--------------")
                print()
        except ( ValueError or IndexError ):
            pass
        if game_map.current_room == len(game_map.rooms):
            print("You have won the game!")
            break


if __name__ == '__main__':
    main()

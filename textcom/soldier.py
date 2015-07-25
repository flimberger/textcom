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
from textcom.items import  ITEM_ALIEN_GRENADE,                                \
                           ITEM_ALLOY_PLATING,                                \
                           ITEM_FRAG_GRENADE,                                 \
                           ITEM_MEDKIT,                                       \
                           ITEM_SCOPE
from textcom.ui import status
from textcom.unit import Unit
from textcom.weapons import BradfordsPistol, BallisticCarbine, BallisticRifle


SEX_FEMALE = 'f'
SEX_MALE = 'm'
XCOM_MALE_FIRSTNAME = [
    'Bob',
    'Grant',
    'Dylan',
    'Fletcher',
    'Daniel',
    'Kav',
    'Jackson',
    'Alex',
    'Tim',
    'Peter',
    'Jeb',
    'Bill',
    'Rune',
    'Jeff',
    'Lee',
    'Iago',
    'Dan',
    'John',
    'Isaac',
    'Pedro',
    'Juan',
    'Rico',
    'David',
    'Andrew',
    'Wilson',
    'James',
    'Richard',
    'Rocky',
    'Adam',
    'Bear',
    'Paul',
    'Guy',
    'Sid',
    'Murray'
]
XCOM_FEMALE_FIRSTNAME = [
    'Becks',
    'Kate',
    'Annetta',
    'Violet',
    'Kim',
    'Iko',
    'Megan',
    'Shelly',
    'Kim',
    'Nina',
    'Olga',
    'Katherina',
    'Anya',
    'Suzie',
    'Rebecca',
    'Joanna',
    'Patricia',
    'Maria',
    'Judith',
    'Carmen',
    'Isabel',
    'Ana',
    'Laura',
    'Sara',
    'Emma',
    'Rachael',
    'Ingrid',
    'Nicole',
    'Chelsea',
    'Chell'
]
XCOM_LASTNAME = [
    'Meier',
    'Durant',
    'Lee',
    'Kerman',
    'Nilsen',
    'Fox',
    'Vern Dern',
    'Beagle',
    'Green',
    'Wolf',
    'Grills',
    'Red',
    'Taa',
    'Tank',
    'Beardly',
    'Sherman',
    'Herman',
    'Nerman',
    'Nuton',
    'Peterson',
    'Clarke',
    'French',
    'Clark',
    'Hayes',
    'Munroe',

]
# <http://www.ufopaedia.org/index.php?title=Nicknames_%28EU2012%29>
XCOM_UNISEX_NICKNAMES_ASSAULT = [
    'All Day',
    'Android',
    'Blitz',
    'Bonzai',
    'Boomer',
    'Caper',
    'Chops',
    'Cobra',
    'Coney',
    'Close Range',
    'D.O.A.',
    'DJ',
    'Desperado',
    'Devil Dog',
    'Dice',
    'Double Down',
    'Geronimo',
    'Gonzo',
    'Gunner',
    'Hardcore',
    'Hazard',
    'Loco',
    'Mad Dog',
    'Mustang',
    'Pitbull',
    'Psycho',
    'Rabid',
    'Rhino',
    'Red Fox',
    'Septic',
    'Sheriff',
    'Shotsy',
    'Smash',
    'Socks',
    'Spitfire',
    'Tombstone',
    'Trips',
    'Twitch',
    'Vandal',
    'Wardog',
    'Werewolf',
    'Wildchild',
    'Wolverine',
    'Zilch',
    'Zap'
]
XCOM_MALE_NICKNAMES_ASSAULT = [
    'Bull',
    'Cash',
    'Cowboy',
    'Duke',
    'Mad Man',
    'Nitro',
    'Rascal',
    'Spike',
    'Viking'
]
XCOM_FEMALE_NICKNAMES_ASSAULT = [
    'All In',
    'Freestyle',
    'Wednesday',
]
XCOM_UNISEX_NICKNAMES_HEAVY = [
    '98',
    'Arcade',
    'Boom Boom',
    'Brick',
    'Casino',
    'Collateral',
    'Crash',
    'Crater',
    'Diesel',
    'Disco',
    'Doomsday',
    'Dozer',
    'Flash',
    'Hulk',
    'Leaded',
    'Lights Out',
    'Nova',
    'Nuke',
    'Painbringer',
    'Prototype',
    'Richter',
    'Road Block',
    'Seismic',
    'Sledge',
    'Smokey',
    'Strobe',
    'Terra',
    'Tectonic',
    'Thunder'
]
XCOM_MALE_NICKNAMES_HEAVY = [
    'Buster',
    'Kingpin',
    'Kong',
    'Mack',
    'Moose',
    'Nero',
    'Odin',
    'Papa Bear',
    'Tank',
    'Yeti'
]
XCOM_FEMALE_NICKNAMES_HEAVY = [
    'Big Momma',
    'Mama Bear'
]
XCOM_UNISEX_NICKNAMES_SNIPER = [
    'Alpha',
    'Checkmate',
    'Claymore',
    'Cyclops',
    'Deadbolt',
    'Demon',
    'Drifter',
    'Echo',
    'Emo',
    'Enigma',
    'Garrote',
    'Ghost',
    'Hex',
    'Ice',
    'Lockdown',
    'Long Shot',
    'Longbow',
    'Low Rider',
    'Nightmare',
    'Nix',
    'Omega',
    'Shadow',
    'Snapsight'
    'Snake Eyes',
    'Solo',
    'Specter',
    'Spider',
    'Stalker',
    'Vampire',
    'Xeno',
    'Zero',
    'Zulu'
]
XCOM_MALE_NICKNAMES_SNIPER = [
    'Godfather',
    'Loki',
    'Pharaoh',
    'Ranger',
    'Slim',
    'Walker',
    'Warlock',
    'Zed',
    'Zeus'
]
XCOM_FEMALE_NICKNAMES_SNIPER = [
    'Athena',
    'Baroness',
    'Black Widow',
    'Lady Grey',
    'Raven',
    'Witchy'
]
XCOM_UNISEX_NICKNAMES_SUPPORT = [
    'Angel',
    'Axle',
    'Bonus',
    'Cargo',
    'Carrier',
    'Combo',
    'Congo',
    'Doc',
    'Fast Lane',
    'Missionary',
    'Pox',
    'Prophet',
    'Rogue',
    'Saturn',
    'Scarecrow',
    'Scotch',
    'Sentinel',
    'Shield',
    'Skinner',
    'Smokes',
    'Stacks',
    'Strings',
    'Vita',
    'Voodoo',
    'Whiskey'
]
XCOM_MALE_NICKNAMES_SUPPORT = [
    'Ace',
    'Atlas',
    'Bishop',
    'Deacon',
    'Freud',
    'Hitch',
    'Magic Man',
    'Mr. Clean',
    'Padre',
    'Pops',
    'Romeo',
    'Santa'
]
XCOM_FEMALE_NICKNAMES_SUPPORT = [
    'Cookie',
    'Gypsy',
    'Kitty',
    'Pixie',
    'Vixen'
]
XCOM_MALE_NICKNAMES_MEC = [
    'Big Daddy',
    'Bolts',
    'Caliban',
    'Chip',
    'Clank',
    'Data',
    'Deep Teal',
    'Forklift',
    'Golem',
    'Marvin',
    'Murphy',
    'Olivaw',
    'Ratchet',
    'Robby',
    'Ryle',
    'Stick',
    'Sputnik',
    'Talos',
    'Tik-Tok',
    'Tin Can',
    'Vulcan'
]
XCOM_FEMALE_NICKNAMES_MEC = [
    'Beeps',
    'Big Mommy',
    'Freya',
    'Friday',
    'Gadget',
    'Gizmo',
    'Hadaly',
    'Iris',
    'Maya',
    'Molly',
    'Number Six',
    'Orianna',
    'Rosie',
    'Vanessa',
    'Vesta',
]

RETORTS = [
    "Suck on this!",
    "Eat this!",
    "Pick on someone your own size!",
    "Take this!",
    "Welcome to Earth!",
    "AAGGHH!!!",
    "HYAAA!"
]
BRADFORD_RETORTS = [
    'CLOSE RANGE?!',
    'WHAT HAVE YOU DONE?!',
    'COMMANDER!',
    "WE'RE PICKING UP MULTIPLE CONTACTS!",
    'CURRENT ENEMY STATUS AT THE SITE IS UNKNOWN!'
]
VAN_DOORN_RETORTS = [
    "I'm the Ops team!",
    "Only fair if I have all the fun.",
    "Get down there!",
    "Come on! I won't go down without a fight.",
    # "Thank God you're here. I'm still breathing, but I can't say the same for a lot of my boys. Let's get out of here before any more of those things show up.",
    "I don't know what outfit you're from, but I haven't seen gear like that before.",
    "Come on!",
    "I won't go down without a fight!",
    "It's looking bad...for you!",
    "I owe you one."
]

#Soldier names
BRADFORD  = 'Bradford'
VAN_DOORN = 'Van Doorn'


RANK_ROOKIE = 0
RANK_SQUADDIE = 1
RANK_CORPORAL = 2
RANK_SERGEANT = 3
RANK_LIEUTENANT = 4
RANK_CAPTAIN = 5
RANK_MAJOR = 6
RANK_COLONEL = 7
RANK_GENERAL = 8 # only for Van Doorn
RANK_CENTRAL_OFFICER = 9 # only for Bradford
XCOM_RANKS = [
    'Rookie',
    'Squaddie',
    'Corporal',
    'Sergeant',
    'Lieutenant',
    'Captain',
    'Major',
    'Colonel',
    # Special ranks
    'General',
    'Central Officer'
]

# Global variables to prevent duplicate hero soldiers
_have_bradford = False
_have_vdoorn = False


class Soldier(Unit):
    def __init__(self, sid, sex, hp, aim, mobility, rank, firstname, lastname,
                 armour, weapon, items, mods):
        super().__init__(hp, aim, mobility, rank, firstname, lastname, armour,
                         weapon, items, mods)
        self.ap = 0
        self.sid = sid
        self.sex = sex
        self.xp = 0
        self.aimpenalty = 0
        self.nickname = None
        self.mods = []
        self.hunkerbonus = 0

    def __str__(self):
        middle = ' '
        if self.nickname:
            middle = " '" + self.nickname + "' "
        return XCOM_RANKS[self.nrank] + middle + self.lastname

    def _handle_death(self):
        status(str(self) + ' was killed!')
        if not self.lastname == "Bradford":
            print('Bradford: Commander, our unit was killed.')
            print('Bradford: We were able to recover some materials, however.')
            print("Fragments:", textcom.fragments)
            print("Elerium:", textcom.elerium)
            print("Meld:", textcom.meld)
            print("Alloy:", textcom.alloy)
            print('Total Score: ' + str(textcom.fragments + textcom.elerium   \
                                        + textcom.meld + textcom.alloy        \
                                        + self.xp + textcom.roomNo))
        else:
            print("Council Speaker: Commander...you 'volunteered' your Central"
                 'Officer to fight on the front lines.')
            print('Council Speaker: This was a foolish endeavour, and as a'
                  'result, you lost him.')
            print('Monthly Rating: F')
            print('Council Speaker: We have negotiated...a deal with the'
                  'aliens, and so...your services are no longer required.')
            print('Council Speaker: We are...terminating the XCOM Project,'
                  'effective...immediately.')
        #doesn't want to stop the whole game straight away for some reason
        quit

    def _handle_kill(self, target):
        """Handle an alien kill.

        Calculates the loot and xp and performs due promotions.
        """
        self.xp += target.nrank * abs(target.hp)
        textcom.fragments += abs(target.hp)
        textcom.elerium += target.nrank
        textcom.meld += 2 * target.nrank
        if ITEM_ALIEN_GRENADE in target.items:
            textcom.elerium += 2
        elif ITEM_ALLOY_PLATING in target.items:
            textcom.alloy += 2
        elif ITEM_SCOPE in target.items:
            textcom.fragments += 2
        e, f = target.weapon.get_materials()
        textcom.elerium += e
        textcom.fragments += f
        self.check_promotion()

    def _handle_overwatch(self, target):
        if super()._handle_overwatch(target) == False:
            self.say(self.get_overwatch_miss_retort())

    def check_promotion(self):
        was_promoted = False
        if self.xp >= 25 and self.nrank < RANK_SQUADDIE:
            self.nrank = RANK_SQUADDIE
            self.hp += 1
            self.aim += 2
            self.mobility += 1
            for _ in range(2):
                drop(self)
            was_promoted = True
        elif self.xp >= 100 and self.nrank < RANK_CORPORAL:
            self.nrank = RANK_CORPORAL
            self.hp += 1
            self.aim += 2
            self.mobility += 1
            for _ in range(2):
                drop(self)
            was_promoted = True
        elif self.xp >= 300 and self.nrank < RANK_SERGEANT:
            nicknames = XCOM_UNISEX_NICKNAMES_ASSAULT                         \
                        + XCOM_UNISEX_NICKNAMES_HEAVY                         \
                        + XCOM_UNISEX_NICKNAMES_SNIPER                        \
                        + XCOM_UNISEX_NICKNAMES_SUPPORT
            if self.sex == SEX_FEMALE:
                nicknames += XCOM_FEMALE_NICKNAMES_ASSAULT                    \
                             + XCOM_FEMALE_NICKNAMES_HEAVY                    \
                             + XCOM_FEMALE_NICKNAMES_MEC                      \
                             + XCOM_FEMALE_NICKNAMES_SNIPER                   \
                             + XCOM_FEMALE_NICKNAMES_SUPPORT
            else:
                nicknames += XCOM_MALE_NICKNAMES_ASSAULT                      \
                             + XCOM_MALE_NICKNAMES_HEAVY                      \
                             + XCOM_MALE_NICKNAMES_MEC                        \
                             + XCOM_MALE_NICKNAMES_SNIPER                     \
                             + XCOM_MALE_NICKNAMES_SUPPORT
            self.nickname = random.choice(nicknames)
            status(XCOM_RANKS[self.nrank] + ' ' + self.firstname + ' '        \
                   + self.lastname  + " earned the nickname '" + self.nickname\
                   + "'")
            self.nrank = RANK_SERGEANT
            self.hp += 2
            self.aim += 1
            self.mobility += 1
            for _ in range(2):
                drop(self)
            was_promoted = True
        elif self.xp >= 900 and self.nrank < RANK_LIEUTENANT:
            self.nrank = RANK_LIEUTENANT
            self.hp += 1
            self.aim += 1
            for _ in range(2):
                drop(self)
            was_promoted = True
        elif self.xp >= 1500 and self.nrank < RANK_CAPTAIN:
            self.nrank = RANK_CAPTAIN
            self.hp += 2
            self.aim += 1
            for _ in range(4):
                drop(self)
            was_promoted = True
        elif self.xp >= 2000 and self.nrank < RANK_MAJOR:
            self.nrank = RANK_MAJOR
            self.hp += 1
            self.aim += 1
            self.mobility += 1
            for _ in range(4):
                drop(self)
            was_promoted = True
        elif self.xp >= 3000 and self.nrank < RANK_COLONEL:
            self.nrank = RANK_COLONEL
            self.hp += 1
            self.aim += 1
            for _ in range(6):
                drop(self)
            was_promoted = True
        if was_promoted:
            status(str(self) + ' was promoted to ' + XCOM_RANKS[self.nrank])

    def get_overwatch_confirmation(self):
        return 'Got it, on Overwatch.'

    def get_overwatch_miss_retort(self):
        return 'Shot failed to connect!'

    def get_reposition_confirmation(self):
        return 'Moving to Full cover!'

    def get_retort(self):
        return random.choice(RETORTS)

    def print_summary(self):
        middle = ' '
        if self.nickname:
            middle = " '" + self.nickname + "' "
        print(XCOM_RANKS[self.nrank] + ' ' + self.firstname + middle          \
              + self.lastname + ' - ' + str(self.hp) + ' HP' + ' - '          \
              + str(self.aim) + ' Aim'+ ' - ' +str(self.mobility) + ' AP')
        print('Items: ' + self.weapon.name + ', ' + self.items[0].name + ', ' \
          + self.items[1].name)

    def say(self, message):
        '''
        Print the name and the message
        '''
        print(XCOM_RANKS[self.nrank] + self.lastname + ': ' + message)


def create_soldier(sid):
    global _have_bradford
    global _have_vdoorn

    items = [(random.choice([ITEM_FRAG_GRENADE, ITEM_MEDKIT, ITEM_SCOPE])),   \
             (random.choice([ITEM_FRAG_GRENADE, ITEM_MEDKIT]))]
    mobility = random.randrange(11, 16)
    armour = 'BDY'
    mods  = []
    if random.randrange(1,100) < 5:
        if random.randrange(0, 2) == 0:
            if not _have_bradford:
                bradford = Soldier(sid, SEX_MALE, 6, 100, mobility,           \
                                   RANK_CENTRAL_OFFICER, '', 'Bradford',      \
                                   armour, BradfordsPistol(), items, mods)
                bradford.get_overwatch_confirmation =                         \
                        lambda: 'Keep your eyes peeled!'
                bradford.get_overwatch_miss_retort =                          \
                        lambda: 'How did I miss that?!'
                bradford.get_reposition_confirmation =                        \
                        lambda: "Moving to...wait...that's CLOSE RANGE!"
                bradford.get_retort = lambda: random.choice(BRADFORD_RETORTS)
                return bradford
        if not _have_vdoorn:
            van_doorn = Soldier(sid, SEX_MALE, 6, 80, mobility, RANK_GENERAL, \
                                'Peter', VAN_DOORN, armour, BallisticRifle(), \
                                items, mods)
            van_doorn.get_overwatch_confirmation =                            \
                    lambda: 'You coming down here or what?'
            van_doorn.get_reposition_confirmation =                           \
                    lambda: "Come on! I won't go down without a fight."
            van_doorn.get_retort = lambda: random.choice(VAN_DOORN_RETORTS)
            return van_doorn
    weapon = None
    if random.randrange(0, 2) == 0:
        weapon = BallisticRifle()
    else:
        weapon = BallisticCarbine()
    sex = None
    if random.randrange(0, 2) == 0:
        sex = SEX_FEMALE
    else:
        sex = SEX_MALE
    name = None
    if sex == SEX_FEMALE:
        name = random.choice(XCOM_FEMALE_FIRSTNAME)
    else:
        name = random.choice(XCOM_MALE_FIRSTNAME)
    return Soldier(sid, sex, random.randrange(3, 6), random.randrange(50, 75),\
                   mobility, RANK_ROOKIE, name, random.choice(XCOM_LASTNAME), \
                   armour, weapon, items, mods)

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

from textcom.items import ITEM_ALIEN_GRENADE, ITEM_ALLOY_PLATING, ITEM_SCOPE
from textcom.ui import status
from textcom.unit import Unit
from textcom.weapons import PlasmaPistol, PlasmaCarbine, PlasmaRifle


ALIEN_RANKS = [
    "Peon",
    "Guard",
    "Soldier",
    "Trooper",
    "Warrior",
    "Officer",
    "Commander",
    "Elite",
    "Uber"
]


sectoidfName = ["Glip","Gleep","Glup","Glorp","Gloop","Glop","Glump","Glerp","Glurp","Glarp"]
sectoidlName = ["Glop","Glarp","Glupple","Glorple","Gloopley","Glopperson","Glep","Glommery"]
thinfName = ["T.","P.","H.","Z.","K.","A.","F.","X.","P.","L.","W.","S.","V."]
thinlName = ["Hinman","Alium","Van Doom","Lmao","Notanalien","Anderson","Smith","Human","Clark","Warzonager","Iper","Thinmint","Mint","Spear","Infiltrator"]
floaterfName = ["Dirk","Ferdinand","Frederick","Algernon","Angus","King","Cornelius","Francis","Christopher","Gustav","Richard","Ivan","Yuri","Vlad"]
floaterlName = ["Meyer","Mleadeer","Peters","Prince","Vos","Wolf","Schwarz","Frank","Miller","Anderssen","Slavolav","Stroganov","Costarov"]

#Aliem names
mutonfName = ["Pooter","Dave","Holk","Billy","Tim","Jeffery","Leeroy","Jimmy","Hank"]
mutonlName = ["Von Mooter","The Muton","Hugan","Jankins","Jefferson","Higgins","Jenkins"]


SPECIES_RANK_FUNC      = 0
SPECIES_HP_BASE        = 1
SPECIES_AIM_RANGE      = 2
SPECIES_MOBILITY_RANGE = 3
SPECIES_WEAPON_CLASS   = 4
SPECIES_FIRSTNAME      = 5
SPECIES_LASTNAME       = 6


# Species data table, used to construct aliens with the `create_alien`
# function with keywords
# rank function, hp base, aim base range, mobility base range,
#     primary weapon class, firstname table, lastname table
ALIEN_SPECIES = {
    'Sectoid': [
        lambda nroom: round(random.randrange(round(nroom / 20), 2)),
        2, (50, 75), (9, 13), PlasmaPistol, sectoidfName, sectoidlName
    ],
    'Thinman': [
        lambda nroom: round(random.randrange(round(nroom / 20), 2)),
        3, (60, 80), (12, 15), PlasmaCarbine, thinfName, thinlName
    ],
    'Floater': [
        lambda nroom: round(random.randrange(round(nroom / 12), 3)),
        4, (50, 70), (12, 15), PlasmaCarbine, floaterfName, floaterlName
    ],
    'Muton': [
        lambda nroom: round(random.randrange(round(nroom / 12), 3)),
        8, (50, 60), (10, 12), PlasmaRifle, mutonfName, mutonlName
    ]
}


class Alien(Unit):
    """Alien unit.

    Different alien species are not implemented as subclasses, as this
    would yield a lot of redundancy for little gain.
    """
    def __init__(self, alien_id, species, hp, aim, mobility, nrank, firstname,\
                 lastname, armour, weapon, items, mods):
        super().__init__(hp, aim, mobility, nrank, firstname, lastname,       \
                         armour, weapon, items, mods)
        self.aid = alien_id
        self.species = species

    #gives us names for when we reference the alien in game
    def __str__(self):
        return '(' + self.species + ') ' + ALIEN_RANKS[self.nrank] + ' '      \
               + self.firstname + " " + self.lastname

    def _handle_death(self):
        status(str(self) + ' died!')
        self.alive = False

    def refresh(self):
        self.hp += self.nrank * round(random.random() * 2)
        self.aim  +=  self.nrank * round(random.random() * 2)


def create_alien(alien_id, room_index, species, **kwargs):
    '''
    Create a alien with random stats or stats supplied by keywords.

    Returns a new alien with the stats read from kwargs, or if the stat
    is not contained in there, random stats according to the
    `ALIEN_SPECIES` table.
    '''
    if species not in ALIEN_SPECIES:
        raise Exception('Unknown alien species')

    # the rank may be used for other values, so it is set differently
    nrank = 0
    if not 'nrank' in kwargs:
        nrank = ALIEN_SPECIES[species][SPECIES_RANK_FUNC](room_index)
        kwargs['nrank'] = nrank
    else:
        nrank = kwargs['nrank']

    if not 'hp' in kwargs:
        kwargs['hp'] = ALIEN_SPECIES[species][SPECIES_HP_BASE] + nrank
    if not 'aim' in kwargs:
        kwargs['aim'] =                                                       \
            random.randrange(*ALIEN_SPECIES[species][SPECIES_AIM_RANGE])      \
            + nrank
    if not 'mobility' in kwargs:
        kwargs['mobility'] =                                                  \
            random.randrange(*ALIEN_SPECIES[species][SPECIES_MOBILITY_RANGE]) \
            + nrank
    if not 'firstname' in kwargs:
        kwargs['firstname'] =                                                 \
            random.choice(ALIEN_SPECIES[species][SPECIES_FIRSTNAME])
    if not 'lastname' in kwargs:
        kwargs['lastname'] =                                                  \
            random.choice(ALIEN_SPECIES[species][SPECIES_LASTNAME])
    if not 'armour' in kwargs:
        kwargs['armour'] = 'BDY'
    if not 'weapon' in kwargs:
        kwargs['weapon'] = ALIEN_SPECIES[species][SPECIES_WEAPON_CLASS]()
    if not 'items' in kwargs:
        kwargs['items'] = [random.choice([ITEM_ALIEN_GRENADE,
                                          ITEM_ALLOY_PLATING,
                                          ITEM_SCOPE])]
    if not 'mods' in kwargs:
        kwargs['mods'] = []

    return Alien(alien_id, species, **kwargs)

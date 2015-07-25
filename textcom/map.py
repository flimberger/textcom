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


def check_for_alien_overwatch(soldier):
    for i in range(len(textcom.room[textcom.roomNo])):
        alium = textcom.room[textcom.roomNo][i]
        alium.overwatch(soldier)


def checkspot(roomNo):
    for i in range(len(textcom.room[roomNo])):
        textcom.ui.status(str(textcom.room[roomNo][i]) + ' spotted!')
    time.sleep(0.5)


def scatter(roomNo):
    """Scatter the aliens in a room, some won't find any cover."""
    cover = ["Full", "Full", "Full", "Half", "Half", "Half", "Half", "Half",
             "Half", "No"]
    covernumber = [40,40,40,20,20,20,20,20,20,-10]
    for i in range(len(textcom.room[roomNo])):
        textcom.room[roomNo][i].cover = random.choice(covernumber)
        if not textcom.room[roomNo][i].cover == -10:
            textcom.ui.status(str(textcom.room[roomNo][i]) + ' moves to '     \
                              + cover[covernumber.index(
                                textcom.room[roomNo][i].cover)]               \
                              + ' cover!')
            time.sleep(.5)
        else:
            textcom.ui.status(str(textcom.room[roomNo][i])                    \
                             + " can't find any cover!")
            time.sleep(.5)
    print()

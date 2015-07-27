"""Contains the logic classes for the textcom game."""

# global map management
# to be removed
def globals_hack_init():
    global fragments
    global elerium
    global meld
    global alloy

    # Global stat counters
    fragments = 0
    elerium = 0
    meld = 0
    alloy = 0


COVER_FLANKED = -20
COVER_NONE = 0
COVER_FULL = 40
COVER_HALF = 20

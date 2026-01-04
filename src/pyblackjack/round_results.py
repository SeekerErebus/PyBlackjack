from enum import Enum

class RoundResults(Enum):
    """
    Enum of Possible Round End States
    """
    DEALER_WON = 1
    PLAYER_WON = 2
    PLAYER_WON_BLACKJACK = 3
    PUSH = 4
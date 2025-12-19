from .actor import Actor
from .bank import Bank
from .playing_card import PlayingCard
from .hand import Hand
from .deck import Deck
from . import constants
import copy


class Player(Actor):
    """
    The player.

    Attributes:
        name (str): The Player Name, default "Player"
        bank (Bank): The Player's Bank
        hand (Hand): The Player's Hand
        split_hands (list[Hand]): A list of hands in case of splitting.
    """
    def __init__(self, name: str = "Player", starting_balance: float | int = constants.PLAYER_BANK) -> None:
        """
        Player constructor
        
        :param name: Name of the Player
        :type name: str
        :param starting_balance: The starting bank balance of the Player
        :type starting_balance: float | int
        """
        super().__init__(name, starting_balance)
        self.split_hands: list[Hand] = [self.hand]
        self.current_hand_index: int = 0
    
    def swap_current_hand(self, new_index: int) -> None:
        try:
            self.hand = self.split_hands[new_index]
            self.current_hand_index = new_index
        except IndexError as e:
            return

    
    def hit(self, card: PlayingCard) -> int:
        return self.hand.add_card(card)
    
    def double_down(self, card: PlayingCard) -> int:
        return self.hand.double_down(card)
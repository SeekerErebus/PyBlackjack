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
    
    def hit(self, card: PlayingCard) -> int:
        return self.hand.add_card(card)
    
    def double_down(self, card: PlayingCard) -> int:
        return self.hand.double_down(card)
    
    def split(self, cards: list[PlayingCard], hand_to_split: Hand):
        if len(cards) != 2:
            raise ValueError("Need two cards to split correctly.")
        split_hand_one = Hand([hand_to_split.cards[0], cards[0]], hand_to_split.bet.balance)
        split_hand_two = Hand([hand_to_split.cards[1], cards[1]], hand_to_split.bet.balance)

        hand_index = self.split_hands.index(hand_to_split)
from .actor import Actor
from .playing_card import PlayingCard
from .hand import Hand
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
        """
        Hits the hand.
        
        :param card: The card to add.
        :type card: PlayingCard
        :return: The new hand value after the card is added.
        :rtype: int
        """
        return self.hand.add_card(card)
    
    def double_down(self, card: PlayingCard) -> int:
        """
        Doubles down. Brings hand to an end.
        
        :param card: The card to add
        :type card: PlayingCard
        :return: The new hand value after the card is added.
        :rtype: int
        """
        result = self.hand.double_down(card)
        self.hand.has_stood = True
        return result
    
    def split(self, cards: list[PlayingCard]) -> None:
        """
        Runs a split.
        
        :param cards: A list of two cards that will make up the two second cards for the new hands.
        :type cards: list[PlayingCard]
        """
        if len(cards) != 2:
            raise ValueError("Need two cards to split correctly.")
        split_hand_one = Hand([self.hand.cards[0], cards[0]], self.hand.bet.balance)
        split_hand_two = Hand([self.hand.cards[1], cards[1]], self.hand.bet.balance)

        hand_index = self.current_hand_index
        self.split_hands[hand_index] = split_hand_one
        self.split_hands.insert(hand_index + 1, split_hand_two)
        self.__update_hand()
    
    def next_hand(self) -> bool:
        """
        Iterates to the next hand.
        
        :return: True if there is a next hand, False otherwise.
        :rtype: bool
        """
        next_index = self.current_hand_index + 1
        return self.__update_hand(new_index=next_index)
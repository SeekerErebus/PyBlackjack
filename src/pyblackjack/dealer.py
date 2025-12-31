from .actor import Actor
from .playing_card import PlayingCard
from . import constants

class Dealer(Actor):
    """
    A Dealer
    Attributes:
        name (str): The Dealer Name, default "Dealer"
        bank (Bank): The Dealer's Bank
        hand (Hand): The Dealer's Hand
    """
    def __init__(self, name: str = "Dealer", starting_balance: float | int = constants.DEALER_BANK) -> None:
        """
        Dealer constructor
        
        :param name: Name of the Dealer
        :type name: str
        :param starting_balance: The starting bank balance of the Dealer
        :type starting_balance: float | int
        """
        super().__init__(name, starting_balance)

    def get_visible_card(self) -> PlayingCard:
        """
        Shows the visible card for the Dealer's hand.
        
        :return: The first card in the Dealer's hand.
        :rtype: PlayingCard
        """
        return self.hand.cards[0]
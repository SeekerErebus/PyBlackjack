from .actor import Actor
from .bank import Bank
from .playing_card import PlayingCard
from .hand import Hand
from .deck import Deck

DEALER_BANK = 100000

class Dealer(Actor):
    def __init__(self, name: str, starting_balance: float | int = DEALER_BANK) -> None:
        super().__init__(name, starting_balance)

    def get_visible_card(self) -> PlayingCard:
        return self.hand.cards[0]
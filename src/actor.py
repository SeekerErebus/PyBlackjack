from .bank import Bank
from .playing_card import PlayingCard
from .hand import Hand
from .deck import Deck

class Actor:
    def __init__(self, name: str, starting_balance: float | int = 0.0) -> None:
        self.name = name
        self.bank = Bank(balance=starting_balance)
        self.hand: Hand = Hand([])
    
    def start_hand(self, starting_cards: list[PlayingCard], bet_value: float | int = 0) -> None:
        self.hand = Hand(starting_cards=starting_cards, bet_value=bet_value)
    
    def hit(self, deck: Deck, double_down: bool = False) -> int:
        if double_down:
            self.hand.bet.add_transaction("Double Down", self.hand.bet.balance)
        return self.hand.add_card(deck.drawCard())
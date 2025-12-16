from .playing_card import PlayingCard, Rank
from .bank import Bank


class Hand:
    """
    A blackjack hand. Add cards to hand, track the value of the hand.
    """
    def __init__(self, starting_cards: list[PlayingCard], bet_value: float | int = 0) -> None:
        self.cards: list[PlayingCard] = starting_cards
        self._ace_active_count: int = 0
        self._update_ace_count(self.cards)
        self.hand_value = self.get_hand_value()
        self.bet = Bank(bet_value)
        self.insurance = Bank()
    
    def get_hand_value(self) -> int:
        """
        Get the current value of the player's hand, adjusted for Aces.
        
        :return: The current hand value
        :rtype: int
        """
        current_value: int = 0
        for card in self.cards:
            current_value += card.value
        current_value += self._ace_active_count * 10
        while (current_value > 21 and self._ace_active_count > 0):
            current_value -= 10
            self._ace_active_count -= 1
        self.hand_value = current_value
        return self.hand_value
    
    def update_bet(self, name: str, amount: float | int) -> float:
        if amount != 0:
            self.bet.add_transaction(name=name, amount=amount)
        return self.bet.balance
    
    def add_card(self, card: PlayingCard) -> int:
        """
        Adds a card to the player's hand, and gets the new hand value.
        
        :param card: The playing card being added to the hand.
        :type card: PlayingCard
        :return: The hand value after the card is added.
        :rtype: int
        """
        self.cards.append(card)
        self._update_ace_count(self.cards)

        return self.get_hand_value()
    
    def double_down(self, card: PlayingCard) -> int:
        self.update_bet("Double Down", self.bet.balance)
        result = self.add_card(card=card)
        return result
    
    def _update_ace_count(self, cards: list[PlayingCard]) -> None:
        self._ace_active_count = 0
        for card in cards:
            if card.rank == Rank.ACE:
                self._ace_active_count += 1
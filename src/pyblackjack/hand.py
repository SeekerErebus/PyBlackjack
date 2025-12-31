from .playing_card import PlayingCard, Rank
from .bank import Bank


class Hand:
    """
    A blackjack hand. Add cards to hand, track the value of the hand.
    """
    def __init__(self, starting_cards: list[PlayingCard], bet_value: float | int = 0) -> None:
        self.cards: list[PlayingCard] = starting_cards
        self._ace_active_count: int = 0
        self._update_ace_count()
        self.hand_value = self.get_hand_value()
        self.has_blackjack = False
        self.has_stood = False
        self.has_busted = False
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
    
    def add_bet(self, name: str, amount: float | int) -> float:
        """
        Adds the amount to the bet
        
        :param name: Name of the Transaction
        :type name: str
        :param amount: The value of the transaction
        :type amount: float | int
        :return: The new balance of the bet.
        :rtype: float
        """
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
        self._update_ace_count()
        self.check_if_busted()

        return self.get_hand_value()
    
    def double_down(self, card: PlayingCard) -> int:
        """
        Doubles the bet for the hand and adds the drawn card.
        
        :param card: The card to add.
        :type card: PlayingCard
        :return: The new hand value after the card is added.
        :rtype: int
        """
        self.add_bet("Double Down", self.bet.balance)
        result = self.add_card(card=card)
        self.has_stood = True
        return result
    
    def check_if_busted(self) -> bool:
        """
        Checks if the hand is busted, and if so, marks the proper flags.
        
        :return: True if busted, false otherwise.
        :rtype: bool
        """
        if self.get_hand_value() > 21:
            self.has_busted = True
            self.has_stood = True
        return self.has_busted
    
    def _update_ace_count(self) -> None:
        self._ace_active_count = 0
        for card in self.cards:
            if card.rank == Rank.ACE:
                self._ace_active_count += 1
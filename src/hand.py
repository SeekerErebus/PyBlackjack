from .playing_card import PlayingCard, Rank


class Hand:
    def __init__(self, starting_cards: list[PlayingCard]) -> None:
        self.cards: list[PlayingCard] = starting_cards
        self.__ace_active_count: int = 0
        self.__update_ace_count(self.cards)
        self.hand_value = self.get_hand_value()
    
    def get_hand_value(self) -> int:
        """
        Get the current value of the player's hand, adjusted for Aces.
        
        :return: The current hand value
        :rtype: int
        """
        current_value: int = 0
        for card in self.cards:
            current_value += card.value
        current_value += self.__ace_active_count * 10
        while (current_value > 21 and self.__ace_active_count > 0):
            current_value -= 10
            self.__ace_active_count -= 1
        self.hand_value = current_value
        return self.hand_value
    
    def add_card(self, card: PlayingCard) -> int:
        """
        Adds a card to the player's hand, and gets the new hand value.
        
        :param card: The playing card being added to the hand.
        :type card: PlayingCard
        :return: The hand value after the card is added.
        :rtype: int
        """
        self.cards.append(card)
        self.__update_ace_count(self.cards)

        return self.get_hand_value()
    
    def __update_ace_count(self, cards: list[PlayingCard]) -> None:
        self.__ace_active_count = 0
        for card in cards:
            if card.rank == Rank.ACE:
                self.__ace_active_count += 1
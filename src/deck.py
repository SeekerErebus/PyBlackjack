import random
from .playing_card import PlayingCard, Rank, Suit


class Deck:
    """
    A 52 card playing deck. Actually maintains all the cards in the deck, so card counting is completely possible.
    """
    def __init__(self) -> None:
        self.cards: list[PlayingCard] = []
        self.__card_set: set[PlayingCard] = set()
        for suit in Suit:
            for rank in Rank:
                card = PlayingCard(rank, suit)
                self.cards.append(card)
                self.__card_set.add(card)
        self.shuffle()
        self.__deck_refresh_percent = 0.2
    def shuffle(self) -> None:
        """
        Shuffles the current deck. Does not require the deck to be full.
        """
        random.shuffle(self.cards)
    def resetDeck(self) -> None:
        """
        Resets the Deck, which restores it to max capacity of 52 cards and shuffles the deck.
        """
        self.cards = list(self.__card_set)
        self.shuffle()
    def drawCard(self, count: int = 1) -> PlayingCard | list[PlayingCard]:
        """
        Draws one or more cards from the Deck.
        
        :param count: The number of cards to draw. Raises ValueError if less than 1 or greater than the maximum deck size.
        :type count: int
        :return: A playing card, or a list of playing cards.
        :rtype: PlayingCard | list[PlayingCard]
        """
        if count < 1:
            raise ValueError("Can't draw less than one card")
        if count > len(self.__card_set):
            raise ValueError("Can't draw more cards than the deck can hold at max.")
        current_deck_percentage = len(self.cards) / len(self.__card_set)
        if current_deck_percentage <= self.__deck_refresh_percent or len(self.cards) < count:
            self.resetDeck()
        if count == 1:
            result = self.cards.pop()
            self.shuffle()
            return result
        out_cards: list[PlayingCard] = []
        for _ in range(count):
            out_cards.append(self.cards.pop())
        self.shuffle()
        return out_cards
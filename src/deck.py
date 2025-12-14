import random
from .playing_card import PlayingCard, Rank, Suit


class Deck:
    """
    A 52 card playing deck. Actually maintains all the cards in the deck, so card counting is completely possible.
    """
    def __init__(self) -> None:
        self.cards: list[PlayingCard] = []
        self._card_set: set[PlayingCard] = set()
        for suit in Suit:
            for rank in Rank:
                card = PlayingCard(rank, suit)
                self.cards.append(card)
                self._card_set.add(card)
        self.shuffle()
        self._deck_refresh_percent = 0.2
    def shuffle(self) -> None:
        """
        Shuffles the current deck. Does not require the deck to be full.
        """
        random.shuffle(self.cards)
    def resetDeck(self) -> None:
        """
        Resets the Deck, which restores it to max capacity of 52 cards and shuffles the deck.
        """
        self.cards = list(self._card_set)
        self.shuffle()
    def drawCard(self) -> PlayingCard:
        """
        Draws a card from the Deck.

        :return: A playing card, or a list of playing cards.
        :rtype: PlayingCard
        """
        current_deck_percentage = len(self.cards) / len(self._card_set)
        if current_deck_percentage <= self._deck_refresh_percent:
            self.resetDeck()
        result = self.cards.pop()
        self.shuffle()
        return result
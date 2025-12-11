from .playing_card import PlayingCard, Rank, Suit


class Deck:
    def __init__(self) -> None:
        self.cards: list[PlayingCard] = []
        self.__card_set: set[PlayingCard] = set()
        for suit in Suit:
            for rank in Rank:
                card = PlayingCard(rank, suit)
                self.cards.append(card)
                self.__card_set.add(card)
        self.shuffle()
    def shuffle(self) -> None:
        """
        Shuffles the current deck. Does not require the deck to be full.
        """
        pass
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
        if len(self.cards) < count:
            self.resetDeck()
        if count == 1:
            return self.cards.pop()
        out_cards: list[PlayingCard] = []
        for _ in range(count):
            out_cards.append(self.cards.pop())
        return out_cards